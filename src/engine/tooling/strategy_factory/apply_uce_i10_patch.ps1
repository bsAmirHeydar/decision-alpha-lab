[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$PatchZip,
    [Parameter(Mandatory=$true)][string]$RepoRoot,
    [string]$ChecksumFile = '',
    [switch]$RemoveZipAfterSuccess
)

$ErrorActionPreference = 'Stop'
$patch = (Resolve-Path -LiteralPath $PatchZip).Path
$repo = (Resolve-Path -LiteralPath $RepoRoot).Path
if (-not (Test-Path -LiteralPath (Join-Path $repo 'lab\11_strategy_factory'))) {
    throw "RepoRoot does not look like Decision Alpha Lab: $repo"
}

if ($ChecksumFile) {
    $checksumPath = (Resolve-Path -LiteralPath $ChecksumFile).Path
    $line = Get-Content -LiteralPath $checksumPath | Where-Object { $_ -match [regex]::Escape([IO.Path]::GetFileName($patch)) } | Select-Object -First 1
    if (-not $line) { throw 'Patch filename is absent from checksum file.' }
    $expected = ($line -split '\s+')[0].ToLowerInvariant()
    $actual = (Get-FileHash -LiteralPath $patch -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $expected) { throw "Checksum mismatch. expected=$expected actual=$actual" }
}

$stage = Join-Path ([IO.Path]::GetTempPath()) ("uce-i10-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $stage | Out-Null
$validated = $false
try {
    Expand-Archive -LiteralPath $patch -DestinationPath $stage -Force
    $files = Get-ChildItem -LiteralPath $stage -File -Recurse
    if (-not $files) { throw 'Patch archive is empty.' }
    foreach ($file in $files) {
        $relative = [IO.Path]::GetRelativePath($stage, $file.FullName)
        if ([IO.Path]::IsPathRooted($relative) -or $relative -match '(^|[\\/])\.\.([\\/]|$)') {
            throw "Unsafe archive path: $relative"
        }
    }
    Copy-Item -Path (Join-Path $stage '*') -Destination $repo -Recurse -Force
    & (Join-Path $repo 'src\engine\tooling\strategy_factory\run_uce_i10_tests.ps1') -RepoRoot $repo
    if ($LASTEXITCODE -ne 0) { throw "UCE-I10 validation failed with exit code $LASTEXITCODE" }
    $validated = $true
}
finally {
    if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
}

if ($validated -and $RemoveZipAfterSuccess) {
    Remove-Item -LiteralPath $patch -Force
}
Write-Host "UCE-I10 patch applied and validated: $repo"
