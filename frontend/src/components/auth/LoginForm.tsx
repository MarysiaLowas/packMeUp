import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Link } from '@/components/ui/link';
import { useAuth } from '@/lib/hooks/useAuth';

const loginFormSchema = z.object({
  email: z.string().email('Wprowadź poprawny adres email'),
  password: z.string()
    .min(8, 'Hasło musi mieć minimum 8 znaków')
    .regex(/[A-Z]/, 'Hasło musi zawierać przynajmniej jedną wielką literę')
    .regex(/[0-9]/, 'Hasło musi zawierać przynajmniej jedną cyfrę'),
});

type LoginFormShape = z.infer<typeof loginFormSchema>;

export const LoginForm = () => {
  const [apiError, setApiError] = useState<string | null>(null);
  const { login, isLoading } = useAuth();

  const form = useForm<LoginFormShape>({
    resolver: zodResolver(loginFormSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const onSubmit = async (data: LoginFormShape) => {
    console.log('🎯 onSubmit called with data:', data);
    setApiError(null);
    
    try {
      console.log('👉 Calling login function');
      await login(data);
      console.log('✅ Login successful');
    } catch (error) {
      console.error('❌ Login failed:', error);
      setApiError(error instanceof Error ? error.message : 'Wystąpił błąd podczas logowania');
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-center">Logowanie</CardTitle>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input 
                      type="email" 
                      placeholder="twoj@email.com" 
                      {...field} 
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Hasło</FormLabel>
                  <FormControl>
                    <Input 
                      type="password" 
                      placeholder="••••••••" 
                      {...field} 
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {apiError && (
              <Alert variant="destructive">
                <AlertDescription>{apiError}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-4">
              <Button 
                type="submit"
                className="w-full" 
                disabled={isLoading}
              >
                {isLoading ? 'Logowanie...' : 'Zaloguj się'}
              </Button>

              <div className="text-center space-y-2">
                <Link href="/reset-password" className="text-sm text-muted-foreground hover:text-primary">
                  Zapomniałeś hasła?
                </Link>
                <div className="text-sm text-muted-foreground">
                  Nie masz konta?{' '}
                  <Link href="/register" className="hover:text-primary">
                    Zarejestruj się
                  </Link>
                </div>
              </div>
            </div>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}; 