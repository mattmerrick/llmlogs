import os
import glob
import re

# Configuration
BLOG_DIR = '../blog'
SOCIAL_IMAGE_SCRIPT = '<script src="../assets/js/social-image.js"></script>'

def update_blog_post(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # More aggressive pattern matching to remove all test-related elements
    patterns_to_remove = [
        # Remove test controls div
        r'\s*<div id="testControls".*?</div>\s*',
        # Remove preview container div
        r'\s*<div id="previewContainer".*?</div>\s*',
        # Remove test scripts
        r'\s*<script>\s*function testSocialImage.*?</script>\s*',
        r'\s*<script>\s*function testMetaTags.*?</script>\s*',
        r'\s*<script>\s*function hidePreview.*?</script>\s*',
        # Remove debug styles
        r'\s*<style>[^<]*#socialImagePreview[^<]*</style>\s*',
        r'\s*<style>[^<]*#testControls[^<]*</style>\s*',
        # Remove any leftover test-related HTML comments
        r'\s*<!-- Test Controls.*?-->\s*',
        r'\s*<!-- Preview container.*?-->\s*',
        # Remove any stray buttons
        r'\s*<button[^>]*onclick="hidePreview\(\)"[^>]*>.*?</button>\s*',
        r'\s*<button[^>]*onclick="testSocialImage\(\)"[^>]*>.*?</button>\s*',
        r'\s*<button[^>]*onclick="testMetaTags\(\)"[^>]*>.*?</button>\s*'
    ]
    
    # Apply all removal patterns
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove development class
    content = re.sub(r'class="development"', '', content)
    content = re.sub(r'class="\s*"', '', content)  # Clean up empty class attributes
    
    # Ensure social image script is present
    if 'social-image.js' not in content:
        content = content.replace('</head>', f'{SOCIAL_IMAGE_SCRIPT}\n</head>')
    
    # Clean up any multiple consecutive empty lines
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Write the updated content back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {filepath}')

def main():
    # Get all HTML files in blog directory except template and index
    blog_files = [f for f in glob.glob(os.path.join(BLOG_DIR, '*.html')) 
                  if not os.path.basename(f) in ['template.html', 'index.html']]
    
    # Update each blog post
    for filepath in blog_files:
        update_blog_post(filepath)
    
    print('\nAll blog posts have been updated!')

if __name__ == '__main__':
    main() 