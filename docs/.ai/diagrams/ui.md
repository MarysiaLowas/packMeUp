<architecture_analysis>
W niniejszej analizie przedstawiono strukturę UI modułu autentykacji:
1. Komponenty:
   • Guest Layout: Odpowiada za wyświetlanie stron dla niezalogowanych użytkowników (logowanie, rejestracja, resetowanie hasła).
   • Auth Layout: Używany dla zalogowanych użytkowników, zapewnia dostęp do chronionych funkcjonalności (nie uwzględniony w tym diagramie szczegółowo).
   • Strony autentykacji: 
       - Strona logowania (/login) zawiera LoginForm.
       - Strona rejestracji (/register) zawiera RegisterForm.
       - Strona resetowania hasła (/reset-password) zawiera ResetPasswordForm.
       - Endpoint wylogowania (/logout) odpowiedzialny za zakończenie sesji.
   • Komponenty formularzy (React):
       - LoginForm: Zawiera pola email i hasło, mechanizmy walidacji, przekazuje dane do endpointu logowania.
       - RegisterForm: Zawiera pola email, imię, hasło i potwierdzenie hasła, waliduje dane przed rejestracją.
       - ResetPasswordForm: Umożliwia wprowadzenie adresu email w celu rozpoczęcia procesu resetu hasła.
2. Strony są renderowane przez Astro, a dynamiczne formularze implementowane jako komponenty React.
3. Przepływ danych:
   - Użytkownik wprowadza dane w formularzach, które są przesyłane do backendowych endpointów (np. /api/auth/login, /api/auth/register, /api/auth/reset-password).
   - Odpowiedzi z API (np. AuthResponseDTO) aktualizują stan autentykacji aplikacji.
4. Komponenty współdzielone:
   - Button i Toast Notification, służą do interakcji i informowania użytkownika o wynikach akcji.
</architecture_analysis>

<mermaid_diagram>
flowchart TD
    subgraph "Moduł Autentykacji"
        subgraph "Guest Layout"
            LPage["Strona Logowania (/login)"]
            RPage["Strona Rejestracji (/register)"]
            PPage["Strona Resetowania Hasła (/reset-password)"]
        end
        LPage --> LF["LoginForm\n(Email, Hasło)"]
        RPage --> RF["RegisterForm\n(Email, Imię, Hasło, Potwierdzenie)"]
        PPage --> PF["ResetPasswordForm\n(Email)"]

        LF -- "Wysyła dane" --> API_L["API: POST /api/auth/login"]
        RF -- "Wysyła dane" --> API_R["API: POST /api/auth/register"]
        PF -- "Inicjuje reset" --> API_P["API: POST /api/auth/reset-password"]

        API_L --> LF_Response["AuthResponseDTO"]
        API_R --> RF_Response["UserCreate DTO"]
        API_P --> PF_Response["Status Response"]

        Logout["Wylogowanie (/logout)"]
    end

    subgraph "Komponenty Współdzielone"
        Btn["Button"]
        Toast["Toast Notification"]
    end

    LF --> Btn
    RF --> Btn
    PF --> Btn
    Btn --> Toast
</mermaid_diagram> 