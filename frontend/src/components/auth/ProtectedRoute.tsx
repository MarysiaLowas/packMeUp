import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/lib/hooks/useAuth";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireAuth?: boolean;
  authRedirect?: string;
  publicRedirect?: string;
}

export function ProtectedRoute({
  children,
  requireAuth = true,
  authRedirect = "/login",
  publicRedirect = "/dashboard",
}: ProtectedRouteProps) {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // Jeśli strona wymaga autoryzacji i użytkownik nie jest zalogowany
    if (requireAuth && !isAuthenticated) {
      navigate(authRedirect, { replace: true });
      return;
    }

    // Jeśli użytkownik jest zalogowany i próbuje dostać się do strony publicznej
    if (isAuthenticated && !requireAuth) {
      navigate(publicRedirect, { replace: true });
      return;
    }
  }, [isAuthenticated, requireAuth, authRedirect, publicRedirect, navigate]);

  // Jeśli warunki autoryzacji są spełnione, renderuj dzieci
  if (requireAuth === isAuthenticated) {
    return <>{children}</>;
  }

  // Podczas przekierowania pokaż pusty div
  return <div />;
}
