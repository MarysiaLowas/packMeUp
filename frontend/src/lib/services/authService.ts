import type {
  LoginCredentials,
  RegisterData,
  AuthResponse,
} from "../types/auth";
import Cookies from "js-cookie";

const API_URL = import.meta.env.PUBLIC_API_URL || "";

class AuthService {
  private static TOKEN_KEY = "auth_token";

  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
      credentials: "include",
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Błąd logowania");
    }

    const data = await response.json();
    this.setToken(data.access_token);
    return data;
  }

  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await fetch(`${API_URL}/api/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
      credentials: "include",
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Błąd rejestracji");
    }

    const responseData = await response.json();
    this.setToken(responseData.access_token);
    return responseData;
  }

  async logout(): Promise<void> {
    try {
      await fetch(`${API_URL}/api/auth/logout`, {
        method: "POST",
        credentials: "include",
      });
    } finally {
      this.removeToken();
    }
  }

  async resetPassword(email: string): Promise<void> {
    const response = await fetch(`${API_URL}/api/auth/reset-password`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email }),
      credentials: "include",
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Błąd resetowania hasła");
    }
  }

  getToken(): string | null {
    if (typeof window === "undefined") {
      // Jesteśmy na serwerze
      return null;
    }
    const token = Cookies.get(AuthService.TOKEN_KEY);
    return token || null;
  }

  private setToken(token: string): void {
    if (typeof window !== "undefined") {
      // Jesteśmy w przeglądarce
      Cookies.set(AuthService.TOKEN_KEY, token, {
        expires: 7, // Token wygasa po 7 dniach
        sameSite: "strict",
        secure: true,
      });
    }
  }

  private removeToken(): void {
    if (typeof window !== "undefined") {
      // Jesteśmy w przeglądarce
      Cookies.remove(AuthService.TOKEN_KEY);
    }
  }
}

export const authService = new AuthService();
