// OpenAI API Configuration
const OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions';
const ALLOWED_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000', 'https://llmlogs.com']; // Add localhost

async function fetchPageContent(url) {
  try {
    const response = await fetch(url);
    const html = await response.text();
    return html;
  } catch (error) {
    console.error('Error fetching page:', error);
    return null;
  }
}

async function extractHeaderTags(html) {
  // Simple regex-based extraction since DOMParser isn't available in Workers
  const h1s = html.match(/<h1[^>]*>(.*?)<\/h1>/gi)?.map(h => h.replace(/<[^>]+>/g, '').trim()) || [];
  const h2s = html.match(/<h2[^>]*>(.*?)<\/h2>/gi)?.map(h => h.replace(/<[^>]+>/g, '').trim()) || [];
  const metaDescription = html.match(/<meta[^>]*name="description"[^>]*content="([^"]*)"[^>]*>/i)?.[1] || 
                         html.match(/<meta[^>]*content="([^"]*)"[^>]*name="description"[^>]*>/i)?.[1] || '';
  const title = html.match(/<title[^>]*>(.*?)<\/title>/i)?.[1] || '';

  return {
    h1: h1s,
    h2: h2s,
    metaDescription,
    title
  };
}

async function checkLLMTxtCompliance(url) {
  try {
    const llmTxtUrl = new URL('/llms.txt', url).href;
    const response = await fetch(llmTxtUrl);
    if (response.ok) {
      const text = await response.text();
      return analyzeLLMTxt(text);
    }
    return { exists: false, score: 0, recommendations: ['No llms.txt file found'] };
  } catch (error) {
    return { exists: false, score: 0, error: error.message };
  }
}

async function analyzeSitemap(url) {
  try {
    const sitemapUrl = new URL('/sitemap.xml', url).href;
    const response = await fetch(sitemapUrl);
    if (response.ok) {
      const text = await response.text();
      return analyzeSitemapStructure(text);
    }
    return { exists: false, score: 0, recommendations: ['No sitemap.xml found'] };
  } catch (error) {
    return { exists: false, score: 0, error: error.message };
  }
}

async function testSemanticRanking(content, env) {
  const prompt = `Analyze this content for semantic relevance and AI-friendliness:
${content}

Please evaluate:
1. Topic clarity
2. Information structure
3. Semantic richness
4. Citation potential
5. Knowledge graph integration`;

  const response = await fetch(OPENAI_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${env.OPENAI_API_KEY}`,
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'You are an AI expert specializing in content analysis and semantic search optimization.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.7,
    }),
  });

  if (!response.ok) {
    throw new Error(`OpenAI API error: ${response.status}`);
  }

  const result = await response.json();
  return result.choices[0].message.content;
}

async function testTopicRanking(headers, env) {
  const topic = headers.h1[0] || headers.title;
  const prompt = `As an AI language model, if I search for information about "${topic}", 
how likely am I to cite this content based on the following aspects:
1. Title clarity and relevance
2. Header structure
3. Meta description effectiveness
4. Topic authority signals

Please provide a detailed analysis and ranking probability score (0-100).`;

  const response = await fetch(OPENAI_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${env.OPENAI_API_KEY}`,
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'You are an AI expert specializing in analyzing content citation potential and ranking factors.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.7,
    }),
  });

  if (!response.ok) {
    throw new Error(`OpenAI API error: ${response.status}`);
  }

  const result = await response.json();
  return result.choices[0].message.content;
}

export default {
  async fetch(request, env) {
    // Handle CORS preflight requests
    if (request.method === 'OPTIONS') {
      return handleCORS(request);
    }

    const url = new URL(request.url);
    
    // Add a test endpoint
    if (url.pathname === '/test') {
      return new Response(JSON.stringify({ status: 'ok', message: 'Worker is running' }), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

    // Only allow POST requests for analyze endpoint
    if (url.pathname === '/analyze') {
      if (request.method !== 'POST') {
        return new Response('Method not allowed', { status: 405 });
      }

      // Verify origin
      const origin = request.headers.get('Origin');
      if (!ALLOWED_ORIGINS.includes(origin)) {
        console.error('Origin not allowed:', origin);
        return new Response('Not allowed', { status: 403 });
      }

      try {
        const data = await request.json();
        const targetUrl = data.url;

        // Fetch and analyze page content
        const pageContent = await fetchPageContent(targetUrl);
        if (!pageContent) {
          throw new Error('Failed to fetch page content');
        }

        const headers = await extractHeaderTags(pageContent);
        const llmTxtAnalysis = await checkLLMTxtCompliance(targetUrl);
        const sitemapAnalysis = await analyzeSitemap(targetUrl);
        const semanticAnalysis = await testSemanticRanking(pageContent, env);
        const topicRanking = await testTopicRanking(headers, env);

        const analysis = {
          headers,
          llmTxtAnalysis,
          sitemapAnalysis,
          semanticAnalysis,
          topicRanking,
          timestamp: new Date().toISOString()
        };

        return corsResponse(request, JSON.stringify({
          success: true,
          analysis
        }));

      } catch (error) {
        console.error('Worker error:', error);
        return corsResponse(request, JSON.stringify({
          success: false,
          error: error.message
        }), 500);
      }
    }

    return new Response('Not found', { status: 404 });
  }
};

function createPrompt(analysis) {
  return `Analyze this website's AI SEO data and provide specific recommendations:

URL: ${analysis.url}

Scores:
- Technical SEO: ${analysis.scores.technicalSEO}
- Content Structure: ${analysis.scores.structure}
- Semantic Markup: ${analysis.scores.semantic}
- LLM Readiness: ${analysis.scores.llmReadiness}
- Content Quality: ${analysis.scores.contentQuality}

Key Findings:
${formatFindings(analysis.findings)}

Please provide a detailed action plan with:
1. Technical improvements for AI crawlers
2. Content structure optimization
3. Semantic markup enhancements
4. Citation and authority building
5. Specific opportunities for backlinks and AI-focused partnerships

Format each recommendation with priority level, implementation steps, and expected impact.`;
}

function formatFindings(findings) {
  return findings.map(finding => `- ${finding.title}: ${finding.description}`).join('\n');
}

function parseRecommendations(content) {
  const plans = [];
  const sections = content.split('\n\n');

  for (const section of sections) {
    if (!section.trim()) continue;

    const lines = section.split('\n');
    const title = lines[0].replace('#', '').trim();

    // Extract priority
    let priority = 'medium';
    if (section.toLowerCase().includes('high priority')) {
      priority = 'high';
    } else if (section.toLowerCase().includes('low priority')) {
      priority = 'low';
    }

    // Extract steps
    const steps = lines
      .filter(line => line.trim().startsWith('-'))
      .map(line => line.trim().replace(/^-\s*/, ''));

    // Extract description
    const description = lines
      .find(line => !line.startsWith('#') && !line.startsWith('-'))
      ?.trim() || '';

    if (title && steps.length > 0) {
      plans.push({
        title,
        priority,
        description,
        steps
      });
    }
  }

  return plans;
}

function handleCORS(request) {
  const origin = request.headers.get('Origin');
  
  if (!ALLOWED_ORIGINS.includes(origin)) {
    return new Response(null, { status: 403 });
  }

  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
    },
  });
}

function corsResponse(request, body, status = 200) {
  const origin = request.headers.get('Origin');
  
  return new Response(body, {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
    },
  });
} 