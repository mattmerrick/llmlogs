# Next.js Development Rules and Guidelines

## Project Structure
1. Use the `app` directory for new projects (App Router)
2. Keep page components in `app/(routes)` directory
3. Store reusable components in `components/`
4. Place API routes in `app/api` directory
5. Use `lib/` for utility functions and shared logic

## Routing & Navigation
1. Use dynamic route segments for variable paths
2. Implement loading states with `loading.tsx`
3. Handle errors with `error.tsx` boundaries
4. Use `Link` component for client-side navigation
5. Implement middleware in `middleware.ts`

## Data Fetching
1. Prefer Server Components for data fetching
2. Use React Server Components (RSC) by default
3. Implement proper caching strategies
4. Handle loading and error states
5. Use `revalidatePath()` for on-demand revalidation

## Performance
1. Optimize images with `next/image`
2. Use font optimization with `next/font`
3. Implement proper metadata for SEO
4. Minimize client-side JavaScript
5. Use proper caching strategies

## Best Practices
1. Follow TypeScript best practices
2. Implement proper error handling
3. Use environment variables for configuration
4. Write clean, maintainable code
5. Follow React best practices 