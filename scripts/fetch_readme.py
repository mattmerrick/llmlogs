import csv
import requests
import markdown
import os
import json
import codecs
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote

def clean_github_url(url):
    """Convert GitHub blob URLs to raw content URLs."""
    if not url:
        return None
    # Convert blob URLs to raw content URLs
    url = url.replace('github.com', 'raw.githubusercontent.com')
    url = url.replace('/blob/', '/')
    return url

def fetch_readme_content(readme_url):
    """Fetch README content from GitHub."""
    if not readme_url:
        return None
    
    raw_url = clean_github_url(readme_url)
    if not raw_url:
        return None
    
    try:
        response = requests.get(raw_url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {raw_url}: {str(e)}")
        return None

def markdown_to_html(md_content):
    """Convert markdown content to HTML."""
    if not md_content:
        return None
    
    # Convert markdown to HTML
    html = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])
    
    # Clean up the HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Add CSS classes for styling
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        tag['class'] = tag.get('class', []) + ['heading']
    
    for tag in soup.find_all('code'):
        tag['class'] = tag.get('class', []) + ['code']
    
    for tag in soup.find_all('pre'):
        tag['class'] = tag.get('class', []) + ['pre']
    
    return str(soup)

def process_csv():
    """Process the CSV file and generate HTML content."""
    output_dir = 'mcp'
    os.makedirs(output_dir, exist_ok=True)
    
    projects = []
    
    # Try different encodings
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
    
    for encoding in encodings:
        try:
            with codecs.open('mcpmain.csv', 'r', encoding=encoding) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Extract the project name from the GitHub URL
                    github_url = row['github_url']
                    if not github_url:
                        continue
                        
                    parsed_url = urlparse(github_url)
                    path_parts = parsed_url.path.strip('/').split('/')
                    if len(path_parts) < 2:
                        continue
                        
                    org_name = path_parts[0]
                    repo_name = path_parts[1]
                    
                    print(f"Processing {org_name}/{repo_name}...")
                    
                    # Fetch and convert README
                    readme_content = fetch_readme_content(row['readme_url'])
                    if not readme_content:
                        print(f"Failed to fetch README for {org_name}/{repo_name}")
                        continue
                        
                    html_content = markdown_to_html(readme_content)
                    if not html_content:
                        print(f"Failed to convert README to HTML for {org_name}/{repo_name}")
                        continue
                    
                    # Create project info
                    project_info = {
                        'name': row['name'],
                        'title': row['title'],
                        'description': row['description'],
                        'github_url': github_url,
                        'stars': row['stars'],
                        'language': row['language'],
                        'topics': row['topics'].split(',') if row['topics'] else [],
                        'html_content': html_content
                    }
                    
                    # Save individual HTML file
                    file_name = f"{org_name}-{repo_name}.html"
                    file_path = os.path.join(output_dir, file_name)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    # Add to projects list without HTML content
                    project_info_without_html = project_info.copy()
                    del project_info_without_html['html_content']
                    projects.append(project_info_without_html)
                
                # If we successfully read the file, break the loop
                break
        except UnicodeDecodeError:
            print(f"Failed to read with {encoding} encoding, trying next...")
            continue
        except Exception as e:
            print(f"Error processing CSV: {str(e)}")
            raise
    
    # Save projects metadata
    with open(os.path.join(output_dir, 'projects.json'), 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2)

if __name__ == '__main__':
    process_csv() 