import { Link } from '@/components/ui/link';
import { Button } from '@/components/ui/button';

interface NavigationProps {
  isAuthenticated?: boolean;
  userName?: string;
}

export const Navigation = ({ isAuthenticated, userName }: NavigationProps) => {
  return (
    <nav className="border-b">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="text-xl font-bold">
          PackMeUp
        </Link>
        
        <div className="flex items-center gap-4">
          {isAuthenticated ? (
            <>
              <span className="text-sm text-muted-foreground">
                Cześć, {userName}
              </span>
              <form action="/api/auth/logout" method="POST">
                <Button type="submit" variant="outline">
                  Wyloguj się
                </Button>
              </form>
            </>
          ) : (
            <>
              <Link href="/login">
                <Button variant="ghost">Zaloguj się</Button>
              </Link>
              <Link href="/register">
                <Button>Zarejestruj się</Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}; 