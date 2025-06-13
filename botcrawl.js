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
  
  export default {
    async fetch(request, env, ctx) {
      const url = new URL(request.url);
      const userAgent = request.headers.get("user-agent") || "";
      const date = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  
      for (const [botName, regex] of Object.entries(knownBots)) {
        if (regex.test(userAgent)) {
          const key = `${date}:${botName}`;
          const count = parseInt(await env.BOT_CRAWLS.get(key)) || 0;
          await env.BOT_CRAWLS.put(key, (count + 1).toString());
          break;
        }
      }
  
      if (url.pathname === "/bot-crawls.json") {
        const stats = {};
        for (const botName of Object.keys(knownBots)) {
          const key = `${date}:${botName}`;
          const count = await env.BOT_CRAWLS.get(key) || "0";
          stats[botName] = parseInt(count);
        }
        return new Response(JSON.stringify({ date, ...stats }), {
          headers: { "Content-Type": "application/json" }
        });
      }
  
      return fetch(request);
    }
  };
  