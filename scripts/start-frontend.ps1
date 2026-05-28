$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
$frontendDir = Join-Path $repoRoot "frontend"
$viteEntry = Join-Path $frontendDir "node_modules\vite\bin\vite.js"

Write-Host "[frontend] workspace: $frontendDir" -ForegroundColor Cyan

if (-not (Test-Path $frontendDir)) {
    Write-Host "[frontend] frontend directory not found." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command pnpm.cmd -ErrorAction SilentlyContinue)) {
    Write-Host "[frontend] pnpm.cmd is not installed or not on PATH." -ForegroundColor Red
    Write-Host "[frontend] Install pnpm first, then rerun this script." -ForegroundColor Yellow
    exit 1
}

Set-Location $frontendDir

if (-not (Test-Path $viteEntry)) {
    Write-Host "[frontend] vite install looks missing or stale, reinstalling dependencies..." -ForegroundColor Yellow

    if (Test-Path (Join-Path $frontendDir "node_modules")) {
        Remove-Item -LiteralPath (Join-Path $frontendDir "node_modules") -Recurse -Force
    }

    pnpm.cmd install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[frontend] dependency install failed." -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

Write-Host "[frontend] starting Vite at http://127.0.0.1:5173" -ForegroundColor Green
pnpm.cmd run dev
