#!/usr/bin/env python3
import os
import re
import json
import base64
import requests
from datetime import datetime
from typing import Dict, List, Optional

GITHUB_API_BASE = "https://api.github.com/repos/pontusab/directories/contents/packages/data/src/rules"
RULES_OUTPUT_DIR = "rules"
RULES_DATA_FILE = "assets/js/rules-data.js"
TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <title>{title} - LLM Logs</title>
    <link rel="stylesheet" href="./../assets/css/style.css">
    <link rel="canonical" href="https://llmlogs.com/rules/{slug}.html" />
    <style>
        .rule-content {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }

        .rule-header {
            margin-bottom: 40px;
        }

        .rule-meta {
            display: flex;
            align-items: center;
            gap: 20px;
            margin: 20px 0;
            color: #586069;
        }

        .author-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .author-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
        }

        .rule-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 20px 0;
        }

        .tag {
            background: #f1f8ff;
            color: #0366d6;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.9em;
        }

        .rule-section {
            margin: 30px 0;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .rule-section h2 {
            color: #24292e;
            border-bottom: 2px solid #e1e4e8;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        .rule-section h3 {
            color: #24292e;
            margin: 20px 0 10px;
        }

        .rule-section ul {
            padding-left: 20px;
        }

        .rule-section li {
            margin: 8px 0;
            line-height: 1.6;
        }

        code {
            background: #f6f8fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
            font-size: 0.9em;
        }

        .navigation-links {
            display: flex;
            justify-content: space-between;
            margin: 40px 0;
            padding: 20px 0;
            border-top: 1px solid #e1e4e8;
        }

        .nav-link {
            color: #0366d6;
            text-decoration: none;
        }

        .nav-link:hover {
            text-decoration: underline;
        }

        @media (max-width: 768px) {
            .rule-meta {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }
        }
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
                <h1>{title}</h1>
                <div class="rule-meta">
                    <div class="author-info">
                        <img src="/assets/images/avatars/default.png" alt="{author_name}" class="author-avatar">
                        <span>By {author_name}</span>
                    </div>
                    <time datetime="{date_iso}">{date_display}</time>
                </div>
                <div class="rule-tags">
                    {tags_html}
                </div>
            </header>

            {content_html}

            <nav class="navigation-links">
                <a href="/rules.html" class="nav-link">← Back to Rules Directory</a>
                <a href="/rules/{next_rule}.html" class="nav-link">Next: {next_rule_title} →</a>
            </nav>
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
</html>
"""

def fetch_rules() -> List[Dict]:
    """Fetch rules from GitHub repository"""
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    print(f"Fetching rules from {GITHUB_API_BASE}")
    response = requests.get(GITHUB_API_BASE, headers=headers)
    print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data)} rules")
        return data
    else:
        print(f"Response content: {response.text}")
        raise Exception(f"Failed to fetch rules: {response.status_code}")

def parse_typescript_exports(content: str) -> Dict:
    """Parse TypeScript exports from content"""
    try:
        # First try to find a rules object
        rules_match = re.search(r'export\s+const\s+rules\s*=\s*({[^}]+})', content, re.DOTALL)
        if not rules_match:
            # Try to find any exported object
            rules_match = re.search(r'export\s+const\s+\w+\s*=\s*({[^}]+})', content, re.DOTALL)
        
        if not rules_match:
            print("No rules object found in content")
            return {}
        
        rules_content = rules_match.group(1)
        
        # Extract fields using more flexible patterns
        title = ""
        title_match = re.search(r'title:\s*[\'"]([^\'"]+)[\'"]', rules_content)
        if title_match:
            title = title_match.group(1)
        else:
            # Try finding title in a different format
            title_match = re.search(r'title:\s*`([^`]+)`', rules_content)
            if title_match:
                title = title_match.group(1)
        
        description = ""
        desc_match = re.search(r'description:\s*[\'"`]([^\'"}`]+)[\'"`]', rules_content)
        if desc_match:
            description = desc_match.group(1)
        
        slug = ""
        slug_match = re.search(r'slug:\s*[\'"`]([^\'"}`]+)[\'"`]', rules_content)
        if slug_match:
            slug = slug_match.group(1)
        
        # Parse tags with more flexible pattern
        tags = []
        tags_match = re.search(r'tags:\s*\[(.*?)\]', rules_content, re.DOTALL)
        if tags_match:
            tags_str = tags_match.group(1)
            # Handle both quoted and unquoted tags
            tags = [tag.strip().strip('"\'"') for tag in re.findall(r'[\'"]([^\'"]+)[\'"]|(\w+)', tags_str) if tag[0] or tag[1]]
            tags = [t[0] if t[0] else t[1] for t in tags]
        
        # Parse content with template literals
        content = ""
        content_match = re.search(r'content:\s*`([^`]+)`', rules_content, re.DOTALL)
        if content_match:
            content = content_match.group(1).strip()
        
        # Parse author information
        author_name = "LLM Logs Team"
        author_match = re.search(r'author:\s*{\s*name:\s*[\'"`]([^\'"}`]+)[\'"`]', rules_content)
        if author_match:
            author_name = author_match.group(1)
        
        if not title or not slug:
            print(f"Missing required fields - Title: {bool(title)}, Slug: {bool(slug)}")
            return {}
        
        return {
            "title": title,
            "description": description,
            "slug": slug,
            "tags": tags,
            "content": content,
            "author": {"name": author_name}
        }
    except Exception as e:
        print(f"Error parsing TypeScript exports: {str(e)}")
        return {}

def convert_rule_content(content: str) -> str:
    """Convert rule content to HTML sections"""
    sections = []
    current_section = {"title": "", "items": []}
    
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('##'):
            if current_section["title"]:
                sections.append(current_section)
            current_section = {"title": line[2:].strip(), "items": []}
        elif line.startswith('- '):
            current_section["items"].append(line[2:])
    
    if current_section["title"]:
        sections.append(current_section)
    
    html = ""
    for section in sections:
        html += f"""
            <section class="rule-section">
                <h2>{section['title']}</h2>
                <ul>
                    {''.join(f'<li>{item}</li>' for item in section['items'])}
                </ul>
            </section>
        """
    
    return html

def generate_rule_page(rule_data: Dict[str, any], next_rule: Optional[Dict] = None):
    """Generate HTML page for a rule"""
    if not rule_data.get("slug"):
        return
        
    slug = rule_data["slug"]
    title = rule_data["title"]
    description = f"Comprehensive {title} programming guidelines and best practices. Learn about code style, naming conventions, and performance optimization."
    keywords = ", ".join([f"{tag} rules" for tag in rule_data["tags"]] + [f"{tag} programming" for tag in rule_data["tags"]])
    
    tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in rule_data["tags"]])
    
    date = datetime.now()
    date_iso = date.strftime("%Y-%m-%d")
    date_display = date.strftime("Updated: %B %d, %Y")
    
    content_html = convert_rule_content(rule_data["content"])
    
    next_rule_html = ""
    if next_rule:
        next_rule_html = f'<a href="/rules/{next_rule["slug"]}.html" class="nav-link">Next: {next_rule["title"]} →</a>'
    
    html = TEMPLATE_HTML.format(
        title=title,
        description=description,
        keywords=keywords,
        slug=slug,
        author_name=rule_data.get("author", {}).get("name", "LLM Logs Team"),
        date_iso=date_iso,
        date_display=date_display,
        tags_html=tags_html,
        content_html=content_html,
        next_rule="javascript",  # This should be dynamic based on rules order
        next_rule_title="JavaScript Rules"  # This should be dynamic based on rules order
    )
    
    # Ensure directory exists
    os.makedirs(RULES_OUTPUT_DIR, exist_ok=True)
    
    # Write the file
    with open(os.path.join(RULES_OUTPUT_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(html)

def generate_rules_data(processed_rules: List[Dict]) -> None:
    """Generate a JavaScript file containing all rules data"""
    rules_data = []
    for rule in processed_rules:
        rules_data.append({
            "title": rule.get("title", "Unknown Rule"),
            "slug": rule.get("slug", ""),
            "description": f"Comprehensive guide for {rule.get('title', '')} development and best practices.",
            "tags": rule.get("tags", []),
            "category": rule.get("category", "General"),
            "author": rule.get("author", {}).get("name", "LLM Logs Team")
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
    """Main function to fetch and generate rules pages"""
    try:
        rules = fetch_rules()
        processed_rules = []
        
        for rule in rules:
            try:
                # Get the raw content
                print(f"Fetching {rule['name']}...")
                response = requests.get(rule["download_url"])
                if response.status_code == 200:
                    ts_content = response.text
                    rule_data = parse_typescript_exports(ts_content)
                    if rule_data and rule_data.get("slug"):
                        # Add category based on file name or content
                        rule_data["category"] = rule["name"].split(".")[0].capitalize()
                        processed_rules.append(rule_data)
                        print(f"Processed {rule_data['title']}")
                        
                        # Generate individual rule page
                        next_rule = rules[(rules.index(rule) + 1) % len(rules)]
                        next_rule_data = None
                        try:
                            next_response = requests.get(next_rule["download_url"])
                            if next_response.status_code == 200:
                                next_rule_data = parse_typescript_exports(next_response.text)
                        except Exception as e:
                            print(f"Error fetching next rule: {str(e)}")
                        
                        generate_rule_page(rule_data, next_rule_data)
                else:
                    print(f"Failed to fetch {rule['name']}: {response.status_code}")
            except Exception as e:
                print(f"Error processing {rule['name']}: {str(e)}")
        
        # Generate rules data file for rules.html
        generate_rules_data(processed_rules)
        print(f"Generated rules data file with {len(processed_rules)} rules")
        
    except Exception as e:
        print(f"Error in main execution: {str(e)}")

if __name__ == "__main__":
    main() 