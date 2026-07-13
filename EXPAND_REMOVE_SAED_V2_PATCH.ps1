$Zip = Get-ChildItem "$env:USERPROFILE\Downloads" `
    -File `
    -Filter "decision-alpha-lab-setup-ai-edge-discovery-institutional-v2.0.0*.zip" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Zip) {
    throw "ZIP معماری SAED V2 داخل Downloads پیدا نشد."
}

Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force

Get-Content ".\SAED_V2_FILE_INDEX.txt" |
    Where-Object { $_.Trim() } |
    ForEach-Object {
        git add -- ":(literal)$_"
    }

git status --short
git commit -m "docs(strategy-factory): add institutional SAED V2 AI edge discovery architecture"
git push origin main
