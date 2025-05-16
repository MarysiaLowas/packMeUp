import { jwtDecode } from "jwt-decode";

// Constants for localStorage keys
const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";

// Użyj import.meta.env dla zmiennych środowiskowych w Astro po stronie klienta
const API_URL = import.meta.env.PUBLIC_API_URL || "http://localhost:8000";

// Check if we're in a browser environment
const isBrowser = typeof window !== "undefined";

export function getApiUrl(path: string): string {
  return `${API_URL}${path}`;
}

// Zaktualizowany typ Session, aby pasował do struktury User i tego, co jest w tokenie
// JWTPayload będzie źródłem prawdy dla tych pól.
export interface DecodedSessionData {
  id: string; // Odpowiada 'sub' w JWTPayload
  email: string;
  first_name: string | null; // Odpowiada 'firstName' w JWTPayload, może być null
  // Można dodać inne pola, jeśli są w tokenie, np. role
}

interface JWTPayload {
  sub: string; // User ID
  email: string;
  exp: number;
  first_name?: string | null; // Zmieniono z firstName na first_name
  // Można dodać inne niestandardowe pola, które są w tokenie
}

export function setAccessToken(token: string) {
  if (!isBrowser) return;
  // console.log("[Auth] Setting access token:", token.substring(0, 10) + "...");
  localStorage.setItem(ACCESS_TOKEN_KEY, token);
}

export function setRefreshToken(token: string) {
  if (!isBrowser) return;
  // console.log("[Auth] Setting refresh token");
  localStorage.setItem(REFRESH_TOKEN_KEY, token);
}

export function clearAccessToken() {
  if (!isBrowser) return;
  // console.log("[Auth] Clearing access token");
  localStorage.removeItem(ACCESS_TOKEN_KEY);
}

export function clearRefreshToken() {
  if (!isBrowser) return;
  // console.log("[Auth] Clearing refresh token");
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

export function getAccessToken(): string | null {
  if (!isBrowser) return null;
  const token = localStorage.getItem(ACCESS_TOKEN_KEY);
  // console.log("[Auth] Getting access token:", token ? "exists" : "null");
  return token;
}

export function getRefreshToken(): string | null {
  if (!isBrowser) return null;
  const token = localStorage.getItem(REFRESH_TOKEN_KEY);
  // console.log("[Auth] Getting refresh token:", token ? "exists" : "null");
  return token;
}

async function refreshAccessToken(): Promise<string | null> {
  // console.log("[Auth] Attempting to refresh token");
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    // console.log("[Auth] No refresh token available");
    return null;
  }

  try {
    // console.log("[Auth] Making request to:", getApiUrl("/api/auth/refresh"));
    const response = await fetch(getApiUrl("/api/auth/refresh"), {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer \${refreshToken}`,
      },
    });

    // console.log("[Auth] Refresh token response status:", response.status);

    if (!response.ok) {
      const errorData = await response
        .json()
        .catch(() => ({ detail: "Failed to refresh token" }));
      console.error("[Auth] Refresh token error:", errorData);
      // Nie czyścimy tokenów tutaj, getSession zdecyduje
      return null;
    }

    const data = await response.json();
    // console.log("[Auth] Refresh token success, new token received");
    setAccessToken(data.access_token);
    if (data.refresh_token) {
      setRefreshToken(data.refresh_token);
    }
    return data.access_token;
  } catch (error) {
    console.error("[Auth] Failed to refresh token:", error);
    return null;
  }
}

function isTokenExpired(token: string): boolean {
  try {
    const decoded = jwtDecode<JWTPayload>(token);
    const currentTime = Math.floor(Date.now() / 1000);
    const isExpired = decoded.exp < currentTime;
    // console.log("[Auth] Token expiration check:", {
    //   exp: new Date(decoded.exp * 1000).toISOString(),
    //   now: new Date(currentTime * 1000).toISOString(),
    //   isExpired,
    // });
    return isExpired;
  } catch {
    // console.log("[Auth] Failed to decode token for expiration check");
    return true; // If decoding fails, treat as expired
  }
}

// Zwraca dane zdekodowane z tokena, lub null jeśli token jest nieważny/brak
export async function getDecodedSessionData(): Promise<DecodedSessionData | null> {
  // console.log("[Auth] Getting decoded session data");
  let token = getAccessToken();
  // console.log("[Auth] Current token status:", token ? "exists" : "null");

  const isClient = typeof window !== "undefined";

  if (isClient && (!token || isTokenExpired(token))) {
    // console.log("[Auth] Token missing or expired on client, attempting refresh");
    token = await refreshAccessToken();
    if (!token) {
      // console.log("[Auth] Failed to refresh token, no session data");
      clearAccessToken(); // Wyczyść stary/nieważny token
      clearRefreshToken(); // Jeśli refresh zawiódł, stary refresh token też może być zły
      return null;
    }
  }

  if (!token) {
    // console.log("[Auth] No token available after potential refresh");
    return null;
  }

  try {
    const decoded = jwtDecode<JWTPayload>(token);
    // console.log("[Auth] Successfully decoded token for user:", decoded.email);

    return {
      id: decoded.sub,
      email: decoded.email,
      first_name: decoded.first_name || null, // Używamy teraz decoded.first_name
    };
  } catch (error) {
    console.error("[Auth] Failed to decode token:", error);
    clearAccessToken(); // Token jest zły, wyczyść go
    // Niekoniecznie czyścimy refresh token tutaj, refreshAccessToken powinien to obsłużyć
    return null;
  }
}

// Funkcja setSession będzie przyjmować tylko tokeny, zgodnie z jej obecną strukturą
// AuthProvider będzie odpowiedzialny za zarządzanie pełnym obiektem User
export async function setSessionTokens(tokenData: {
  access_token: string;
  refresh_token: string;
  // expires_in: number; // expires_in nie jest bezpośrednio używane przez localStorage session
}): Promise<void> {
  // console.log("[Auth] Setting new session tokens");
  setAccessToken(tokenData.access_token);
  setRefreshToken(tokenData.refresh_token);
}

export async function clearSession(): Promise<void> {
  // console.log("[Auth] Clearing session");
  const token = getAccessToken(); // Pobierz token przed wyczyszczeniem, aby wysłać go do /logout
  try {
    if (token && isBrowser) {
      // Wyślij żądanie wylogowania tylko jeśli jest token i jesteśmy w przeglądarce
      await fetch(getApiUrl("/api/auth/logout"), {
        method: "POST",
        headers: {
          // Akceptacja nie jest potrzebna dla POST bez ciała, Content-Type też nie, jeśli ciało jest puste
          Authorization: `Bearer \${token}`,
        },
      });
      // console.log("[Auth] Logout API request potentially successful");
    }
  } catch (error) {
    console.error("[Auth] Logout API call failed:", error);
    // Niezależnie od błędu API, kontynuuj czyszczenie lokalne
  } finally {
    clearAccessToken();
    clearRefreshToken();
    // Dodatkowo można wyczyścić inne dane związane z sesją użytkownika, jeśli są przechowywane
    // np. localStorage.removeItem(USER_DETAILS_KEY);
  }
}

// Zmieniam nazwę getSession na getDecodedSessionData, aby było jasne, że zwraca tylko to co z tokena.
// Stara funkcja getSession jest teraz getDecodedSessionData
// Jeśli potrzebna jest stara sygnatura dla AuthProvider, AuthProvider będzie musiał wywołać getDecodedSessionData.
// Na razie usuwam starą getSession, żeby uniknąć konfliktu. Możemy ją przywrócić jako alias jeśli trzeba.
