<#
.SYNOPSIS
    pc-maintenance-master: Comprehensive System & Performance Diagnostic Script
#>
param(
    [switch]$Json
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'SilentlyContinue'

# 1. Memory Metrics
$os = Get-CimInstance Win32_OperatingSystem
$totalRAM = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
$freeRAM = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
$usedRAM = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1MB, 2)
$usedPercent = [math]::Round((($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / $os.TotalVisibleMemorySize) * 100, 1)

$perf = Get-CimInstance Win32_PerfFormattedData_PerfOS_Memory
$nonPagedMB = if ($perf) { [math]::Round($perf.PoolNonpagedBytes / 1MB, 1) } else { 0 }
$pagedMB = if ($perf) { [math]::Round($perf.PoolPagedBytes / 1MB, 1) } else { 0 }
$committedGB = if ($perf) { [math]::Round($perf.CommittedBytes / 1GB, 2) } else { 0 }

# 2. Top Process Groups
$topProcesses = Get-Process | Group-Object ProcessName | ForEach-Object {
    $ws = [math]::Round(($_.Group | Measure-Object -Property WorkingSet64 -Sum).Sum / 1MB, 1)
    $pm = [math]::Round(($_.Group | Measure-Object -Property PrivateMemorySize64 -Sum).Sum / 1MB, 1)
    [PSCustomObject]@{
        Name = $_.Name
        Count = $_.Count
        'TotalWS_MB' = $ws
        'TotalPM_MB' = $pm
    }
} | Sort-Object 'TotalWS_MB' -Descending | Select-Object -First 12

# 3. Disks
$disks = Get-CimInstance Win32_LogicalDisk -Filter "DriveType = 3" | Select-Object DeviceID, VolumeName, 
    @{N='TotalGB';E={[math]::Round($_.Size/1GB, 1)}}, 
    @{N='FreeGB';E={[math]::Round($_.FreeSpace/1GB, 1)}}, 
    @{N='FreePercent';E={[math]::Round(($_.FreeSpace/$_.Size)*100, 1)}}

# 4. Critical Services Check
$checkServices = @('RemotePC_Service', 'WinDefend', 'SysMain', 'DoSvc', 'SWVisualize2024.Queue.Server', 'DiagTrack')
$servicesStatus = foreach ($s in $checkServices) {
    $svc = Get-Service -Name $s -ErrorAction SilentlyContinue
    if ($svc) {
        [PSCustomObject]@{
            Name = $svc.Name
            Status = $svc.Status.ToString()
            StartType = $svc.StartType.ToString()
        }
    }
}

# 5. Temp Junk Files
$tempSizeMB = [math]::Round(((Get-ChildItem -Path $env:TEMP -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB), 1)

$report = [PSCustomObject]@{
    Memory = [PSCustomObject]@{
        Total_GB = $totalRAM
        Used_GB = $usedRAM
        Free_GB = $freeRAM
        Used_Percent = $usedPercent
        NonPagedPool_MB = $nonPagedMB
        PagedPool_MB = $pagedMB
        Committed_GB = $committedGB
    }
    TopProcesses = $topProcesses
    Disks = $disks
    KeyServices = $servicesStatus
    TempJunk_MB = $tempSizeMB
}

if ($Json) {
    $report | ConvertTo-Json -Depth 4
} else {
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host " 💻 PC 综合体检与性能诊断报告 (PC Maintenance Master)" -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "[1] 物理内存状态:" -ForegroundColor Yellow
    Write-Host "    总内存: $totalRAM GB | 已占用: $usedRAM GB ($usedPercent%) | 可用: $freeRAM GB"
    Write-Host "    非分页池: $nonPagedMB MB | 分页池: $pagedMB MB | 已提交: $committedGB GB"
    Write-Host ""
    Write-Host "[2] 占用最高的进程组 (前 10):" -ForegroundColor Yellow
    $topProcesses | Select-Object -First 10 | Format-Table -AutoSize | Out-String | Write-Host
    Write-Host "[3] 本地磁盘空间:" -ForegroundColor Yellow
    $disks | Format-Table -AutoSize | Out-String | Write-Host
    Write-Host "[4] 核心后台服务状态:" -ForegroundColor Yellow
    $servicesStatus | Format-Table -AutoSize | Out-String | Write-Host
    Write-Host "[5] 用户临时缓存占用: $tempSizeMB MB" -ForegroundColor Yellow
    Write-Host "==========================================================" -ForegroundColor Cyan
}
