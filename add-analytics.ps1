# Analytics Tracking Addition Script
Write-Host "Starting analytics tracking check..." -ForegroundColor Green

# Get all HTML files recursively
$htmlFiles = Get-ChildItem -Recurse -Filter "*.html"
Write-Host "Found $($htmlFiles.Count) HTML files to check." -ForegroundColor Cyan

foreach ($file in $htmlFiles) {
    Write-Host "`nChecking $($file.FullName)..." -ForegroundColor Yellow
    $content = Get-Content $file.FullName -Raw
    $modified = $false
    
    # Check for Google Tag Manager
    if (-not ($content -match "GTM-P33Z79C6")) {
        Write-Host "  Adding Google Tag Manager..." -ForegroundColor White
        
        # Add GTM script to head
        $gtmScript = @"
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-P33Z79C6');</script>
<!-- End Google Tag Manager -->
"@
        $content = $content -replace '<head>', "<head>`n$gtmScript"
        $modified = $true
    }
    
    # Check for Google Analytics 4
    if (-not ($content -match "G-CDEBMDP5PL")) {
        Write-Host "  Adding Google Analytics 4..." -ForegroundColor White
        
        # Add GA4 script before </head>
        $ga4Script = @"
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-CDEBMDP5PL"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-CDEBMDP5PL');
</script>
<!-- End Google tag (gtag.js) -->
"@
        $content = $content -replace '</head>', "$ga4Script`n</head>"
        $modified = $true
    }
    
    # Check for DataFa.st
    if (-not ($content -match "682d6fb7b163eb08ed813a43")) {
        Write-Host "  Adding DataFa.st Analytics..." -ForegroundColor White
        
        # Add DataFa.st script before </head>
        $datafastScript = @"
<!-- DataFa.st Analytics -->
<script
    defer
    data-website-id="682d6fb7b163eb08ed813a43"
    data-domain="llmlogs.com"
    src="https://datafa.st/js/script.js">
</script>
<script async src="https://scripts.simpleanalyticscdn.com/latest.js"></script>
<!-- End DataFa.st Analytics -->
"@
        $content = $content -replace '</head>', "$datafastScript`n</head>"
        $modified = $true
    }
    
    # Check for GTM noscript
    if (-not ($content -match "GTM-P33Z79C6.*?noscript")) {
        Write-Host "  Adding GTM noscript tag..." -ForegroundColor White
        
        # Add GTM noscript after <body>
        $gtmNoscript = @"
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-P33Z79C6"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
"@
        $content = $content -replace '<body>', "<body>`n$gtmNoscript"
        $modified = $true
    }
    
    # Save changes if modifications were made
    if ($modified) {
        Write-Host "  Saving changes to $($file.Name)..." -ForegroundColor Green
        $content | Set-Content $file.FullName -Force
    } else {
        Write-Host "  No changes needed for $($file.Name) - analytics already present." -ForegroundColor Gray
    }
}

Write-Host "`nAnalytics check completed!" -ForegroundColor Green 