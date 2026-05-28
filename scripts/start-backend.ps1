$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
$backendDir = Join-Path $repoRoot "backend"
$pythonExe = Join-Path $backendDir ".venv\Scripts\python.exe"
$uvCacheDir = Join-Path $repoRoot ".uv-cache"

Write-Host "[backend] workspace: $backendDir" -ForegroundColor Cyan

if (-not (Test-Path $backendDir)) {
    Write-Host "[backend] backend directory not found." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "[backend] uv is not installed or not on PATH." -ForegroundColor Red
    Write-Host "[backend] Install uv first, then rerun this script." -ForegroundColor Yellow
    exit 1
}

Set-Location $backendDir

if (-not (Test-Path $uvCacheDir)) {
    New-Item -ItemType Directory -Path $uvCacheDir | Out-Null
}

$env:UV_CACHE_DIR = $uvCacheDir

if (-not (Test-Path $pythonExe)) {
    Write-Host "[backend] virtual environment missing, syncing dependencies..." -ForegroundColor Yellow
    uv sync --dev
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[backend] dependency sync failed." -ForegroundColor Red
        exit $LASTEXITCODE
    }
}
else {
    Write-Host "[backend] using existing virtual environment." -ForegroundColor Yellow
}

if (-not (Test-Path $pythonExe)) {
    Write-Host "[backend] virtual environment python not found: $pythonExe" -ForegroundColor Red
    exit 1
}

Write-Host "[backend] starting FastAPI at http://127.0.0.1:8000" -ForegroundColor Green
& $pythonExe -m uvicorn app.main:app --reload
