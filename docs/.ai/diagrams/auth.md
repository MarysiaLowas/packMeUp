<authentication_analysis>
Przepływy autentykacji:
1. Rejestracja:
   - Przeglądarka wysyła dane rejestracyjne przez Middleware do Astro API, które przekazuje je do FastAPI.
   - FastAPI waliduje dane, tworzy konto i wywołuje EmailService do wysłania emaila potwierdzającego.
   - Odpowiedź trafia z powrotem do przeglądarki informując o sukcesie rejestracji.
2. Logowanie:
   - Przeglądarka przesyła dane logowania przez Middleware i Astro API do FastAPI.
   - Po weryfikacji FastAPI generuje token sesji, który jest przesyłany z powrotem do przeglądarki.
3. Reset hasła:
   a. Inicjacja:
      - Przeglądarka wysyła żądanie resetu hasła (email) przez Middleware i Astro API do FastAPI.
      - FastAPI generuje token resetowania i wysyła email za pośrednictwem EmailService.
   b. Potwierdzenie:
      - Przeglądarka przesyła nowy password oraz token resetu do FastAPI przez Middleware i Astro API.
      - FastAPI weryfikuje token i aktualizuje hasło, a potwierdzenie trafia z powrotem do przeglądarki.
4. Wylogowanie:
   - Przeglądarka wysyła żądanie wylogowania, które jest przetwarzane przez FastAPI w celu unieważnienia sesji.
5. Odświeżanie tokenu:
   - W przypadku wygaśnięcia tokenu, przeglądarka wysyła żądanie odświeżenia tokenu.
   - FastAPI weryfikuje żądanie i generuje nowy token, który zostaje przesłany z powrotem.
</authentication_analysis>

<mermaid_diagram>
sequenceDiagram
    autonumber
    participant Browser as "Przeglądarka"
    participant Middleware as "Middleware"
    participant AstroAPI as "Astro API"
    participant FastAPI as "FastAPI"
    participant Email as "EmailService"
    
    %% Rejestracja
    Browser->>Middleware: Złożenie formularza rejestracji
    Middleware->>AstroAPI: Przekazanie danych rejestracji
    AstroAPI->>FastAPI: POST /api/auth/register
    activate FastAPI
    FastAPI-->>Email: Walidacja i tworzenie konta
    Email-->>FastAPI: Wysłanie emaila potwierdzającego
    FastAPI-->>AstroAPI: Potwierdzenie rejestracji
    deactivate FastAPI
    AstroAPI-->>Middleware: Odpowiedź rejestracyjna
    Middleware-->>Browser: Rejestracja pomyślna
        (Oczekuj na email potwierdzający)
    
    %% Logowanie
    Browser->>Middleware: Przesłanie danych logowania
    Middleware->>AstroAPI: Przekazanie danych logowania
    AstroAPI->>FastAPI: POST /api/auth/login
    activate FastAPI
    FastAPI-->>AstroAPI: Weryfikacja danych
        oraz generacja tokenu
    deactivate FastAPI
    AstroAPI-->>Middleware: Odpowiedź logowania (Token)
    Middleware-->>Browser: Logowanie pomyślne (Token)
    
    %% Reset hasła - inicjacja
    Browser->>Middleware: Żądanie resetu hasła (email)
    Middleware->>AstroAPI: Przekazanie żądania resetu hasła
    AstroAPI->>FastAPI: POST /api/auth/reset-password
    activate FastAPI
    FastAPI-->>Email: Wygenerowanie tokenu resetowania
    Email-->>FastAPI: Wysłanie emaila resetującego
    FastAPI-->>AstroAPI: Potwierdzenie resetu hasła
    deactivate FastAPI
    AstroAPI-->>Middleware: Odpowiedź resetu hasła
    Middleware-->>Browser: Email z instrukcjami resetu
    
    %% Reset hasła - potwierdzenie
    Browser->>Middleware: Przesłanie nowego hasła i tokenu resetu
    Middleware->>AstroAPI: Przekazanie potwierdzenia resetu
    AstroAPI->>FastAPI: POST /api/auth/reset-password/confirm
    activate FastAPI
    FastAPI-->>AstroAPI: Weryfikacja tokenu
        oraz aktualizacja hasła
    deactivate FastAPI
    AstroAPI-->>Middleware: Potwierdzenie zmiany hasła
    Middleware-->>Browser: Reset hasła pomyślny
    
    %% Wylogowanie
    Browser->>Middleware: Żądanie wylogowania
    Middleware->>AstroAPI: Przekazanie żądania wylogowania
    AstroAPI->>FastAPI: POST /api/auth/logout
    activate FastAPI
    FastAPI-->>AstroAPI: Unieważnienie sesji/tokenu
    deactivate FastAPI
    AstroAPI-->>Middleware: Potwierdzenie wylogowania
    Middleware-->>Browser: Wylogowanie pomyślne
    
    %% Odświeżanie tokenu
    Browser->>Middleware: Żądanie odświeżenia tokenu
        (Token wygasł)
    Middleware->>AstroAPI: Przekazanie żądania odświeżenia
    AstroAPI->>FastAPI: POST /api/auth/refresh-token
    activate FastAPI
    FastAPI-->>AstroAPI: Weryfikacja i generacja nowego tokenu
    deactivate FastAPI
    AstroAPI-->>Middleware: Nowy token
    Middleware-->>Browser: Token odświeżony
</sequenceDiagram>
</mermaid_diagram> 