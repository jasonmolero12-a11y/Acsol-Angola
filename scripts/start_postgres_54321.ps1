$ErrorActionPreference = "Stop"

$pgCtl = "C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe"
$pgData = "C:\Program Files\PostgreSQL\18\data"

if (-not (Test-Path $pgCtl)) {
    throw "pg_ctl.exe nao encontrado em: $pgCtl"
}

if (-not (Test-Path $pgData)) {
    throw "Diretorio de dados PostgreSQL nao encontrado em: $pgData"
}

& $pgCtl status -D $pgData
if ($LASTEXITCODE -ne 0) {
    & $pgCtl start -D $pgData
}

Write-Host "PostgreSQL verificado. A aplicacao ACSOL usa a porta 54321."
