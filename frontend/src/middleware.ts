import { defineMiddleware } from 'astro:middleware';

const protectedRoutes = ['/dashboard', '/new-trip', '/profile'];
const authRoutes = ['/login', '/register', '/reset-password'];

export const onRequest = defineMiddleware(async (context, next) => {
  const { cookies, url } = context;
  const token = cookies.get('auth_token');
  const isProtectedRoute = protectedRoutes.some(route => url.pathname.startsWith(route));
  const isAuthRoute = authRoutes.some(route => url.pathname.startsWith(route));

  // Jeśli użytkownik jest zalogowany i próbuje dostać się do strony logowania/rejestracji
  if (token && isAuthRoute) {
    return context.redirect('/dashboard');
  }

  // Jeśli użytkownik nie jest zalogowany i próbuje dostać się do chronionej strony
  if (!token && isProtectedRoute) {
    return context.redirect('/login');
  }

  return next();
}); 