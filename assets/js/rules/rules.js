// Rules data store
const rulesData = {
    nextjs: [
        // Your provided rules data here
    ]
};

// Function to download rule content as .mdc file
function downloadRuleAsMDC(rule) {
    const content = rule.content;
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${rule.slug}.mdc`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// Function to create a rule card element
function createRuleCard(rule) {
    const card = document.createElement('div');
    card.className = 'rule-card';
    card.onclick = () => window.location.href = `/rules/${rule.slug}-full.html`;

    card.innerHTML = `
        <div class="rule-card-header">
            <h2>${rule.title}</h2>
            <div class="rule-tags">
                ${rule.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                ${rule.libs?.map(lib => `<span class="tag lib-tag">${lib}</span>`).join('')}
            </div>
        </div>
        <div class="rule-card-content">
            <p>${rule.content.split('\n')[0]}</p>
        </div>
        <div class="rule-author">
            <img src="${rule.author.avatar}" alt="${rule.author.name}" class="author-avatar">
            <a href="${rule.author.url}" class="author-name" target="_blank" rel="noopener">${rule.author.name}</a>
        </div>
        <a href="#" class="download-button" onclick="event.stopPropagation(); downloadRuleAsMDC(${JSON.stringify(rule)})">
            Download .mdc
        </a>
    `;

    return card;
}

// Function to initialize rules grid
function initRulesGrid() {
    const grid = document.querySelector('.rules-grid');
    if (!grid) return;

    const rules = rulesData.nextjs;
    rules.forEach(rule => {
        grid.appendChild(createRuleCard(rule));
    });
}

// Rules processing script
class RuleProcessor {
    constructor() {
        this.init();
    }

    init() {
        this.processRules();
    }

    async processRules() {
        try {
            const response = await fetch('/assets/data/rules.json');
            const rules = await response.json();
            
            if (window.location.pathname.includes('-full.html')) {
                this.renderFullPage(rules);
            } else {
                this.renderCardView(rules);
            }
        } catch (error) {
            console.error('Error processing rules:', error);
        }
    }

    renderFullPage(rules) {
        const slug = window.location.pathname.split('/').pop().replace('-full.html', '');
        const rule = rules.find(r => this.slugify(r.title) === slug);
        
        if (!rule) return;

        // Update meta information
        document.title = `${rule.title} - LLM Logs Rules`;
        document.querySelector('meta[name="description"]').content = rule.content.description;

        // Update hero section
        document.querySelector('.hero-section h1').textContent = rule.title;
        
        // Process tags
        const tagsContainer = document.querySelector('.rule-tags');
        tagsContainer.innerHTML = this.processRuleTags(rule.tags, rule.libTags);

        // Update author information
        const authorContainer = document.querySelector('.rule-author');
        authorContainer.querySelector('img').src = rule.author.avatar;
        authorContainer.querySelector('img').alt = rule.author.name;
        const authorLink = authorContainer.querySelector('a');
        authorLink.href = rule.author.link;
        authorLink.textContent = rule.author.name;

        // Process content
        const contentContainer = document.querySelector('.rule-content');
        contentContainer.innerHTML = this.processContent(rule.content);
    }

    renderCardView(rules) {
        const container = document.querySelector('.rules-container');
        const template = document.querySelector('#rule-card-template').innerHTML;
        
        const cardsHtml = rules.map(rule => {
            const cardHtml = template
                .replace('[Rule Title]', rule.title)
                .replace('[Rule Description]', rule.content.description)
                .replace('[Author Avatar]', rule.author.avatar)
                .replace('[Author Name]', rule.author.name)
                .replace('[Author Link]', rule.author.link)
                .replace('[Rule Full Page]', `/rules/${this.slugify(rule.title)}-full.html`);

            const card = document.createElement('div');
            card.innerHTML = cardHtml;
            
            // Process tags
            const tagsContainer = card.querySelector('.rule-tags');
            tagsContainer.innerHTML = this.processRuleTags(rule.tags, rule.libTags);

            return card.innerHTML;
        }).join('');

        container.innerHTML = cardsHtml;
    }

    processRuleTags(tags = [], libTags = []) {
        const tagElements = tags.map(tag => 
            `<span class="tag">${tag}</span>`
        );
        
        const libTagElements = libTags.map(tag => 
            `<span class="tag lib-tag">${tag}</span>`
        );
        
        return [...tagElements, ...libTagElements].join('');
    }

    processContent(content) {
        const sections = content.sections.map(section => {
            const items = section.items.map(item => `<li>${item}</li>`).join('');
            const codeBlocks = section.code ? section.code.map(this.processCodeBlock).join('') : '';
            
            return `
                <section>
                    <h2>${section.title}</h2>
                    <ul class="list-unstyled">${items}</ul>
                    ${codeBlocks}
                </section>
            `;
        }).join('');

        return `
            <p class="lead mb-4">${content.description}</p>
            ${sections}
        `;
    }

    processCodeBlock(code) {
        return `
            <div class="code-block">
                <div class="filename">${code.filename}</div>
                <pre><code class="language-typescript">${this.escapeHtml(code.content)}</code></pre>
            </div>
        `;
    }

    slugify(text) {
        return text.toLowerCase()
            .replace(/[^\w ]+/g, '')
            .replace(/ +/g, '-');
    }

    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new RuleProcessor();
}); 