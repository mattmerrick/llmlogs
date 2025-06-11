import os
import glob
import re

# Configuration
BLOG_DIR = '../blog'
SOCIAL_IMAGE_SCRIPT = '<script src="../assets/js/social-image.js"></script>'

def update_blog_post(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove test controls and their content
    content = re.sub(r'<!-- Test Controls.*?</div>\s*-->', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- Preview container.*?</div>\s*-->', '', content, flags=re.DOTALL)
    
    # Remove test scripts
    content = re.sub(r'<script>\s*function testSocialImage.*?</script>', '', content, flags=re.DOTALL)
    
    # Remove debug styles
    content = re.sub(r'<style>\s*#socialImagePreview.*?</style>', '', content, flags=re.DOTALL)
    
    # Remove development class
    content = content.replace('class="development"', '')
    
    # Ensure social image script is present
    if 'social-image.js' not in content:
        content = content.replace('</head>', f'{SOCIAL_IMAGE_SCRIPT}\n</head>')
    
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