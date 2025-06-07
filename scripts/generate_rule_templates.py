#!/usr/bin/env python3
import os
from datetime import datetime

# List of all rules (filename without .ts extension will be the slug)
RULES = [
    "abap", "al", "android", "angular-ionic-firebase-firestore", "angular",
    "arduino-framework", "astro", "autohotkey", "blazor", "bootstrap",
    "c", "chrome-extension", "cloudflare", "convex", "cosmwasm",
    "cpp", "data-analyst", "deep-learning", "devops-backend", "django",
    "dotnet", "drupal", "elixir", "expo", "fastapi",
    "fastify", "flask", "flutter", "front-end", "gastby",
    "ghost-tailwindcss", "global", "go", "htmlandcss", "htmx",
    "ionic", "java", "jax", "jekyll", "julia",
    "laravel", "lua", "meta-prompt", "monorepo-tamagui", "nestjs",
    "nextjs", "nuxtjs", "odoo", "onchainkit", "pixijs",
    "playwright", "privacy_ux", "python", "rails-api", "rails",
    "react-native", "remix", "robocorp", "rspec", "rust",
    "salesforce", "sanity", "solana", "solidity", "svelte",
    "sveltekit", "swift", "tauri", "tech-stack", "technical-tutorials",
    "terraform", "typescript", "uiux-design", "unity-c-sharp", "viewcomfy",
    "vivado", "vue", "web-development", "web-scraping", "wordpress-woocommerce",
    "wordpress"
]

def create_title(slug):
    """Convert slug to title"""
    # Handle special cases
    if slug.upper() == slug:
        return slug.upper()
    if slug == "htmlandcss":
        return "HTML and CSS"
    if "wordpress" in slug:
        return slug.replace("wordpress", "WordPress").replace("-", " ").title()
    
    # General case
    return slug.replace("-", " ").replace("_", " ").title()

def generate_template(slug):
    """Generate HTML template for a rule"""
    title = create_title(slug)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title} programming guidelines and best practices. Learn about code style, naming conventions, and development standards.">
    <meta name="keywords" content="{title}, programming rules, coding standards, best practices">
    <title>{title} Programming Rules - LLM Logs</title>
    <link rel="stylesheet" href="./../assets/css/style.css">
    <link rel="canonical" href="https://llmlogs.com/rules/{slug}.html" />
    <style>
        .rule-content {{
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }}

        .rule-header {{
            margin-bottom: 40px;
        }}

        .rule-meta {{
            display: flex;
            align-items: center;
            gap: 20px;
            margin: 20px 0;
            color: #586069;
        }}

        .author-info {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .author-avatar {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
        }}

        .rule-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 20px 0;
        }}

        .tag {{
            background: #f1f8ff;
            color: #0366d6;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.9em;
        }}

        .rule-section {{
            margin: 30px 0;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        .rule-section h2 {{
            color: #24292e;
            border-bottom: 2px solid #e1e4e8;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}

        .rule-section ul {{
            padding-left: 20px;
        }}

        .rule-section li {{
            margin: 8px 0;
            line-height: 1.6;
        }}

        code {{
            background: #f6f8fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <!-- Include Standard Header -->
    <header class="site-header">
        <div class="nav-container">
            <button class="mobile-menu-toggle" aria-label="Toggle navigation menu">
                <span class="hamburger"></span>
            </button>
            <a href="/" class="site-logo">LLM Logs</a>
            <nav class="nav-links">
                <a href="/start-here.html" class="start-here-link">Start Here</a>
                <a href="/guides/llm-optimization">Guides</a>
                <a href="/free-tools">Tools</a>
                <a href="/blog">Blog</a>
                <a href="https://github.com/mattmerrick/llmseoguide" target="_blank" rel="noopener">GitHub</a>
            </nav>
        </div>
    </header>

    <!-- Main Content Container -->
    <div class="rule-content">
        <article>
            <header class="rule-header">
                <h1>{title} Programming Rules</h1>
                <div class="rule-meta">
                    <div class="author-info">
                        <img src="/assets/images/avatars/default.png" alt="LLM Logs Team" class="author-avatar">
                        <span>By LLM Logs Team</span>
                    </div>
                    <time datetime="{datetime.now().strftime('%Y-%m-%d')}">{datetime.now().strftime('Updated: %B %d, %Y')}</time>
                </div>
                <div class="rule-tags">
                    <span class="tag">{title}</span>
                    <span class="tag">Programming</span>
                    <span class="tag">Best Practices</span>
                </div>
            </header>

            <div class="rule-content">
                <!-- Content will be added here -->
                <section class="rule-section">
                    <h2>Overview</h2>
                    <p>Comprehensive guide for {title} development best practices and standards.</p>
                </section>

                <section class="rule-section">
                    <h2>Code Style</h2>
                    <ul>
                        <li>Content to be added</li>
                    </ul>
                </section>

                <section class="rule-section">
                    <h2>Best Practices</h2>
                    <ul>
                        <li>Content to be added</li>
                    </ul>
                </section>
            </div>
        </article>
    </div>

    <!-- Include Standard Footer -->
    <footer class="site-footer">
        <div class="footer-content">
            <div class="footer-links">
                <a href="/">Home</a>
                <a href="/guides">Guides</a>
                <a href="/free-tools">Tools</a>
                <a href="/blog">Blog</a>
                <a href="https://github.com/mattmerrick/llmseoguide" target="_blank" rel="noopener">GitHub</a>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 LLM Logs. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Required Scripts -->
    <script src="../assets/js/main.js"></script>
</body>
</html>"""

    # Ensure directory exists
    os.makedirs("rules", exist_ok=True)
    
    # Write the file
    with open(f"rules/{slug}.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated template for {title}")

def main():
    """Generate templates for all rules"""
    for rule in RULES:
        generate_template(rule)
    print(f"\nGenerated {len(RULES)} rule templates")

if __name__ == "__main__":
    main() 