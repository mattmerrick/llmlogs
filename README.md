# LLM Logs

Master LLM SEO to increase your content visibility in AI responses. Learn how to optimize for Large Language Models and get more clicks with our comprehensive guide.

## 📚 Resources

Visit our [Resources Page](resources.html) for a complete collection of:
- Free LLM optimization tools
- Learning materials and guides
- Latest blog posts
- Community resources

## 🛠️ Free Tools

Access our suite of tools designed to help you optimize your content for AI understanding and visibility:

### Bot Crawl Tracker
- Track and analyze bot crawls on your website in real-time
- Monitor LLM bot activity (GPT, Claude, etc.)
- View hourly and daily crawl statistics
- Get insights into search engine bot behavior
- [Try Bot Crawl Tracker](https://llmlogs.com/bot-dashboard)

### Site Scanner
- Analyze your website's LLM optimization
- Get comprehensive ranking report
- Check technical elements (robots.txt, sitemap.xml, llms.txt)
- Evaluate content structure and semantic clarity
- [Try Site Scanner](https://llmlogs.com/scan-site)

### Alt Text Checker
- Analyze images and their alt text for AI readability
- Get recommendations for improving alt text descriptions
- Check for missing or ineffective alt text
- Support for both direct HTML input and URL scanning

### Prompt Injection Tester
- Test prompts for potential security vulnerabilities
- Get detailed vulnerability reports and risk scores
- Receive mitigation recommendations
- Support for basic and advanced testing patterns

### AI Content Scanner
- Analyze content structure and readability
- Check semantic clarity and context completeness
- Evaluate citation potential and authority signals
- Get actionable recommendations for improvement

### llms.txt Generator
- Create optimized llms.txt files for AI crawlers
- Configure access for multiple AI bots (GPT, Claude, Cohere, Google)
- Manage allowed and disallowed paths
- Get instant preview and easy download options

### AI Robots.txt Generator
Generate optimized robots.txt files for AI and LLM crawlers with support for major search engines. Control which AI models can crawl your content and ensure proper indexing by search engines.

[Try AI Robots.txt Generator →](/free-tools/ai-robots-txt-generator.html)

## 🎓 Free AI SEO Course

Master the fundamentals of AI SEO with our comprehensive course:

- Learn how to optimize for LLMs
- Understand bot crawling and indexing
- Master content structure for AI
- Get hands-on with real examples
- [Start Free AI SEO Course](https://llmlogs.com/ai-seo-course)

## 📚 Core Concepts

Understanding how Large Language Models work is crucial for effective SEO. This section covers the fundamental principles of LLM optimization, including how AI models process and rank content, the importance of structured data, and the role of citations in establishing authority.

- [Understanding LLM Optimization](https://llmlogs.com/guides/llm-optimization/core-concepts)
  - Learn the basics of how LLMs work and how to optimize your content for better visibility
- [Mean Cumulative Precision (MCP)](https://llmlogs.com/guides/llm-optimization/mean-cumulative-precision)
  - Master MCP metrics to evaluate and improve your content's performance with AI models
- [Structured Data Implementation](https://llmlogs.com/guides/llm-optimization/structured-data)
  - Master the implementation of structured data to help LLMs better understand your content
- [Citation Strategy](https://llmlogs.com/guides/llm-optimization/citation-strategy)
  - Develop a robust citation strategy to build authority and improve content credibility

## 🎯 Content Optimization

Learn how to structure and format your content for maximum impact in LLM responses. This section provides detailed guidance on content organization, formatting best practices, and technical implementation strategies to improve your content's visibility in AI-generated responses.

- [Content Structure & Formatting](https://llmlogs.com/guides/llm-optimization/content-optimization)
  - Optimize your content structure and formatting for better LLM comprehension
- [Testing & Validation](https://llmlogs.com/guides/llm-optimization/testing)
  - Learn how to test and validate your LLM optimization efforts using MCP and other metrics

## 📝 Latest Blog Posts

Stay up to date with the latest developments in LLM SEO:

- [How to Automate LLM Prompts with n8n Event Triggers](https://llmlogs.com/blog/automate-llm-prompts-with-n8n-event-triggers)
- [How to Automate GPT Workflows with n8n](https://llmlogs.com/blog/how-to-automate-gpt-workflows-with-n8n)
- [Evaluating LLM Ranking Quality: MCP vs MAP vs NDCG](https://llmlogs.com/blog/evaluating-llm-ranking-quality-mcp-vs-map-vs-ndcg)
- [How to Track If ChatGPT Cites Your Blog Early — Using MCP](https://llmlogs.com/blog/how-to-track-if-chatgpt-cites-your-blog-early-using-mcp)
- [What Is Mean Cumulative Precision (MCP) and Why It Matters for AI SEO](https://llmlogs.com/blog/what-is-mean-cumulative-precision-mcp-ai-seo)

## Quick Links

- [Resources](resources.html)
- [Guides](https://llmlogs.com/guides/llm-optimization)
- [Free Tools](https://llmlogs.com/free-tools)
- [Examples](https://llmlogs.com/guides/llm-optimization/examples)
- [Blog](https://llmlogs.com/blog)
- [Contact](https://llmlogs.com/contact)

## Connect With Us

- [GitHub](https://github.com/mattmerrick/llmseoguide)
- [Twitter](https://twitter.com/llmseoguide)
- [LinkedIn](https://linkedin.com/company/llmseoguide)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more information.

# LLM Logs Forum

Static forum implementation using Supabase.

## Quick Start

1. Copy config template and add your keys:
```bash
cp forum/config.template.js forum/config.js
```

2. Start local server:
```bash
python -m http.server 3000
```

3. Open `http://localhost:3000`

## Deployment

1. Add environment variables in Cloudflare Pages:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `RESEND_API_KEY`

2. Update production domain in `config.js`

Note: `config.js` is gitignored - keep your keys secure!