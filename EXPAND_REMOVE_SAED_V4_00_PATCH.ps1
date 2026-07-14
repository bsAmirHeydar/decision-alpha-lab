$Zip = Get-ChildItem "$env:USERPROFILE\Downloads" `
    -File `
    -Filter "decision-alpha-lab-saed-v4-00-program-constitution-v1.0.0*.zip" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Zip) {
    throw "ZIP patch SAED V4-00 was not found in Downloads."
}

Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force

Get-Content ".\SAED_V4_00_FILE_INDEX.txt" |
    Where-Object { $_.Trim() } |
    ForEach-Object {
        git add -- ":(literal)$_"
    }

git status --short
git commit -m "feat(saed-v4): implement V4-00 executable research constitution"
git push origin main
