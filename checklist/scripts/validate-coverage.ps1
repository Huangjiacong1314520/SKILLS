$ErrorActionPreference = 'Stop'

$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$sourceDir = Join-Path $root 'references\source'
$assetDir = Join-Path $root 'references\assets'
$guidePath = Join-Path $root 'GUIDE.md'
$coveragePath = Join-Path $root 'COVERAGE.md'

$errors = [System.Collections.Generic.List[string]]::new()

foreach ($required in @($guidePath, $coveragePath, $sourceDir, $assetDir)) {
    if (-not (Test-Path -LiteralPath $required)) {
        $errors.Add("Missing required path: $required")
    }
}

if ($errors.Count -eq 0) {
    $sourceFiles = @(Get-ChildItem -LiteralPath $sourceDir -File -Filter '*.md')
    $assetFiles = @(Get-ChildItem -LiteralPath $assetDir -File)

    if ($sourceFiles.Count -ne 34) {
        $errors.Add("Expected 34 unique source Markdown files, found $($sourceFiles.Count).")
    }
    if ($assetFiles.Count -ne 120) {
        $errors.Add("Expected 120 unique referenced images, found $($assetFiles.Count).")
    }
    if (@($sourceFiles | Where-Object Name -Like '* (1).md').Count -gt 0) {
        $errors.Add('Duplicate 1.1 source copy with suffix (1) must not be packaged.')
    }

    $coverage = Get-Content -Raw -LiteralPath $coveragePath
    foreach ($file in $sourceFiles) {
        if (-not $coverage.Contains($file.Name)) {
            $errors.Add("Source is absent from COVERAGE.md: $($file.Name)")
        }
    }

    $guide = Get-Content -Raw -LiteralPath $guidePath
    $guideRuleIds = @([regex]::Matches($guide, '(?m)^### (R\d{2})\b') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    $expectedRuleIds = @(1..25 | ForEach-Object { 'R{0:D2}' -f $_ })
    foreach ($ruleId in $expectedRuleIds) {
        if ($ruleId -notin $guideRuleIds) {
            $errors.Add("Missing rule heading in GUIDE.md: $ruleId")
        }
        if (-not [regex]::IsMatch($coverage, "\b$ruleId\b")) {
            $errors.Add("Rule is absent from COVERAGE.md: $ruleId")
        }
    }
    foreach ($ruleId in $guideRuleIds) {
        if ($ruleId -notin $expectedRuleIds) {
            $errors.Add("Unexpected rule heading in GUIDE.md: $ruleId")
        }
    }

    $imagePattern = '!\[[^\]]*\]\((?:<)?([^)<>]+)(?:>)?\)'
    $resolvedImagePaths = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($source in $sourceFiles) {
        $raw = Get-Content -Raw -LiteralPath $source.FullName
        foreach ($match in [regex]::Matches($raw, $imagePattern)) {
            $target = $match.Groups[1].Value
            if ($target -match '^(?:https?|data):') { continue }
            $resolved = [System.IO.Path]::GetFullPath((Join-Path $source.DirectoryName $target))
            [void]$resolvedImagePaths.Add($resolved)
            if (-not (Test-Path -LiteralPath $resolved)) {
                $errors.Add("Broken image link in $($source.Name): $target")
            }
        }
    }

    if ($resolvedImagePaths.Count -ne 120) {
        $errors.Add("Expected source Markdown to reference 120 unique local images, found $($resolvedImagePaths.Count).")
    }
    foreach ($asset in $assetFiles) {
        if (-not $resolvedImagePaths.Contains($asset.FullName)) {
            $errors.Add("Unreferenced packaged asset: $($asset.Name)")
        }
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Output 'Checklist coverage validation passed.'
Write-Output 'Rules: 25'
Write-Output 'Unique source Markdown files: 34'
Write-Output 'Unique referenced images: 120'

