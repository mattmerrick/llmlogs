// Social Image Generator Utility
class SocialImageGenerator {
    constructor(config = {}) {
        this.config = {
            width: 1200,
            height: 630,
            backgroundColor: '#0D6EFD',
            fontColor: '#FFFFFF',
            fontFamily: 'Arial, sans-serif',
            fontSize: 60,
            padding: 60,
            lineHeight: 1.4,
            ...config
        };
    }

    async generateAndSetMetaTags() {
        // Get the page title
        const title = document.title.split('-')[0].trim();
        
        // Create canvas
        const canvas = document.createElement('canvas');
        canvas.width = this.config.width;
        canvas.height = this.config.height;
        const context = canvas.getContext('2d');

        // Set background
        context.fillStyle = this.config.backgroundColor;
        context.fillRect(0, 0, this.config.width, this.config.height);

        // Configure text
        context.fillStyle = this.config.fontColor;
        context.font = `bold ${this.config.fontSize}px ${this.config.fontFamily}`;
        context.textAlign = 'center';

        // Wrap and draw text
        const maxWidth = this.config.width - (this.config.padding * 2);
        const lines = this._wrapText(context, title, maxWidth);
        const totalHeight = lines.length * this.config.fontSize * this.config.lineHeight;
        const startY = (this.config.height - totalHeight) / 2;

        lines.forEach((line, index) => {
            const y = startY + (index * this.config.fontSize * this.config.lineHeight);
            context.fillText(line, this.config.width / 2, y);
        });

        // Add logo
        context.font = `24px ${this.config.fontFamily}`;
        context.fillText('LLM Logs', this.config.width / 2, this.config.height - 40);

        // Convert to data URL
        const imageUrl = canvas.toDataURL('image/png');

        // Set meta tags
        this._setMetaTags(imageUrl);
    }

    _wrapText(context, text, maxWidth) {
        const words = text.split(' ');
        const lines = [];
        let currentLine = words[0];

        for (let i = 1; i < words.length; i++) {
            const word = words[i];
            const width = context.measureText(currentLine + " " + word).width;
            if (width < maxWidth) {
                currentLine += " " + word;
            } else {
                lines.push(currentLine);
                currentLine = word;
            }
        }
        lines.push(currentLine);
        return lines;
    }

    _setMetaTags(imageUrl) {
        // Function to create or update meta tag
        const setMetaTag = (property, content) => {
            let meta = document.querySelector(`meta[property="${property}"]`);
            if (!meta) {
                meta = document.createElement('meta');
                meta.setAttribute('property', property);
                document.head.appendChild(meta);
            }
            meta.setAttribute('content', content);
        };

        // Set Open Graph image
        setMetaTag('og:image', imageUrl);
        setMetaTag('og:image:width', this.config.width.toString());
        setMetaTag('og:image:height', this.config.height.toString());

        // Set Twitter Card image
        setMetaTag('twitter:image', imageUrl);
        setMetaTag('twitter:card', 'summary_large_image');
    }
}

// Auto-initialize when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const generator = new SocialImageGenerator();
    generator.generateAndSetMetaTags();
}); 