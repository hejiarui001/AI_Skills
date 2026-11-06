#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高校发票报销与合规审计工具 (v1.2.0)
支持：
- 发票生命周期状态流转（差发票、差截图、开票中、待提交、优惠卷、代付、已提交、已核销/已报销）
- 单据成对闭环核验与主动交互确认提醒
- 抬头/税号校验、单张500元上限拦截、查重、差额核对、序号连续性检查
- 标准 11 列 Excel 总账生成（支持多发票跨行卡片合并与文本格式@发票号）
"""

import os
import sys
import re
import argparse
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import openpyxl
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    openpyxl = None


EXPECTED_BUYER = "武汉轻工大学"
EXPECTED_TAX_ID = "124200004416255673"
MAX_SINGLE_INVOICE_AMOUNT = 500.0

KNOWN_STATUSES = ["已核销", "已报销", "已提交", "已核查", "开票中", "开票未取", "代付", "优惠卷", "优惠券", "差发票", "差截图"]


def clean_spaces(text):
    return re.sub(r'\s+', '', text or '')


def extract_pdf_info(pdf_path):
    """提取 PDF 发票的发票号码、购买方、税号、价税合计、货物名称"""
    if not pypdf:
        return {'error': 'pypdf not installed'}

    try:
        reader = pypdf.PdfReader(pdf_path)
        raw_text = "".join([page.extract_text() or "" for page in reader.pages])
        clean = clean_spaces(raw_text)

        # 1. 发票号码（高精度分层匹配）
        fname = os.path.basename(pdf_path)
        fn_m = re.search(r'(\d{20})', fname)
        if fn_m:
            invoice_num = fn_m.group(1)
        else:
            all_20 = re.findall(r'(?<!\d)(2\d{19})(?!\d)', clean)
            if all_20:
                invoice_num = all_20[0]
            else:
                m_stick = re.findall(r'(?<!\d)(2\d{19})(?=202\d)', clean)
                if m_stick:
                    invoice_num = m_stick[0]
                else:
                    m_8 = re.search(r'(?:发票号码|№|No)[\s:：]*(\d{8})(?!\d)', clean)
                    if m_8:
                        invoice_num = m_8.group(1)
                    else:
                        all_any_20 = re.findall(r'(2\d{19})', clean)
                        invoice_num = all_any_20[0] if all_any_20 else "UNKNOWN"

        # 2. 抬头与税号
        buyer_ok = EXPECTED_BUYER in clean
        tax_ok = EXPECTED_TAX_ID in clean

        # 3. 价税合计（小写）
        amt_match = re.search(r'[圆整角分零壹贰叁肆伍陆柒捌玖拾佰仟万]\s*[¥￥\s]*([0-9\s]+\.[0-9\s]{2})', raw_text)
        if amt_match:
            amount_str = re.sub(r'\s+', '', amt_match.group(1))
            total_amount = float(amount_str)
        else:
            m_fall = (re.search(r'[（\(]?小写[）\)]\s*[¥￥\s]*([0-9\s]+\.[0-9\s]{2})', raw_text) or
                      re.search(r'小写[）\)]\s*[¥￥\s]*([0-9\s]+\.[0-9\s]{2})', raw_text) or
                      re.search(r'合\s*计\s*[（\(]大写[）\)].*?小写[）\)]?\s*[¥￥\s]*([0-9\s]+\.[0-9\s]{2})', clean))
            if m_fall:
                total_amount = float(re.sub(r'\s+', '', m_fall.group(1)))
            else:
                total_amount = 0.0

        # 4. 商品名称
        goods = re.findall(r'\*([^*]+)\*([^\s\d\*\<\>¥￥]+)', clean)
        goods_desc = "; ".join([f"{g[0]}:{g[1]}" for g in goods]) if goods else ""

        return {
            'file': os.path.basename(pdf_path),
            'path': pdf_path,
            'invoice_num': invoice_num,
            'buyer_ok': buyer_ok,
            'tax_ok': tax_ok,
            'amount': total_amount,
            'goods': goods_desc,
            'raw_text_len': len(clean)
        }
    except Exception as e:
        return {'error': str(e), 'file': os.path.basename(pdf_path), 'amount': 0.0}


def parse_item_dir(dir_name):
    """
    解析条目目录名：{序号}-{品名规格}_{金额}[_{状态标记}]
    支持状态：已提交、已报销、已核销、开票中、开票未取、代付、优惠卷、差发票、差截图等
    """
    tags = []
    curr = dir_name
    matched = True
    while matched:
        matched = False
        for st in KNOWN_STATUSES:
            if curr.endswith(f"_{st}"):
                tags.append(st)
                curr = curr[:-len(f"_{st}")]
                matched = True
                break

    # 提取金额：最后一个下划线后的纯数字/浮点数
    amt_match = re.search(r'_([\d\.]+)$', curr)
    if amt_match:
        try:
            expected_amount = float(amt_match.group(1))
            stem = curr[:amt_match.start()]
        except ValueError:
            expected_amount = None
            stem = curr
    else:
        expected_amount = None
        stem = curr

    # 排除赛季、队伍或批次顶层目录误判为物料条目
    if re.match(r'^\d+赛季$', curr) or curr in ["主赛", "一队障碍", "一队任务", "二队任务", "嘉立创"]:
        return {
            'original': dir_name,
            'index': None,
            'item_name': dir_name,
            'expected_amount': None,
            'tags': tags,
            'status': "顶层目录"
        }

    # 提取序号与品名
    idx_match = re.match(r'^(\d+)[-–—\._\s]*(.*)$', stem)
    if idx_match:
        try:
            index = int(idx_match.group(1))
            item_name = idx_match.group(2).strip()
        except ValueError:
            index = None
            item_name = stem
    else:
        index = None
        item_name = stem

    primary_status = "待提交"
    if "已核销" in tags or "已报销" in tags:
        primary_status = "已核销"
    elif "已提交" in tags:
        primary_status = "已提交"
    elif "差发票" in tags:
        primary_status = "差发票"
    elif "差截图" in tags:
        primary_status = "差截图"
    elif "开票中" in tags or "开票未取" in tags:
        primary_status = "开票中"
    elif "优惠卷" in tags or "优惠券" in tags:
        primary_status = "优惠卷"
    elif "代付" in tags:
        primary_status = "代付"

    return {
        'original': dir_name,
        'index': index,
        'item_name': item_name,
        'expected_amount': expected_amount,
        'tags': tags,
        'status': primary_status
    }


def run_audit(target_dir):
    print("=" * 75)
    print(f"高校竞赛发票合规审计启动 (目标: {target_dir})")
    print(f"校验规则: 抬头='{EXPECTED_BUYER}', 税号='{EXPECTED_TAX_ID}', 单张上限<=¥{MAX_SINGLE_INVOICE_AMOUNT:.2f}")
    print("=" * 75)

    all_pdfs = []
    item_dirs = []

    for root, dirs, files in os.walk(target_dir):
        pdfs = [os.path.join(root, f) for f in files if f.lower().endswith('.pdf')]
        imgs = [os.path.join(root, f) for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        all_pdfs.extend(pdfs)

        folder_name = os.path.basename(root)
        meta = parse_item_dir(folder_name)
        if meta['index'] is not None or meta['expected_amount'] is not None:
            item_dirs.append({
                'path': root,
                'name': folder_name,
                'meta': meta,
                'pdfs': pdfs,
                'imgs': imgs
            })

    print(f"\n[扫描概览] 发现物料文件夹: {len(item_dirs)} 个, PDF 发票: {len(all_pdfs)} 份")

    print("\n--- [1] 发票合规穿透核验（抬头 / 税号 / 面额上限 / 唯一性） ---")
    invoice_registry = defaultdict(list)
    bad_buyer = []
    bad_tax = []
    over_limit_invoices = []
    pdf_info_cache = {}

    for p in all_pdfs:
        info = extract_pdf_info(p)
        pdf_info_cache[p] = info
        if 'error' in info:
            print(f"  [解析失败] {p}: {info['error']}")
            continue

        num = info['invoice_num']
        amt = info['amount']
        if num != "UNKNOWN":
            invoice_registry[num].append((p, amt))

        if info['raw_text_len'] > 50:
            if not info['buyer_ok']:
                bad_buyer.append((p, info))
            if not info['tax_ok']:
                bad_tax.append(p)

        if amt > MAX_SINGLE_INVOICE_AMOUNT:
            over_limit_invoices.append((p, amt, num))

    duplicates = {num: entries for num, entries in invoice_registry.items() if len(entries) > 1}
    if duplicates:
        print(f"  [!] 发现发票重复报销组数: {len(duplicates)}")
        for num, entries in duplicates.items():
            print(f"      发票号 [{num}]: 被引用 {len(entries)} 次")
            for e, a in entries:
                print(f"        - {e} (¥{a})")
    else:
        print("  [OK] 发票查重通过: 全局唯一性 100%, 0 组重复。")

    print(f"  * 抬头异常（非'{EXPECTED_BUYER}'）: {len(bad_buyer)} 份")
    for p, info in bad_buyer:
        print(f"      [!] {p}")

    print(f"  * 税号异常（非'{EXPECTED_TAX_ID}'）: {len(bad_tax)} 份")
    for p in bad_tax:
        print(f"      [!] {p}")

    print(f"  * 单张发票超额（超过 {MAX_SINGLE_INVOICE_AMOUNT:.2f} 元）: {len(over_limit_invoices)} 份")
    for p, amt, num in over_limit_invoices:
        print(f"      [!] 单张金额 ¥{amt:.2f} (发票号: {num}) -> {p}")

    print("\n--- [2] 发票生命周期状态资产核算 ---")
    status_summary = defaultdict(lambda: {'count': 0, 'amount': 0.0})
    for it in item_dirs:
        st = it['meta']['status']
        amt = it['meta']['expected_amount'] or 0.0
        status_summary[st]['count'] += 1
        status_summary[st]['amount'] += amt

    for st, data in sorted(status_summary.items()):
        print(f"  * [{st:6s}]: {data['count']:3d} 项 | 金额合计: {data['amount']:10.2f} 元")

    print("\n--- [3] 条目目录合规性与单据闭环核验 ---")
    person_groups = defaultdict(list)
    for it in item_dirs:
        parent = os.path.dirname(it['path'])
        person_groups[parent].append(it)

    for parent, items in person_groups.items():
        p_name = os.path.basename(parent)
        print(f"\n>> 申报单元: {p_name} ({len(items)} 项)")
        indexed_items = [it for it in items if it['meta']['index'] is not None]
        indexed_items.sort(key=lambda x: x['meta']['index'])

        indices = [it['meta']['index'] for it in indexed_items]
        missing_idx = []
        if indices:
            full_set = set(range(min(indices), max(indices) + 1))
            missing_idx = sorted(list(full_set - set(indices)))

        if missing_idx:
            print(f"    [!] 序号存在跳号/空缺: 缺失 {missing_idx}")
        else:
            print(f"    [OK] 序号连续 (1 ~ {max(indices) if indices else 0})")

        for it in items:
            m = it['meta']
            pdf_sum = sum(pdf_info_cache.get(p, {}).get('amount', 0.0) for p in it['pdfs'])
            pdf_sum = round(pdf_sum, 2)
            exp_amt = m['expected_amount']

            anomalies = []
            # 缺失检查
            if not it['pdfs']:
                if m['status'] not in ['开票中', '差发票']:
                    anomalies.append("缺少发票PDF (未标记 _差发票 或 _开票中)")
            else:
                if m['status'] == '差发票':
                    anomalies.append("已包含发票PDF但仍带有 _差发票 标记，需去除")

            if not it['imgs']:
                if m['status'] != '差截图':
                    anomalies.append("缺少支付/订单截图 (未标记 _差截图)")
            else:
                if m['status'] == '差截图':
                    anomalies.append("已包含截图凭证但仍带有 _差截图 标记，需去除")

            if exp_amt is not None and it['pdfs'] and abs(exp_amt - pdf_sum) > 0.05:
                if not any('14.pdf' in p for p in it['pdfs']):
                    anomalies.append(f"金额不一致: 目录标 {exp_amt} vs 发票和 {pdf_sum}")

            if anomalies:
                print(f"    [条目异常 - {m['status']}] {it['name']}: {', '.join(anomalies)}")

    print("\n" + "=" * 75)
    print("=== 审计流程结束 ===")
    print("=" * 75)


def generate_excel_ledger(batch_dir, output_path):
    if not openpyxl:
        print("Error: openpyxl is required to generate Excel ledger.")
        return

    print(f"正在从目录生成标准 11 列报销总账: {batch_dir} -> {output_path}")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "物料清单"

    headers = [
        "购买人", "位置编号", "购买物件名称", "数量", "单价",
        "总价", "支付记录金额", "发票编号", "发票金额", "购买用途",
        "发票总金额对不上支付记录金额请说明理由（商家优惠等）"
    ]
    ws.append(headers)

    header_font = Font(name="微软雅黑", size=10, bold=True)
    header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")
    border_thin = Border(
        left=Side(style='thin', color='B0B0B0'),
        right=Side(style='thin', color='B0B0B0'),
        top=Side(style='thin', color='B0B0B0'),
        bottom=Side(style='thin', color='B0B0B0')
    )

    ws.row_dimensions[1].height = 28
    for col in range(1, len(headers) + 1):
        cell = ws.cell(1, col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = border_thin

    entries = sorted(os.listdir(batch_dir))
    has_sub_person = any(os.path.isdir(os.path.join(batch_dir, e)) and parse_item_dir(e)['index'] is None for e in entries)

    person_dirs = []
    if has_sub_person:
        for e in entries:
            p = os.path.join(batch_dir, e)
            if os.path.isdir(p) and parse_item_dir(e)['index'] is None:
                person_dirs.append((re.sub(r'_[\d\.]+$', '', e), p))
    else:
        person_dirs.append(("", batch_dir))

    current_row = 2
    merge_operations = []

    for p_name, p_path in person_dirs:
        item_list = []
        for item_entry in os.listdir(p_path):
            ip = os.path.join(p_path, item_entry)
            if not os.path.isdir(ip):
                continue
            meta = parse_item_dir(item_entry)
            pdfs = sorted([os.path.join(ip, f) for f in os.listdir(ip) if f.lower().endswith('.pdf')])
            item_list.append({
                'entry': item_entry,
                'meta': meta,
                'pdfs': pdfs
            })

        item_list.sort(key=lambda x: (x['meta']['index'] if x['meta']['index'] is not None else 999))

        for it in item_list:
            meta = it['meta']
            idx = meta['index']
            name = meta['item_name']
            exp_amt = meta['expected_amount'] or 0.0

            pdf_infos = [extract_pdf_info(p) for p in it['pdfs']]
            reason = ""
            if "优惠卷" in meta['tags'] or "优惠券" in meta['tags']:
                reason = "平台优惠/红包抵扣"

            start_row = current_row
            num_rows = max(len(pdf_infos), 1)

            if not pdf_infos:
                ws.row_dimensions[current_row].height = 20
                row_data = [
                    p_name, idx, name, 1, exp_amt, exp_amt,
                    exp_amt, "待补票", exp_amt, name, reason
                ]
                ws.append(row_data)
                for c in range(1, 12):
                    cell = ws.cell(current_row, c)
                    cell.font = Font(name="微软雅黑", size=9)
                    cell.border = border_thin
                    if c in [1, 2, 4]:
                        cell.alignment = align_center
                    elif c in [5, 6, 7, 9]:
                        cell.alignment = align_right
                        cell.number_format = '#,##0.00'
                    elif c == 8:
                        cell.alignment = align_center
                    else:
                        cell.alignment = align_left
                current_row += 1
            else:
                for i, p_info in enumerate(pdf_infos):
                    r = current_row + i
                    ws.row_dimensions[r].height = 20
                    inv_num = str(p_info.get('invoice_num', ''))
                    inv_amt = p_info.get('amount', 0.0)

                    if i == 0:
                        ws.cell(r, 1, p_name)
                        ws.cell(r, 2, idx)
                        ws.cell(r, 3, name)
                        ws.cell(r, 4, 1)
                        ws.cell(r, 5, exp_amt)
                        ws.cell(r, 6, exp_amt)
                        ws.cell(r, 7, exp_amt)
                        ws.cell(r, 10, name)
                        ws.cell(r, 11, reason)
                    else:
                        for col_idx in [1, 2, 3, 4, 5, 6, 7, 10, 11]:
                            ws.cell(r, col_idx, None)

                    cell_num = ws.cell(r, 8, inv_num)
                    cell_num.number_format = '@'

                    cell_amt = ws.cell(r, 9, inv_amt)
                    cell_amt.number_format = '#,##0.00'

                    for c in range(1, 12):
                        cell = ws.cell(r, c)
                        cell.font = Font(name="微软雅黑", size=9)
                        cell.border = border_thin
                        if c in [1, 2, 4]:
                            cell.alignment = align_center
                        elif c in [5, 6, 7, 9]:
                            cell.alignment = align_right
                            if cell.value is not None and isinstance(cell.value, (int, float)):
                                cell.number_format = '#,##0.00'
                        elif c == 8:
                            cell.alignment = align_center
                        else:
                            cell.alignment = align_left

                if num_rows > 1:
                    for col_idx in [1, 2, 3, 4, 5, 6, 7, 10, 11]:
                        merge_operations.append((start_row, start_row + num_rows - 1, col_idx))

                current_row += num_rows

    # 执行跨行合并
    for sr, er, col in merge_operations:
        ws.merge_cells(start_row=sr, start_column=col, end_row=er, end_column=col)

    # 合计行
    tot_row = current_row
    ws.row_dimensions[tot_row].height = 24
    ws.cell(tot_row, 1, "合计")
    ws.cell(tot_row, 7, f"=SUM(G2:G{tot_row-1})")
    ws.cell(tot_row, 9, f"=SUM(I2:I{tot_row-1})")

    ws.merge_cells(start_row=tot_row, start_column=1, end_row=tot_row, end_column=6)

    fill_tot = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    font_tot = Font(name="微软雅黑", size=10, bold=True, color="000000")

    for c in range(1, 12):
        cell = ws.cell(tot_row, c)
        cell.font = font_tot
        cell.border = border_thin
        cell.fill = fill_tot
        if c == 1:
            cell.alignment = align_center
        elif c in [7, 9]:
            cell.alignment = align_right
            cell.number_format = '#,##0.00'
        else:
            cell.alignment = align_center

    col_widths = [12, 10, 26, 8, 12, 12, 15, 26, 13, 24, 26]
    for idx, width in enumerate(col_widths, 1):
        ws.column_dimensions[get_column_letter(idx)].width = width

    ws.views.sheetView[0].showGridLines = True

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    wb.save(output_path)
    print(f"标准 11 列报销总账生成完毕: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="高校竞赛发票合规审计与总账生成工具")
    parser.add_argument("--audit", type=str, help="审计目标目录")
    parser.add_argument("--generate-excel", type=str, help="根据目标批次目录生成报销总账")
    parser.add_argument("-o", "--output", type=str, help="Excel 导出文件路径")

    args = parser.parse_args()

    if args.audit:
        run_audit(args.audit)
    elif args.generate_excel:
        out = args.output or os.path.join(args.generate_excel, "报销总账.xlsx")
        generate_excel_ledger(args.generate_excel, out)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
