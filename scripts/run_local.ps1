$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$postgresScript = Join-Path $PSScriptRoot "start_postgres_54321.ps1"

if (-not (Test-Path $python)) {
    throw "Python do ambiente virtual nao encontrado em: $python"
}

if (Test-Path $postgresScript) {
    powershell -ExecutionPolicy Bypass -File $postgresScript
}

Set-Location $projectRoot
& $python manage.py runserver 127.0.0.1:8000
