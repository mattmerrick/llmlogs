// Share functionality
function initShareSection() {
    const copyUrlButton = document.getElementById('copyUrlButton');
    const copyCitationButton = document.getElementById('copyCitationButton');
    const shareUrl = document.getElementById('shareUrl');
    const citationText = document.getElementById('citationText');

    if (!copyUrlButton || !copyCitationButton || !shareUrl || !citationText) {
        console.warn('Share section elements not found');
        return;
    }

    function copyToClipboard(text, button) {
        navigator.clipboard.writeText(text).then(() => {
            const originalText = button.querySelector('.copy-text').textContent;
            button.querySelector('.copy-text').textContent = 'Copied!';
            button.classList.add('copied');
            
            setTimeout(() => {
                button.querySelector('.copy-text').textContent = originalText;
                button.classList.remove('copied');
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy text: ', err);
        });
    }

    copyUrlButton.addEventListener('click', () => copyToClipboard(shareUrl.value, copyUrlButton));
    copyCitationButton.addEventListener('click', () => copyToClipboard(citationText.value, copyCitationButton));
}

// Initialize share section when DOM is loaded
document.addEventListener('DOMContentLoaded', initShareSection); 