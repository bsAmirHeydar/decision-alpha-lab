param(
    [string]$ProjectRoot = "."
)

$ErrorActionPreference = "Stop"

function Write-Info([string]$msg) { Write-Host "[DAL PATCH] $msg" }
function Write-Warn([string]$msg) { Write-Host "[DAL PATCH WARNING] $msg" -ForegroundColor Yellow }
function Write-Fail([string]$msg) { Write-Host "[DAL PATCH ERROR] $msg" -ForegroundColor Red }

function Resolve-ProjectRoot([string]$root) {
    $full = [System.IO.Path]::GetFullPath($root)
    if (-not (Test-Path -LiteralPath $full)) {
        throw "Project root not found: $full"
    }
    return $full
}

function Get-TextUtf8([string]$path) {
    return [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
}

function Set-TextUtf8([string]$path, [string]$text) {
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($path, $text, $utf8NoBom)
}

function Split-TopLevelArgs([string]$argsText) {
    $items = New-Object System.Collections.Generic.List[string]
    $start = 0
    $depthParen = 0
    $depthBracket = 0
    $depthBrace = 0
    $inString = $false
    $stringChar = [char]0
    $escape = $false

    for ($i = 0; $i -lt $argsText.Length; $i++) {
        $c = $argsText[$i]

        if ($inString) {
            if ($escape) {
                $escape = $false
                continue
            }
            if ($c -eq '\\') {
                $escape = $true
                continue
            }
            if ($c -eq $stringChar) {
                $inString = $false
                $stringChar = [char]0
            }
            continue
        }

        if ($c -eq '"' -or $c -eq "'") {
            $inString = $true
            $stringChar = $c
            continue
        }

        switch ($c) {
            '(' { $depthParen++ }
            ')' { if ($depthParen -gt 0) { $depthParen-- } }
            '[' { $depthBracket++ }
            ']' { if ($depthBracket -gt 0) { $depthBracket-- } }
            '{' { $depthBrace++ }
            '}' { if ($depthBrace -gt 0) { $depthBrace-- } }
            ',' {
                if ($depthParen -eq 0 -and $depthBracket -eq 0 -and $depthBrace -eq 0) {
                    $items.Add($argsText.Substring($start, $i - $start).Trim())
                    $start = $i + 1
                }
            }
        }
    }

    $tail = $argsText.Substring($start).Trim()
    if ($tail.Length -gt 0 -or $argsText.Trim().Length -gt 0) {
        $items.Add($tail)
    }
    return $items
}

function Find-MatchingParen([string]$text, [int]$openIndex) {
    $depth = 0
    $inString = $false
    $stringChar = [char]0
    $escape = $false
    $inLineComment = $false
    $inBlockComment = $false

    for ($i = $openIndex; $i -lt $text.Length; $i++) {
        $c = $text[$i]
        $n = if ($i + 1 -lt $text.Length) { $text[$i + 1] } else { [char]0 }

        if ($inLineComment) {
            if ($c -eq "`n") { $inLineComment = $false }
            continue
        }
        if ($inBlockComment) {
            if ($c -eq '*' -and $n -eq '/') { $inBlockComment = $false; $i++ }
            continue
        }
        if ($inString) {
            if ($escape) { $escape = $false; continue }
            if ($c -eq '\\') { $escape = $true; continue }
            if ($c -eq $stringChar) { $inString = $false; $stringChar = [char]0 }
            continue
        }

        if ($c -eq '/' -and $n -eq '/') { $inLineComment = $true; $i++; continue }
        if ($c -eq '/' -and $n -eq '*') { $inBlockComment = $true; $i++; continue }
        if ($c -eq '"' -or $c -eq "'") { $inString = $true; $stringChar = $c; continue }

        if ($c -eq '(') { $depth++ }
        elseif ($c -eq ')') {
            $depth--
            if ($depth -eq 0) { return $i }
        }
    }
    return -1
}

function Is-ProbablyFunctionDefinition([string]$prefix) {
    $tail = $prefix
    if ($tail.Length -gt 160) { $tail = $tail.Substring($tail.Length - 160) }
    return ($tail -match '(?s)\b(double|int|void|bool|string|datetime|long|ulong|float)\s+DAL_M0001RandomFractionK\s*$')
}

function Patch-RandomFractionK([string]$text, [ref]$patchedCount) {
    $name = 'DAL_M0001RandomFractionK'
    $sb = New-Object System.Text.StringBuilder
    $pos = 0
    $count = 0

    while ($true) {
        $idx = $text.IndexOf($name, $pos, [System.StringComparison]::Ordinal)
        if ($idx -lt 0) { break }

        $afterName = $idx + $name.Length
        $j = $afterName
        while ($j -lt $text.Length -and [char]::IsWhiteSpace($text[$j])) { $j++ }
        if ($j -ge $text.Length -or $text[$j] -ne '(') {
            $pos = $afterName
            continue
        }

        $prefix = $text.Substring([Math]::Max(0, $idx - 180), $idx - [Math]::Max(0, $idx - 180))
        if (Is-ProbablyFunctionDefinition $prefix) {
            $pos = $afterName
            continue
        }

        $close = Find-MatchingParen $text $j
        if ($close -lt 0) {
            throw "Unmatched parenthesis near DAL_M0001RandomFractionK at char $idx"
        }

        $argsText = $text.Substring($j + 1, $close - $j - 1)
        $args = Split-TopLevelArgs $argsText

        if ($args.Count -eq 3) {
            [void]$sb.Append($text.Substring($pos, $close - $pos))
            [void]$sb.Append(', 0')
            $pos = $close
            $count++
        } else {
            $pos = $close
        }
    }

    [void]$sb.Append($text.Substring($pos))
    $patchedCount.Value = $count
    return $sb.ToString()
}

try {
    $root = Resolve-ProjectRoot $ProjectRoot
    Write-Info "Project root: $root"

    $mqlFiles = Get-ChildItem -LiteralPath $root -Recurse -File -Include *.mqh,*.mq5 -ErrorAction SilentlyContinue
    if (-not $mqlFiles -or $mqlFiles.Count -eq 0) {
        throw "No .mqh/.mq5 files found under: $root"
    }

    $targetFiles = $mqlFiles | Where-Object { $_.Name -eq 'DAL_M0003Reports.mqh' }
    if (-not $targetFiles -or $targetFiles.Count -eq 0) {
        throw "DAL_M0003Reports.mqh not found under: $root"
    }

    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    $backupDir = Join-Path $root ".dal_patch_backup_$stamp"
    New-Item -ItemType Directory -Path $backupDir | Out-Null

    $totalPatches = 0
    foreach ($file in $targetFiles) {
        Write-Info "Checking: $($file.FullName)"
        $oldText = Get-TextUtf8 $file.FullName
        $localCount = 0
        $newText = Patch-RandomFractionK $oldText ([ref]$localCount)

        if ($localCount -gt 0) {
            $relative = $file.FullName.Substring($root.Length).TrimStart('\','/')
            $backupPath = Join-Path $backupDir $relative
            $backupParent = Split-Path $backupPath -Parent
            if (-not (Test-Path -LiteralPath $backupParent)) { New-Item -ItemType Directory -Path $backupParent -Force | Out-Null }
            Copy-Item -LiteralPath $file.FullName -Destination $backupPath -Force
            Set-TextUtf8 $file.FullName $newText
            Write-Info "Patched $localCount call(s) in $relative"
            $totalPatches += $localCount
        } else {
            Write-Info "No 3-argument DAL_M0001RandomFractionK call found in $($file.Name)."
        }
    }

    if ($totalPatches -eq 0) {
        Write-Warn "Nothing changed. If compiler still errors, send the exact compiler lines again."
    } else {
        Write-Info "Done. Total patched calls: $totalPatches"
        Write-Info "Backup saved at: $backupDir"
    }

    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $scriptName = Split-Path -Leaf $scriptDir
    if ($scriptName -like 'dal_mql_*patch*') {
        Write-Info "Removing patch folder: $scriptDir"
        Set-Location $root
        Remove-Item -LiteralPath $scriptDir -Recurse -Force
    }

    Write-Info "Finished. Now compile in MetaEditor."
    exit 0
}
catch {
    Write-Fail $_.Exception.Message
    exit 1
}
