[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$InputPptx,
    [Parameter(Mandatory=$true)][string]$OutputDir,
    [ValidateSet('png','pdf','both')][string]$Format='both',
    [ValidateRange(72,300)][int]$Dpi=120,
    [switch]$Overwrite
)

$ErrorActionPreference='Stop'
$sourcePptx=(Resolve-Path -LiteralPath $InputPptx).Path
$renderDir=[IO.Path]::GetFullPath($OutputDir)
if ([IO.Path]::GetExtension($sourcePptx) -ine '.pptx') { throw 'Input must be a PPTX file.' }
[IO.Directory]::CreateDirectory($renderDir) | Out-Null
$renderApp=$null
$renderDeck=$null
$exportRecords=@()
try {
    $renderApp=New-Object -ComObject PowerPoint.Application
    # Open only this task's file read-only and without a presentation window.
    # Do not set application visibility, attach to/close another document, or Quit PowerPoint.
    $renderDeck=$renderApp.Presentations.Open($sourcePptx,[int32]-1,[int32]0,[int32]0)
    $slideTotal=[int]$renderDeck.Slides.Count
    $pixelWidth=[int][Math]::Round([double]$renderDeck.PageSetup.SlideWidth / 72.0 * $Dpi)
    $pixelHeight=[int][Math]::Round([double]$renderDeck.PageSetup.SlideHeight / 72.0 * $Dpi)
    $pdfTarget=Join-Path $renderDir 'presentation.pdf'
    $reportTarget=Join-Path $renderDir 'render-report.json'
    $targets=@($reportTarget)
    if ($Format -eq 'pdf' -or $Format -eq 'both') { $targets+=@($pdfTarget) }
    if ($Format -eq 'png' -or $Format -eq 'both') {
        for ($pageIndex=1;$pageIndex -le $slideTotal;$pageIndex++) {
            $targets+=@(Join-Path $renderDir ('slide_{0:D3}.png' -f $pageIndex))
        }
    }
    if (-not $Overwrite) {
        foreach ($targetFile in $targets) {
            if (Test-Path -LiteralPath $targetFile) { throw "Output exists; choose a new directory or use authorized -Overwrite: $targetFile" }
        }
    }
    if ($Format -eq 'png' -or $Format -eq 'both') {
        for ($pageIndex=1;$pageIndex -le $slideTotal;$pageIndex++) {
            $pngTarget=Join-Path $renderDir ('slide_{0:D3}.png' -f $pageIndex)
            $currentSlide=$renderDeck.Slides.Item($pageIndex)
            try { $currentSlide.Export($pngTarget,'PNG',$pixelWidth,$pixelHeight) }
            finally { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($currentSlide) }
            if (-not (Test-Path -LiteralPath $pngTarget)) { throw "PNG export missing: $pngTarget" }
            $exportRecords+=@([ordered]@{slide=$pageIndex;png=$pngTarget})
        }
    }
    if ($Format -eq 'pdf' -or $Format -eq 'both') {
        # ppSaveAsPDF = 32. This writes a separate PDF; the read-only source is retained.
        $renderDeck.SaveAs($pdfTarget,[int32]32)
        if (-not (Test-Path -LiteralPath $pdfTarget)) { throw 'PowerPoint did not create the requested PDF.' }
    }
    $report=[ordered]@{source=$sourcePptx;renderer='Microsoft PowerPoint COM';slide_count=$slideTotal;
        format=$Format;width_px=$pixelWidth;height_px=$pixelHeight;slides=$exportRecords;
        pdf=$(if ($Format -ne 'png') {$pdfTarget} else {$null})}
    [IO.File]::WriteAllText($reportTarget,($report | ConvertTo-Json -Depth 5),[Text.UTF8Encoding]::new($false))
    Write-Output ($report | ConvertTo-Json -Depth 5)
}
finally {
    if ($null -ne $renderDeck) {
        try { $renderDeck.Close() } finally { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($renderDeck) }
    }
    if ($null -ne $renderApp) { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($renderApp) }
}
