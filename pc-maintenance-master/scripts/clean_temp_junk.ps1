<#
.SYNOPSIS
    pc-maintenance-master: Safe Disk & Temp Junk Cleaner
#>
param(
    [switch]$Force
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'SilentlyContinue'

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " 🧹 PC 临时文件与垃圾安全清理 (PC Maintenance Master)" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

$targets = @(
    $env:TEMP,
    "$env:LOCALAPPDATA\CrashDumps",
    "$env:LOCALAPPDATA\Microsoft\Windows\INetCache"
)

$totalCleaned = 0
$cleanedFiles = 0

foreach ($folder in $targets) {
    if (Test-Path $folder) {
        Write-Host "正在扫描: $folder" -ForegroundColor Yellow
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

$freedMB = [math]::Round($totalCleaned / 1MB, 2)
Write-Host "----------------------------------------------------------" -ForegroundColor Cyan
Write-Host "清理完成！" -ForegroundColor Green
Write-Host "共清理文件: $cleanedFiles 个"
Write-Host "释放磁盘空间: $freedMB MB"
Write-Host "==========================================================" -ForegroundColor Cyan
