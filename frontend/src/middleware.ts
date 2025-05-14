import { defineMiddleware } from 'astro:middleware';

// Middleware może być potrzebne do innych celów w przyszłości,
// ale na razie nie jest potrzebne do autoryzacji
export const onRequest = defineMiddleware(async (context, next) => {
  return next();
}); 