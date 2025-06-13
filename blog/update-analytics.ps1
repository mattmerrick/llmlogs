$analyticsCodes = Get-Content -Path "analytics-codes.txt" -Raw
$headCodes = ($analyticsCodes -split "<!-- Google Tag Manager \(noscript\) -->")[0]
$bodyCodes = "<!-- Google Tag Manager (noscript) -->" + ($analyticsCodes -split "<!-- Google Tag Manager \(noscript\) -->")[1]

Get-ChildItem -Path "." -Filter "*.html" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # Add head codes
    $content = $content -replace '<head>', "<head>`n$headCodes"
    
    # Add body codes
    $content = $content -replace '<body[^>]*>', "<body>`n$bodyCodes"
    
    Set-Content -Path $_.FullName -Value $content -NoNewline
} 