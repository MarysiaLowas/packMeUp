import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Link } from "react-router-dom";
import { useAuth } from "@/lib/hooks/useAuth";

const resetPasswordFormSchema = z.object({
  email: z.string().email("Wprowadź poprawny adres email"),
});

type ResetPasswordFormShape = z.infer<typeof resetPasswordFormSchema>;

const ResetPasswordForm = () => {
  const [apiError, setApiError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);
  const { resetPassword, isLoading } = useAuth();

  const form = useForm<ResetPasswordFormShape>({
    resolver: zodResolver(resetPasswordFormSchema),
    defaultValues: {
      email: "",
    },
  });

  const onSubmit = async (data: ResetPasswordFormShape) => {
    setApiError(null);
    setIsSuccess(false);

    try {
      await resetPassword(data.email);
      setIsSuccess(true);
      form.reset();
    } catch (error) {
      setApiError(
        error instanceof Error
          ? error.message
          : "Wystąpił błąd podczas resetowania hasła",
      );
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-center">
          Reset hasła
        </CardTitle>
        <CardDescription className="text-center">
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

            {isSuccess && (
              <Alert>
                <AlertDescription>
                  Instrukcje resetowania hasła zostały wysłane na podany adres
                  email.
                </AlertDescription>
              </Alert>
            )}

            <div className="space-y-4">
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? "Wysyłanie..." : "Wyślij instrukcje"}
              </Button>

              <div className="text-center text-sm text-muted-foreground">
                Pamiętasz hasło?{" "}
                <Link to="/login" className="hover:text-primary">
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

export default ResetPasswordForm;
