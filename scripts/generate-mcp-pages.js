const fs = require('fs');
const path = require('path');
const https = require('https');

// Configuration
const MCP_TEMPLATE_PATH = path.join(__dirname, '..', 'assets', 'js', 'mcp', 'mcp-template.html');
const MCP_DATA_PATH = path.join(__dirname, '..', 'mcpmain.json');
const MCP_OUTPUT_DIR = path.join(__dirname, '..', 'mcp');

// Ensure MCP directory exists
if (!fs.existsSync(MCP_OUTPUT_DIR)) {
    fs.mkdirSync(MCP_OUTPUT_DIR, { recursive: true });
}

// Function to fetch README content
async function fetchReadme(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => resolve(data));
            res.on('error', (error) => reject(error));
        }).on('error', (error) => reject(error));
    });
}

// Function to get clean filename
function getCleanFilename(name) {
    // Remove username/org from the repository name (everything before the /)
    const repoName = name.split('/')[1] || name;
    return repoName.toLowerCase()
        .replace(/[^\w-]+/g, '-') // Replace non-word chars (except -) with -
        .replace(/-+/g, '-')      // Replace multiple - with single -
        .replace(/^-+|-+$/g, ''); // Remove leading/trailing -
}

// Read MCP data and template
const mcpData = JSON.parse(fs.readFileSync(MCP_DATA_PATH, 'utf8'));
const template = fs.readFileSync(MCP_TEMPLATE_PATH, 'utf8');

// Generate pages for each MCP repository
async function generatePages() {
    for (const mcp of mcpData.repositories) {
        try {
            // Fetch README content
            let readmeContent = '';
            try {
                readmeContent = await fetchReadme(mcp.readme_url);
                console.log(`Fetched README for ${mcp.name}`);
            } catch (error) {
                console.warn(`Failed to fetch README for ${mcp.name}:`, error.message);
                readmeContent = '# README Not Available\nThe README content could not be loaded.';
            }

            let pageContent = template
                .replace(/\[MCP Title\]/g, mcp.title)
                .replace(/\[MCP Description\]/g, mcp.description)
                .replace(/\[Stars\]/g, mcp.stars)
                .replace(/\[Watchers\]/g, mcp.watchers)
                .replace(/\[GitHub URL\]/g, mcp.github_url)
                .replace('<!-- README Content Placeholder -->', readmeContent);

            const filename = getCleanFilename(mcp.name);
            const outputPath = path.join(MCP_OUTPUT_DIR, `${filename}.html`);
            fs.writeFileSync(outputPath, pageContent);
            console.log(`Generated page for ${mcp.title} at ${outputPath}`);
        } catch (error) {
            console.error(`Error generating page for ${mcp.title}:`, error);
        }
    }
}

// Run the page generation
generatePages().then(() => {
    console.log('\nMCP page generation complete!');
}).catch(error => {
    console.error('Error during page generation:', error);
}); 