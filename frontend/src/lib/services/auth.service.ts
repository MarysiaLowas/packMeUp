import type {
  LoginCommand as LoginCredentials,
  RegisterUserCommand as RegisterData,
  UserDTO as User,
} from "@/types";

// Define a token interface that matches the backend response
interface Token {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  token_type: string;
}

const API_URL = import.meta.env.PUBLIC_API_URL || "http://localhost:8000";

export class AuthService {
  private static instance: AuthService;
  private accessToken: string | null = null;
  private refreshTimeout: NodeJS.Timeout | null = null;

  // Private constructor for singleton pattern
  private constructor() {
    // Intentionally empty: singleton initialization handled by getInstance
  }

  static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  private setAccessToken(token: Token) {
    this.accessToken = token.access_token;

    // Set up automatic token refresh
    if (this.refreshTimeout) {
      clearTimeout(this.refreshTimeout);
    }

    // Refresh token 1 minute before expiration
    const refreshIn = (token.expires_in - 60) * 1000;
    this.refreshTimeout = setTimeout(() => this.refreshToken(), refreshIn);
  }

  public getAccessToken(): string | null {
    return this.accessToken;
  }

  public async login(credentials: LoginCredentials): Promise<void> {
    const formData = new FormData();
    formData.append("username", credentials.email);
    formData.append("password", credentials.password);

    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Login failed");
    }

    const token = (await response.json()) as Token;
    this.setAccessToken(token);
  }

  public async register(data: RegisterData): Promise<User> {
    const response = await fetch(`${API_URL}/api/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Registration failed");
    }

    return response.json();
  }

  public async refreshToken(): Promise<void> {
    try {
      const response = await fetch(`${API_URL}/api/auth/refresh`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Token refresh failed");
      }

      const token = (await response.json()) as Token;
      this.setAccessToken(token);
    } catch (error) {
      console.error("Token refresh failed", error);
      // If refresh fails, clear token and redirect to login
      this.logout();
      window.location.href = "/login";
    }
  }

  public async logout(): Promise<void> {
    try {
      await fetch(`${API_URL}/api/auth/logout`, {
        method: "POST",
        headers: this.getAuthHeaders(),
      });
    } finally {
      // Clear local state regardless of logout request success
      this.accessToken = null;
      if (this.refreshTimeout) {
        clearTimeout(this.refreshTimeout);
        this.refreshTimeout = null;
      }
      window.location.href = "/login";
    }
  }

  public getAuthHeaders(): HeadersInit {
    return this.accessToken
      ? { Authorization: `Bearer ${this.accessToken}` }
      : {};
  }
}
