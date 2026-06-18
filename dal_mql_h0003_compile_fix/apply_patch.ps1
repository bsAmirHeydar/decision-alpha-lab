param(
  [string]$ProjectRoot = ".",
  [switch]$NoCleanup
)

$ErrorActionPreference = "Stop"

function Resolve-ProjectRoot([string]$Path) {
  if ([string]::IsNullOrWhiteSpace($Path)) { $Path = "." }
  return (Resolve-Path -LiteralPath $Path).Path
}

function Find-MatchingParen([string]$Text, [int]$OpenIndex) {
  $depth = 0
  $inString = $false
  $quote = [char]0
  for ($i = $OpenIndex; $i -lt $Text.Length; $i++) {
    $ch = $Text[$i]
    if ($inString) {
      if ($ch -eq $quote) { $inString = $false }
      continue
    }
    if ($ch -eq '"' -or $ch -eq "'") {
      $inString = $true
      $quote = $ch
      continue
    }
    if ($ch -eq '(') { $depth++ }
    elseif ($ch -eq ')') {
      $depth--
      if ($depth -eq 0) { return $i }
    }
  }
  return -1
}

function Count-TopLevelArgs([string]$ArgsText) {
  if ([string]::IsNullOrWhiteSpace($ArgsText)) { return 0 }
  $depth = 0
  $commas = 0
  $inString = $false
  $quote = [char]0

  for ($i = 0; $i -lt $ArgsText.Length; $i++) {
    $ch = $ArgsText[$i]
    if ($inString) {
      if ($ch -eq $quote) { $inString = $false }
      continue
    }
    if ($ch -eq '"' -or $ch -eq "'") {
      $inString = $true
      $quote = $ch
      continue
    }
    if ($ch -eq '(' -or $ch -eq '[' -or $ch -eq '{') { $depth++ }
    elseif ($ch -eq ')' -or $ch -eq ']' -or $ch -eq '}') { if ($depth -gt 0) { $depth-- } }
    elseif ($ch -eq ',' -and $depth -eq 0) { $commas++ }
  }
  return ($commas + 1)
}

function Is-In-LineComment([string]$Text, [int]$Index) {
  $lineStart = $Text.LastIndexOf("`n", [Math]::Max(0, $Index - 1))
  if ($lineStart -lt 0) { $lineStart = 0 } else { $lineStart++ }
  $prefix = $Text.Substring($lineStart, $Index - $lineStart)
  return ($prefix.Contains("//"))
}

function Patch-RandomFractionCallArity([System.IO.FileInfo]$File) {
  $text = Get-Content -LiteralPath $File.FullName -Raw
  $matches = [regex]::Matches($text, 'DAL_M0001RandomFractionK\s*\(')
  $edits = New-Object System.Collections.Generic.List[object]
  $patchIndex = 0

  foreach ($m in $matches) {
    if (Is-In-LineComment $text $m.Index) { continue }

    $openIndex = $text.IndexOf('(', $m.Index)
    if ($openIndex -lt 0) { continue }

    $closeIndex = Find-MatchingParen $text $openIndex
    if ($closeIndex -lt 0) { continue }

    $args = $text.Substring($openIndex + 1, $closeIndex - $openIndex - 1)
    $count = Count-TopLevelArgs $args

    # The compiler error says DAL_M0001RandomFractionK now requires 4 args.
    # We only patch old call sites that still pass exactly 3 args.
    if ($count -eq 3) {
      $patchIndex++
      $salt = 300300 + $patchIndex
      $newArgs = $args.TrimEnd() + ", " + $salt.ToString()
      $edits.Add([pscustomobject]@{ Start = $openIndex + 1; End = $closeIndex; Text = $newArgs }) | Out-Null
    }
  }

  if ($edits.Count -eq 0) {
    return 0
  }

  $backup = $File.FullName + ".bak_" + (Get-Date -Format "yyyyMMdd_HHmmss")
  Copy-Item -LiteralPath $File.FullName -Destination $backup -Force

  for ($i = $edits.Count - 1; $i -ge 0; $i--) {
    $e = $edits[$i]
    $before = $text.Substring(0, $e.Start)
    $after = $text.Substring($e.End)
    $text = $before + $e.Text + $after
  }

  Set-Content -LiteralPath $File.FullName -Value $text -Encoding UTF8
  return $edits.Count
}

$root = Resolve-ProjectRoot $ProjectRoot
Write-Host "DAL MQL H0003 compile patch"
Write-Host "Project root: $root"

$reportFiles = Get-ChildItem -Path $root -Recurse -File -Filter "DAL_M0003Reports.mqh" -ErrorAction SilentlyContinue
if (-not $reportFiles -or $reportFiles.Count -eq 0) {
  throw "DAL_M0003Reports.mqh was not found under: $root. Run this on the MQL project root, not the Python/docs zip."
}

$total = 0
foreach ($file in $reportFiles) {
  $n = Patch-RandomFractionCallArity $file
  $total += $n
  if ($n -gt 0) {
    Write-Host "patched $n call(s): $($file.FullName)"
  } else {
    Write-Host "no 3-arg DAL_M0001RandomFractionK call found: $($file.FullName)"
  }
}

Write-Host "Total patched calls: $total"
if ($total -eq 0) {
  Write-Host "Nothing changed. The arity error may already be fixed, or the failing file is different."
}

Write-Host "Next: compile the EA/indicator in MetaEditor and check remaining errors."

if (-not $NoCleanup) {
  $patchDir = $PSScriptRoot
  Write-Host "Cleaning patch folder: $patchDir"
  try {
    Push-Location (Split-Path -Parent $patchDir)
    Remove-Item -LiteralPath $patchDir -Recurse -Force -ErrorAction Stop
    Pop-Location
  } catch {
    try { Pop-Location } catch {}
    Write-Host "Patch was applied, but the patch folder could not be removed automatically. You can delete it manually."
  }
}
