import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/lib/hooks/useAuth';

const DashboardHome = () => {
  const { user } = useAuth();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Panel główny</h1>
        <p className="text-muted-foreground">
          Witaj z powrotem, {user?.first_name}! Oto przegląd Twoich podróży i list pakowania.
        </p>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Nadchodzące podróże</CardTitle>
            <CardDescription>Lista Twoich zaplanowanych podróży</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Aktywne listy</CardTitle>
            <CardDescription>Listy pakowania w przygotowaniu</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Ukończone podróże</CardTitle>
            <CardDescription>Historia Twoich podróży</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Ostatnia aktywność</CardTitle>
          <CardDescription>Historia Twoich ostatnich działań</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">Brak ostatniej aktywności</p>
        </CardContent>
      </Card>
    </div>
  );
};

export default DashboardHome; 