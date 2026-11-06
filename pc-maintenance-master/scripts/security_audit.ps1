<#
.SYNOPSIS
    pc-maintenance-master: Comprehensive System Security Posture Audit
#>
param(
    [switch]$Json
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'SilentlyContinue'

# 1. Antivirus & Defender Posture
$mp = Get-MpComputerStatus -ErrorAction SilentlyContinue
$avEnabled = $mp.AntivirusEnabled
$rtEnabled = $mp.RealTimeProtectionEnabled
$sigAge = $mp.AntivirusSignatureAge
$cloudEnabled = $mp.MAPSReporting -gt 0

# Check exclusions
$exclusions = (Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows Defender\Exclusions\Paths" -ErrorAction SilentlyContinue)
$unsafeExclusion = $false
if ($exclusions) {
    foreach ($prop in $exclusions.PSObject.Properties) {
        if ($prop.Name -in @('C:\', 'C:\Windows', 'C:\Windows\System32', 'C:\Program Files')) {
            $unsafeExclusion = $true
        }
    }
}

# 2. Firewall Status
$fwProfiles = Get-NetFirewallProfile -ErrorAction SilentlyContinue
$allFwActive = ($fwProfiles | Where-Object { $_.Enabled -eq $true }).Count -eq 3

# 3. UAC & System Hardening
$uac = (Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -ErrorAction SilentlyContinue).EnableLUA
$uacActive = ($uac -eq 1)

# RDP status
$rdpDeny = (Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server" -ErrorAction SilentlyContinue).fDenyTSConnections
$rdpEnabled = ($rdpDeny -eq 0)

# 4. Listening High-Risk Ports Check
$listening = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue
$port3389 = ($listening | Where-Object { $_.LocalPort -eq 3389 }).Count -gt 0
$port445  = ($listening | Where-Object { $_.LocalPort -eq 445 -and $_.LocalAddress -match '0\.0\.0\.0|::' }).Count -gt 0

# 5. Suspicious Temp-based Startup Items
$suspiciousStartups = @()
$runItems = Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run", "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run" -ErrorAction SilentlyContinue
foreach ($item in $runItems) {
    foreach ($prop in $item.PSObject.Properties) {
        $val = "$($prop.Value)"
        if ($val -match "AppData\\Local\\Temp|AppData\\Roaming\\Temp|C:\\Users\\Public") {
            $suspiciousStartups += "$($prop.Name): $val"
        }
    }
}

$secReport = [PSCustomObject]@{
    Antivirus = [PSCustomObject]@{
        Enabled = $avEnabled
        RealTime = $rtEnabled
        SignatureAgeDays = $sigAge
        CloudProtection = $cloudEnabled
        HasDangerousExclusions = $unsafeExclusion
    }
    Firewall = [PSCustomObject]@{
        AllProfilesActive = $allFwActive
        Profiles = ($fwProfiles | ForEach-Object { "$($_.Name): $($_.Enabled)" }) -join '; '
    }
    SystemHardening = [PSCustomObject]@{
        UAC_Active = $uacActive
        RDP_Exposed = $rdpEnabled
        Port3389_Listening = $port3389
        Port445_PublicListening = $port445
    }
    StartupIntegrity = [PSCustomObject]@{
        SuspiciousTempItems = $suspiciousStartups
        IsClean = ($suspiciousStartups.Count -eq 0)
    }
}

if ($Json) {
    $secReport | ConvertTo-Json -Depth 4
} else {
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host " 🛡️ 系统安全态势基线检查 (PC Maintenance Master)" -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Cyan
    
    if ($avEnabled -and $rtEnabled -and ($sigAge -le 2)) {
        Write-Host " [OK] 病毒防护引擎: 正常 (实时防护开启, 病毒库今日最新)" -ForegroundColor Green
    } else {
        Write-Host " [WARN] 病毒防护引擎: 异常 (实时防护: $rtEnabled, 病毒库超期: $sigAge 天)" -ForegroundColor Red
    }
    
    if ($unsafeExclusion) {
        Write-Host " [WARN] 排除项审计: 检测到根目录或系统关键目录存在全盘排除项！" -ForegroundColor Red
    } else {
        Write-Host " [OK] 排除项审计: 正常 (未发现全盘或System32高危全免扫描)" -ForegroundColor Green
    }

    if ($allFwActive) {
        Write-Host " [OK] Windows 网络防火墙: 正常 (域/专用/公用网络全开启)" -ForegroundColor Green
    } else {
        Write-Host " [WARN] Windows 网络防火墙: 部分未开启 ($($secReport.Firewall.Profiles))" -ForegroundColor Yellow
    }

    if ($uacActive) {
        Write-Host " [OK] UAC 用户账户控制: 正常开启 (防止恶意程序静默提权)" -ForegroundColor Green
    } else {
        Write-Host " [WARN] UAC 用户账户控制: 已关闭 (高风险!)" -ForegroundColor Red
    }

    if ($rdpEnabled) {
        Write-Host " [INFO] 远程桌面 (RDP / 3389端口): 已开启 (用于远程连接，请确保系统用户为强密码)" -ForegroundColor Yellow
    } else {
        Write-Host " [OK] 远程桌面 (RDP): 已关闭" -ForegroundColor Green
    }

    if ($suspiciousStartups.Count -eq 0) {
        Write-Host " [OK] 自启项安全审计: 正常 (未检测到隐藏在 Temp/Public 的可疑启动项)" -ForegroundColor Green
    } else {
        Write-Host " [WARN] 警告: 发现可疑临时目录自启动项: $($suspiciousStartups -join ', ')" -ForegroundColor Red
    }

    Write-Host "==========================================================" -ForegroundColor Cyan
}
