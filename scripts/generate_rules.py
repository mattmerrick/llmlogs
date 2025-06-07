#!/usr/bin/env python3
import os
import json
from datetime import datetime

RULES_OUTPUT_DIR = "rules"
RULES_DATA_FILE = "assets/js/rules-data.js"

# Define our programming rules
RULES = [
    {
        "title": "TypeScript Best Practices",
        "slug": "typescript",
        "description": "Essential TypeScript best practices and patterns for building scalable applications",
        "category": "Languages",
        "tags": ["TypeScript", "JavaScript", "Web Development"],
        "author": {"name": "LLM Logs Team"},
        "content": """
## Type Safety

- Use strict TypeScript configuration with `"strict": true`
- Avoid using `any` type unless absolutely necessary
- Leverage TypeScript's built-in utility types
- Use interfaces for object shapes and types for unions/primitives

## Code Organization

- Follow the Single Responsibility Principle
- Use modules to organize related functionality
- Implement proper error handling with custom error types
- Keep functions pure and predictable

## Best Practices

- Use async/await for asynchronous operations
- Implement proper error boundaries
- Write unit tests for critical functionality
- Document complex functions and interfaces
"""
    },
    {
        "title": "React Development Guidelines",
        "slug": "react",
        "description": "Comprehensive guide for building maintainable React applications",
        "category": "Frameworks",
        "tags": ["React", "JavaScript", "Frontend"],
        "author": {"name": "LLM Logs Team"},
        "content": """
## Component Structure

- Use functional components with hooks
- Keep components small and focused
- Implement proper prop validation
- Use proper component composition

## State Management

- Choose appropriate state management solutions
- Use Context API for shared state
- Implement proper data fetching strategies
- Handle loading and error states

## Performance

- Use React.memo for expensive computations
- Implement proper lazy loading
- Optimize re-renders with useMemo and useCallback
- Profile and monitor performance
"""
    },
    {
        "title": "Python Code Style Guide",
        "slug": "python",
        "description": "Python coding standards and best practices for clean, maintainable code",
        "category": "Languages",
        "tags": ["Python", "Backend", "Programming"],
        "author": {"name": "LLM Logs Team"},
        "content": """
## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Keep functions focused and small
- Use proper docstrings and comments

## Best Practices

- Write modular and reusable code
- Implement proper error handling
- Use virtual environments
- Follow the principle of least surprise

## Testing

- Write comprehensive unit tests
- Use pytest for testing
- Implement proper test coverage
- Mock external dependencies
"""
    }
]

def generate_rule_page(rule):
    """Generate HTML page for a rule"""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{rule['description']}">
    <meta name="keywords" content="{', '.join(rule['tags'])}">
    <title>{rule['title']} - LLM Logs</title>
    <link rel="stylesheet" href="./../assets/css/style.css">
    <link rel="canonical" href="https://llmlogs.com/rules/{rule['slug']}.html" />
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
                <h1>{rule['title']}</h1>
                <div class="rule-meta">
                    <div class="author-info">
                        <img src="/assets/images/avatars/default.png" alt="{rule['author']['name']}" class="author-avatar">
                        <span>By {rule['author']['name']}</span>
                    </div>
                    <time datetime="{datetime.now().strftime('%Y-%m-%d')}">{datetime.now().strftime('Updated: %B %d, %Y')}</time>
                </div>
                <div class="rule-tags">
                    {' '.join(f'<span class="tag">{tag}</span>' for tag in rule['tags'])}
                </div>
            </header>

            <div class="rule-content">
                {rule['content']}
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
    os.makedirs(RULES_OUTPUT_DIR, exist_ok=True)
    
    # Write the file
    with open(os.path.join(RULES_OUTPUT_DIR, f"{rule['slug']}.html"), "w", encoding="utf-8") as f:
        f.write(html)

def generate_rules_data():
    """Generate rules data JavaScript file"""
    rules_data = []
    for rule in RULES:
        rules_data.append({
            "title": rule["title"],
            "slug": rule["slug"],
            "description": rule["description"],
            "tags": rule["tags"],
            "category": rule["category"],
            "author": rule["author"]["name"]
        })
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(RULES_DATA_FILE), exist_ok=True)
    
    # Write the JavaScript file
    with open(RULES_DATA_FILE, "w", encoding="utf-8") as f:
        f.write("// Auto-generated rules data\n")
        f.write("const rulesData = ")
        json.dump(rules_data, f, indent=2)
        f.write(";\n")

def main():
    """Generate all rule pages and data file"""
    try:
        # Generate individual rule pages
        for rule in RULES:
            generate_rule_page(rule)
            print(f"Generated page for {rule['title']}")
        
        # Generate rules data file
        generate_rules_data()
        print(f"Generated rules data file with {len(RULES)} rules")
        
    except Exception as e:
        print(f"Error generating rules: {str(e)}")

if __name__ == "__main__":
    main() 