const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

// Directory paths
const ROOT_DIR = path.join(__dirname, '..');
const TOOLS_DIR = path.join(__dirname, '..', 'free-tools');
const GUIDES_DIR = path.join(__dirname, '..', 'guides/llm-optimization');

// Files to exclude from root conversion
const EXCLUDE_FILES = [
    'index.html',  // Handle separately due to special layout
    'sitemap.xml',
    'robots.txt',
    'llms.txt',
    'README.md'
];

// Template parts
const HEAD_TEMPLATE = `
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
`;

const STYLE_TEMPLATE = `
    <style>
        body {
            font-family: 'Inter', var(--bs-font-sans-serif);
        }
        pre, code {
            font-family: 'Fira Code', monospace;
            background-color: var(--bs-gray-100);
            padding: 0.2rem 0.4rem;
            border-radius: 0.2rem;
            font-size: 0.875em;
        }
        pre code {
            padding: 0;
            background-color: transparent;
        }
        .hero-section {
            background-color: var(--bs-primary);
            color: white;
            padding: 4rem 0;
            margin-bottom: 2rem;
        }
        .content h2 {
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        .content h3 {
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        .content p {
            margin-bottom: 1.25rem;
            line-height: 1.7;
        }
        .content ul, .content ol {
            margin-bottom: 1.25rem;
        }
        .content blockquote {
            border-left: 4px solid var(--bs-primary);
            padding-left: 1rem;
            margin-left: 0;
            color: var(--bs-gray-700);
        }
        .tool-card {
            transition: transform 0.2s;
            height: 100%;
        }
        .tool-card:hover {
            transform: translateY(-5px);
        }
        .guide-card {
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .guide-card:hover {
            transform: translateY(-5px);
        }
        .feature-card {
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s;
            height: 100%;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
        .home-hero {
            background: linear-gradient(135deg, var(--bs-primary) 0%, #2563eb 100%);
            padding: 6rem 0;
            margin-bottom: 4rem;
        }
        .home-hero h1 {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
        }
        .home-hero p {
            font-size: 1.25rem;
            opacity: 0.9;
        }
    </style>
`;

const NAVBAR_TEMPLATE = `
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
`;

const FOOTER_TEMPLATE = `
    <footer class="bg-white py-5 mt-5">
        <div class="container">
            <div class="row justify-content-center text-center">
                <div class="col-md-8">
                    <div class="d-flex flex-column flex-md-row justify-content-center gap-4 mb-4">
                        <a href="/" class="text-muted text-decoration-none">Home</a>
                        <a href="/guides" class="text-muted text-decoration-none">Guides</a>
                        <a href="/free-tools" class="text-muted text-decoration-none">Tools</a>
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
`;

function convertPage(filePath, type) {
    const html = fs.readFileSync(filePath, 'utf8');
    const $ = cheerio.load(html);

    // Store original content
    const title = $('title').text();
    const description = $('meta[name="description"]').attr('content');
    let mainContent = type === 'tool' ? $('.tool-content').html() : 
                     type === 'guide' ? $('.guide-content').html() : 
                     $('.content').html();
    
    // If no specific content class found, try getting the main content
    if (!mainContent) {
        mainContent = $('main').html() || $('body').html();
    }

    // Determine breadcrumb path
    const isIndex = path.basename(filePath) === 'index.html';
    const fileName = path.basename(filePath, '.html');
    
    let breadcrumbTitle = isIndex ? 
        (type === 'tool' ? 'Free Tools' : 
         type === 'guide' ? 'LLM Optimization Guides' : 
         title.split(' - ')[0]) :
        title.split(' - ')[0];

    // Create new document structure
    const newHtml = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <meta name="description" content="${description || ''}">
    ${HEAD_TEMPLATE}
    ${STYLE_TEMPLATE}
</head>
<body>
    ${NAVBAR_TEMPLATE}

    <!-- Hero Section -->
    <div class="hero-section">
        <div class="container">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb mb-4">
                    <li class="breadcrumb-item"><a href="/" class="text-white">Home</a></li>
                    ${type === 'tool' ? 
                        `<li class="breadcrumb-item ${isIndex ? 'active text-white' : ''}"><a href="/free-tools" class="text-white">Free Tools</a></li>` :
                     type === 'guide' ? 
                        `<li class="breadcrumb-item ${isIndex ? 'active text-white' : ''}"><a href="/guides/llm-optimization" class="text-white">LLM Optimization</a></li>` :
                        ''
                    }
                    ${!isIndex ? `<li class="breadcrumb-item active text-white" aria-current="page">${breadcrumbTitle}</li>` : ''}
                </ol>
            </nav>
            <h1 class="display-4 mb-3">${breadcrumbTitle}</h1>
        </div>
    </div>

    <!-- Main Content -->
    <main class="container py-5">
        <div class="row justify-content-center">
            <div class="col-lg-10">
                <div class="content">
                    ${mainContent || ''}
                </div>
            </div>
        </div>
    </main>

    ${FOOTER_TEMPLATE}
</body>
</html>`;

    // Write the new file
    fs.writeFileSync(filePath, newHtml);
    console.log(`Converted ${path.basename(filePath)}`);
}

function convertHomePage(filePath) {
    const html = fs.readFileSync(filePath, 'utf8');
    const $ = cheerio.load(html);

    // Store original content
    const title = $('title').text();
    const description = $('meta[name="description"]').attr('content');
    const mainContent = $('.content').html() || $('main').html() || $('body').html();

    // Create new document structure with special home page layout
    const newHtml = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <meta name="description" content="${description || ''}">
    ${HEAD_TEMPLATE}
    ${STYLE_TEMPLATE}
</head>
<body>
    ${NAVBAR_TEMPLATE}

    <!-- Home Hero Section -->
    <div class="home-hero text-white">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-8 mx-auto text-center">
                    <h1>LLM Logs</h1>
                    <p class="lead mb-4">Your guide to optimizing content for Large Language Models</p>
                    <div class="d-flex justify-content-center gap-3">
                        <a href="/start-here.html" class="btn btn-light btn-lg px-4">Get Started</a>
                        <a href="/guides/llm-optimization" class="btn btn-outline-light btn-lg px-4">View Guides</a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <main class="container py-5">
        <div class="content">
            ${mainContent || ''}
        </div>
    </main>

    ${FOOTER_TEMPLATE}
</body>
</html>`;

    // Write the new file
    fs.writeFileSync(filePath, newHtml);
    console.log(`Converted home page`);
}

// Convert all HTML files in both directories
function convertDirectory(dir, type) {
    if (!fs.existsSync(dir)) {
        console.log(`Directory not found: ${dir}`);
        return;
    }

    const files = fs.readdirSync(dir)
        .filter(file => file.endsWith('.html'));

    files.forEach(file => {
        const filePath = path.join(dir, file);
        if (file === 'index.html' && dir === ROOT_DIR) {
            convertHomePage(filePath);
        } else {
            convertPage(filePath, type);
        }
    });
}

// Convert root directory files
console.log('Converting root files...');
const rootFiles = fs.readdirSync(ROOT_DIR)
    .filter(file => file.endsWith('.html') && !EXCLUDE_FILES.includes(file));

rootFiles.forEach(file => {
    const filePath = path.join(ROOT_DIR, file);
    convertPage(filePath, 'page');
});

// Convert tools and guides
console.log('\nConverting tools...');
convertDirectory(TOOLS_DIR, 'tool');

console.log('\nConverting guides...');
convertDirectory(GUIDES_DIR, 'guide'); 