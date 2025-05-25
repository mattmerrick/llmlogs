addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  // Get the response from the origin
  let response = await fetch(request)
  
  // Clone the response so we can modify headers
  response = new Response(response.body, response)
  
  // Add security headers
  response.headers.set('Content-Security-Policy', 
    "default-src 'self'; " +
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.googletagmanager.com https://www.google-analytics.com https://datafa.st https://scripts.simpleanalyticscdn.com https://ghbtns.com https://app.tinyadz.com; " +
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; " +
    "font-src 'self' https://fonts.gstatic.com; " +
    "img-src 'self' data: https:; " +
    "frame-src 'self' https://www.googletagmanager.com https://ghbtns.com; " +
    "connect-src 'self' https://www.google-analytics.com https://www.googletagmanager.com https://datafa.st https://scripts.simpleanalyticscdn.com"
  )
  
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  response.headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
  
  return response
} 