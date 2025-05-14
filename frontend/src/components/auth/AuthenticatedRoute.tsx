import type { ReactNode } from 'react';
import { AuthProvider } from '@/lib/providers/AuthProvider';
import { ProtectedRoute } from './ProtectedRoute';

interface AuthenticatedRouteProps {
  children: ReactNode;
  requireAuth?: boolean;
  authRedirect?: string;
  publicRedirect?: string;
}

export function AuthenticatedRoute({ 
  children, 
  requireAuth = true,
  authRedirect = '/login',
  publicRedirect = '/dashboard'
}: AuthenticatedRouteProps) {
  return (
    <AuthProvider>
      <ProtectedRoute 
        requireAuth={requireAuth}
        authRedirect={authRedirect}
        publicRedirect={publicRedirect}
      >
        {children}
      </ProtectedRoute>
    </AuthProvider>
  );
} 