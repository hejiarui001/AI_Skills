<#
.SYNOPSIS
    pc-maintenance-master: Unified Launcher for Full PC Toolkit (D:\Tools)
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$Tool,
    
    [switch]$RunAsAdmin
)

$toolsRoot = "D:\Tools"

# Complete mapping across 7 standardized categories
$toolsMap = [ordered]@{
    # 01_Sysinternals
    'RAMMap'              = "$toolsRoot\01_Sysinternals\RAMMap\RAMMap64.exe"
    'Autoruns'            = "$toolsRoot\01_Sysinternals\Autoruns\Autoruns64.exe"
    'ProcessExplorer'     = "$toolsRoot\01_Sysinternals\ProcessExplorer\procexp64.exe"
    'TCPView'             = "$toolsRoot\01_Sysinternals\TCPView\tcpview64.exe"

    # 02_Hardware_Benchmark
    'HWiNFO'              = "$toolsRoot\02_Hardware_Benchmark\HWiNFO\HWiNFO64.exe"
    'CrystalDiskInfo'     = "$toolsRoot\02_Hardware_Benchmark\CrystalDiskInfo\DiskInfo64.exe"
    'CrystalDiskMark'     = "$toolsRoot\02_Hardware_Benchmark\CrystalDiskMark\DiskMark64.exe"
    'WizTree'             = "$toolsRoot\02_Hardware_Benchmark\WizTree\WizTree64.exe"

    # 03_System_Utilities
    'QuickLook'           = "$toolsRoot\03_System_Utilities\QuickLook\QuickLook.exe"
    'Everything'          = "$toolsRoot\03_System_Utilities\Everything\Everything.exe"
    'UniGetUI'            = "$toolsRoot\03_System_Utilities\UniGetUI\UniGetUI.exe"
    'HiBitUninstaller'    = "$toolsRoot\03_System_Utilities\HiBit Uninstaller\HiBitUninstaller.exe"
    'BleachBit'           = "$toolsRoot\03_System_Utilities\BleachBit\bleachbit.exe"
    'FreeFileSync'        = "$toolsRoot\03_System_Utilities\FreeFileSync\FreeFileSync.exe"
    'Carnac'              = "$toolsRoot\03_System_Utilities\Carnac\Carnac.exe"
    'TrafficMonitor'      = "$toolsRoot\03_System_Utilities\TrafficMonitor\TrafficMonitor.exe"
    'Ventoy'              = "$toolsRoot\03_System_Utilities\Ventoy\Ventoy2Disk.exe"
    'DesktopOK'           = "$toolsRoot\03_System_Utilities\DesktopOK\DesktopOK_x64.exe"
    'Nexus'               = "$toolsRoot\03_System_Utilities\Winstep Nexus\Nexus.exe"
    '7Zip'                = "$toolsRoot\03_System_Utilities\7-Zip\7zFM.exe"
    'PartitionAssistant'  = "$toolsRoot\03_System_Utilities\AOMEI Partition Assistant\PartAssist.exe"
    'RecoveryStar'        = "$toolsRoot\03_System_Utilities\傲梅恢复之星\4.9.0\MR.exe"
    'IHasher'             = "$toolsRoot\03_System_Utilities\IHasherv0.2.exe"

    # 04_Network_Transfer
    'ClashVerge'          = "$toolsRoot\04_Network_Transfer\Clash Verge\clash-verge.exe"
    'CloudDrive2'         = "$toolsRoot\04_Network_Transfer\CloudDrive2\clouddrive.exe"
    'Rayburst'            = "$toolsRoot\04_Network_Transfer\Rayburst\rayburst.exe"
    'SpeedManager'        = "$toolsRoot\04_Network_Transfer\SpeedManager\测速网.exe"
    'ToDesk'              = "$toolsRoot\04_Network_Transfer\ToDesk\ToDesk.exe"

    # 05_Productivity_Office
    'Zotero'              = "$toolsRoot\05_Productivity_Office\Zotero\zotero.exe"
    'ZoteroPdf2Zh'        = "$toolsRoot\05_Productivity_Office\zotero-pdf2zh\start_server.bat"
    'Notion'              = "$toolsRoot\05_Productivity_Office\Notion\Notion.exe"
    'TencentDocs'         = "$toolsRoot\05_Productivity_Office\TencentDocs\TencentDocsLauncher.exe"
    'YoudaoDict'          = "$toolsRoot\05_Productivity_Office\YoudaoDict\YoudaoDict.exe"

    # 06_Peripherals_Drivers
    'AtkHub'              = "$toolsRoot\06_Peripherals_Drivers\ATK HUB\ATK HUB.exe"
    'AulaKeyboard'        = "$toolsRoot\06_Peripherals_Drivers\AULA F3020\Config.exe"
    'MouseClick'          = "$toolsRoot\06_Peripherals_Drivers\MouseClick\MouseClick.exe"
    'VivoSuite'           = "$toolsRoot\06_Peripherals_Drivers\VivoSuite\pcsuite\pcsuite.exe"

    # 07_Media_Tools
    'EVCapture'           = "$toolsRoot\07_Media_Tools\EVCapture\EVCapture.exe"
    'FormatFactory'       = "$toolsRoot\07_Media_Tools\FormatFactory\FormatFactory.exe"
}

# Fuzzy / alias key match
$matchedKey = $toolsMap.Keys | Where-Object { $_ -like "*$Tool*" -or $Tool -like "*$_*" } | Select-Object -First 1

if (-not $matchedKey) {
    # Try direct name lookup
    $matchedKey = $Tool
}

$targetPath = $toolsMap[$matchedKey]

# Fallback resolution if primary path does not exist
if (-not $targetPath -or -not (Test-Path $targetPath)) {
    # Search under D:\Tools by name
    $search = Get-ChildItem -Path $toolsRoot -Recurse -Filter "*$Tool*.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($search) {
        $targetPath = $search.FullName
    }
}

if ($targetPath -and (Test-Path $targetPath)) {
    Write-Host "🚀 正在启动: $matchedKey ($targetPath)" -ForegroundColor Green
    if ($RunAsAdmin) {
        Start-Process -FilePath $targetPath -Verb RunAs
    } else {
        Start-Process -FilePath $targetPath
    }
} else {
    Write-Error "❌ 未在 D:\Tools 中找到可执行工具: $Tool"
    Write-Host "可用工具列表:" -ForegroundColor Yellow
    $toolsMap.Keys | ForEach-Object { Write-Host " - $_" }
}
