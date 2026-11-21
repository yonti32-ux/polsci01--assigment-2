param([string]$TexBin = '', [string]$PythonExe = 'python', [switch]$RegenerateFigures)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if ($TexBin) { $env:PATH = "$TexBin;$env:PATH" }
foreach ($tool in @('lualatex', 'biber')) {
    if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
        throw "$tool is missing. Install MiKTeX/TinyTeX or pass -TexBin with its bin directory."
    }
}
if ($RegenerateFigures) {
    & $PythonExe code/make_figures.py
    if ($LASTEXITCODE -ne 0) { throw 'Figure generation failed.' }
}
& lualatex -interaction=nonstopmode -halt-on-error main.tex
if ($LASTEXITCODE -ne 0) { throw 'First LaTeX pass failed. See main.log.' }
& biber main
if ($LASTEXITCODE -ne 0) { throw 'Bibliography build failed. See main.blg.' }
1..2 | ForEach-Object {
    & lualatex -interaction=nonstopmode -halt-on-error main.tex
    if ($LASTEXITCODE -ne 0) { throw 'LaTeX pass failed. See main.log.' }
}
$log = Get-Content -LiteralPath main.log -Raw
if ($log -match 'There were undefined references|Please \(re\)run Biber|Missing character:|Overfull \\[hv]box|Rerun to get cross-references right') {
    throw 'Build has unresolved references, missing glyphs, or overflowing content. See main.log.'
}
Write-Host 'Built main.pdf. Inspect every page visually before submission.'
