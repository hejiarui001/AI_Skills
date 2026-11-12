<#
.SYNOPSIS
    pc-maintenance-master: Safe Disk & Temp Junk Cleaner (with BleachBit CLI preview/clean)
#>
param(
    [switch]$Force,
    [switch]$DeepPreview,
    [switch]$DeepClean,
    [switch]$Json
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'SilentlyContinue'

function Invoke-BleachBitSafe {
    param(
        [ValidateSet('preview', 'clean')]
        [string]$Mode = 'preview'
    )

    $bbExe = "D:\Tools\03_System_Utilities\BleachBit\bleachbit_console.exe"
    if (-not (Test-Path -LiteralPath $bbExe)) {
        return [PSCustomObject]@{ Available = $false; Mode = $Mode; Error = "bleachbit_console.exe not found" }
    }

    # Whitelisted stateless cleaners only (never touch browser sessions, cookies, or recycle bin)
    $cleaners = @('system.tmp', 'system.logs', 'system.prefetch')
    $flag = if ($Mode -eq 'clean') { '-c' } else { '-p' }

    $origEnc = [Console]::OutputEncoding
    try {
        [Console]::OutputEncoding = [System.Text.Encoding]::GetEncoding(936)
        $lines = & $bbExe $flag @cleaners 2>&1 | ForEach-Object { "$_" }
    } finally {
        [Console]::OutputEncoding = $origEnc
    }

    $tail = @($lines | Where-Object { $_ -and $_.Trim() } | Select-Object -Last 6)
    $spaceText = ($tail | Where-Object { $_ -match '(预计释放磁盘空间|Disk space (to be )?recovered)[：:]\s*(.+)$' } | Select-Object -Last 1)
    $countText = ($tail | Where-Object { $_ -match '(即将删除的文件数量|Files (to be )?deleted|Deleted)[：:]\s*(\d+)' } | Select-Object -Last 1)

    $spaceVal = if ($spaceText -match '[：:]\s*(.+)$') { $Matches[1].Trim() } else { "0B" }
    $fileCount = if ($countText -match '(\d+)\s*$') { [int]$Matches[1] } else { 0 }

    return [PSCustomObject]@{
        Available      = $true
        Mode           = $Mode
        Cleaners       = $cleaners
        EstimatedSpace = $spaceVal
        FileCount      = $fileCount
    }
}

$result = [PSCustomObject]@{
    Mode           = if ($DeepPreview) { 'DeepPreview' } elseif ($DeepClean) { 'Standard+DeepClean' } else { 'Standard' }
    NativeCleaned  = $null
    BleachBit      = $null
}

if (-not $DeepPreview) {
    $targets = @(
        $env:TEMP,
        "$env:LOCALAPPDATA\CrashDumps",
        "$env:LOCALAPPDATA\Microsoft\Windows\INetCache"
    )

    $totalCleaned = 0
    $cleanedFiles = 0

    foreach ($folder in $targets) {
        if (Test-Path $folder) {
            if (-not $Json) { Write-Host "正在扫描: $folder" -ForegroundColor Yellow }
            $files = Get-ChildItem -Path $folder -Recurse -File -ErrorAction SilentlyContinue
            foreach ($file in $files) {
                $len = $file.Length
                try {
                    Remove-Item -Path $file.FullName -Force -ErrorAction Stop
                    $totalCleaned += $len
                    $cleanedFiles++
                } catch {
                    # In-use/locked files skipped safely
                }
            }
        }
    }

    $result.NativeCleaned = [PSCustomObject]@{
        Files   = $cleanedFiles
        FreedMB = [math]::Round($totalCleaned / 1MB, 2)
    }
}

if ($DeepPreview) {
    $result.BleachBit = Invoke-BleachBitSafe -Mode 'preview'
} elseif ($DeepClean) {
    $result.BleachBit = Invoke-BleachBitSafe -Mode 'clean'
}

if ($Json) {
    $result | ConvertTo-Json -Depth 4
} else {
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host " 🧹 PC 临时文件与垃圾安全清理 (PC Maintenance Master)" -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Cyan
    if ($result.NativeCleaned) {
        Write-Host "原生临时目录清理完成: 文件 $($result.NativeCleaned.Files) 个 | 释放 $($result.NativeCleaned.FreedMB) MB" -ForegroundColor Green
    }
    if ($result.BleachBit) {
        $bb = $result.BleachBit
        if ($bb.Available) {
            Write-Host "BleachBit [$($bb.Mode)] ($($bb.Cleaners -join ', ')): 空间 $($bb.EstimatedSpace) | 文件 $($bb.FileCount) 个" -ForegroundColor Yellow
        } else {
            Write-Host "BleachBit 不可用: $($bb.Error)" -ForegroundColor Red
        }
    }
    Write-Host "==========================================================" -ForegroundColor Cyan
}
