param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("indicator", "tool")]
    [string]$Type,

    [Parameter(Mandatory = $true)]
    [ValidatePattern("^[a-z0-9][a-z0-9-]*[a-z0-9]$")]
    [string]$Slug,

    [Parameter(Mandatory = $false)]
    [string]$Title
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProductLabRoot = Resolve-Path (Join-Path $ScriptDir "..")

if ([string]::IsNullOrWhiteSpace($Title)) {
    $Title = $Slug
}

$CreatedDate = (Get-Date).ToString("yyyy-MM-dd")

if ($Type -eq "indicator") {
    $TemplatePath = Join-Path $ProductLabRoot "indicators\_template"
    $DestinationPath = Join-Path $ProductLabRoot ("indicators\" + $Slug)
} else {
    $TemplatePath = Join-Path $ProductLabRoot "tools\_template"
    $DestinationPath = Join-Path $ProductLabRoot ("tools\" + $Slug)
}

if (-not (Test-Path $TemplatePath)) {
    throw "Template not found: $TemplatePath"
}

if (Test-Path $DestinationPath) {
    throw "Destination already exists: $DestinationPath"
}

Copy-Item -Path $TemplatePath -Destination $DestinationPath -Recurse

$Files = Get-ChildItem -Path $DestinationPath -Recurse -File
foreach ($File in $Files) {
    $Content = Get-Content -Path $File.FullName -Raw -ErrorAction SilentlyContinue
    if ($null -ne $Content) {
        $Content = $Content.Replace("{{PRODUCT_TITLE}}", $Title)
        $Content = $Content.Replace("{{PRODUCT_SLUG}}", $Slug)
        $Content = $Content.Replace("{{CREATED_DATE}}", $CreatedDate)
        Set-Content -Path $File.FullName -Value $Content -Encoding UTF8
    }
}

Write-Host "Created $Type product scaffold:" -ForegroundColor Green
Write-Host $DestinationPath
Write-Host "Next: fill spec files and update product_lab\registry." -ForegroundColor Yellow
