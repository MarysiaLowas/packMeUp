import { getAccessToken } from "../auth/session";
import { getApiUrl } from "../auth/session";

interface ApiClientOptions extends RequestInit {
  skipAuth?: boolean;
  bodyFormat?: "json" | "form";
}

class ApiClient {
  private async fetch(
    path: string,
    options: ApiClientOptions = {},
  ): Promise<Response> {
    const {
      skipAuth = false,
      headers = {},
      bodyFormat = "json",
      ...rest
    } = options;
    const url = getApiUrl(path);

    const finalHeaders: Record<string, string> = {
      "Content-Type":
        bodyFormat === "json"
          ? "application/json"
          : "application/x-www-form-urlencoded",
      ...(headers as Record<string, string>),
    };

    if (!skipAuth) {
      const token = getAccessToken();
      if (token) {
        finalHeaders["Authorization"] = `Bearer ${token}`;
      }
    }

    const finalBody =
      bodyFormat === "json"
        ? JSON.stringify(rest.body)
        : rest.body instanceof URLSearchParams
          ? rest.body.toString()
          : new URLSearchParams(rest.body as Record<string, string>).toString();

    const response = await fetch(url, {
      headers: finalHeaders,
      body: finalBody,
      ...rest,
    });

    if (!response.ok) {
      const errorData = await response
        .json()
        .catch(() => ({ detail: "Unknown error" }));
      throw new Error(
        errorData.detail || `HTTP error! status: ${response.status}`,
      );
    }

    return response;
  }

  async get<T>(path: string, options: ApiClientOptions = {}): Promise<T> {
    const response = await this.fetch(path, {
      method: "GET",
      ...options,
    });

    return response.json();
  }

  async post<T>(
    path: string,
    data: Record<string, unknown>,
    options: ApiClientOptions = {},
  ): Promise<T> {
    const response = await this.fetch(path, {
      method: "POST",
      body: data,
      ...options,
    });

    return response.json();
  }

  async put<T>(
    path: string,
    data: Record<string, unknown>,
    options: ApiClientOptions = {},
  ): Promise<T> {
    const response = await this.fetch(path, {
      method: "PUT",
      body: data,
      ...options,
    });

    return response.json();
  }

  async delete<T>(path: string, options: ApiClientOptions = {}): Promise<T> {
    const response = await this.fetch(path, {
      method: "DELETE",
      ...options,
    });

    return response.json();
  }
}

export const apiClient = new ApiClient();
