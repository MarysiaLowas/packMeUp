import { type ReactNode } from 'react';
import { useAuth } from '@/lib/hooks/useAuth';
import { Navigation } from '@/components/ui/navigation';

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  const { isAuthenticated, user } = useAuth();

  return (
    <div className="min-h-screen bg-background">
      <Navigation isAuthenticated={isAuthenticated} userName={user?.first_name} />
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
      <footer className="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
        <p>&copy; {new Date().getFullYear()} PackMeUp. Wszystkie prawa zastrzeżone.</p>
      </footer>
    </div>
  );
} 