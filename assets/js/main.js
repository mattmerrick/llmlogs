// Share button functionality
document.addEventListener('DOMContentLoaded', function() {
    const shareButtons = document.querySelectorAll('.share-button');
    
    shareButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const url = this.dataset.url;
            const type = this.dataset.type;
            const originalText = this.textContent;
            
            try {
                await navigator.clipboard.writeText(url);
                this.classList.add('copied');
                this.textContent = 'Copied!';
                
                setTimeout(() => {
                    this.classList.remove('copied');
                    this.textContent = originalText;
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
                // Fallback for older browsers
                const textarea = document.createElement('textarea');
                textarea.value = url;
                document.body.appendChild(textarea);
                textarea.select();
                try {
                    document.execCommand('copy');
                    this.classList.add('copied');
                    this.textContent = 'Copied!';
                    
                    setTimeout(() => {
                        this.classList.remove('copied');
                        this.textContent = originalText;
                    }, 2000);
                } catch (err) {
                    console.error('Failed to copy with fallback:', err);
                }
                document.body.removeChild(textarea);
            }
        });
    });
}); 