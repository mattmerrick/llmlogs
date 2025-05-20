# LLM Guides Template

This template defines the structure and styling rules for all pages in the LLM Guides project.

## Required Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="[Page Description]">
    <meta name="keywords" content="[Page Keywords]">
    <title>[Page Title] - LLM Guides</title>
    
    <!-- Open Graph / Social Media -->
    <meta property="og:title" content="[Page Title] - LLM Guides">
    <meta property="og:description" content="[Page Description]">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://llm-guides.com/[page-url]">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="[Page Title]">
    <meta name="twitter:description" content="[Page Description]">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "[Page Title]",
        "description": "[Page Description]",
        "url": "https://llm-guides.com/[page-url]"
    }
    </script>

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Styles -->
    <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
    <!-- Consistent Header -->
    <header class="site-header">
        <div class="nav-container">
            <a href="/" class="site-logo">LLM Guides</a>
            <nav class="nav-links">
                <a href="/guides/llm-optimization">Guides</a>
                <a href="/rank-tracker">Rank Tracker</a>
                <a href="/guides/llm-optimization/examples">Examples</a>
                <div class="github-star">
                    <iframe src="https://ghbtns.com/github-btn.html?user=mattmerrick&repo=llmguides&type=star&count=true&size=large" 
                            frameborder="0" 
                            scrolling="0" 
                            width="150" 
                            height="30" 
                            title="GitHub">
                    </iframe>
                    <p>Star us on <a href="https://github.com/mattmerrick/llmguides" target="_blank">GitHub</a></p>
                </div>
            </nav>
        </div>
    </header>

    <div class="container">
        <!-- Breadcrumbs -->
        <nav class="breadcrumbs">
            <a href="/">Home</a> / <a href="/guides/llm-optimization">Guides</a> / [Current Page]
        </nav>

        <!-- Main Content -->
        <main class="content">
            <h1>[Page Title]</h1>
            [Page Content]
        </main>
    </div>

    <!-- Scripts -->
    <script src="/assets/js/main.js"></script>
</body>
</html>
```

## Required Assets

1. CSS File: `/assets/css/style.css`
   - Contains all styles from the template
   - Must be included in all pages

2. JavaScript File: `/assets/js/main.js`
   - Contains any interactive functionality
   - Must be included in all pages

3. Images Directory: `/assets/images/`
   - Store all page-specific images here
   - Use relative paths: `/assets/images/[image-name]`

## Design Rules

1. **Colors**
   - Primary: #2563eb
   - Text: #1f2937
   - Background: #f9fafb
   - Border: #e5e7eb

2. **Typography**
   - Font: Inter
   - Weights: 400, 500, 600, 700
   - Line height: 1.6

3. **Layout**
   - Max width: 1200px
   - Padding: 2rem (1rem on mobile)
   - Border radius: 1rem for content, 0.5rem for smaller elements

4. **Responsive Breakpoints**
   - Mobile: < 768px
   - Tablet: 768px - 1024px
   - Desktop: > 1024px

## Required Meta Tags

1. **Basic Meta**
   - charset
   - viewport
   - description
   - keywords

2. **Open Graph**
   - title
   - description
   - type
   - url

3. **Twitter Card**
   - card
   - title
   - description

4. **Structured Data**
   - Article schema
   - Required fields: headline, description, url

## Navigation Rules

1. **Header**
   - Must be present on all pages
   - Sticky positioning
   - Contains logo, main nav, and GitHub star button

2. **Breadcrumbs**
   - Must be present on all pages
   - Format: Home / Guides / [Current Page]
   - Links must be properly nested

## Content Structure

1. **Main Content**
   - Must be wrapped in `<main class="content">`
   - Must have an `<h1>` title
   - Should use semantic HTML elements

2. **Sections**
   - Use `<section>` for major content blocks
   - Use `<h2>` for section titles
   - Include descriptive paragraphs and lists

## Best Practices

1. **Accessibility**
   - Use semantic HTML
   - Include alt text for images
   - Ensure proper heading hierarchy

2. **Performance**
   - Optimize images
   - Minimize CSS and JS
   - Use proper caching headers

3. **SEO**
   - Include all required meta tags
   - Use proper heading structure
   - Include structured data

4. **Mobile**
   - Test on multiple devices
   - Ensure proper touch targets
   - Maintain readability 