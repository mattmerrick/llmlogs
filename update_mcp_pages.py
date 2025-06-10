import os
import re
import json
from bs4 import BeautifulSoup
from datetime import datetime

# Load project metadata
def load_project_metadata():
    try:
        with open('mcp/projects.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading projects.json: {e}")
        return []

# Standard HTML template following blog post structure
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="{title} - MCP Directory">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="https://llmlogs.com/mcp/{filename}">
    <meta property="og:type" content="article">
    
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title} - MCP Directory">
    <meta name="twitter:description" content="{description}">
    
    <title>{title} - MCP Directory - LLM Logs</title>
    
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-P33Z79C6');</script>
    <!-- End Google Tag Manager -->
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Inter Font -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Main CSS -->
    <link rel="stylesheet" href="../assets/css/style.css">
    
    <style>
        body {{
            font-family: 'Inter', var(--bs-font-sans-serif);
        }}
        pre, code {{
            font-family: 'Fira Code', monospace;
            background-color: var(--bs-gray-100);
            padding: 0.2rem 0.4rem;
            border-radius: 0.2rem;
            font-size: 0.875em;
        }}
        pre code {{
            padding: 0;
            background-color: transparent;
        }}
        .hero-section {{
            background-color: var(--bs-primary);
            color: white;
            padding: 4rem 0;
            margin-bottom: 2rem;
        }}
        .blog-meta {{
            color: var(--bs-gray-600);
            font-size: 0.9rem;
        }}
        .blog-content h2 {{
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        .blog-content h3 {{
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }}
        .blog-content p {{
            margin-bottom: 1.25rem;
            line-height: 1.7;
        }}
        .blog-content ul, .blog-content ol {{
            margin-bottom: 1.25rem;
        }}
        .blog-content blockquote {{
            border-left: 4px solid var(--bs-primary);
            padding-left: 1rem;
            margin-left: 0;
            color: var(--bs-gray-700);
        }}
        /* Project-specific styles */
        .project-meta {{
            background-color: var(--bs-gray-100);
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 2rem 0;
        }}
        .project-meta .meta-item {{
            display: flex;
            align-items: center;
            margin-bottom: 0.75rem;
        }}
        .project-meta .meta-item svg {{
            width: 1.25rem;
            height: 1.25rem;
            margin-right: 0.75rem;
        }}
        .topic-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1rem;
        }}
        .topic-tag {{
            background-color: var(--bs-gray-200);
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
        }}
        .readme-content {{
            margin-top: 2rem;
        }}
        .readme-content pre {{
            background-color: var(--bs-gray-100);
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            position: relative;
        }}
        .readme-content img {{
            max-width: 100%;
            height: auto;
        }}
        /* Copy button styles */
        .copy-button {{
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            padding: 0.25rem 0.75rem;
            font-size: 0.875rem;
            border-radius: 0.25rem;
            background-color: var(--bs-light);
            border: 1px solid var(--bs-gray-300);
            color: var(--bs-gray-700);
            transition: all 0.2s;
        }}
        .copy-button:hover {{
            background-color: var(--bs-gray-200);
        }}
        .copy-button.copied {{
            background-color: var(--bs-success);
            color: white;
            border-color: var(--bs-success);
        }}
        /* Share section styles */
        .share-section {{
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid var(--bs-gray-200);
        }}
        .share-buttons {{
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }}
        .back-to-top {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            padding: 0.75rem;
            border-radius: 50%;
            background-color: var(--bs-primary);
            color: white;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 1000;
        }}
        .back-to-top:not(.hidden) {{
            opacity: 1;
        }}
    </style>
</head>
<body>
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-P33Z79C6"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->

    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top">
        <div class="container">
            <a class="navbar-brand fw-semibold" href="/">LLM Logs</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/start-here.html">Start Here</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/guides/llm-optimization">Guides</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/free-tools">Tools</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/blog">Blog</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="https://github.com/mattmerrick/llmseoguide" target="_blank" rel="noopener">GitHub</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <div class="hero-section">
        <div class="container">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb mb-4">
                    <li class="breadcrumb-item"><a href="/" class="text-white">Home</a></li>
                    <li class="breadcrumb-item"><a href="/mcp" class="text-white">MCP Directory</a></li>
                    <li class="breadcrumb-item active text-white" aria-current="page">{title}</li>
                </ol>
            </nav>
            <h1 class="display-4 mb-3">{title}</h1>
        </div>
    </div>

    <!-- Main Content -->
    <main class="container py-5">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <article class="blog-content">
                    <!-- Project Meta -->
                    <div class="project-meta">
                        <div class="meta-item">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor">
                                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                            </svg>
                            <span>Stars: {stars}</span>
                        </div>
                        <div class="meta-item">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor">
                                <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zM7 6.5C7 7.328 6.552 8 6 8s-1-.672-1-1.5S5.448 5 6 5s1 .672 1 1.5zM4.285 9.567a.5.5 0 0 1 .683.183A3.498 3.498 0 0 0 8 11.5a3.498 3.498 0 0 0 3.032-1.75.5.5 0 1 1 .866.5A4.498 4.498 0 0 1 8 12.5a4.498 4.498 0 0 1-3.898-2.25.5.5 0 0 1 .183-.683zM10 8c-.552 0-1-.672-1-1.5S9.448 5 10 5s1 .672 1 1.5S10.552 8 10 8z"/>
                            </svg>
                            <span>Language: {language}</span>
                        </div>
                        <div class="topic-tags">
                            {topic_tags}
                        </div>
                        <a href="{github_url}" class="btn btn-primary mt-3" target="_blank" rel="noopener">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16" class="me-2">
                                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                            </svg>
                            View on GitHub
                        </a>
                    </div>

                    <!-- README Content -->
                    <div class="readme-content">
                        {content}
                    </div>

                    <!-- Share Section -->
                    <div class="share-section">
                        <h3>Share this Project</h3>
                        <div class="share-buttons">
                            <button class="btn btn-outline-primary share-button" data-url="https://llmlogs.com/mcp/{filename}">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-link-45deg me-2" viewBox="0 0 16 16">
                                    <path d="M4.715 6.542 3.343 7.914a3 3 0 1 0 4.243 4.243l1.828-1.829A3 3 0 0 0 8.586 5.5L8 6.086a1.002 1.002 0 0 0-.154.199 2 2 0 0 1 .861 3.337L6.88 11.45a2 2 0 1 1-2.83-2.83l.793-.792a4.018 4.018 0 0 1-.128-1.287z"/>
                                    <path d="M6.586 4.672A3 3 0 0 0 7.414 9.5l.775-.776a2 2 0 0 1-.896-3.346L9.12 3.55a2 2 0 1 1 2.83 2.83l-.793.792c.112.42.155.855.128 1.287l1.372-1.372a3 3 0 1 0-4.243-4.243L6.586 4.672z"/>
                                </svg>
                                Copy Link
                            </button>
                        </div>
                    </div>
                </article>
            </div>
        </div>
    </main>

    <button class="btn btn-primary back-to-top hidden" aria-label="Back to top">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-up" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 0 .5.5z"/>
        </svg>
    </button>

    <footer class="bg-white py-5 mt-5">
        <div class="container">
            <div class="row justify-content-center text-center">
                <div class="col-md-8">
                    <div class="d-flex flex-column flex-md-row justify-content-center gap-4 mb-4">
                        <a href="/" class="text-muted text-decoration-none">Home</a>
                        <a href="/guides" class="text-muted text-decoration-none">Guides</a>
                        <a href="/tools" class="text-muted text-decoration-none">Tools</a>
                        <a href="/blog" class="text-muted text-decoration-none">Blog</a>
                        <a href="https://github.com/mattmerrick/llmseoguide" target="_blank" rel="noopener" class="text-muted text-decoration-none">GitHub</a>
                    </div>
                    <p class="text-muted small mb-0">&copy; 2025 LLM Logs. All rights reserved.</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="../assets/js/main.js"></script>
</body>
</html>'''

def update_html_file(file_path, projects):
    try:
        # Read existing content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin1') as f:
                content = f.read()
        except:
            print(f"Error reading file: {file_path}")
            return

    # Parse HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract filename and find corresponding project data
    filename = os.path.basename(file_path)
    project = None
    for p in projects:
        if p['github_url']:
            org_repo = p['github_url'].split('/')[-2:]
            if f"{org_repo[0]}-{org_repo[1]}.html" == filename:
                project = p
                break

    if not project:
        print(f"Could not find project data for {filename}")
        return

    # Get the title from the first h1 or use the project name
    title = soup.find('h1')
    if title:
        title = title.get_text(strip=True)
    else:
        title = project['name']

    # Get the description from the first p or use the project description
    description = soup.find('p')
    if description:
        description = description.get_text(strip=True)[:160]
    else:
        description = project['description'][:160] if project['description'] else ''

    # Generate topic tags HTML
    topic_tags_html = ''.join([f'<span class="topic-tag">{topic}</span>' for topic in project['topics']])

    # Create the new HTML content
    new_html = HTML_TEMPLATE.format(
        title=title,
        description=description,
        filename=filename,
        stars=project['stars'],
        language=project['language'] or 'Not specified',
        topic_tags=topic_tags_html,
        github_url=project['github_url'],
        content=str(soup)
    )

    # Save the updated file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Successfully updated {filename}")

def main():
    # Load project metadata
    projects = load_project_metadata()
    if not projects:
        print("Failed to load projects metadata")
        return

    # Process all HTML files in the mcp directory
    mcp_dir = 'mcp'
    for filename in os.listdir(mcp_dir):
        if filename.endswith('.html') and filename not in ['index.html', 'project-template.html']:
            file_path = os.path.join(mcp_dir, filename)
            print(f"Updating {filename}...")
            update_html_file(file_path, projects)

if __name__ == "__main__":
    main() 