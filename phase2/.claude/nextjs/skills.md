# Next.js Skills and Capabilities

## Overview
This document outlines the skills and capabilities required for working with Next.js applications. Next.js is a React-based framework that enables functionality such as server-side rendering and generating static websites.

## Core Skills

### 1. Page Router and App Router
- Understanding of both the traditional pages router and the newer app router
- Knowledge of file-based routing system
- Implementation of dynamic routes, nested routes, and catch-all routes
- Route handlers in the app router for API endpoints

### 2. Rendering Strategies
- Server-Side Rendering (SSR)
- Static Site Generation (SSG)
- Client-Side Rendering (CSR)
- Incremental Static Regeneration (ISR)
- Streaming and Suspense for React 18+

### 3. Data Fetching
- `getServerSideProps` for server-side rendering
- `getStaticProps` and `getStaticPaths` for static generation
- Client-side data fetching with SWR or React Query
- New React server functions and server actions

### 4. API Routes
- Creating API endpoints within the Next.js application
- Handling different HTTP methods
- Middleware implementation
- Request and response handling

### 5. Styling and CSS
- CSS Modules
- Styled-jsx
- Tailwind CSS integration
- CSS-in-JS libraries
- Global and component-level styling

### 6. Image Optimization
- Using the built-in `next/image` component
- Image optimization and responsive images
- Different image formats (WebP, AVIF)
- Lazy loading implementation

### 7. Performance Optimization
- Code splitting and dynamic imports
- Bundle analysis and optimization
- Font optimization with `next/font`
- Caching strategies
- Preloading and prefetching

### 8. Deployment and Production
- Building and deploying Next.js applications
- Environment configuration
- Static export capability
- Integration with hosting platforms (Vercel, Netlify, etc.)

## Advanced Skills

### 1. Middleware
- Implementing request/response middleware
- Authentication and authorization flows
- A/B testing implementation
- Internationalization routing

### 2. Internationalization (i18n)
- Locale detection and routing
- Static generation with multiple locales
- Client-side locale switching
- Translation management

### 3. Forms and Actions
- Server actions for form handling
- Client actions for interactive components
- Form validation strategies
- Optimistic UI updates

### 4. Search Engine Optimization
- Meta tags and structured data
- Sitemap generation
- Canonical URLs
- Social media sharing tags

## Best Practices

### 1. Project Structure
- Organizing components, pages, and utilities
- Environment-specific configurations
- API integration patterns
- Testing file organization

### 2. Error Handling
- Global error boundaries
- Custom error pages
- 404 and 500 page implementations
- Logging and monitoring strategies

### 3. Security
- Preventing XSS attacks
- Securing API routes
- Environment variable management
- Header security configurations

## Common Commands

```bash
# Create a new Next.js project
npx create-next-app@latest

# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Linting
npm run lint
```

## File Structure Convention

```
my-nextjs-app/
├── app/                 # App Router (Next.js 13+)
│   ├── page.js          # Route page
│   ├── layout.js        # Route layout
│   └── ...              # Other route segments
├── pages/              # Pages Router
│   ├── index.js        # Home page
│   └── ...             # Other pages
├── components/         # Reusable components
├── public/             # Static assets
├── styles/             # Global styles
├── lib/                # Utility functions
├── next.config.js      # Next.js configuration
├── package.json
└── .env*               # Environment variables
```

## Troubleshooting Common Issues

1. **Hydration Errors**: Ensure server and client render the same content
2. **Bundle Size**: Use dynamic imports and analyze bundle with `@next/bundle-analyzer`
3. **Image Optimization**: Configure loader for external images if needed
4. **Environment Variables**: Use proper prefixes (NEXT_PUBLIC_ for client-side)
5. **API Routes**: Remember they're server-side only and not component code

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://reactjs.org/docs)
- [Vercel Platform](https://vercel.com)
- [Next.js GitHub Repository](https://github.com/vercel/next.js)