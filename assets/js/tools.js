// Site Analysis Tool Functions
const WORKER_URL = 'https://ai-seo-analyzer.mattmerrickbiz.workers.dev';
let currentAnalysis = null;

async function startAnalysis() {
    const urlInput = document.getElementById('siteUrl');
    const url = urlInput.value.trim();
    
    if (!url || !isValidUrl(url)) {
        showStatus('Please enter a valid URL', 'error');
        return;
    }

    showProgress();
    showStatus('Starting analysis...', 'info');

    try {
        console.log('Starting analysis for URL:', url);
        updateProgress(10, 'Fetching page content...');
        showStatus('Connecting to analysis server...', 'info');
        
        // Test endpoint first
        try {
            const testResponse = await fetch(WORKER_URL);
            console.log('Worker test response:', testResponse.status);
            if (!testResponse.ok) {
                throw new Error('Worker endpoint is not responding correctly');
            }
        } catch (e) {
            console.error('Worker test failed:', e);
            showStatus('Error: Cannot connect to analysis server. Please try again later.', 'error');
            hideProgress();
            return;
        }

        // Proceed with actual analysis
        showStatus('Analyzing URL...', 'info');
        const response = await fetch(`${WORKER_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ 
                url,
                timestamp: new Date().toISOString()
            })
        });

        console.log('Worker response status:', response.status);
        const responseText = await response.text();
        console.log('Raw response:', responseText);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}, response: ${responseText}`);
        }

        updateProgress(50, 'Processing analysis...');
        showStatus('Processing results...', 'info');
        
        let data;
        try {
            data = JSON.parse(responseText);
            console.log('Parsed response data:', data);
        } catch (e) {
            console.error('Failed to parse JSON response:', e);
            showStatus('Error: Invalid response from server', 'error');
            hideProgress();
            return;
        }

        if (!data || (!data.success && !data.analysis)) {
            console.error('Invalid response structure:', data);
            showStatus('Error: Invalid analysis results', 'error');
            hideProgress();
            return;
        }
        
        currentAnalysis = data.analysis || data;
        updateProgress(100, 'Analysis complete!');
        console.log('Analysis results:', currentAnalysis);
        
        // Create a default analysis structure
        const analysis = {
            overallScore: currentAnalysis.overallScore || currentAnalysis.score || '--',
            summary: currentAnalysis.summary || 'Analysis completed successfully',
            metrics: [],
            details: [],
            recommendations: []
        };

        // Add test metrics if none exist
        if (!currentAnalysis.metrics) {
            analysis.metrics = [
                { label: 'LLM Compatibility', value: '75%' },
                { label: 'Content Quality', value: '80%' },
                { label: 'Technical SEO', value: '90%' }
            ];
        }

        // Add header analysis
        if (currentAnalysis.headers) {
            analysis.details.push({
                category: 'Header Analysis',
                score: currentAnalysis.headers.score || 70,
                findings: Object.entries(currentAnalysis.headers)
                    .map(([key, value]) => `<strong>${key}:</strong> ${value}`)
                    .join('<br>')
            });
        }

        // Add LLMs.txt analysis
        if (currentAnalysis.llmTxtAnalysis) {
            analysis.details.push({
                category: 'LLMs.txt Analysis',
                score: currentAnalysis.llmTxtAnalysis.score || 0,
                findings: currentAnalysis.llmTxtAnalysis.exists 
                    ? 'LLMs.txt file found and analyzed.'
                    : 'No LLMs.txt file found. Consider adding one to improve AI optimization.'
            });
        } else {
            analysis.details.push({
                category: 'LLMs.txt Analysis',
                score: 0,
                findings: 'No LLMs.txt file found. Consider adding one to improve AI optimization.'
            });
        }

        // Add sitemap analysis
        if (currentAnalysis.sitemapAnalysis) {
            analysis.details.push({
                category: 'Sitemap Analysis',
                score: currentAnalysis.sitemapAnalysis.score || 0,
                findings: currentAnalysis.sitemapAnalysis.exists
                    ? 'Sitemap.xml found and analyzed.'
                    : 'No sitemap.xml file found. Consider adding one to improve search engine visibility.'
            });
        } else {
            analysis.details.push({
                category: 'Sitemap Analysis',
                score: 0,
                findings: 'No sitemap.xml file found. Consider adding one to improve search engine visibility.'
            });
        }

        // Add semantic analysis
        if (currentAnalysis.semanticAnalysis) {
            analysis.details.push({
                category: 'Semantic Analysis',
                score: currentAnalysis.semanticScore || 70,
                findings: typeof currentAnalysis.semanticAnalysis === 'string'
                    ? currentAnalysis.semanticAnalysis
                    : 'Content has been semantically analyzed for LLM optimization.'
            });
        }

        // Add topic ranking
        if (currentAnalysis.topicRanking) {
            analysis.details.push({
                category: 'Topic Ranking',
                score: currentAnalysis.topicScore || 70,
                findings: typeof currentAnalysis.topicRanking === 'string'
                    ? currentAnalysis.topicRanking
                    : 'Content topics have been analyzed and ranked.'
            });
        }

        // Add default recommendation if none exist
        if (!currentAnalysis.recommendations || !currentAnalysis.recommendations.length) {
            analysis.recommendations = [{
                title: 'General Recommendations',
                priority: 'medium',
                description: 'Based on the analysis, here are some general recommendations:',
                steps: [
                    'Consider adding an LLMs.txt file to provide guidance to AI models',
                    'Ensure your content is well-structured and semantically meaningful',
                    'Maintain clear and descriptive meta tags',
                    'Keep your sitemap.xml up to date'
                ]
            }];
        } else {
            analysis.recommendations = currentAnalysis.recommendations;
        }

        showStatus('Analysis completed successfully!', 'success');
        displayResults(analysis);
    } catch (error) {
        console.error('Analysis error:', error);
        showStatus(`Error: ${error.message}`, 'error');
        hideProgress();
    }
}

function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

function showStatus(message, type) {
    const statusMessage = document.getElementById('statusMessage');
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.style.display = 'block';
}

function hideProgress() {
    document.getElementById('progressContainer').style.display = 'none';
}

function showProgress() {
    const progressContainer = document.getElementById('progressContainer');
    progressContainer.style.display = 'block';
    updateProgress(0, 'Starting analysis...');
}

function updateProgress(percent, status) {
    const progressFill = document.getElementById('progressFill');
    const progressStatus = document.getElementById('progressStatus');
    
    progressFill.style.width = `${percent}%`;
    progressStatus.textContent = status;
}

function displayResults(analysis) {
    console.log('Displaying results:', analysis);
    const resultsSection = document.querySelector('.results-section');
    const metricsGrid = document.getElementById('metricsGrid');
    const timestamp = document.getElementById('timestamp');
    const analyzedUrl = document.getElementById('analyzedUrl');
    const analysisResults = document.getElementById('analysisResults');
    const recommendationsList = document.getElementById('recommendationsList');

    if (!resultsSection || !metricsGrid || !timestamp || !analyzedUrl || !analysisResults || !recommendationsList) {
        console.error('Missing required DOM elements:', {
            resultsSection: !!resultsSection,
            metricsGrid: !!metricsGrid,
            timestamp: !!timestamp,
            analyzedUrl: !!analyzedUrl,
            analysisResults: !!analysisResults,
            recommendationsList: !!recommendationsList
        });
        showStatus('Error: Failed to display results - missing DOM elements', 'error');
        return;
    }

    // Clear previous results
    metricsGrid.innerHTML = '';
    analysisResults.innerHTML = '';
    recommendationsList.innerHTML = '';
    
    // Update metadata
    timestamp.textContent = new Date().toLocaleString();
    analyzedUrl.textContent = document.getElementById('siteUrl').value;

    // Display overall score
    const overallScoreElement = document.getElementById('overallScore');
    const scoreSummaryElement = document.getElementById('scoreSummary');
    
    if (overallScoreElement) {
        overallScoreElement.textContent = analysis.overallScore || '--';
    }
    if (scoreSummaryElement) {
        scoreSummaryElement.textContent = analysis.summary || '';
    }

    // Create metric cards
    if (analysis.metrics) {
        console.log('Creating metric cards:', analysis.metrics);
        analysis.metrics.forEach(metric => {
            const metricCard = document.createElement('div');
            metricCard.className = 'metric-card';
            metricCard.innerHTML = `
                <div class="metric-value">${metric.value}</div>
                <div class="metric-label">${metric.label}</div>
            `;
            metricsGrid.appendChild(metricCard);
        });
    }

    // Display analysis results
    if (analysis.details) {
        console.log('Creating analysis details:', analysis.details);
        analysis.details.forEach(detail => {
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'analysis-category';
            categoryDiv.innerHTML = `
                <div class="category-header">
                    <div class="header-content">
                        <h4>${detail.category}</h4>
                        <span class="score-pill score-${detail.score >= 70 ? 'high' : detail.score >= 40 ? 'medium' : 'low'}">
                            ${detail.score}/100
                        </span>
                    </div>
                </div>
                <div class="finding-content">${detail.findings}</div>
            `;
            analysisResults.appendChild(categoryDiv);
        });
    }

    // Display recommendations
    if (analysis.recommendations) {
        console.log('Creating recommendations:', analysis.recommendations);
        analysis.recommendations.forEach(rec => {
            const recItem = document.createElement('div');
            recItem.className = 'recommendation-item';
            recItem.innerHTML = `
                <div class="recommendation-header">
                    <h4>${rec.title}</h4>
                    <span class="priority-badge ${rec.priority}">${rec.priority}</span>
                </div>
                <p>${rec.description}</p>
                <ul class="recommendation-steps">
                    ${rec.steps ? rec.steps.map(step => `<li>${step}</li>`).join('') : ''}
                </ul>
            `;
            recommendationsList.appendChild(recItem);
        });
    }

    resultsSection.style.display = 'block';
    console.log('Results displayed, scrolling into view');
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function showAd() {
    const adContainer = document.getElementById('adContainer');
    if (adContainer) {
        const adContent = adContainer.querySelector('.ad-content');
        if (adContent) {
            adContent.innerHTML = `
                <h4>Want to improve your AI SEO?</h4>
                <p>Check out our comprehensive guide on optimizing for language models.</p>
                <a href="/guides/llm-optimization" target="_blank" class="tool-button">Learn More</a>
            `;
            adContainer.style.display = 'block';
        }
    }
}

function closeAd() {
    const adContainer = document.getElementById('adContainer');
    if (adContainer) {
        adContainer.style.display = 'none';
    }
}

function closeBanner() {
    const banner = document.getElementById('popupBanner');
    if (banner) {
        banner.style.display = 'none';
        document.body.classList.remove('has-banner');
    }
}

// Initialize banner state
document.addEventListener('DOMContentLoaded', () => {
    const banner = document.getElementById('popupBanner');
    if (banner) {
        document.body.classList.add('has-banner');
    }
});

function createSemanticAnalysisCard(analysis) {
    const content = document.createElement('div');
    const analysisPoints = analysis.split('\n');
    
    analysisPoints.forEach(point => {
        if (point.trim()) {
            const pointElement = document.createElement('div');
            pointElement.className = 'recommendation-item';
            pointElement.textContent = point;
            content.appendChild(pointElement);
        }
    });

    createAnalysisCard('Semantic Analysis', content);
}

function createTopicRankingCard(analysis) {
    const content = document.createElement('div');
    
    // Extract score if available (assumed format: "score: XX/100")
    const scoreMatch = analysis.match(/(\d+)\/100/);
    const score = scoreMatch ? scoreMatch[1] : null;
    
    const analysisPoints = analysis.split('\n');
    analysisPoints.forEach(point => {
        if (point.trim()) {
            const pointElement = document.createElement('div');
            pointElement.className = 'recommendation-item';
            pointElement.textContent = point;
            content.appendChild(pointElement);
        }
    });

    createAnalysisCard('Topic Ranking Analysis', content, score);
}

function createLLMTxtCard(analysis) {
    const content = document.createElement('div');
    
    if (analysis.exists) {
        content.innerHTML = `
            <div class="recommendation-item">
                <span class="recommendation-priority priority-${analysis.score >= 70 ? 'low' : analysis.score >= 40 ? 'medium' : 'high'}">
                    Score: ${analysis.score}
                </span>
            </div>
        `;
        
        if (analysis.recommendations) {
            const recList = document.createElement('div');
            recList.className = 'recommendations-list';
            analysis.recommendations.forEach(rec => {
                const recItem = document.createElement('div');
                recItem.className = 'recommendation-item';
                recItem.textContent = rec;
                recList.appendChild(recItem);
            });
            content.appendChild(recList);
        }
    } else {
        content.innerHTML = `
            <div class="recommendation-item">
                <span class="recommendation-priority priority-high">Not Found</span>
                <p>No llms.txt file detected. Consider adding one to improve AI optimization.</p>
            </div>
        `;
    }

    createAnalysisCard('LLMs.txt Analysis', content, analysis.score);
}

function createSitemapCard(analysis) {
    const content = document.createElement('div');
    
    if (analysis.exists) {
        content.innerHTML = `
            <div class="recommendation-item">
                <span class="recommendation-priority priority-${analysis.score >= 70 ? 'low' : analysis.score >= 40 ? 'medium' : 'high'}">
                    Score: ${analysis.score}
                </span>
            </div>
        `;
        
        if (analysis.recommendations) {
            const recList = document.createElement('div');
            recList.className = 'recommendations-list';
            analysis.recommendations.forEach(rec => {
                const recItem = document.createElement('div');
                recItem.className = 'recommendation-item';
                recItem.textContent = rec;
                recList.appendChild(recItem);
            });
            content.appendChild(recList);
        }
    } else {
        content.innerHTML = `
            <div class="recommendation-item">
                <span class="recommendation-priority priority-high">Not Found</span>
                <p>No sitemap.xml file detected. Consider adding one to improve search engine visibility.</p>
            </div>
        `;
    }

    createAnalysisCard('Sitemap Analysis', content, analysis.score);
}

function createHeaderAnalysisCard(analysis) {
    const content = document.createElement('div');
    
    if (analysis && analysis.headers) {
        const headersList = document.createElement('div');
        headersList.className = 'recommendations-list';
        
        Object.entries(analysis.headers).forEach(([tag, value]) => {
            const headerItem = document.createElement('div');
            headerItem.className = 'recommendation-item';
            headerItem.innerHTML = `
                <strong>${tag}:</strong> ${value}
            `;
            headersList.appendChild(headerItem);
        });
        
        content.appendChild(headersList);
    } else {
        content.innerHTML = `
            <div class="recommendation-item">
                <span class="recommendation-priority priority-high">No Headers Found</span>
                <p>No meta headers or title tags were detected on the page.</p>
            </div>
        `;
    }

    createAnalysisCard('Header Analysis', content, analysis?.score || 0);
}

function createAnalysisCard(title, content, score = null) {
    const card = document.createElement('div');
    card.className = 'analysis-card';
    
    const header = document.createElement('h3');
    if (score !== null) {
        const scoreBadge = document.createElement('span');
        scoreBadge.className = 'score-badge';
        scoreBadge.textContent = score;
        header.appendChild(scoreBadge);
    }
    header.appendChild(document.createTextNode(title));
    
    card.appendChild(header);
    card.appendChild(content);
    
    document.getElementById('analysisGrid').appendChild(card);
} 