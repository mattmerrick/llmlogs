# Get all HTML files in the blog directory
$files = Get-ChildItem -Path "blog/*.html" -File

# JSON-LD template
$jsonLdTemplate = @"
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": "TITLE_PLACEHOLDER",
        "author": {
            "@type": "Person",
            "name": "Matt Merrick"
        },
        "datePublished": "DATE_PLACEHOLDER",
        "description": "DESCRIPTION_PLACEHOLDER",
        "mainEntity": {
            "@type": "Question",
            "name": "QUESTION_PLACEHOLDER",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "ANSWER_PLACEHOLDER"
            }
        }
    }
    </script>

</head>
"@

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    
    # Remove existing JSON-LD if present
    $content = $content -replace '<script type="application/ld\+json">[\s\S]*?</script>\s*', ''
    
    # Extract title, date, and description from meta tags
    $title = if ($content -match '<title>(.*?)</title>') { $matches[1] -replace ' - LLM Logs$', '' } else { '' }
    $date = if ($content -match '<time datetime="(.*?)"') { $matches[1] } else { '2025-03-20' }
    $description = if ($content -match '<meta name="description" content="(.*?)"') { $matches[1] } else { '' }
    
    # Extract the first paragraph for the answer text
    $answer = if ($content -match '<p>(.*?)</p>') { 
        $matches[1] -replace '<[^>]+>', '' # Remove any HTML tags
    } else { 
        "Learn about $title and how to implement it effectively in your AI and LLM optimization strategy." 
    }
    
    # Create question from title
    $question = "What is $($title -replace '^(How|What|Why)\s+(to|is|are)\s+', '' -replace ':\s.*$', '')?"
    
    # Create the JSON-LD with the appropriate values
    $jsonLd = $jsonLdTemplate `
        -replace 'TITLE_PLACEHOLDER', $title `
        -replace 'DATE_PLACEHOLDER', $date `
        -replace 'DESCRIPTION_PLACEHOLDER', $description `
        -replace 'QUESTION_PLACEHOLDER', $question `
        -replace 'ANSWER_PLACEHOLDER', $answer
    
    # Add the JSON-LD before the closing head tag
    $content = $content -replace '</head>', $jsonLd
    
    # Save the modified content
    $content | Set-Content $file.FullName -Force
} 