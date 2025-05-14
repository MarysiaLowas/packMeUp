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

const registerFormSchema = z.object({
  email: z.string().email('Wprowadź poprawny adres email'),
  firstName: z.string()
    .min(2, 'Imię musi mieć minimum 2 znaki')
    .max(50, 'Imię nie może być dłuższe niż 50 znaków'),
  password: z.string()
    .min(8, 'Hasło musi mieć minimum 8 znaków')
    .regex(/[A-Z]/, 'Hasło musi zawierać przynajmniej jedną wielką literę')
    .regex(/[0-9]/, 'Hasło musi zawierać przynajmniej jedną cyfrę'),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Hasła muszą być takie same",
  path: ["confirmPassword"],
});

type RegisterFormShape = z.infer<typeof registerFormSchema>;

export const RegisterForm = () => {
  const [apiError, setApiError] = useState<string | null>(null);
  const { register, isLoading } = useAuth();

  const form = useForm<RegisterFormShape>({
    resolver: zodResolver(registerFormSchema),
    defaultValues: {
      email: '',
      firstName: '',
      password: '',
      confirmPassword: '',
    },
  });

  const onSubmit = async (data: RegisterFormShape) => {
    setApiError(null);
    
    try {
      await register({
        email: data.email,
        firstName: data.firstName,
        password: data.password,
      });
      // Przekierowanie nastąpi automatycznie przez AuthService
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Wystąpił błąd podczas rejestracji');
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-center">Rejestracja</CardTitle>
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
              name="firstName"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Imię</FormLabel>
                  <FormControl>
                    <Input 
                      type="text" 
                      placeholder="Jan" 
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

            <FormField
              control={form.control}
              name="confirmPassword"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Potwierdź hasło</FormLabel>
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
                {isLoading ? 'Rejestracja...' : 'Zarejestruj się'}
              </Button>

              <div className="text-center text-sm text-muted-foreground">
                Masz już konto?{' '}
                <Link href="/login" className="hover:text-primary">
                  Zaloguj się
                </Link>
              </div>
            </div>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}; 