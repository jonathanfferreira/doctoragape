$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Instale e inicie o Docker Desktop com backend WSL2 antes de continuar."
}
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 start.py --restart-check
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python start.py --restart-check
} else {
    throw "Python 3 não encontrado. Instale Python 3 antes de continuar."
}
if ($LASTEXITCODE -ne 0) {
    throw "A inicialização ou verificação falhou. Consulte a mensagem anterior e os logs do Docker."
}
