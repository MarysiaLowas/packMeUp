# Specyfikacja modułu autentykacji - PackMeUp

## 1. Architektura interfejsu użytkownika

### 1.1. Struktura stron i layoutów
- Utworzone zostaną dedykowane strony:
  - **/login** – strona logowania
  - **/register** – strona rejestracji
  - **/reset-password** – strona odzyskiwania hasła
  - **/logout** – endpoint wylogowania, który przekierowuje użytkownika do strony logowania lub strony głównej
- Wszystkie strony będą renderowane na bazie jednego layoutu Astro. Chcemy ograniczyć SSR do absolutnego minimum.

### 1.2. Komponenty klienta (React)
- Dynamiczne formularze zostaną zaimplementowane jako komponenty React:
  - **LoginForm**: pola - email, hasło; przycisk submit; link do odzyskiwania hasła.
  - **RegisterForm**: pola - email, imię, hasło, potwierdzenie hasła; mechanizmy walidacji (sprawdzenie poprawności formatu email, siły hasła, unikalności adresu email).
  - **ResetPasswordForm**: pole umożliwiające wpisanie adresu email do wysłania instrukcji resetu hasła.
- Komponenty odpowiedzialne będą za walidację po stronie klienta (np. format email, minimalna długość hasła) oraz prezentowanie komunikatów błędów otrzymanych z API.

### 1.3. Integracja z backendem
- Komponenty React komunikują się z backendowymi endpointami autentykacji (np. za pomocą fetch lub dedykowanej biblioteki HTTP).
- Backend, oparty na FastAPI, przetwarza żądania i zwraca odpowiedzi w formacie JSON z sukcesem lub z komunikatami błędów.
- W przypadku błędów walidacji, komunikaty te są przekazywane do komponentów React w celu wyświetlenia odpowiednich informacji użytkownikowi.

### 1.4. Scenariusze i walidacja
- **Rejestracja (US-001):**
  - Walidacja: poprawność adresu email, siła hasła (min. 8 znaków, mieszane wielkości liter, cyfry).
  - Obsługa błędów: komunikaty o błędach związane z duplikacją email lub nieprawidłowo sformatowanym hasłem.
- **Logowanie (US-002):**
  - Weryfikacja danych logowania; w przypadku niepowodzenia – komunikat "Nieprawidłowy email lub hasło".
- **Odzyskiwanie hasła (US-011):**
  - Formularz umożliwiający wprowadzenie adresu email; komunikat zatwierdzający wysłanie instrukcji resetowania hasła.
- **Wylogowanie (US-012):**
  - Wywołanie endpointu wylogowania, usunięcie sesji użytkownika i przekierowanie do strony logowania.

## 2. Logika backendowa

### 2.1. Struktura endpointów API
- **POST /api/auth/register** – rejestracja nowego użytkownika
- **POST /api/auth/login** – logowanie użytkownika
- **GET/POST /api/auth/logout** – wylogowanie użytkownika
- **POST /api/auth/reset-password** – inicjowanie procesu odzyskiwania hasła
- **POST /api/auth/reset-password/confirm** – potwierdzenie resetu hasła na podstawie tokenu

### 2.2. Modele danych i walidacja (Pydantic)
- Zdefiniowanie modeli Pydantic odpowiedzialnych za walidację wejściowych danych:
  - **UserCreate**: email, imię, hasło
  - **UserLogin**: email, hasło
  - **PasswordResetRequest**: email
  - **PasswordResetConfirm**: token, nowe hasło, potwierdzenie hasła
- Implementacja niestandardowej walidacji, np. dla siły hasła i poprawności formatu email.
- Wykorzystanie dependency injection FastAPI do zarządzania bazą danych (SQLAlchemy) oraz usługą wysyłki email.

### 2.3. Obsługa wyjątków
- Użycie HTTPException do zgłaszania błędów (np. 400 dla błędów walidacji, 401 dla nieautoryzowanych prób).
- Implementacja centralnych mechanizmów obsługi błędów (custom exception handlers), które logują błędy i zwracają czytelne komunikaty do klienta.

### 2.4. Renderowanie stron
- Należy ograniczyć SSR do absolutnego minimum. Zarządzanie stanem zalogowanego bądź niezalogowanego użytkownika powinno odbywać się w całości po stronie clienta.

## 3. System autentykacji

### 3.1. Mechanizm autentykacji
- Implementacja logiki autentykacji przy użyciu FastAPI:
  - Wykorzystanie JWT do zarządzania sesją użytkownika.
  - Dependency injection dla baz danych, logowania oraz usług dodatkowych (np. EmailService).
- Endpointy autentykacyjne korzystają z warstwy usług biznesowych (AuthService, UserService), które zarządzają logiką rejestracji, logowania, wylogowania oraz resetu hasła.

### 3.2. Proces rejestracji i logowania
- **Rejestracja:**
  - Użytkownik wypełnia formularz rejestracji, dane są walidowane przez backend.
  - System tworzy nowego użytkownika, hasło jest bezpiecznie hashowane, sprawdzana jest unikalność adresu email.
  - Po rejestracji użytkownik otrzymuje email potwierdzający rejestrację, zgodnie z wymogami RODO.
- **Logowanie:**
  - Użytkownik podaje dane (email, hasło), które są weryfikowane przez backend.
  - W przypadku pomyślnego logowania, generowany jest token sesyjny (JWT lub mechanizm oparty o cookies) i ustawiany mechanizm sesji.
- **Reset hasła:**
  - Użytkownik inicjuje proces resetu hasła poprzez podanie swojego adresu email.
  - System generuje token resetujący (ważny przez 24 godziny) i wysyła instrukcje na email użytkownika.
  - Po otrzymaniu tokenu, użytkownik przesyła nowe hasło, które jest następnie walidowane i zapisywane.
- **Wylogowanie:**
  - Endpoint wylogowania unieważnia sesję (token/cookies) i przekierowuje użytkownika do strony logowania.

### 3.3. Usługi i kontrakty
- **AuthService:** centralna logika obsługująca rejestrację, logowanie, reset hasła i wylogowanie.
- **UserService:** operacje na użytkownikach, weryfikacja unikalności adresu email, hash'owanie haseł.
- **EmailService:** usługa odpowiedzialna za wysyłkę wiadomości email (potwierdzenie rejestracji, instrukcje resetu hasła).
- Kontrakty API definiują dokładnie dane wejściowe i wyjściowe dla operacji autentykacyjnych, zapewniając spójność komunikacji między frontendem a backendem.

## Wnioski końcowe

System autentykacji w PackMeUp zostanie zrealizowany z podziałem na starannie rozdzielone warstwy frontendu i backendu. Warstwa front-endowa (Astro + React) odpowiada za renderowanie stron i dynamiczną obsługę formularzy, natomiast backend (FastAPI) odpowiada za logikę autentykacji, walidację danych oraz bezpieczeństwo komunikacji. Dzięki zastosowaniu dependency injection, Pydantic do walidacji oraz centralnej obsługi wyjątków, system będzie skalowalny, bezpieczny i łatwy w utrzymaniu, spełniając wymagania US-001, US-002, US-011 oraz US-012 przedstawione w dokumencie PRD. 