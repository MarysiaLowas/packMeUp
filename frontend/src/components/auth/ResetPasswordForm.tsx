import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Link } from '@/components/ui/link';

const resetPasswordFormSchema = z.object({
  email: z.string().email('Wprowadź poprawny adres email'),
});

type ResetPasswordFormShape = z.infer<typeof resetPasswordFormSchema>;

export const ResetPasswordForm = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const form = useForm<ResetPasswordFormShape>({
    resolver: zodResolver(resetPasswordFormSchema),
    defaultValues: {
      email: '',
    },
  });

  const onSubmit = async (data: ResetPasswordFormShape) => {
    setIsLoading(true);
    setApiError(null);
    // Backend integration will be implemented later
    setIsSuccess(true);
    setIsLoading(false);
  };

  if (isSuccess) {
    return (
      <Card className="w-full max-w-md mx-auto">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">Sprawdź swoją skrzynkę</CardTitle>
          <CardDescription className="text-center mt-2">
            Wysłaliśmy instrukcje resetowania hasła na podany adres email.
          </CardDescription>
        </CardHeader>
        <CardContent className="text-center">
          <Link href="/login" className="hover:text-primary">
            Powrót do logowania
          </Link>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-center">Resetowanie hasła</CardTitle>
        <CardDescription className="text-center mt-2">
          Wprowadź swój adres email, a wyślemy Ci instrukcje resetowania hasła.
        </CardDescription>
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
                {isLoading ? 'Wysyłanie...' : 'Wyślij instrukcje'}
              </Button>

              <div className="text-center text-sm text-muted-foreground">
                <Link href="/login" className="hover:text-primary">
                  Powrót do logowania
                </Link>
              </div>
            </div>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}; 