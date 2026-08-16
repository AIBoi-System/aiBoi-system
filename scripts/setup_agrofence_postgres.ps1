[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$utf8NoBom = [Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8NoBom
[Console]::OutputEncoding = $utf8NoBom
$OutputEncoding = $utf8NoBom

$projectRoot = Split-Path -Parent $PSScriptRoot
$envPath = Join-Path $projectRoot ".env"
$backendEnvPath = Join-Path $projectRoot "backend\.env"
$psqlPath = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$databaseHost = "localhost"
$databasePort = 5432
$databaseName = "db_agrofence"
$adminUser = "postgres"
$appUser = "agrofence_app"
$readerUser = "codex_reader"

if (-not (Test-Path -LiteralPath $psqlPath -PathType Leaf)) {
    throw "psql não encontrado em $psqlPath"
}

function ConvertFrom-SecureValue {
    param([Parameter(Mandatory)][Security.SecureString]$Value)

    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Value)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
    }
}

function Read-ConfirmedSecret {
    param([Parameter(Mandatory)][string]$Label)

    while ($true) {
        $firstSecure = Read-Host "$Label" -AsSecureString
        $secondSecure = Read-Host "Confirme $Label" -AsSecureString
        $first = ConvertFrom-SecureValue $firstSecure
        $second = ConvertFrom-SecureValue $secondSecure
        if ([string]::IsNullOrEmpty($first)) {
            Write-Host "A senha não pode ficar vazia." -ForegroundColor Yellow
            continue
        }
        if ($first -ceq $second) {
            return $first
        }
        Write-Host "As senhas não coincidem. Tente novamente." -ForegroundColor Yellow
    }
}

function ConvertTo-SqlLiteral {
    param([Parameter(Mandatory)][string]$Value)

    return "'" + $Value.Replace("'", "''") + "'"
}

function Invoke-Psql {
    param(
        [Parameter(Mandatory)][string]$User,
        [Parameter(Mandatory)][string]$Database,
        [Parameter(Mandatory)][string]$Password,
        [Parameter(Mandatory)][string]$Sql
    )

    $startInfo = [Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = $psqlPath
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardInput = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.CreateNoWindow = $true
    $startInfo.EnvironmentVariables["PGPASSWORD"] = $Password
    $startInfo.Arguments = (
        '-h "{0}" -p {1} -U "{2}" -d "{3}" -X -q -A -t -v ON_ERROR_STOP=1 -f -' -f
        $databaseHost, $databasePort, $User, $Database
    )

    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $startInfo
    [void]$process.Start()
    $process.StandardInput.WriteLine($Sql)
    $process.StandardInput.Close()
    $stdout = $process.StandardOutput.ReadToEnd()
    $stderr = $process.StandardError.ReadToEnd()
    $process.WaitForExit()

    if ($process.ExitCode -ne 0) {
        foreach ($secret in @($adminPassword, $appPassword, $readerPassword)) {
            if (-not [string]::IsNullOrEmpty($secret)) {
                $stderr = $stderr.Replace($secret, "[REDACTED]")
            }
        }
        throw "Falha do psql (código $($process.ExitCode)): $($stderr.Trim())"
    }

    return $stdout.Trim()
}

function ConvertTo-DotEnvValue {
    param([Parameter(Mandatory)][string]$Value)

    $escaped = $Value.Replace("\", "\\").Replace("'", "\'")
    return "'$escaped'"
}

function Set-DotEnvValues {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][Collections.Specialized.OrderedDictionary]$Values
    )

    $lines = [Collections.Generic.List[string]]::new()
    if (Test-Path -LiteralPath $Path) {
        $existingLines = [IO.File]::ReadAllLines($Path, $utf8NoBom)
        if ($existingLines.Length -gt 0) {
            $lines.AddRange([string[]]$existingLines)
        }
    }

    foreach ($name in $Values.Keys) {
        $replacement = "$name=$(ConvertTo-DotEnvValue ([string]$Values[$name]))"
        $found = $false
        for ($index = 0; $index -lt $lines.Count; $index++) {
            if ($lines[$index] -match "^\s*$([regex]::Escape([string]$name))\s*=") {
                $lines[$index] = $replacement
                $found = $true
                break
            }
        }
        if (-not $found) {
            $lines.Add($replacement)
        }
    }

    [IO.File]::WriteAllLines($Path, $lines, $utf8NoBom)
}

$adminPassword = $null
$appPassword = $null
$readerPassword = $null

try {
    Write-Host "Configuração segura do PostgreSQL local do AgroFence" -ForegroundColor Cyan
    Write-Host "As senhas não serão exibidas nem gravadas no script ou no config.toml."

    $adminPassword = ConvertFrom-SecureValue (Read-Host "Senha do administrador postgres" -AsSecureString)
    if ([string]::IsNullOrEmpty($adminPassword)) {
        throw "A senha do administrador não pode ficar vazia."
    }

    [void](Invoke-Psql -User $adminUser -Database "postgres" -Password $adminPassword -Sql "SELECT 1;")
    Write-Host "Autenticação do administrador confirmada." -ForegroundColor Green

    $appPassword = Read-ConfirmedSecret "a senha de agrofence_app"
    $readerPassword = Read-ConfirmedSecret "a senha de codex_reader"

    $before = Invoke-Psql -User $adminUser -Database "postgres" -Password $adminPassword -Sql @"
SELECT
  EXISTS (SELECT 1 FROM pg_database WHERE datname = '$databaseName')::int,
  EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '$appUser')::int,
  EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '$readerUser')::int;
"@

    $appPasswordSql = ConvertTo-SqlLiteral $appPassword
    $readerPasswordSql = ConvertTo-SqlLiteral $readerPassword

    [void](Invoke-Psql -User $adminUser -Database "postgres" -Password $adminPassword -Sql @"
SELECT 'CREATE ROLE $appUser LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS'
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '$appUser') \gexec
SELECT 'CREATE ROLE $readerUser LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS'
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '$readerUser') \gexec

ALTER ROLE $appUser LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS PASSWORD $appPasswordSql;
ALTER ROLE $readerUser LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS PASSWORD $readerPasswordSql;
ALTER ROLE $readerUser SET default_transaction_read_only = on;

SELECT 'CREATE DATABASE $databaseName OWNER $appUser'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = '$databaseName') \gexec

REVOKE CONNECT, TEMPORARY ON DATABASE $databaseName FROM PUBLIC;
GRANT CONNECT, CREATE, TEMPORARY ON DATABASE $databaseName TO $appUser;
REVOKE ALL PRIVILEGES ON DATABASE $databaseName FROM $readerUser;
GRANT CONNECT ON DATABASE $databaseName TO $readerUser;
"@)

    [void](Invoke-Psql -User $adminUser -Database $databaseName -Password $adminPassword -Sql @"
GRANT USAGE, CREATE ON SCHEMA public TO $appUser;
REVOKE CREATE ON SCHEMA public FROM $readerUser;
GRANT USAGE ON SCHEMA public TO $readerUser;

REVOKE INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER
ON ALL TABLES IN SCHEMA public FROM $readerUser;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO $readerUser;
REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM $readerUser;

ALTER DEFAULT PRIVILEGES FOR ROLE $appUser IN SCHEMA public
REVOKE INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON TABLES FROM $readerUser;
ALTER DEFAULT PRIVILEGES FOR ROLE $appUser IN SCHEMA public
GRANT SELECT ON TABLES TO $readerUser;
"@)

    $appTest = Invoke-Psql -User $appUser -Database $databaseName -Password $appPassword -Sql @"
SELECT current_user, current_database(), current_setting('port'), current_setting('server_version');
"@
    $readerTest = Invoke-Psql -User $readerUser -Database $databaseName -Password $readerPassword -Sql @"
SELECT current_user, current_database(), current_setting('port'), current_setting('server_version');
SELECT schema_name FROM information_schema.schemata ORDER BY schema_name;
SELECT count(*) AS visible_base_tables FROM information_schema.tables WHERE table_type = 'BASE TABLE';
SHOW default_transaction_read_only;
"@

    $values = [ordered]@{
        AGROFENCE_DB_HOST = $databaseHost
        AGROFENCE_DB_PORT = [string]$databasePort
        AGROFENCE_DB_NAME = $databaseName
        AGROFENCE_APP_USER = $appUser
        AGROFENCE_APP_PASSWORD = $appPassword
        AGROFENCE_READER_USER = $readerUser
        AGROFENCE_READER_PASSWORD = $readerPassword
    }
    Set-DotEnvValues -Path $envPath -Values $values

    $encodedAppPassword = [Uri]::EscapeDataString($appPassword)
    $backendValues = [ordered]@{
        DATABASE_URL = "postgresql+psycopg://${appUser}:${encodedAppPassword}@${databaseHost}:${databasePort}/${databaseName}"
        MIGRATION_DATABASE_URL = "postgresql+psycopg://${appUser}:${encodedAppPassword}@${databaseHost}:${databasePort}/${databaseName}"
        DB_HOST = $databaseHost
        DB_PORT = [string]$databasePort
        DB_NAME = $databaseName
        DB_USER = $appUser
        DB_PASSWORD = $appPassword
    }
    Set-DotEnvValues -Path $backendEnvPath -Values $backendValues

    $beforeParts = $before -split "\|"
    Write-Host "" 
    Write-Host "Resultado:" -ForegroundColor Cyan
    Write-Host "- Banco: $databaseName ($(if ($beforeParts[0] -eq '1') { 'já existia' } else { 'criado' }))"
    Write-Host "- Usuário ${appUser}: $(if ($beforeParts[1] -eq '1') { 'já existia; senha/permissões atualizadas' } else { 'criado' })"
    Write-Host "- Usuário ${readerUser}: $(if ($beforeParts[2] -eq '1') { 'já existia; senha/permissões atualizadas' } else { 'criado' })"
    Write-Host "- Conexão app: $appTest"
    Write-Host "- Leitura reader: validada; transações somente leitura por padrão"
    Write-Host "- Credenciais: .env da raiz (MCP) e backend/.env (API) atualizados; ambos ignorados pelo Git"
    Write-Host "" 
    Write-Host "Pressione Enter para fechar esta janela."
    [void](Read-Host)
}
catch {
    Write-Host "" 
    Write-Host "Configuração interrompida: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Nenhuma senha foi exibida. Pressione Enter para fechar esta janela."
    [void](Read-Host)
    exit 1
}
finally {
    $adminPassword = $null
    $appPassword = $null
    $readerPassword = $null
}
