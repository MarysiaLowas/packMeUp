import { Link } from 'react-router-dom';
import { Button } from './button';
import { useAuth } from '@/lib/hooks/useAuth';
import { ThemeToggle } from './theme-provider';

interface NavigationProps {
  isAuthenticated: boolean;
  userName?: string;
}

export function Navigation({ isAuthenticated, userName }: NavigationProps) {
  const { logout } = useAuth();

  return (
    <nav className="border-b bg-gradient-to-r from-brandGreen/10 to-brandLime/10 shadow-sm">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold relative after:absolute after:bottom-[-2px] after:left-0 after:w-full after:h-[2px] after:bg-gradient-to-r after:from-brandGreen after:to-brandPink after:rounded-full">
          PackMeUp
        </Link>
        
        <div className="flex items-center gap-4">
          <ThemeToggle />
          
          {isAuthenticated ? (
            <>
              <span className="text-sm text-muted-foreground">
                Witaj, {userName || 'użytkowniku'}!
              </span>
              <Button 
                variant="outline" 
                onClick={logout}
                className="border-grayPurple/20 hover:bg-brandGreen/10 hover:border-brandGreen transition-all duration-200 hover:-translate-y-0.5"
              >
                Wyloguj się
              </Button>
            </>
          ) : (
            <>
              <Link to="/login">
                <Button 
                  variant="ghost"
                  className="hover:bg-brandGreen/10 transition-all duration-200"
                >
                  Zaloguj się
                </Button>
              </Link>
              <Link to="/register">
                <Button 
                  className="bg-gradient-to-r from-brandGreen to-brandLime border-none shadow hover:shadow-md hover:-translate-y-0.5 transition-all duration-200"
                >
                  Zarejestruj się
                </Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
} 