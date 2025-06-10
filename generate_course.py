import os
import json
import markdown2
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

GITHUB_WIKI_BASE = "https://github.com/mattmerrick/llmlogs/wiki"
WIKI_RAW_BASE = "https://raw.githubusercontent.com/wiki/mattmerrick/llmlogs"

# Course structure with wiki page mappings
COURSE_PAGES = [
    {
        "filename": "1-introduction.html",
        "title": "Introduction: Why AI Search Matters",
        "description": "Learn why AI search is revolutionizing SEO and how it differs from traditional search engines.",
        "progress": 12.5,
        "wiki_page": "1.-Introduction:-Why-AI-Search-Matters",
        "prev_link": "",
        "next_link": '<a href="2-how-ai-search-works.html" class="btn btn-primary float-end">Next: How AI Search Works →</a>'
    },
    {
        "filename": "2-how-ai-search-works.html",
        "title": "How AI Search and LLMs Work",
        "description": "Understand the fundamentals of AI search engines and Large Language Models.",
        "progress": 25,
        "wiki_page": "2.-How-AI-Search-and-LLMs-Work",
        "prev_link": '<a href="1-introduction.html" class="btn btn-outline-primary">← Previous: Introduction</a>',
        "next_link": '<a href="3-five-pillars.html" class="btn btn-primary float-end">Next: The 5 Pillars →</a>'
    },
    {
        "filename": "3-five-pillars.html",
        "title": "The 5 Pillars of LLM SEO",
        "description": "Master the five fundamental principles that drive success in AI search optimization.",
        "progress": 37.5,
        "wiki_page": "3.-The-5-Pillars-of-LLM-SEO",
        "prev_link": '<a href="2-how-ai-search-works.html" class="btn btn-outline-primary">← Previous: How AI Search Works</a>',
        "next_link": '<a href="4-content-types.html" class="btn btn-primary float-end">Next: Content Types →</a>'
    },
    {
        "filename": "4-content-types.html",
        "title": "Content Types That Perform Well",
        "description": "Discover which types of content perform best in AI search results and why.",
        "progress": 50,
        "wiki_page": "4.-Content-Types-That-Perform-Well",
        "prev_link": '<a href="3-five-pillars.html" class="btn btn-outline-primary">← Previous: The 5 Pillars</a>',
        "next_link": '<a href="5-site-architecture.html" class="btn btn-primary float-end">Next: Site Architecture →</a>'
    },
    {
        "filename": "5-site-architecture.html",
        "title": "Site Architecture for AI",
        "description": "Learn how to structure your site for optimal AI crawling and understanding.",
        "progress": 62.5,
        "wiki_page": "5.-Site-Architecture-for-AI-Visibility",
        "prev_link": '<a href="4-content-types.html" class="btn btn-outline-primary">← Previous: Content Types</a>',
        "next_link": '<a href="6-prompt-engineering.html" class="btn btn-primary float-end">Next: Prompt Engineering →</a>'
    },
    {
        "filename": "6-prompt-engineering.html",
        "title": "Prompt Engineering for Visibility",
        "description": "Master the art of prompt engineering to improve your content's visibility in AI search.",
        "progress": 75,
        "wiki_page": "6.-Prompt-Engineering-for-Visibility-Feedback",
        "prev_link": '<a href="5-site-architecture.html" class="btn btn-outline-primary">← Previous: Site Architecture</a>',
        "next_link": '<a href="7-crawler-logs.html" class="btn btn-primary float-end">Next: Crawler Logs →</a>'
    },
    {
        "filename": "7-crawler-logs.html",
        "title": "AI Crawler Logs and Monitoring",
        "description": "Learn how to monitor and analyze AI crawler behavior on your site.",
        "progress": 87.5,
        "wiki_page": "7.-AI-Crawler-Logs-and-Monitoring",
        "prev_link": '<a href="6-prompt-engineering.html" class="btn btn-outline-primary">← Previous: Prompt Engineering</a>',
        "next_link": '<a href="8-case-studies.html" class="btn btn-primary float-end">Next: Case Studies →</a>'
    },
    {
        "filename": "8-case-studies.html",
        "title": "Real-World Case Studies",
        "description": "Explore real-world examples of successful AI search optimization strategies.",
        "progress": 100,
        "wiki_page": "8.-Real‐World-Case-Studies",
        "prev_link": '<a href="7-crawler-logs.html" class="btn btn-outline-primary">← Previous: Crawler Logs</a>',
        "next_link": ""
    }
]

def get_wiki_content(wiki_page):
    """Fetch content from GitHub wiki page"""
    # First try the raw content
    raw_url = f"{WIKI_RAW_BASE}/{wiki_page}.md"
    response = requests.get(raw_url)
    
    if response.status_code == 200:
        return response.text, datetime.now(pytz.UTC).isoformat()
    
    # If raw content fails, try scraping the HTML page
    html_url = f"{GITHUB_WIKI_BASE}/{wiki_page}"
    response = requests.get(html_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the last updated time
        time_element = soup.find('relative-time')
        last_updated = time_element['datetime'] if time_element else datetime.now(pytz.UTC).isoformat()
        
        # Find the wiki content
        wiki_content = soup.find('div', {'class': 'markdown-body'})
        if wiki_content:
            return wiki_content.get_text(), last_updated
    
    return None, None

def read_template():
    """Read the course page template"""
    with open('ai-seo-course/course-template.html', 'r', encoding='utf-8') as f:
        return f.read()

def create_course_page(template, page_info, content, last_updated=None):
    """Create a single course page"""
    # For index page, use content directly without markdown conversion
    if page_info["filename"] == "index.html":
        html_content = content
    else:
        # Convert markdown content to HTML for other pages
        html_content = markdown2.markdown(content, extras=['fenced-code-blocks', 'tables', 'header-ids'])
    
    # Add schema.org markup
    schema_markup = f"""
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{page_info['title']} - AI SEO Course",
        "description": "{page_info['description']}",
        "image": "https://llmlogs.com/ai-seo-course/images/course-header.png",
        "author": {{
            "@type": "Person",
            "name": "Matt Merrick"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "LLM Logs",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://llmlogs.com/assets/images/logo.png"
            }}
        }},
        "datePublished": "2025-03-21T08:00:00+00:00",
        "dateModified": "{last_updated if last_updated else datetime.now(pytz.UTC).isoformat()}",
        "isPartOf": {{
            "@type": "Course",
            "name": "AI SEO Course",
            "description": "Master the art of optimizing your content for AI search engines",
            "provider": {{
                "@type": "Organization",
                "name": "LLM Logs",
                "sameAs": "https://llmlogs.com"
            }}
        }}
    }}
    </script>
    """
    
    # Add GitHub source link and last updated info
    if page_info["filename"] != "index.html" and last_updated:
        wiki_url = f"{GITHUB_WIKI_BASE}/{page_info['wiki_page']}"
        metadata_html = f"""
        <div class="alert alert-light border mt-5">
            <p class="mb-1"><small class="text-muted">Last updated: {last_updated}</small></p>
            <p class="mb-0"><small>Source: <a href="{wiki_url}" target="_blank" rel="noopener">View on GitHub Wiki</a></small></p>
        </div>
        """
        html_content += metadata_html
    
    # Format code blocks with copy button (only for non-index pages)
    if page_info["filename"] != "index.html":
        soup = BeautifulSoup(html_content, 'html.parser')
        for pre in soup.find_all('pre'):
            code = pre.find('code')
            if code:
                # Add copy button
                copy_btn = soup.new_tag('button')
                copy_btn['class'] = 'copy-code-button btn btn-sm btn-outline-primary'
                copy_btn['data-clipboard-target'] = '#' + code['id'] if code.get('id') else ''
                copy_btn.string = 'Copy'
                
                # Wrap in container
                container = soup.new_tag('div')
                container['class'] = 'code-block-container'
                pre.wrap(container)
                container.insert(0, copy_btn)
        html_content = str(soup)
    
    # Set active state for current page in sidebar
    active_states = {f"active_{i+1}": "" for i in range(8)}
    
    # Special case for index page
    if page_info["filename"] == "index.html":
        current_page_num = 0
    else:
        current_page_num = int(page_info["filename"].split("-")[0])
        active_states[f"active_{current_page_num}"] = "active"
    
    # Fill in template
    page_html = template.format(
        title=page_info["title"],
        description=page_info["description"],
        filename=page_info["filename"],
        content=schema_markup + html_content,
        progress=page_info["progress"],
        prev_link=page_info["prev_link"],
        next_link=page_info["next_link"],
        **active_states
    )
    
    # Save the page
    output_path = os.path.join('ai-seo-course', page_info["filename"])
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(page_html)
    print(f"Created {page_info['filename']}")

def create_index_page():
    """Create the course index page"""
    index_content = """
    <h1>AI SEO Course</h1>
    <p class="lead">Master the art of optimizing your content for AI search engines with our comprehensive guide.</p>
    
    <div class="alert alert-info border-0 bg-primary bg-opacity-10 p-4 mb-5">
        <h2 class="h4 mb-3">🔍 Why AI SEO Matters</h2>
        <p>In today's AI-driven world, traditional SEO isn't enough. AI search engines and large language models are changing how content is discovered and ranked. This course will teach you the essential strategies to optimize your content for AI algorithms.</p>
        <p class="mb-0"><strong>Key fact:</strong> Websites listed in AI directories see an average increase of 30-50% in domain authority within the first 3 months.</p>
    </div>

    <div class="card border-success mb-5">
        <div class="card-body">
            <h2 class="h4 mb-3">💝 Why This Course is Free</h2>
            <p>I believe that understanding AI search optimization shouldn't be locked behind a paywall. As AI reshapes the digital landscape, everyone deserves access to the knowledge needed to stay competitive and visible online.</p>
            <p>While others charge hundreds for similar courses, I've made this comprehensive guide completely free. My goal is simple: to help as many people as possible succeed in the age of AI search.</p>
            <div class="bg-light p-4 rounded">
                <h3 class="h5 mb-3">✨ Support This Initiative</h3>
                <p class="mb-4">If you find this course valuable, here are two simple ways you can help:</p>
                <div class="d-flex gap-3">
                    <a href="https://github.com/mattmerrick/llmseoguide" target="_blank" rel="noopener" class="btn btn-dark">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-github me-2" viewBox="0 0 16 16">
                            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                        </svg>
                        Star on GitHub
                    </a>
                    <button class="btn btn-primary" onclick="navigator.share({title: 'AI SEO Course', url: window.location.href})" title="Share this course">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-share me-2" viewBox="0 0 16 16">
                            <path d="M13.5 1a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zM11 2.5a2.5 2.5 0 1 1 .603 1.628l-6.718 3.12a2.499 2.499 0 0 1 0 1.504l6.718 3.12a2.5 2.5 0 1 1-.488.876l-6.718-3.12a2.5 2.5 0 1 1 0-3.256l6.718-3.12A2.5 2.5 0 0 1 11 2.5zm-8.5 4a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm11 5.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"/>
                        </svg>
                        Share with a Friend
                    </button>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row mt-5">
        <div class="col-lg-8">
            <div class="card mb-4">
                <div class="card-body">
                    <h2>What You'll Learn</h2>
                    <ul class="list-unstyled">
                        <li class="mb-3">✓ Understanding AI search fundamentals</li>
                        <li class="mb-3">✓ The 5 pillars of LLM SEO</li>
                        <li class="mb-3">✓ Content optimization strategies</li>
                        <li class="mb-3">✓ Site architecture best practices</li>
                        <li class="mb-3">✓ Prompt engineering techniques</li>
                        <li class="mb-3">✓ Monitoring and analytics</li>
                        <li class="mb-3">✓ Real-world case studies</li>
                    </ul>
                    <a href="1-introduction.html" class="btn btn-primary btn-lg mt-3">Start Learning Now →</a>
                </div>
            </div>
            
            <div class="alert alert-info">
                <h3 class="h5">📚 Open Source Learning</h3>
                <p class="mb-0">This course content is maintained in our <a href="{GITHUB_WIKI_BASE}" target="_blank" rel="noopener">GitHub Wiki</a>. Feel free to contribute, suggest improvements, or report issues!</p>
            </div>
        </div>
        
        <div class="col-lg-4">
            <div class="card mb-4">
                <div class="card-body">
                    <h3>Course Details</h3>
                    <ul class="list-unstyled">
                        <li class="mb-2">📚 8 comprehensive lessons</li>
                        <li class="mb-2">⏱️ 2-3 hours to complete</li>
                        <li class="mb-2">🎯 Practical examples</li>
                        <li class="mb-2">💻 Code samples included</li>
                        <li class="mb-2">🆓 100% Free forever</li>
                        <li class="mb-2">🔄 Regularly updated</li>
                        <li class="mb-2">👥 Community-driven</li>
                    </ul>
                </div>
            </div>

            <div class="card bg-primary bg-opacity-10 border-primary">
                <div class="card-body">
                    <h3 class="h4">💡 Pro Tip: Build Authority</h3>
                    <p>While learning AI SEO, start building your site's authority by getting listed in AI directories. This parallel approach will give you a head start in improving your domain rating.</p>
                    <a href="https://www.aidirectori.es/?via=llmlogs" target="_blank" rel="noopener" class="btn btn-primary">Get Listed Now →</a>
                </div>
            </div>
        </div>
    </div>
    
    <div class="mt-5">
        <h2>Course Outline</h2>
        <div class="list-group">
    """
    
    # Add course outline
    for page in COURSE_PAGES:
        index_content += f"""
            <a href="{page['filename']}" class="list-group-item list-group-item-action">
                <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">{page['title']}</h5>
                    <small>{page['progress']}% Complete</small>
                </div>
                <p class="mb-1">{page['description']}</p>
            </a>
        """
    
    index_content += """
        </div>
    </div>
    """
    
    # Create index page using template
    template = read_template()
    create_course_page(template, {
        "filename": "index.html",
        "title": "AI SEO Course",
        "description": "Master the art of optimizing your content for AI search engines with our comprehensive guide.",
        "progress": 0,
        "prev_link": "",
        "next_link": '<a href="1-introduction.html" class="btn btn-primary float-end">Start Course →</a>'
    }, index_content)

def main():
    # Create course directory if it doesn't exist
    os.makedirs('ai-seo-course', exist_ok=True)
    
    # Read template
    template = read_template()
    
    # Create index page
    create_index_page()
    
    # Create course pages
    for page in COURSE_PAGES:
        print(f"Fetching content for {page['title']}...")
        content, last_updated = get_wiki_content(page['wiki_page'])
        
        if content:
            create_course_page(template, page, content, last_updated)
        else:
            print(f"Warning: Could not fetch content for {page['wiki_page']}, using placeholder")
            content = f"""
            # {page['title']}
            
            This content will be updated from the GitHub wiki soon.
            
            [View the content on GitHub]({GITHUB_WIKI_BASE}/{page['wiki_page']})
            """
            create_course_page(template, page, content)
    
    print("Course generation complete!")

if __name__ == "__main__":
    main() 