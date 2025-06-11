const fs = require('fs');
const path = require('path');

// Configuration
const blogDir = '../blog';
const socialImageScript = '<script src="../assets/js/social-image.js"></script>';
const testControlsHtml = `
    <!-- Test Controls (only visible in development) -->
    <div id="testControls">
        <button class="btn btn-primary mb-2" onclick="testSocialImage()">Test Social Image</button>
        <button class="btn btn-info mb-2" onclick="testMetaTags()">Check Meta Tags</button>
        <button class="btn btn-secondary" onclick="hidePreview()">Hide Preview</button>
    </div>

    <!-- Preview container -->
    <div id="previewContainer" style="display:none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 20px; box-shadow: 0 0 20px rgba(0,0,0,0.2); max-width: 90vw; max-height: 90vh; overflow: auto; z-index: 1001;">
        <h3>Social Image Preview</h3>
        <img id="socialImagePreview" alt="Social image preview">
        <div id="metaTagInfo" style="margin-top: 15px; font-family: monospace; white-space: pre-wrap;"></div>
        <button class="btn btn-secondary mt-3" onclick="hidePreview()">Close Preview</button>
    </div>
`;

const testingScripts = `
    <script>
        function testSocialImage() {
            const preview = document.getElementById('previewContainer');
            const img = document.getElementById('socialImagePreview');
            
            // Get the current og:image
            const ogImage = document.querySelector('meta[property="og:image"]');
            if (ogImage) {
                img.src = ogImage.content;
                img.style.display = 'block';
                preview.style.display = 'block';
            } else {
                alert('No social image found! Make sure the generator script is running.');
            }
        }

        function testMetaTags() {
            const preview = document.getElementById('previewContainer');
            const info = document.getElementById('metaTagInfo');
            const metaTags = {
                'og:image': document.querySelector('meta[property="og:image"]')?.content,
                'og:image:width': document.querySelector('meta[property="og:image:width"]')?.content,
                'og:image:height': document.querySelector('meta[property="og:image:height"]')?.content,
                'twitter:image': document.querySelector('meta[property="twitter:image"]')?.content,
                'twitter:card': document.querySelector('meta[property="twitter:card"]')?.content
            };

            let infoText = 'Social Meta Tags:\\n\\n';
            for (const [tag, value] of Object.entries(metaTags)) {
                infoText += tag + ': ' + (value || 'Not found!') + '\\n';
            }
            
            info.textContent = infoText;
            preview.style.display = 'block';
        }

        function hidePreview() {
            document.getElementById('previewContainer').style.display = 'none';
        }
    </script>
`;

const debugStyles = `
    <style>
        #socialImagePreview {
            max-width: 100%;
            height: auto;
            margin: 20px 0;
            border: 1px solid #ddd;
            display: none;
        }
        #testControls {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: none;
        }
        /* Only show test controls in development */
        body.development #testControls {
            display: block;
        }
    </style>
`;

function updateBlogPost(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');

    // Skip if already updated
    if (content.includes('social-image.js')) {
        console.log(`Skipping ${filePath} - already updated`);
        return;
    }

    // Add social image script before closing head tag
    content = content.replace('</head>', `${socialImageScript}\n${debugStyles}\n</head>`);

    // Add development class to body tag
    content = content.replace('<body', '<body class="development"');

    // Add test controls before closing body tag
    content = content.replace('</body>', `${testControlsHtml}\n${testingScripts}\n</body>`);

    // Write the updated content back to the file
    fs.writeFileSync(filePath, content);
    console.log(`Updated ${filePath}`);
}

// Get all HTML files in the blog directory
const files = fs.readdirSync(blogDir)
    .filter(file => file.endsWith('.html'))
    // Exclude template files and index
    .filter(file => !['template.html', 'index.html'].includes(file));

// Update each blog post
files.forEach(file => {
    const filePath = path.join(blogDir, file);
    updateBlogPost(filePath);
});

console.log('All blog posts have been updated!'); 