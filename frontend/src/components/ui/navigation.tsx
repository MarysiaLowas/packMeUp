import { Link } from 'react-router-dom';
import { Button } from './button';
import { useAuth } from '@/lib/hooks/useAuth';

interface NavigationProps {
  isAuthenticated: boolean;
  userName?: string;
}

export function Navigation({ isAuthenticated, userName }: NavigationProps) {
  const { logout } = useAuth();

  return (
    <nav className="border-b">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold">
          PackMeUp
        </Link>
        
        <div className="flex items-center gap-4">
          {isAuthenticated ? (
            <>
              <span className="text-sm text-muted-foreground">
                Witaj, {userName || 'użytkowniku'}!
              </span>
              <Button variant="outline" onClick={logout}>
                Wyloguj się
              </Button>
            </>
          ) : (
            <>
              <Link to="/login">
                <Button variant="ghost">Zaloguj się</Button>
              </Link>
              <Link to="/register">
                <Button>Zarejestruj się</Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
} 