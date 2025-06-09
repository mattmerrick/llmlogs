# Get all HTML files in the blog directory
$files = Get-ChildItem -Path "blog/*.html" -File

# Summary box template
$summaryBoxTemplate = @"
                <div class="summary-box">
                    <strong>TL;DR:</strong>
                    SUMMARY_PLACEHOLDER
                </div>

"@

# Summaries for different types of content
$summaries = @{
    "what-is-llm-seo" = "LLM SEO is the practice of optimizing content for AI language models and AI-powered search engines. It focuses on natural language, semantic relevance, and comprehensive topic coverage rather than traditional keyword optimization."
    "complete-guide-to-ai-seo-optimization" = "This comprehensive guide covers everything you need to know about AI SEO optimization. Learn how to structure content for AI understanding, implement semantic HTML, and create content that both AI models and humans find valuable."
    "how-to-write-content-that-gets-cited-by-chatgpt" = "To get your content cited by ChatGPT, focus on creating authoritative, well-structured content with clear information hierarchy. Use semantic HTML, implement proper metadata, and ensure your content provides unique, valuable insights."
    "llm-seo-checklist-for-blog-optimization" = "This comprehensive checklist helps you optimize your blog for LLMs and AI search engines. Key areas include content structure, semantic HTML implementation, metadata optimization, and content quality assessment."
    "traditional-vs-llm-seo" = "Learn the key differences between traditional SEO and LLM SEO. While traditional SEO focuses on keywords and backlinks, LLM SEO emphasizes natural language, context, and comprehensive topic coverage."
    "semantic-html-llm" = "Semantic HTML is crucial for LLM understanding. Learn how to structure your content with proper HTML elements that convey meaning and hierarchy to both humans and AI models."
    "llm-token-cost-management" = "Understand how to effectively manage and optimize token costs when working with LLMs. Learn strategies for efficient prompt design and response handling to minimize costs while maintaining quality."
    "llm-observability-tracing" = "Learn how to implement observability and tracing in your LLM applications. Track model performance, monitor usage patterns, and optimize your AI systems effectively."
    "best-llms" = "A comprehensive comparison of the best Large Language Models available. Evaluate different models based on performance, cost, and specific use cases to choose the right one for your needs."
    "how-are-llms-trained" = "Understand the process of training Large Language Models, including data preparation, model architecture, and fine-tuning techniques. Learn about the key factors that influence model performance."
}

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    
    # Skip if the file already has a summary box
    if ($content -match 'class="summary-box"') {
        continue
    }
    
    # Get the base name without extension
    $baseName = $file.BaseName
    
    # Get the appropriate summary
    $summary = $summaries[$baseName]
    
    # If we don't have a specific summary, generate a generic one based on the title
    if (-not $summary) {
        $title = if ($content -match '<title>(.*?)</title>') {
            $matches[1]
        } else {
            $baseName -replace '-', ' ' -replace '([a-z])([A-Z])', '$1 $2'
        }
        $summary = "Learn about $title. This guide provides comprehensive information and practical insights to help you understand and implement these concepts effectively."
    }
    
    # Create the summary box with the appropriate summary
    $summaryBox = $summaryBoxTemplate -replace 'SUMMARY_PLACEHOLDER', $summary
    
    # Add the summary box after the header
    $content = $content -replace '(?<=</header>)\s*(?=<)', "`n$summaryBox"
    
    # Save the modified content
    $content | Set-Content $file.FullName -Force
} 