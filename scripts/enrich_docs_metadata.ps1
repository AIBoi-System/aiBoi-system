param(
    [string]$DocsRoot = "docs",
    [switch]$NormalizeDraftBodies,
    [switch]$NormalizeEof
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path $DocsRoot).Path

function Get-Owner([string]$relative) {
    switch -Regex ($relative) {
        '^01-product/' { 'product'; break }
        '^02-mvp/' { 'product'; break }
        '^03-domain/' { 'domain'; break }
        '^04-architecture/' { 'engineering'; break }
        '^05-security/' { 'security'; break }
        '^06-database/' { 'data'; break }
        '^07-api/' { 'backend'; break }
        '^08-frontend/' { 'frontend'; break }
        '^09-backend/' { 'backend'; break }
        '^10-quality/' { 'quality'; break }
        '^11-operations/' { 'operations'; break }
        '^12-engineering/' { 'engineering'; break }
        '^13-modules/' { 'domain'; break }
        default { 'documentation' }
    }
}

function Get-Type([string]$relative) {
    switch -Regex ($relative) {
        'template|guide|setup|running-|build-|troubleshooting|runbooks' { 'how-to'; break }
        'overview|vision|principles|strategy|architecture|model|explanation' { 'explanation'; break }
        'README|INDEX|CHANGELOG|decisions|roadmap|policy|definition' { 'governance'; break }
        'archive|deprecated|superseded|previous-versions' { 'archive'; break }
        default { 'reference' }
    }
}

Get-ChildItem $root -Recurse -File -Filter '*.md' | ForEach-Object {
    if ($_.Name -eq 'source-original-agrofence-v1.2.md') { return }

    $relative = $_.FullName.Substring($root.Length + 1).Replace('\', '/')
    $content = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
    if ($NormalizeEof) {
        $content = $content.TrimEnd() + "`n"
        Set-Content -LiteralPath $_.FullName -Value $content -Encoding UTF8 -NoNewline
    }
    if ($content.StartsWith('---')) {
        if (
            $NormalizeDraftBodies -and
            $content -match '(?m)^status:\s*draft\s*$' -and
            $content -match 'Definir o tratamento de \*\*'
        ) {
            $end = $content.IndexOf("`n---`n", 4)
            $frontMatter = $content.Substring(0, $end + 5)
            $heading = [regex]::Match($content, '(?m)^#\s+(.+)$')
            $title = if ($heading.Success) { $heading.Groups[1].Value.Trim() } else { $_.BaseName }
            $replacement = @"

# $title

> Estado: Rascunho nao canonico e excluido da indexacao por IA.

## Finalidade

Reservar o tema **$($title.ToLower())** na arquitetura documental sem afirmar que existe uma especificacao aprovada.

## Para tornar esta pagina canonica

1. Identificar o requisito, decisao ou fluxo que exige esta pagina.
2. Referenciar codigo, contrato ou evidencia de pesquisa verificavel.
3. Documentar comportamento atual, comportamento desejado e divergencias.
4. Definir criterios de aceite e testes.
5. Solicitar revisao do proprietario indicado nos metadados.

Enquanto esses itens nao forem atendidos, consulte o README da area e docs/CANONICAL-DOCUMENTS.md.
"@
            Set-Content -LiteralPath $_.FullName -Value (($frontMatter + $replacement).TrimEnd() + "`n") -Encoding UTF8 -NoNewline
        }
        return
    }

    $heading = [regex]::Match($content, '(?m)^#\s+(.+)$')
    $title = if ($heading.Success) { $heading.Groups[1].Value.Trim() } else { $_.BaseName }
    $isLegacy = $relative -match '^(mvp|product)/'
    $isArchive = $relative -match '^18-archive/'
    $isGeneratedDraft = $content -match 'Definir o tratamento de \*\*'
    $status = if ($isArchive) { 'archived' } elseif ($isLegacy) { 'deprecated' } elseif ($isGeneratedDraft) { 'draft' } elseif ($content -match 'Estado:\s*Planejado') { 'planned' } elseif ($content -match 'Estado:\s*Parcial|lacunas') { 'partial' } else { 'active' }
    $canonical = (-not $isLegacy -and -not $isArchive -and -not $isGeneratedDraft).ToString().ToLower()
    $aiIndex = $canonical
    $owner = Get-Owner $relative
    $type = Get-Type $relative
    $safeTitle = $title.Replace('"', '\"')

    $frontMatter = @"
---
title: "$safeTitle"
type: $type
status: $status
owner: $owner
canonical: $canonical
ai_index: $aiIndex
last_verified: 2026-07-16
---

"@
    Set-Content -LiteralPath $_.FullName -Value (($frontMatter + $content).TrimEnd() + "`n") -Encoding UTF8 -NoNewline
}
