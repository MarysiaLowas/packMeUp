import { useEffect } from 'react';
import { useAuth } from '@/lib/hooks/useAuth';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireAuth?: boolean;
  authRedirect?: string;
  publicRedirect?: string;
}

export function ProtectedRoute({ 
  children, 
  requireAuth = true,
  authRedirect = '/login',
  publicRedirect = '/dashboard'
}: ProtectedRouteProps) {
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    // Jeśli strona wymaga autoryzacji i użytkownik nie jest zalogowany
    if (requireAuth && !isAuthenticated) {
      window.location.replace(authRedirect);
      return;
    }

    // Jeśli użytkownik jest zalogowany i próbuje dostać się do strony publicznej
    if (isAuthenticated && !requireAuth) {
      window.location.replace(publicRedirect);
      return;
    }
  }, [isAuthenticated, requireAuth, authRedirect, publicRedirect]);

  // Jeśli warunki autoryzacji są spełnione, renderuj dzieci
  if (requireAuth === isAuthenticated) {
    return <>{children}</>;
  }

  // Podczas przekierowania pokaż pusty div
  return <div />;
} 