const fs = require('fs');
const path = require('path');

// Configuration
const TEMPLATE_PATH = path.join(__dirname, '..', 'rules', 'template.html');
const RULES_MD_DIR = path.join(__dirname, '..', 'rules-md');
const OUTPUT_DIR = path.join(__dirname, '..', 'rules');

// Technology metadata
const technologies = [
    { name: "TypeScript", count: 22, category: "languages", icon: "code-slash" },
    { name: "Python", count: 15, category: "languages", icon: "filetype-py" },
    { name: "Next.js", count: 12, category: "frameworks", icon: "box-arrow-up-right" },
    { name: "React", count: 12, category: "frameworks", icon: "box-arrow-up-right" },
    { name: "PHP", count: 8, category: "languages", icon: "filetype-php" },
    { name: "JavaScript", count: 5, category: "languages", icon: "filetype-js" },
    { name: "TailwindCSS", count: 5, category: "frameworks", icon: "palette" },
    { name: "Laravel", count: 5, category: "frameworks", icon: "box-arrow-up-right" },
    { name: "C#", count: 4, category: "languages", icon: "hash" },
    { name: "Game Development", count: 4, category: "platforms", icon: "controller" },
    { name: "Expo", count: 4, category: "frameworks", icon: "phone" },
    { name: "React Native", count: 4, category: "frameworks", icon: "phone" },
    { name: "Flutter", count: 4, category: "frameworks", icon: "phone" },
    { name: "Testing", count: 4, category: "tools", icon: "bug" },
    { name: "Vite", count: 4, category: "tools", icon: "lightning" },
    { name: "Supabase", count: 4, category: "platforms", icon: "database" },
    { name: "Rust", count: 3, category: "languages", icon: "gear" },
    { name: "Web Development", count: 3, category: "platforms", icon: "globe" },
    { name: "API", count: 3, category: "tools", icon: "box-arrow-up-right" },
    { name: "Meta-Prompt", count: 3, category: "tools", icon: "chat" },
    { name: "Node.js", count: 3, category: "platforms", icon: "server" },
    { name: "SvelteKit", count: 3, category: "frameworks", icon: "box-arrow-up-right" },
    { name: "SwiftUI", count: 3, category: "frameworks", icon: "phone" },
    { name: "Swift", count: 3, category: "languages", icon: "apple" },
    { name: "WordPress", count: 3, category: "platforms", icon: "wordpress" },
    // Add all other technologies here...
];

// Ensure directories exist
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}
if (!fs.existsSync(RULES_MD_DIR)) {
    fs.mkdirSync(RULES_MD_DIR, { recursive: true });
}

// Read template
const template = fs.readFileSync(TEMPLATE_PATH, 'utf8');

// Generate pages for each technology
technologies.forEach(tech => {
    try {
        // Read markdown content
        const mdPath = path.join(RULES_MD_DIR, `${tech.name.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.md`);
        let markdownContent = '';
        
        try {
            markdownContent = fs.readFileSync(mdPath, 'utf8');
        } catch (err) {
            console.log(`No markdown file found for ${tech.name}, creating placeholder content`);
            markdownContent = `# ${tech.name} Development Rules and Guidelines\n\n*Content coming soon...*`;
            
            // Create markdown file with placeholder content
            fs.writeFileSync(mdPath, markdownContent);
        }

        // Generate HTML content
        let htmlContent = template
            .replace(/{{TECH_NAME}}/g, tech.name)
            .replace(/{{TECH_ICON}}/g, tech.icon)
            .replace(/{{TECH_CATEGORY}}/g, tech.category)
            .replace(/{{RULE_COUNT}}/g, tech.count)
            .replace(/{{MARKDOWN_CONTENT}}/g, markdownContent);

        // Write HTML file
        const outputPath = path.join(OUTPUT_DIR, `${tech.name.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.html`);
        fs.writeFileSync(outputPath, htmlContent);
        
        console.log(`Generated page for ${tech.name}`);
    } catch (err) {
        console.error(`Error generating page for ${tech.name}:`, err);
    }
});

console.log('Page generation complete!'); 