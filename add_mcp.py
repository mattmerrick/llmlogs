import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import base64
import re

def get_github_repo_info(github_url):
    """Fetch repository information from GitHub API"""
    # Extract owner and repo from URL
    match = re.match(r'https://github.com/([^/]+)/([^/]+)', github_url)
    if not match:
        raise ValueError("Invalid GitHub URL")
    
    owner, repo = match.groups()
    
    # GitHub API endpoint
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    
    # Add your GitHub token here if you have one
    headers = {
        "Accept": "application/vnd.github.v3+json",
        # "Authorization": "token YOUR_GITHUB_TOKEN"
    }
    
    # Fetch repo info
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch repo info: {response.status_code}")
    
    repo_data = response.json()
    
    # Fetch README
    readme_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    readme_response = requests.get(readme_url, headers=headers)
    if readme_response.status_code != 200:
        raise Exception("Failed to fetch README")
    
    readme_data = readme_response.json()
    readme_content = base64.b64decode(readme_data["content"]).decode("utf-8")
    
    return {
        "name": repo_data["name"],
        "description": repo_data["description"] or "",
        "stars": repo_data["stargazers_count"],
        "language": repo_data["language"],
        "topics": repo_data["topics"],
        "last_updated": repo_data["updated_at"],
        "readme": readme_content,
        "github_url": github_url
    }

def update_projects_json(repo_info):
    """Update projects.json with new repository information"""
    projects_file = "mcp/projects.json"
    
    try:
        with open(projects_file, 'r', encoding='utf-8') as f:
            projects = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        projects = []
    
    # Check if project already exists
    for project in projects:
        if project["github_url"] == repo_info["github_url"]:
            # Update existing project
            project.update({
                "name": repo_info["name"],
                "description": repo_info["description"],
                "stars": repo_info["stars"],
                "language": repo_info["language"],
                "topics": repo_info["topics"],
                "last_updated": repo_info["last_updated"]
            })
            break
    else:
        # Add new project
        projects.append({
            "name": repo_info["name"],
            "github_url": repo_info["github_url"],
            "description": repo_info["description"],
            "stars": repo_info["stars"],
            "language": repo_info["language"],
            "topics": repo_info["topics"],
            "last_updated": repo_info["last_updated"]
        })
    
    # Save updated projects.json
    with open(projects_file, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2)

def create_mcp_page(repo_info):
    """Create a new MCP page from repository information"""
    # Generate filename from GitHub URL
    org_repo = repo_info["github_url"].split("/")[-2:]
    filename = f"mcp/{org_repo[0]}-{org_repo[1]}.html"
    
    # Convert README markdown to HTML
    # Note: You might want to use a markdown parser here
    readme_html = f"<div class='readme-content'>{repo_info['readme']}</div>"
    
    # Generate topic tags HTML
    topic_tags_html = ''.join([f'<span class="topic-tag">{topic}</span>' for topic in repo_info["topics"]])
    
    # Read HTML template
    with open('update_mcp_pages.py', 'r', encoding='utf-8') as f:
        content = f.read()
        template_match = re.search(r'HTML_TEMPLATE = \'\'\'(.*?)\'\'\'', content, re.DOTALL)
        if not template_match:
            raise Exception("Could not find HTML template in update_mcp_pages.py")
        template = template_match.group(1)
    
    # Create the new HTML content
    new_html = template.format(
        title=repo_info["name"],
        description=repo_info["description"][:160],
        filename=os.path.basename(filename),
        stars=repo_info["stars"],
        language=repo_info["language"] or "Not specified",
        topic_tags=topic_tags_html,
        github_url=repo_info["github_url"],
        content=readme_html
    )
    
    # Save the new file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_html)

def update_mcp_index():
    """Update the main MCP index page with the new project"""
    os.system('python update_mcp_pages.py')

def main():
    # Get GitHub URL from user
    github_url = input("Enter the GitHub repository URL: ")
    
    try:
        # Fetch repository information
        print("Fetching repository information...")
        repo_info = get_github_repo_info(github_url)
        
        # Update projects.json
        print("Updating projects.json...")
        update_projects_json(repo_info)
        
        # Create MCP page
        print("Creating MCP page...")
        create_mcp_page(repo_info)
        
        # Update index
        print("Updating MCP index...")
        update_mcp_index()
        
        print("Successfully added new MCP!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 