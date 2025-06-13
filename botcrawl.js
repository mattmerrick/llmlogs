const knownBots = {
    gptbot: /gptbot/i,
    claudebot: /claude(bot|\-web)/i,
    ccBot: /ccbot/i,
    amazonbot: /amazonbot/i,
    bingbot: /bingbot/i,
    googleExtended: /google-extended/i,
    googlebot: /googlebot/i,
    bytespider: /bytespider/i,
    yandexbot: /yandexbot/i,
};

// Cache for rate limiting
const RATE_LIMIT = {
    window: 60, // 1 minute window
    maxRequests: 100 // max requests per minute
};

const isBot = (userAgent) => {
    const botPatterns = [
        /bot/i,
        /crawler/i,
        /spider/i,
        /slurp/i,
        /wget/i,
        /curl/i,
        /fetch/i,
        /headless/i,
        /phantom/i,
        /selenium/i
    ];
    return botPatterns.some(pattern => pattern.test(userAgent));
};

const getBotName = (userAgent) => {
    // First check known bots
    for (const [botName, regex] of Object.entries(knownBots)) {
        if (regex.test(userAgent)) {
            return botName;
        }
    }
    
    // If not a known bot, try to extract a meaningful name
    const botMatch = userAgent.match(/([a-zA-Z0-9]+(?:bot|crawler|spider))/i);
    if (botMatch) {
        return botMatch[1].toLowerCase();
    }
    
    // If no meaningful name can be extracted, use a hash of the user agent
    return 'unknown_bot';
};

// Batch updates to reduce KV writes
let updateQueue = new Map();
let lastFlush = Date.now();
const FLUSH_INTERVAL = 60000; // Flush every minute

async function flushUpdates(env) {
    const now = Date.now();
    if (now - lastFlush < FLUSH_INTERVAL) return;
    
    for (const [key, count] of updateQueue) {
        const currentCount = parseInt(await env.BOT_CRAWLS.get(key)) || 0;
        await env.BOT_CRAWLS.put(key, (currentCount + count).toString());
    }
    
    updateQueue.clear();
    lastFlush = now;
}

export default {
    async fetch(request, env, ctx) {
        const url = new URL(request.url);
        const userAgent = request.headers.get("user-agent") || "";
        const date = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
        const hour = new Date().getUTCHours(); // 0-23

        // Rate limiting
        const ip = request.headers.get('cf-connecting-ip');
        const rateLimitKey = `ratelimit:${ip}`;
        const currentRequests = parseInt(await env.BOT_CRAWLS.get(rateLimitKey)) || 0;
        
        if (currentRequests >= RATE_LIMIT.maxRequests) {
            return new Response('Rate limit exceeded', { status: 429 });
        }
        
        await env.BOT_CRAWLS.put(rateLimitKey, (currentRequests + 1).toString(), {
            expirationTtl: RATE_LIMIT.window
        });

        if (isBot(userAgent)) {
            const botName = getBotName(userAgent);
            const key = `${date}:${botName}`;
            const hourlyKey = `${date}:${hour}:${botName}`;
            
            // Queue updates instead of immediate writes
            updateQueue.set(key, (updateQueue.get(key) || 0) + 1);
            updateQueue.set(hourlyKey, (updateQueue.get(hourlyKey) || 0) + 1);
            
            // Flush updates if needed
            await flushUpdates(env);
        }

        if (url.pathname === "/bot-crawls.json") {
            // Ensure all pending updates are flushed
            await flushUpdates(env);
            
            const stats = {
                date,
                hourly: {},
                daily: {},
                total: 0,
                limits: {
                    remaining: 100000 - currentRequests, // Approximate remaining requests
                    resetTime: new Date(Date.now() + RATE_LIMIT.window * 1000).toISOString()
                }
            };

            // Get all keys for today
            const keys = await env.BOT_CRAWLS.list({ prefix: date });
            
            // Process all keys
            for (const key of keys.keys) {
                const count = parseInt(await env.BOT_CRAWLS.get(key.name)) || 0;
                const [_, time, botName] = key.name.split(':');
                
                if (time) {
                    // Hourly data
                    if (!stats.hourly[time]) {
                        stats.hourly[time] = {};
                    }
                    stats.hourly[time][botName] = count;
                } else {
                    // Daily data
                    stats.daily[botName] = count;
                    stats.total += count;
                }
            }

            return new Response(JSON.stringify(stats), {
                headers: { 
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Cache-Control": "no-cache"
                }
            });
        }

        return fetch(request);
    }
};
  