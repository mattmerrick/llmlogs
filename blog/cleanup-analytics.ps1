$headCodes = @'
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-KXZQZ8N');</script>
    <!-- End Google Tag Manager -->

    <!-- DataFast Analytics -->
    <script>
        (function(i,s,o,g,r,a,m){i['DataFastObject']=r;i[r]=i[r]||function(){
        (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
        m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
        })(window,document,'script','https://analytics.datafast.io/analytics.js','df');
        df('init', '7f800216-d735-4a8e-a5e5-51cbd2c7f357');
    </script>
    <!-- End DataFast Analytics -->
'@

$bodyCodes = @'
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KXZQZ8N"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
'@

Get-ChildItem -Path "." -Filter "*.html" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # Remove any existing analytics codes
    $content = $content -replace '(?s)<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->', ''
    $content = $content -replace '(?s)<!-- DataFast Analytics -->.*?<!-- End DataFast Analytics -->', ''
    $content = $content -replace '(?s)<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->', ''
    
    # Add head codes
    $content = $content -replace '<head>', "<head>`n$headCodes"
    
    # Add body codes
    $content = $content -replace '<body[^>]*>', "<body>`n$bodyCodes"
    
    Set-Content -Path $_.FullName -Value $content -NoNewline
} 