param(
    [Parameter(Mandatory = $false)]
    [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path,

    [Parameter(Mandatory = $false)]
    [switch]$WhatIfOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = (Resolve-Path $ProjectRoot).Path
$ArchiveRoot = Join-Path $Root "docs\history\root_archive"

$Groups = @{
    "00_start_here" = @("00_*.md")
    "install_guides" = @("INSTALL_*.md")
    "patch_readmes" = @("README_*.md")
    "patch_diffs" = @("*.diff")
}

$KeepNames = @(
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "requirements.txt",
    ".gitignore"
)

function Move-DocFile {
    param(
        [System.IO.FileInfo]$File,
        [string]$GroupName
    )

    if ($KeepNames -contains $File.Name) {
        return $false
    }

    $TargetDir = Join-Path $ArchiveRoot $GroupName
    $TargetPath = Join-Path $TargetDir $File.Name

    if ($WhatIfOnly) {
        Write-Host "WHATIF: $($File.Name) -> docs\history\root_archive\$GroupName\$($File.Name)"
        return $true
    }

    if (-not (Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    }

    if (Test-Path $TargetPath) {
        $Stamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
        $BaseName = [System.IO.Path]::GetFileNameWithoutExtension($File.Name)
        $Ext = [System.IO.Path]::GetExtension($File.Name)
        $TargetPath = Join-Path $TargetDir ("$BaseName`_$Stamp$Ext")
    }

    Move-Item -Path $File.FullName -Destination $TargetPath
    Write-Host "MOVED: $($File.Name) -> $TargetPath"
    return $true
}

$MovedCount = 0

foreach ($GroupName in $Groups.Keys) {
    foreach ($Pattern in $Groups[$GroupName]) {
        $Files = Get-ChildItem -Path $Root -File -Filter $Pattern
        foreach ($File in $Files) {
            if (Move-DocFile -File $File -GroupName $GroupName) {
                $MovedCount += 1
            }
        }
    }
}

$ReadmePath = Join-Path $ArchiveRoot "README.md"
if (-not $WhatIfOnly) {
    if (-not (Test-Path $ArchiveRoot)) {
        New-Item -ItemType Directory -Path $ArchiveRoot -Force | Out-Null
    }

    if (-not (Test-Path $ReadmePath)) {
        @"
# Root Archive

این پوشه برای جمع‌آوری فایل‌های مستنداتی است که قبلاً در روت پروژه پخش شده بودند.

## گروه‌ها

- `00_start_here/` فایل‌های شروع سریع و نقطه ورود پچ‌ها
- `install_guides/` راهنماهای نصب پچ‌ها
- `patch_readmes/` READMEهای مربوط به پچ‌ها و ماژول‌ها
- `patch_diffs/` فایل‌های diff قدیمی

فایل‌های اصلی روت مثل `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `requirements.txt` و `.gitignore` در روت باقی می‌مانند.
"@ | Set-Content -Path $ReadmePath -Encoding UTF8
    }
}

Write-Host "Done. Matched files: $MovedCount" -ForegroundColor Green
if ($WhatIfOnly) {
    Write-Host "No files were moved because -WhatIfOnly was used." -ForegroundColor Yellow
}
