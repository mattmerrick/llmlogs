document.addEventListener('DOMContentLoaded', () => {
    const generateButton = document.getElementById('generateRules');
    const rulesPreview = document.querySelector('.rules-preview');
    const rulesPreviewCode = document.getElementById('rulesPreview');
    const downloadButton = document.querySelector('.download-button');
    const copyButton = document.querySelector('.copy-button');

    // Store rule templates
    const ruleTemplates = {
        nextjs: '# Next.js rules\n\n- Use the App Router structure with `page.tsx` files in route directories.\n- Client components must be explicitly marked with `\'use client\'` at the top of the file.\n- Use kebab-case for directory names and PascalCase for component files.\n- Prefer named exports for components.',
        react: '# React rules\n\n- Use functional components with hooks instead of class components\n- Use custom hooks for reusable logic\n- Use the Context API for state management when needed\n- Use proper prop validation with PropTypes\n- Use React.memo for performance optimization when necessary',
        express: '# Express.js rules\n\n- Use proper middleware order: body parsers, custom middleware, routes, error handlers\n- Organize routes using Express Router for modular code structure\n- Use async/await with proper error handling\n- Create a centralized error handler middleware',
        postgresql: '# PostgreSQL rules\n\n- Use appropriate data types for columns\n- Create indexes for frequently queried columns\n- Use foreign keys for referential integrity\n- Write optimized queries using EXPLAIN ANALYZE\n- Implement proper backup strategies',
        testing: '# Testing Guidelines\n\n- Use Vitest for testing\n- Colocate test files next to source files\n- Mock external dependencies appropriately\n- Write meaningful test descriptions\n- Follow AAA pattern (Arrange, Act, Assert)',
        tailwind: '# Tailwind CSS rules\n\n- Use responsive prefixes for mobile-first design\n- Utilize state variants for interactive elements\n- Create consistent spacing using the spacing scale\n- Extract common patterns into components',
    };

    generateButton.addEventListener('click', () => {
        const selectedFrameworks = {
            frontend: document.querySelector('input[name="frontend"]:checked')?.value,
            backend: document.querySelector('input[name="backend"]:checked')?.value,
            database: document.querySelector('input[name="database"]:checked')?.value,
            features: Array.from(document.querySelectorAll('input[name="features"]:checked')).map(cb => cb.value)
        };

        // Generate combined rules
        let combinedRules = '# Combined Cursor Rules\n\n';
        
        if (selectedFrameworks.frontend && ruleTemplates[selectedFrameworks.frontend]) {
            combinedRules += ruleTemplates[selectedFrameworks.frontend] + '\n\n';
        }
        
        if (selectedFrameworks.backend && ruleTemplates[selectedFrameworks.backend]) {
            combinedRules += ruleTemplates[selectedFrameworks.backend] + '\n\n';
        }
        
        if (selectedFrameworks.database && ruleTemplates[selectedFrameworks.database]) {
            combinedRules += ruleTemplates[selectedFrameworks.database] + '\n\n';
        }

        selectedFrameworks.features.forEach(feature => {
            if (ruleTemplates[feature]) {
                combinedRules += ruleTemplates[feature] + '\n\n';
            }
        });

        // Show preview
        rulesPreviewCode.textContent = combinedRules;
        rulesPreview.style.display = 'block';
    });

    // Handle download
    downloadButton.addEventListener('click', () => {
        const blob = new Blob([rulesPreviewCode.textContent], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'cursor-rules.mdc';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    });

    // Handle copy to clipboard
    copyButton.addEventListener('click', async () => {
        try {
            await navigator.clipboard.writeText(rulesPreviewCode.textContent);
            copyButton.textContent = 'Copied!';
            setTimeout(() => {
                copyButton.textContent = 'Copy to Clipboard';
            }, 2000);
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
    });
}); 