# Nuxt.js Development Rules and Guidelines

## Project Structure
1. Use the `pages/` directory for route components
2. Store reusable components in `components/`
3. Place server middleware in `server/`
4. Use `composables/` for shared logic
5. Keep plugins in `plugins/` directory

## Routing & Navigation
1. Implement dynamic routes with proper parameters
2. Use `<NuxtLink>` for client-side navigation
3. Handle route middleware effectively
4. Implement proper navigation guards
5. Use route validation when needed

## Data Management
1. Use `useState` for reactive state
2. Implement proper data fetching with `useFetch`
3. Handle API calls efficiently
4. Use proper error handling
5. Implement caching strategies

## Performance
1. Use proper image optimization
2. Implement lazy loading where appropriate
3. Optimize component imports
4. Use proper SEO practices
5. Implement proper caching

## Best Practices
1. Follow Vue.js best practices
2. Use TypeScript for better type safety
3. Implement proper error boundaries
4. Use environment variables correctly
5. Write maintainable, clean code 