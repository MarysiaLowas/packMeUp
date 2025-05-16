import { AuthService } from "../services/auth.service";

export class AuthInterceptor {
  private static instance: AuthInterceptor;
  private authService: AuthService;

  private constructor() {
    this.authService = AuthService.getInstance();
  }

  public static getInstance(): AuthInterceptor {
    if (!AuthInterceptor.instance) {
      AuthInterceptor.instance = new AuthInterceptor();
    }
    return AuthInterceptor.instance;
  }

  public async fetch(
    input: RequestInfo | URL,
    init?: RequestInit,
  ): Promise<Response> {
    // Don't intercept auth endpoints
    if (
      typeof input === "string" &&
      (input.includes("/auth/login") ||
        input.includes("/auth/register") ||
        input.includes("/auth/refresh"))
    ) {
      return fetch(input, init);
    }

    // Add auth headers to request
    const headers = {
      ...init?.headers,
      ...this.authService.getAuthHeaders(),
    };

    try {
      const response = await fetch(input, { ...init, headers });

      // If unauthorized, try to refresh token
      if (response.status === 401) {
        try {
          await this.authService.refreshToken();

          // Retry original request with new token
          return fetch(input, {
            ...init,
            headers: {
              ...init?.headers,
              ...this.authService.getAuthHeaders(),
            },
          });
        } catch (error) {
          // If refresh fails, redirect to login
          window.location.href = "/login";
          throw error;
        }
      }

      return response;
    } catch (error) {
      // Handle network errors
      console.error("Request failed:", error);
      throw error;
    }
  }
}
