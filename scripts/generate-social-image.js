const { createCanvas, registerFont } = require('canvas');
const fs = require('fs');
const path = require('path');

// Configuration
const config = {
    width: 1200,
    height: 630,
    backgroundColor: '#0D6EFD', // Bootstrap primary blue
    fontColor: '#FFFFFF',
    fontFamily: 'Inter',
    fontSize: 60,
    padding: 60,
    lineHeight: 1.4
};

function wrapText(context, text, maxWidth) {
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

async function generateSocialImage(title, outputPath) {
    // Create canvas
    const canvas = createCanvas(config.width, config.height);
    const context = canvas.getContext('2d');

    // Set background
    context.fillStyle = config.backgroundColor;
    context.fillRect(0, 0, config.width, config.height);

    // Configure text
    context.fillStyle = config.fontColor;
    context.font = `bold ${config.fontSize}px ${config.fontFamily}`;
    context.textAlign = 'center';

    // Wrap and draw text
    const maxWidth = config.width - (config.padding * 2);
    const lines = wrapText(context, title, maxWidth);
    const totalHeight = lines.length * config.fontSize * config.lineHeight;
    const startY = (config.height - totalHeight) / 2;

    lines.forEach((line, index) => {
        const y = startY + (index * config.fontSize * config.lineHeight);
        context.fillText(line, config.width / 2, y);
    });

    // Add logo or watermark
    context.font = `24px ${config.fontFamily}`;
    context.fillText('LLM Logs', config.width / 2, config.height - 40);

    // Save the image
    const buffer = canvas.toBuffer('image/png');
    fs.writeFileSync(outputPath, buffer);
}

// Export the function
module.exports = generateSocialImage;

// If running directly, generate a test image
if (require.main === module) {
    const title = process.argv[2] || "Test Social Image";
    const outputPath = process.argv[3] || "test-social-image.png";
    generateSocialImage(title, outputPath)
        .then(() => console.log(`Generated image: ${outputPath}`))
        .catch(console.error);
} 