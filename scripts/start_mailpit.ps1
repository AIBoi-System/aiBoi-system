[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$mailpitPath = Join-Path $projectRoot ".local-tools\mailpit\mailpit.exe"
$dataDirectory = Join-Path $projectRoot ".local-data\mailpit"
$databasePath = Join-Path $dataDirectory "mailpit.db"

if (-not (Test-Path -LiteralPath $mailpitPath -PathType Leaf)) {
    throw "Mailpit não instalado em $mailpitPath"
}

$uiListening = Get-NetTCPConnection -State Listen -LocalPort 8025 `
    -ErrorAction SilentlyContinue
$smtpListening = Get-NetTCPConnection -State Listen -LocalPort 1025 `
    -ErrorAction SilentlyContinue

if ($uiListening -or $smtpListening) {
    if ($uiListening -and $smtpListening) {
        Write-Output "Mailpit já está ativo em http://127.0.0.1:8025/"
        exit 0
    }
    throw "Somente uma das portas 8025/1025 está ocupada; início recusado."
}

New-Item -ItemType Directory -Path $dataDirectory -Force | Out-Null

$arguments = @(
    "--listen", "127.0.0.1:8025",
    "--smtp", "127.0.0.1:1025",
    "--database", $databasePath
)

Start-Process -FilePath $mailpitPath -ArgumentList $arguments `
    -WindowStyle Hidden

$deadline = (Get-Date).AddSeconds(10)
do {
    Start-Sleep -Milliseconds 250
    $ready = Test-NetConnection -ComputerName 127.0.0.1 -Port 8025 `
        -WarningAction SilentlyContinue
} until ($ready.TcpTestSucceeded -or (Get-Date) -ge $deadline)

if (-not $ready.TcpTestSucceeded) {
    throw "Mailpit não abriu a interface local dentro do prazo esperado."
}

Write-Output "Mailpit ativo em http://127.0.0.1:8025/"
