# Update navigation links in all HTML files
Get-ChildItem -Recurse -Filter "*.html" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # Update start-here link
    $content = $content -replace 'href="/start-here.html"', 'href="/start"'
    
    # Update tool reviews navigation
    $content = $content -replace 'href="/tools" class="text-white">Tools</a>', 'href="/tool-reviews" class="text-white">Tool Reviews</a>'
    $content = $content -replace 'href="/tools">Tools</a>', 'href="/tool-reviews">Tool Reviews</a>'
    
    # Update remaining /tools references to /free-tools
    $content = $content -replace 'href="/tools/', 'href="/free-tools/'
    
    # Update blog post links
    $content = $content -replace '/blog/how-to-add-a-llms.txt-file-to-any-website-in-under-10-minutes', '/blog/ultimate-guide-to-llms-txt-implementation'
    $content = $content -replace '/blog/understanding-llm-optimization', '/blog/llm-optimization-guide'
    $content = $content -replace '/blog/seo-best-practices-2025', '/blog/llm-seo-best-practices'
    $content = $content -replace '/blog/ai-content-optimization', '/blog/content-optimization-for-llms'
    
    # Save the changes
    $content | Set-Content $_.FullName -NoNewline
} 