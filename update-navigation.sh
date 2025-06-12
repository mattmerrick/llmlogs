#!/bin/bash

# Update all href="/start" to href="/start-here"
find . -type f -name "*.html" -exec sed -i 's|href="/start"|href="/start-here"|g' {} +

# Also update any potential variations
find . -type f -name "*.html" -exec sed -i 's|href="/start/"|href="/start-here"|g' {} +
find . -type f -name "*.html" -exec sed -i 's|href="/start.html"|href="/start-here"|g' {} +

# Update breadcrumb navigation for tool reviews
find . -name "*.html" -type f -exec sed -i 's|href="/tools" class="text-white">Tools</a>|href="/tool-reviews" class="text-white">Tool Reviews</a>|g' {} +

# Update main navigation for tool reviews section
find . -name "*.html" -type f -exec sed -i 's|href="/tools">Tools</a>|href="/tool-reviews">Tool Reviews</a>|g' {} +

# Keep /free-tools links as is since they point to actual tools
# Update any remaining /tools references to point to the correct section
find . -name "*.html" -type f -exec sed -i 's|href="/tools/|href="/free-tools/|g' {} +

# Update blog post links
find . -name "*.html" -type f -exec sed -i 's|/blog/how-to-add-a-llms.txt-file-to-any-website-in-under-10-minutes|/blog/ultimate-guide-to-llms-txt-implementation|g' {} +
find . -name "*.html" -type f -exec sed -i 's|/blog/understanding-llm-optimization|/blog/llm-optimization-guide|g' {} +
find . -name "*.html" -type f -exec sed -i 's|/blog/seo-best-practices-2025|/blog/llm-seo-best-practices|g' {} +
find . -name "*.html" -type f -exec sed -i 's|/blog/ai-content-optimization|/blog/content-optimization-for-llms|g' {} + 