[CmdletBinding()]
param(
    [string]$PatchZip = '.\decision-alpha-lab-ucee-i10-deep-multiview-pack-v1.1.0.zip',
    [string]$RepoRoot = '.',
    [string]$ChecksumFile = '.\UCEE_I10_RELEASE_SHA256.txt'
)

$apply = Join-Path (Resolve-Path -LiteralPath $RepoRoot).Path 'tools\strategy_factory\apply_uce_i10_patch.ps1'
if (-not (Test-Path -LiteralPath $apply)) {
    throw "Apply script not found after resolving RepoRoot: $apply"
}
& $apply -PatchZip $PatchZip -RepoRoot $RepoRoot -ChecksumFile $ChecksumFile -RemoveZipAfterSuccess
