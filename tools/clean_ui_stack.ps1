# Removes the old React/FastAPI visual UI stack from Decision Alpha Lab.
# Run from the project root.

Remove-Item -Recurse -Force apps/web -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force apps/api -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force docs/operations/ui -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force apps/web/node_modules -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force apps/web/dist -ErrorAction SilentlyContinue
Remove-Item -Force apps/web/tsconfig.tsbuildinfo -ErrorAction SilentlyContinue
Remove-Item -Force package-lock.json -ErrorAction SilentlyContinue
Remove-Item -Force pnpm-lock.yaml -ErrorAction SilentlyContinue
Remove-Item -Force pnpm-workspace.yaml -ErrorAction SilentlyContinue
Remove-Item -Force apps/web/package-lock.json -ErrorAction SilentlyContinue
Remove-Item -Force apps/web/pnpm-lock.yaml -ErrorAction SilentlyContinue
Remove-Item -Force apps/web/pnpm-workspace.yaml -ErrorAction SilentlyContinue
Remove-Item -Force quant_lab_*.zip -ErrorAction SilentlyContinue
Remove-Item -Force quant_lab_*.patch -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -File -Filter "*.pyc" | Remove-Item -Force

Write-Host "Old UI stack removed. MQL visual lab architecture remains." -ForegroundColor Green
