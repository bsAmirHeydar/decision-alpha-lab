# Run from the project root before applying the Phoenix rebuild patch.
# This removes old FlagCounting code paths that created patch-on-patch conflicts.

$ErrorActionPreference = "SilentlyContinue"

Remove-Item -Recurse -Force ".\mql5\Include\FlagCounting"
Remove-Item -Recurse -Force ".\mql5\Include\FlagCountingVNext"
Remove-Item -Recurse -Force ".\mql5\Include\FlagCountingV6"
Remove-Item -Recurse -Force ".\mql5\Include\FlagCountingPhoenix"

Get-ChildItem ".\mql5\Experts\FlagCounting" -Filter "FlagCounting*.mq5" | Remove-Item -Force

$ErrorActionPreference = "Continue"
Write-Host "Old FlagCounting code paths removed. Now apply the Phoenix patch zip."
