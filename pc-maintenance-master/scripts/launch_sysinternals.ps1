<#
.SYNOPSIS
    pc-maintenance-master: Unified Launcher for System Maintenance Toolkit
#>
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('RAMMap', 'Autoruns', 'ProcessExplorer', 'TCPView', 'WizTree', 'CrystalDiskInfo', 'Everything', 'BleachBit', 'HiBitUninstaller')]
    [string]$Tool,
    
    [switch]$RunAsAdmin
)

$toolsMap = @{
    'RAMMap'           = 'D:\Tools\RAMMap\RAMMap64.exe'
    'Autoruns'         = 'D:\Tools\Autoruns\Autoruns64.exe'
    'ProcessExplorer'  = 'D:\Tools\ProcessExplorer\procexp64.exe'
    'TCPView'          = 'D:\Tools\TCPView\tcpview64.exe'
    'WizTree'          = 'D:\Tools\WizTree\WizTree64.exe'
    'CrystalDiskInfo'  = 'D:\Tools\CrystalDiskInfo\DiskInfo64.exe'
    'Everything'       = 'D:\Tools\Everything\Everything.exe'
    'BleachBit'        = 'D:\Tools\BleachBit\bleachbit.exe'
    'HiBitUninstaller' = 'D:\Tools\HiBit Uninstaller\HiBitUninstaller.exe'
}

$targetPath = $toolsMap[$Tool]

# Fallbacks if 64-bit specific name differs
if (!(Test-Path $targetPath)) {
    if ($Tool -eq 'ProcessExplorer') { $targetPath = 'D:\Tools\ProcessExplorer\procexp.exe' }
    elseif ($Tool -eq 'RAMMap') { $targetPath = 'D:\Tools\RAMMap\RAMMap.exe' }
    elseif ($Tool -eq 'Autoruns') { $targetPath = 'D:\Tools\Autoruns\Autoruns.exe' }
    elseif ($Tool -eq 'TCPView') { $targetPath = 'D:\Tools\TCPView\tcpview.exe' }
    elseif ($Tool -eq 'WizTree') { $targetPath = 'D:\Tools\WizTree\WizTree.exe' }
    elseif ($Tool -eq 'CrystalDiskInfo') { $targetPath = 'D:\Tools\CrystalDiskInfo\DiskInfo32.exe' }
}

if (Test-Path $targetPath) {
    Write-Host "正在启动工具: $Tool -> $targetPath" -ForegroundColor Green
    if ($RunAsAdmin) {
        Start-Process -FilePath $targetPath -Verb RunAs
    } else {
        Start-Process -FilePath $targetPath
    }
} else {
    Write-Error "未找到工具文件: $targetPath"
}
