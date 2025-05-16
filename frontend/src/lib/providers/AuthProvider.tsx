import React, {
  createContext,
  useState,
  useEffect,
  type ReactNode,
  useCallback,
} from "react";
import { useNavigate } from "react-router-dom";
import type {
  User,
  LoginCredentials,
  RegisterData,
  AuthContextType,
  TokenResponse,
  // UserDetails, // Nie potrzebujemy już UserDetails, jeśli nie ma fetchCurrentUserDetails
} from "@/lib/types/auth";
import {
  getApiUrl,
  setSessionTokens,
  clearSession,
  getAccessToken,
  getDecodedSessionData,
} from "@/lib/auth/session";
// import { apiClient } from "../api/client"; // Niepotrzebne, jeśli nie ma fetchCurrentUserDetails

export const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

// Usunięta funkcja fetchCurrentUserDetails, ponieważ polegamy na danych z tokena
// async function fetchCurrentUserDetails(): Promise<UserDetails | null> { ... }

export function AuthProvider({ children }: AuthProviderProps) {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<User | null>(null);
  const isAuthenticated = !!user && !!getAccessToken();

  useEffect(() => {
    async function initializeAuth() {
      setIsLoading(true);
      try {
        const decodedData = await getDecodedSessionData(); // Dane z tokena

        if (decodedData && decodedData.id) {
          // Mamy dane z tokena, ustawiamy użytkownika
          setUser({
            id: decodedData.id,
            email: decodedData.email,
            first_name: decodedData.first_name, // first_name jest już w decodedData
          });
          // Nie ma już wywołania fetchCurrentUserDetails
        } else {
          // Brak danych z tokena (lub token nieważny i nie udało się odświeżyć)
          // clearSession() jest wywoływane w getDecodedSessionData w razie problemów z tokenem
          setUser(null);
        }
      } catch (error) {
        console.error("Failed to initialize auth:", error);
        await clearSession(); // Na wszelki wypadek, choć getDecodedSessionData powinno to obsłużyć
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    }

    initializeAuth();
  }, []);

  const login = useCallback(
    async (credentials: LoginCredentials) => {
      setIsLoading(true);
      try {
        const response = await fetch(`${getApiUrl("/api/auth/login")}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: credentials.email,
            password: credentials.password,
          }),
        });

        if (!response.ok) {
          const errorData = await response
            .json()
            .catch(() => ({ detail: "Login request failed" }));
          throw new Error(errorData.detail || "Failed to login");
        }

        const tokenData = (await response.json()) as TokenResponse;
        await setSessionTokens(tokenData); // Zapisz tokeny

        // Po zapisaniu tokenów, getDecodedSessionData odczyta z nich dane użytkownika
        const decodedData = await getDecodedSessionData();

        if (decodedData && decodedData.id) {
          setUser({
            id: decodedData.id,
            email: decodedData.email,
            first_name: decodedData.first_name,
          });
          navigate("/dashboard");
        } else {
          // Powinno się to zdarzyć tylko jeśli token jest natychmiast nieważny
          // lub getDecodedSessionData zawiedzie z innego powodu
          await clearSession();
          setUser(null);
          throw new Error(
            "Login successful, but failed to decode user data from token.",
          );
        }
      } catch (error) {
        console.error("Login error:", error);
        await clearSession();
        setUser(null);
        if (error instanceof Error) {
          throw error;
        }
        throw new Error("Wystąpił nieznany błąd podczas logowania");
      } finally {
        setIsLoading(false);
      }
    },
    [navigate],
  );

  const logout = useCallback(async () => {
    setIsLoading(true);
    await clearSession();
    setUser(null);
    setIsLoading(false);
    navigate("/login");
  }, [navigate]);

  const register = useCallback(
    async (data: RegisterData) => {
      setIsLoading(true);
      try {
        const response = await fetch(`${getApiUrl("/api/auth/register")}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          const errorData = await response
            .json()
            .catch(() => ({ detail: "Registration request failed" }));
          throw new Error(errorData.detail || "Failed to register");
        }
        await login({ email: data.email, password: data.password });
      } catch (error) {
        console.error("Registration error:", error);
        if (error instanceof Error) {
          throw error;
        }
        throw new Error("Wystąpił nieznany błąd podczas rejestracji");
      } finally {
        setIsLoading(false);
      }
    },
    [login],
  );

  const resetPassword = useCallback(async (email: string) => {
    setIsLoading(true);
    try {
      // apiClient jest potrzebny tutaj, jeśli /api/auth/reset-password jest chronione
      // lub jeśli chcemy używać wspólnego klienta. Jeśli nie jest chronione, można użyć fetch.
      // Na razie zakładam, że apiClient byłby użyty, ale go zakomentowałem na górze.
      // Jeśli ten endpoint nie wymaga tokena, można użyć fetch.
      // Załóżmy, że na razie nie jest chroniony i użyjemy fetch
      await fetch(`${getApiUrl("/api/auth/reset-password")}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      // alert("If the email exists, a password reset link has been sent."); // Można dodać feedback
    } catch (error) {
      console.error("Reset password error:", error);
      // Można rzucić błąd dalej lub poinformować użytkownika
      // throw new Error("Failed to send password reset email.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  const value: AuthContextType = {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    resetPassword,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
