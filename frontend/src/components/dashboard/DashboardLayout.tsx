import { type ReactNode } from 'react';
import { useAuth } from '@/lib/hooks/useAuth';
import { NavLink, Outlet } from 'react-router-dom';
import { cn } from '@/lib/utils';

interface DashboardLayoutProps {
  children?: ReactNode;
}

const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  const { user } = useAuth();

  return (
    <div className="grid grid-cols-1 md:grid-cols-[240px_1fr] gap-6">
      <aside className="hidden md:flex flex-col gap-6 p-6 border-r">
        <div className="flex items-center gap-3 px-2">
          <div className="flex flex-col">
            <span className="text-sm font-medium">Witaj,</span>
            <span className="text-lg font-semibold">{user?.first_name}</span>
          </div>
        </div>
        <nav className="flex flex-col gap-2">
          <NavLink
            to="/dashboard"
            end
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg hover:bg-muted",
                isActive && "bg-muted"
              )
            }
          >
            Panel główny
          </NavLink>
          <NavLink
            to="/dashboard/new-trip"
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg hover:bg-muted",
                isActive && "bg-muted"
              )
            }
          >
            Nowa podróż
          </NavLink>
          <div className="flex items-center gap-3 px-3 py-2 text-sm font-medium text-muted-foreground">
            Moje podróże (wkrótce)
          </div>
          <div className="flex items-center gap-3 px-3 py-2 text-sm font-medium text-muted-foreground">
            Listy pakowania (wkrótce)
          </div>
        </nav>
      </aside>
      <main className="p-6">
        {children || <Outlet />}
      </main>
    </div>
  );
};

export default DashboardLayout; 