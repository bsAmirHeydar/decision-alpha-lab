$ErrorActionPreference = "Stop"
$tag = (Get-Content -Raw ".\LCM_00_TAG_NAME.txt").Trim()
$message = Get-Content -Raw ".\LCM_00_TAG_MESSAGE.md"
git tag -a $tag -m $message
git push origin $tag
