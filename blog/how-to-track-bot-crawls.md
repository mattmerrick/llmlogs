---
title: "How to Track Bot Crawls on Your Website: A Complete Guide"
date: "2024-03-20"
description: "Learn how to track and analyze bot crawls on your website using Cloudflare Workers and a simple dashboard. Monitor LLM bots, search engines, and more."
author: "Matt Merrick"
tags: ["bot-tracking", "cloudflare-workers", "llm-seo", "web-analytics"]
---

# How to Track Bot Crawls on Your Website: A Complete Guide

Have you ever wondered which bots are crawling your website? With the rise of AI and LLM bots, understanding your site's bot traffic has become more important than ever. In this guide, I'll show you how to build a comprehensive bot tracking system using Cloudflare Workers and a simple dashboard.

## Why Track Bot Crawls?

Bot tracking helps you understand:
- Which AI models are crawling your content
- How search engines index your site
- When and how often bots visit
- Potential security threats
- Content optimization opportunities

## The Solution: Cloudflare Worker + Dashboard

We'll build a system that:
1. Tracks bot crawls in real-time
2. Categorizes bots (LLM, Search, Other)
3. Provides hourly and daily statistics
4. Shows historical data
5. Updates automatically

## Step 1: Set Up the Cloudflare Worker

First, create a new Cloudflare Worker with this configuration:

```toml
# wrangler.toml
name = "bot-crawl-tracker"
main = "botcrawl.js"
compatibility_date = "2024-01-01"

[[kv_namespaces]]
binding = "BOT_CRAWLS"
id = "your-kv-id"
```

## Step 2: Implement the Worker Code

Here's the core worker code that tracks bot crawls:

```javascript
// botcrawl.js
const BOT_CATEGORIES = {
    llm: ['gptbot', 'claudebot'],
    search: ['googlebot', 'bingbot', 'yandexbot'],
    other: ['ccBot', 'amazonbot', 'bytespider', 'googleExtended']
};

async function handleRequest(request) {
    const url = new URL(request.url);
    const userAgent = request.headers.get('user-agent') || '';
    const bot = identifyBot(userAgent);
    
    if (bot) {
        await trackBotCrawl(bot);
    }
    
    return new Response('OK', { status: 200 });
}

function identifyBot(userAgent) {
    const ua = userAgent.toLowerCase();
    for (const [bot, patterns] of Object.entries(BOT_PATTERNS)) {
        if (patterns.some(pattern => ua.includes(pattern))) {
            return bot;
        }
    }
    return null;
}

async function trackBotCrawl(bot) {
    const now = new Date();
    const hour = now.getUTCHours().toString();
    const date = now.toISOString().split('T')[0];
    
    // Update hourly stats
    const hourlyKey = `hourly:${date}:${hour}`;
    let hourlyData = await BOT_CRAWLS.get(hourlyKey, { type: 'json' }) || {};
    hourlyData[bot] = (hourlyData[bot] || 0) + 1;
    await BOT_CRAWLS.put(hourlyKey, JSON.stringify(hourlyData));
    
    // Update daily stats
    const dailyKey = `daily:${date}`;
    let dailyData = await BOT_CRAWLS.get(dailyKey, { type: 'json' }) || {};
    dailyData[bot] = (dailyData[bot] || 0) + 1;
    await BOT_CRAWLS.put(dailyKey, JSON.stringify(dailyData));
}

addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request));
});
```

## Step 3: Create the Dashboard

The dashboard provides a beautiful interface to view bot crawl data. Here's the key HTML structure:

```html
<!-- bot-dashboard.html -->
<div class="container">
    <!-- Stats Overview -->
    <div class="row">
        <div class="col-md-4">
            <div class="stat-card">
                <div class="stat-value" id="totalCrawls">0</div>
                <div class="stat-label">Total Crawls Today</div>
            </div>
        </div>
        <!-- More stat cards... -->
    </div>
    
    <!-- Charts -->
    <div class="row">
        <div class="col-md-8">
            <canvas id="crawlsChart"></canvas>
        </div>
        <div class="col-md-4">
            <canvas id="distributionChart"></canvas>
        </div>
    </div>
</div>
```

## Step 4: Add Real-time Updates

The dashboard updates automatically every 5 minutes:

```javascript
// Update dashboard every 5 minutes
setInterval(initializeDashboard, 5 * 60 * 1000);

async function initializeDashboard() {
    const data = await fetchBotData();
    updateStats(data);
    updateCharts(data);
    updateBotList(data);
}
```

## Understanding the Data

The dashboard shows several key metrics:

1. **Total Crawls**: All bot visits in the last 24 hours
2. **Unique Bots**: Different types of bots detected
3. **LLM Bots**: AI model crawlers (GPT, Claude, etc.)
4. **Hourly Activity**: Crawl patterns throughout the day
5. **Bot Distribution**: Breakdown of bot types

## Bot Categories

We track three main categories:

1. **LLM Bots**
   - GPT Bot
   - Claude Bot
   - Other AI crawlers

2. **Search Bots**
   - Google Bot
   - Bing Bot
   - Yandex Bot

3. **Other Bots**
   - Amazon Bot
   - CC Bot
   - ByteSpider
   - Google Extended

## Visualizing the Data

The dashboard includes three main charts:

1. **Crawls Over Time**: Line chart showing hourly activity
2. **Bot Distribution**: Doughnut chart of top 10 bots
3. **Activity by Type**: Bar chart showing LLM vs Search vs Other

## Benefits of This System

1. **Real-time Monitoring**: See bot activity as it happens
2. **Cost-effective**: Uses Cloudflare's free tier
3. **Easy to Deploy**: Simple setup with minimal configuration
4. **Scalable**: Handles high traffic without issues
5. **Insightful**: Provides valuable data for SEO and content strategy

## Next Steps

To enhance your bot tracking:

1. Add more bot patterns to detect
2. Implement rate limiting
3. Add email notifications for unusual activity
4. Create custom reports
5. Track bot behavior patterns

## Conclusion

Tracking bot crawls is essential for understanding how AI models and search engines interact with your content. This system provides a solid foundation that you can build upon based on your specific needs.

The code is available on [GitHub](https://github.com/mattmerrick/llmseoguide) if you want to implement it yourself or contribute improvements.

## Resources

- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [Bot Detection Patterns](https://github.com/mattmerrick/llmseoguide/blob/main/botcrawl.js)

---

*Want to see this in action? Check out our [live bot tracking dashboard](https://llmlogs.com/bot-dashboard).* 