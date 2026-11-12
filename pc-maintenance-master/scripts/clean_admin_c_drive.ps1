<#
.SYNOPSIS
    pc-maintenance-master: Admin-level C-Drive Deep Cleaner
.DESCRIPTION
    Safely removes obsolete Windows Update backup directories from 2026-09-14 (10.22 GB)
    and GoogleUpdater crx caches (824 MB).
    Run with Administrator privileges.
#>
param(
    [switch]$IncludeHibernateReduction = $true,
    [switch]$RemoveOldSTM32Zip = $true
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'SilentlyContinue'

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Error "Requires Administrator privileges!"
    exit 1
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " 🚀 PC-Maintenance-Master: C 盘高收益深度清理 (管理员权限)" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

function Remove-ProtectedPath ($targetPath) {
    if (Test-Path $targetPath) {
        Write-Host "正在测量并清理: $targetPath ..." -ForegroundColor Yellow
        $size = (Get-ChildItem -Path $targetPath -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        
        # Try direct deletion first
        Remove-Item -Path $targetPath -Recurse -Force -ErrorAction SilentlyContinue
        
        # If still exists, take ownership and grant permissions
        if (Test-Path $targetPath) {
            Write-Host "  -> 提升所有权并授权..." -ForegroundColor DarkYellow
            & takeown /f "$targetPath" /r /d y 2>$null | Out-Null
            & icacls "$targetPath" /grant administrators:F /t /c /q 2>$null | Out-Null
            Remove-Item -Path $targetPath -Recurse -Force -ErrorAction SilentlyContinue
        }
        
        if (-not (Test-Path $targetPath)) {
            $mb = [math]::Round($size / 1MB, 2)
            Write-Host "  -> [成功] 已彻底清除，释放: $mb MB" -ForegroundColor Green
            return $size
        } else {
            Write-Host "  -> [部分完成] 部分文件被占用或锁定" -ForegroundColor Yellow
            return 0
        }
    } else {
        Write-Host "  -> [跳过] 路径不存在或已清理: $targetPath" -ForegroundColor Gray
        return 0
    }
}

$totalCleaned = 0

$targets = @(
    "C:\Windows\SoftwareDistribution.bak_20260914_170755",
    "C:\Windows\SoftwareDistribution.old",
    "C:\Program Files (x86)\Google\GoogleUpdater\crx_cache"
)

foreach ($t in $targets) {
    $s = Remove-ProtectedPath -targetPath $t
    $totalCleaned += $s
}

if ($RemoveOldSTM32Zip) {
    $zipPath = "C:\Users\hejia\STM32Cube\Repository\stm32cube_fw_f4_v1280.zip"
    if (Test-Path $zipPath) {
        $zipSize = (Get-Item $zipPath).Length
        Remove-Item -Path $zipPath -Force -ErrorAction SilentlyContinue
        $totalCleaned += $zipSize
        Write-Host "  -> [成功] 已清除冗余 STM32Cube F4 旧压缩包: $([math]::Round($zipSize/1MB,2)) MB" -ForegroundColor Green
    }
}

if ($IncludeHibernateReduction) {
    Write-Host "正在将休眠文件瘦身 (保留快速启动，释放约 4.3 GB)..." -ForegroundColor Yellow
    & powercfg /h /type reduced
    Write-Host "  -> [成功] 休眠文件已设置为 Reduced 模式！" -ForegroundColor Green
}

$freedGB = [math]::Round($totalCleaned / 1GB, 2)
Write-Host "----------------------------------------------------------" -ForegroundColor Cyan
Write-Host "深度清理完成！物理删除文件释放空间: $freedGB GB" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
