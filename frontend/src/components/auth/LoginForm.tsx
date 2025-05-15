import { useState } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Input, FormLabel } from '@/components/ui/input';
import { Form, FormControl, FormField, FormItem, FormMessage } from '@/components/ui/form';
import { Card, CardContent, CardHeader, CardTitle, ThemedCard } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { useAuth } from '@/lib/hooks/useAuth';

const loginFormSchema = z.object({
  email: z.string().email('Wprowadź poprawny adres email'),
  password: z.string()
    .min(8, 'Hasło musi mieć minimum 8 znaków')
    .regex(/[A-Z]/, 'Hasło musi zawierać przynajmniej jedną wielką literę')
    .regex(/[0-9]/, 'Hasło musi zawierać przynajmniej jedną cyfrę'),
});

type LoginFormShape = z.infer<typeof loginFormSchema>;

const LoginForm = () => {
  const [apiError, setApiError] = useState<string | null>(null);
  const { login, isLoading } = useAuth();
  const navigate = useNavigate();

  const form = useForm<LoginFormShape>({
    resolver: zodResolver(loginFormSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const onSubmit = async (data: LoginFormShape) => {
    setApiError(null);
    
    try {
      await login(data);
      // Nawigacja jest teraz obsługiwana przez AuthProvider
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Wystąpił błąd podczas logowania');
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="text-center mb-6">
        <h1 className="text-3xl font-bold mb-2">Witaj z powrotem</h1>
        <p className="text-muted-foreground">Zaloguj się, aby kontynuować</p>
      </div>
      
      <ThemedCard variant="primary" className="border-grayPurple/10">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center relative pb-3 after:absolute after:left-1/2 after:-translate-x-1/2 after:bottom-0 after:h-0.5 after:w-16 after:bg-gradient-to-r after:from-brandGreen after:to-brandLime after:rounded-full">
            Logowanie
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel variant="primary">Email</FormLabel>
                    <FormControl>
                      <Input 
                        type="email" 
                        placeholder="twoj@email.com" 
                        variant="primary"
                        className="bg-white/80 focus-visible:bg-white"
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
                    <FormLabel variant="primary">Hasło</FormLabel>
                    <FormControl>
                      <Input 
                        type="password" 
                        placeholder="••••••••" 
                        variant="primary"
                        className="bg-white/80 focus-visible:bg-white"
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

              <div className="flex flex-col gap-4 pt-2">
                <Button 
                  type="submit" 
                  disabled={isLoading}
                  variant="gradient"
                  className="w-full"
                >
                  {isLoading ? 'Logowanie...' : 'Zaloguj się'}
                </Button>
                
                <div className="text-center space-y-3 pt-2">
                  <RouterLink to="/reset-password" className="text-sm text-muted-foreground hover:text-brandGreen transition-colors">
                    Zapomniałeś hasła?
                  </RouterLink>
                  <div className="text-sm">
                    Nie masz konta?{' '}
                    <RouterLink to="/register" className="text-brandGreen font-medium hover:text-brandGreen/80 transition-colors">
                      Zarejestruj się
                    </RouterLink>
                  </div>
                </div>
              </div>
            </form>
          </Form>
        </CardContent>
      </ThemedCard>
      
      <div className="h-px bg-gradient-to-r from-transparent via-brandGreen/30 to-transparent border-0 my-8"></div>
      
      <div className="text-center text-sm text-muted-foreground">
        PackMeUp &copy; {new Date().getFullYear()}
      </div>
    </div>
  );
};

export default LoginForm; 