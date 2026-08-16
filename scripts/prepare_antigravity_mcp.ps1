[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$utf8NoBom = [Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = $utf8NoBom
$OutputEncoding = $utf8NoBom

$projectRoot = Split-Path -Parent $PSScriptRoot
$dbhubConfigPath = Join-Path $projectRoot "config\mcp\dbhub-agrofence.toml"
$localToolsPath = Join-Path $projectRoot ".local-tools"
$outputPath = Join-Path $localToolsPath "antigravity-mcp-agrofence.json"
$envPaths = @(
    (Join-Path $projectRoot ".env"),
    (Join-Path $projectRoot "backend\.env")
)

foreach ($requiredPath in @($dbhubConfigPath)) {
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
        throw "Arquivo obrigatório não encontrado: $requiredPath"
    }
}

$envPath = $envPaths |
    Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } |
    Select-Object -First 1
if (-not $envPath) {
    throw "Execute scripts\setup_agrofence_postgres.ps1 antes de preparar o MCP."
}

$readerSettingExists = [IO.File]::ReadAllLines($envPath) |
    Where-Object { $_ -match '^AGROFENCE_READER_PASSWORD=.+$' } |
    Select-Object -First 1
if (-not $readerSettingExists) {
    throw "AGROFENCE_READER_PASSWORD não está configurada no .env local."
}

$nodeCommand = Get-Command "node.exe" -ErrorAction SilentlyContinue
$npxCommand = Get-Command "npx.cmd" -ErrorAction SilentlyContinue
if (-not $nodeCommand -or -not $npxCommand) {
    throw "Instale Node.js 22.5.0 ou superior e confirme que node/npx estão no PATH."
}

$nodeVersion = [Version]((& $nodeCommand.Source --version).Trim().TrimStart("v"))
if ($nodeVersion -lt [Version]"22.5.0") {
    throw "DBHub exige Node.js 22.5.0 ou superior. Versão atual: $nodeVersion"
}

$configuration = [ordered]@{
    mcpServers = [ordered]@{
        agrofence_postgres = [ordered]@{
            command = $npxCommand.Source
            args = @(
                "-y",
                "@bytebase/dbhub@0.24.0",
                "--transport",
                "stdio",
                "--config",
                $dbhubConfigPath
            )
            cwd = $projectRoot
            env = [ordered]@{
                NODE_ENV = "production"
            }
            disabled = $false
        }
    }
}

New-Item -ItemType Directory -Path $localToolsPath -Force | Out-Null
$json = $configuration | ConvertTo-Json -Depth 6
[IO.File]::WriteAllText($outputPath, "$json`n", $utf8NoBom)

Write-Output "Configuração local criada sem credenciais:"
Write-Output $outputPath
Write-Output "Configuração global a atualizar manualmente:"
Write-Output (Join-Path $env:USERPROFILE ".gemini\config\mcp_config.json")
