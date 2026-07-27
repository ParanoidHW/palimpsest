param(
    [Parameter(Mandatory = $true)]
    [string]$InputPptx,

    [Parameter(Mandatory = $true)]
    [string]$OutputDir
)

$ErrorActionPreference = "Stop"
$powerPoint = $null
$presentation = $null

try {
    New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
    $slideDir = Join-Path $OutputDir "powerpoint-slides"
    New-Item -ItemType Directory -Force -Path $slideDir | Out-Null
    $pdfPath = Join-Path $OutputDir "powerpoint-rendered.pdf"

    $powerPoint = New-Object -ComObject PowerPoint.Application
    $powerPoint.Visible = 1
    $presentation = $powerPoint.Presentations.Open($InputPptx, $true, $true, $false)

    # ppSaveAsPDF = 32
    $presentation.SaveAs($pdfPath, 32)
    $presentation.Export($slideDir, "PNG", 1600, 900)
}
finally {
    if ($null -ne $presentation) {
        $presentation.Close()
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($presentation)
    }
    if ($null -ne $powerPoint) {
        $powerPoint.Quit()
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($powerPoint)
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}

