<user_journey_analysis>
W niniejszej analizie przedstawiono podróż użytkownika dla modułu logowania i rejestracji:
1. Użytkownik rozpoczyna na stronie logowania jako niezalogowany.
2. Ze strony logowania użytkownik ma trzy opcje:
   - Wprowadzenie danych logowania (Proces Logowania).
   - Przejście do formularza rejestracji (Proces Rejestracji), gdzie po wprowadzeniu danych następuje walidacja i wysłanie emaila weryfikacyjnego, a następnie aktywacja konta po potwierdzeniu.
   - Skorzystanie z opcji "Zapomniałem hasła" (Proces Odzyskiwania), gdzie użytkownik resetuje hasło.
3. W procesie logowania, po poprawnym wprowadzeniu danych, użytkownik zostaje przekierowany do Dashboardu, a z poziomu Dashboardu może się wylogować, powracając do strony logowania.
</user_journey_analysis>

<mermaid_diagram>
```mermaid
stateDiagram-v2
    [*] --> StronaLogowania

    %% Opcje ze strony logowania
    StronaLogowania --> FormularzLogowania : Wprowadź dane logowania
    StronaLogowania --> FormularzRejestracji : Kliknij "Rejestracja"
    StronaLogowania --> FormularzOdzyskiwania : Kliknij "Zapomniałem hasła"

    %% Proces Logowania
    state "Proces Logowania" as PL {
        [*] --> FormularzLogowania
        FormularzLogowania --> WeryfikacjaDanych : Dane wprowadzone
        WeryfikacjaDanych --> LogowanieSukces : Dane poprawne
        WeryfikacjaDanych --> PowrotLogowania : Dane błędne
        LogowanieSukces --> [*]
        PowrotLogowania --> FormularzLogowania
    }

    %% Proces Rejestracji
    state "Proces Rejestracji" as PR {
        [*] --> FormularzRejestracji
        FormularzRejestracji --> WalidacjaDanych : Dane wprowadzone
        WalidacjaDanych --> WysłanieEmaila : Walidacja OK
        WysłanieEmaila --> OczekiwaniePotwierdzenia : Email wysłany
        OczekiwaniePotwierdzenia --> [*] : Email potwierdzony
    }

    %% Proces Odzyskiwania Hasła
    state "Proces Odzyskiwania" as PO {
        [*] --> FormularzOdzyskiwania
        FormularzOdzyskiwania --> WysłanieInstrukcji : Email wprowadzony
        WysłanieInstrukcji --> ResetHasla : Instrukcje wysłane
        ResetHasla --> [*] : Hasło zmienione
    }

    %% Przepływ po logowaniu
    LogowanieSukces --> Dashboard : Użytkownik zalogowany
    Dashboard --> Wylogowanie : Kliknij "Wyloguj"
    Wylogowanie --> StronaLogowania

    %% Powrót do strony logowania po rejestracji
    OczekiwaniePotwierdzenia --> StronaLogowania : Potwierdzenie email
```
</mermaid_diagram> 