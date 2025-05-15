<plan_testów>
# Plan Testów Projektu "Pack Me Up"

## 1. Wprowadzenie i Cele Testowania

### 1.1. Wprowadzenie

Niniejszy dokument opisuje plan testów dla aplikacji "Pack Me Up", systemu wspomagającego planowanie podróży poprzez generowanie spersonalizowanych list pakowania, w tym z wykorzystaniem sztucznej inteligencji. Projekt składa się z backendu opartego na FastAPI (Python) oraz frontendu zbudowanego przy użyciu Astro i React (TypeScript).

### 1.2. Cele Testowania

Główne cele procesu testowania to:

*   Weryfikacja, czy aplikacja spełnia zdefiniowane wymagania funkcjonalne i niefunkcjonalne.
*   Identyfikacja i zaraportowanie defektów w oprogramowaniu.
*   Zapewnienie wysokiej jakości, stabilności i niezawodności aplikacji przed wdrożeniem produkcyjnym.
*   Ocena użyteczności i satysfakcji użytkownika (UX).
*   Weryfikacja bezpieczeństwa aplikacji, zwłaszcza w kontekście danych użytkowników i integracji z zewnętrznymi API.
*   Potwierdzenie poprawnej integracji pomiędzy komponentami backendu i frontendu oraz z usługami zewnętrznymi (np. OpenRouter API).

## 2. Zakres Testów

### 2.1. Funkcjonalności objęte testami:

*   **Backend API:**
    *   Moduł uwierzytelniania i autoryzacji (rejestracja, logowanie, wylogowywanie, zarządzanie sesją, odświeżanie tokenów).
    *   Zarządzanie użytkownikami (tworzenie, odczyt, aktualizacja – jeśli dotyczy).
    *   Zarządzanie wycieczkami (CRUD dla wycieczek).
    *   Generowanie list pakowania (standardowe i wspomagane AI).
    *   Zarządzanie listami specjalnymi (CRUD dla list specjalnych).
    *   Poprawność odpowiedzi API (kody statusu, formaty danych, obsługa błędów).
    *   Walidacja danych wejściowych dla wszystkich endpointów.
*   **Frontend:**
    *   Interfejs użytkownika (UI) i doświadczenie użytkownika (UX) dla wszystkich stron i komponentów.
    *   Proces rejestracji, logowania i resetowania hasła.
    *   Panel użytkownika (Dashboard) – nawigacja, wyświetlanie danych.
    *   Proces tworzenia nowej wycieczki (formularz wieloetapowy, walidacja, zapis danych).
    *   Wyświetlanie i interakcja z wygenerowanymi listami pakowania.
    *   Wyświetlanie i zarządzanie listami specjalnymi.
    *   Responsywność interfejsu na różnych urządzeniach (desktop, tablet, mobile).
    *   Obsługa błędów i komunikatów dla użytkownika.
*   **Integracja:**
    *   Poprawność komunikacji między frontendem a backendem.
    *   Integracja z API OpenRouter (obsługa żądań, odpowiedzi, błędów).
    *   Integracja z bazą danych PostgreSQL (poprawność zapisywanych i odczytywanych danych).
*   **Bezpieczeństwo:**
    *   Ochrona przed podstawowymi atakami (np. XSS, SQL Injection – weryfikacja na poziomie frameworków).
    *   Poprawność mechanizmów autoryzacji (dostęp do zasobów tylko dla uprawnionych użytkowników).
    *   Bezpieczne przechowywanie haseł.
    *   Zarządzanie tokenami JWT.
*   **Wydajność (w ograniczonym zakresie):**
    *   Czas odpowiedzi kluczowych endpointów API.
    *   Czas ładowania głównych stron frontendu.
*   **Użyteczność:**
    *   Intuicyjność interfejsu.
    *   Łatwość nawigacji.
    *   Czytelność prezentowanych informacji.

### 2.2. Funkcjonalności nieobjęte testami (lub testowane w ograniczonym zakresie):

*   Zaawansowane testy penetracyjne (wymagają specjalistycznych narzędzi i wiedzy, mogą być realizowane przez zewnętrzny zespół).
*   Testy obciążeniowe na dużą skalę (początkowo skupimy się na podstawowych testach wydajności).
*   Dogłębne testy jakości generowanych przez AI treści pod kątem merytorycznym (skupimy się na poprawności technicznej integracji i podstawowej weryfikacji wyników).
*   Testy konfiguracji serwerów produkcyjnych (poza testami środowiska testowego).

## 3. Typy Testów do Przeprowadzenia

*   **Testy Jednostkowe (Unit Tests):**
    *   **Backend:** Testowanie poszczególnych funkcji, metod w serwisach, operacji CRUD, logiki modeli Pydantic. Wykorzystanie `pytest`. Mockowanie zależności (np. baza danych, zewnętrzne API).
    *   **Frontend:** Testowanie logiki pojedynczych komponentów React (np. `Vitest`), funkcji pomocniczych.
*   **Testy Integracyjne (Integration Tests):**
    *   **Backend:** Testowanie interakcji między komponentami backendu, np. między API a serwisami, serwisami a CRUD, CRUD a bazą danych (z wykorzystaniem testowej bazy danych). FastAPI `TestClient` będzie tu kluczowy. Testowanie middleware.
    *   **Frontend:** Testowanie interakcji między grupami komponentów, np. cały formularz tworzenia wycieczki, przepływ logowania. Mockowanie żądań API do backendu.
    *   **Backend-Frontend:** Weryfikacja poprawności kontraktów API i przepływu danych między frontendem a backendem.
*   **Testy End-to-End (E2E Tests):**
    *   Symulowanie rzeczywistych scenariuszy użytkownika przechodzących przez całą aplikację (od interfejsu frontendu, przez API backendu, aż po bazę danych i z powrotem). Wykorzystanie narzędzi takich jak `Playwright` lub `Cypress`.
*   **Testy API (API Tests):**
    *   Szczegółowe testowanie endpointów backendu pod kątem poprawności żądań, odpowiedzi, kodów statusu, walidacji, autoryzacji, obsługi błędów. Narzędzia: `Postman`, `Newman` (do automatyzacji) lub `pytest` z biblioteką `requests` / `httpx`.
*   **Testy Użyteczności (Usability Tests):**
    *   Ocena łatwości obsługi aplikacji, intuicyjności interfejsu. Może być realizowane poprzez testy korytarzowe lub dedykowane sesje z użytkownikami.
*   **Testy Bezpieczeństwa (Security Tests - podstawowe):**
    *   Weryfikacja poprawności implementacji mechanizmów uwierzytelniania i autoryzacji.
    *   Testowanie ochrony przed podstawowymi podatnościami (np. poprzez odpowiednie konfiguracje frameworków i bibliotek).
    *   Skanowanie zależności pod kątem znanych podatności (np. `pip-audit`, `npm audit`).
*   **Testy Wydajności (Performance Tests - podstawowe):**
    *   Pomiar czasu odpowiedzi kluczowych endpointów API pod umiarkowanym obciążeniem.
    *   Analiza czasu ładowania stron frontendu.
    *   Narzędzia: `locust` (dla backendu), narzędzia deweloperskie przeglądarki (dla frontendu).
*   **Testy Akceptacyjne Użytkownika (UAT - User Acceptance Tests):**
    *   Przeprowadzane przez interesariuszy lub wyznaczoną grupę użytkowników w celu potwierdzenia, że aplikacja spełnia ich oczekiwania i potrzeby biznesowe.
*   **Testy Kompatybilności (Compatibility Tests):**
    *   Sprawdzenie działania frontendu na różnych przeglądarkach (Chrome, Firefox, Safari, Edge - najnowsze wersje) i potencjalnie na różnych systemach operacyjnych.
*   **Testy Instalacji/Deploymentu:**
    *   Weryfikacja poprawności procesu budowania i wdrażania aplikacji na środowisku testowym. Sprawdzenie poprawności działania skryptów migracyjnych Alembic.

## 4. Scenariusze Testowe dla Kluczowych Funkcjonalności

Poniżej przedstawiono przykładowe, wysokopoziomowe scenariusze testowe. Szczegółowe przypadki testowe zostaną opracowane na ich podstawie.

### 4.1. Rejestracja i Logowanie Użytkownika

*   **Scenariusz 1.1: Poprawna rejestracja nowego użytkownika.**
    *   Kroki: Użytkownik podaje poprawne dane (email, hasło, powtórzone hasło). System tworzy konto, użytkownik może się zalogować.
    *   Oczekiwany rezultat: Konto utworzone, użytkownik zalogowany, przekierowany do panelu.
*   **Scenariusz 1.2: Próba rejestracji z istniejącym adresem email.**
    *   Kroki: Użytkownik próbuje zarejestrować się z emailem, który już istnieje w systemie.
    *   Oczekiwany rezultat: Wyświetlenie odpowiedniego komunikatu błędu, konto nie jest tworzone.
*   **Scenariusz 1.3: Poprawne logowanie istniejącego użytkownika.**
    *   Kroki: Użytkownik podaje poprawny email i hasło.
    *   Oczekiwany rezultat: Użytkownik zalogowany, przekierowany do panelu.
*   **Scenariusz 1.4: Próba logowania z błędnym hasłem/emailem.**
    *   Kroki: Użytkownik podaje niepoprawne dane logowania.
    *   Oczekiwany rezultat: Wyświetlenie komunikatu o błędnych danych, użytkownik nie jest logowany.
*   **Scenariusz 1.5: Wylogowanie użytkownika.**
    *   Kroki: Zalogowany użytkownik klika przycisk "Wyloguj".
    *   Oczekiwany rezultat: Sesja użytkownika zakończona, użytkownik przekierowany na stronę logowania, zabezpieczone trasy niedostępne.

### 4.2. Tworzenie Nowej Wycieczki

*   **Scenariusz 2.1: Poprawne utworzenie nowej wycieczki (wszystkie kroki formularza).**
    *   Kroki: Użytkownik przechodzi przez wszystkie etapy formularza, podając poprawne dane (informacje podstawowe, preferencje, bagaż).
    *   Oczekiwany rezultat: Wycieczka zostaje utworzona i zapisana w systemie, użytkownik widzi potwierdzenie lub listę pakowania.
*   **Scenariusz 2.2: Próba przejścia do następnego kroku z niekompletnymi/błędnymi danymi.**
    *   Kroki: Użytkownik pomija wymagane pola lub wprowadza niepoprawne dane na jednym z etapów.
    *   Oczekiwany rezultat: Wyświetlenie komunikatów walidacyjnych, brak możliwości przejścia do kolejnego kroku.
*   **Scenariusz 2.3: Nawigacja wstecz w formularzu tworzenia wycieczki.**
    *   Kroki: Użytkownik cofa się do poprzednich kroków formularza.
    *   Oczekiwany rezultat: Wcześniej wprowadzone dane są zachowane i poprawnie wyświetlane.
*   **Scenariusz 2.4: Anulowanie tworzenia wycieczki.**
    *   Kroki: Użytkownik rezygnuje z tworzenia wycieczki w trakcie wypełniania formularza.
    *   Oczekiwany rezultat: Dane nie są zapisywane, użytkownik wraca do poprzedniego widoku.

### 4.3. Generowanie i Wyświetlanie Listy Pakowania

*   **Scenariusz 3.1: Generowanie listy pakowania na podstawie danych wycieczki (bez AI).**
    *   Kroki: Użytkownik tworzy wycieczkę, system generuje podstawową listę pakowania.
    *   Oczekiwany rezultat: Lista zawiera oczekiwane elementy bazujące na wprowadzonych danych.
*   **Scenariusz 3.2: Generowanie listy pakowania z wykorzystaniem AI.**
    *   Kroki: Użytkownik tworzy wycieczkę, system wysyła zapytanie do OpenRouter API i generuje listę.
    *   Oczekiwany rezultat: Lista zawiera elementy sugerowane przez AI, integracja z API przebiegła poprawnie.
*   **Scenariusz 3.3: Obsługa błędów podczas generowania listy przez AI (np. niedostępność OpenRouter API).**
    *   Kroki: Symulacja błędu odpowiedzi z OpenRouter API.
    *   Oczekiwany rezultat: System informuje użytkownika o problemie i/lub generuje listę awaryjną (jeśli zaimplementowano).
*   **Scenariusz 3.4: Interakcja z listą pakowania (odhaczanie elementów, dodawanie/usuwanie własnych).**
    *   Kroki: Użytkownik modyfikuje wygenerowaną listę.
    *   Oczekiwany rezultat: Zmiany są poprawnie zapisywane i odzwierciedlane w UI.

### 4.4. Zarządzanie Listami Specjalnymi

*   **Scenariusz 4.1: Tworzenie, edycja i usuwanie listy specjalnej.**
    *   Kroki: Użytkownik wykonuje operacje CRUD na listach specjalnych.
    *   Oczekiwany rezultat: Listy są poprawnie tworzone, aktualizowane i usuwane z systemu i UI.
*   **Scenariusz 4.2: Wykorzystanie listy specjalnej podczas tworzenia wycieczki.**
    *   Kroki: Użytkownik wybiera elementy z listy specjalnej do dołączenia do listy pakowania wycieczki.
    *   Oczekiwany rezultat: Wybrane elementy są poprawnie dodawane do listy pakowania.

## 5. Środowisko Testowe

*   **Backend:**
    *   **System operacyjny:** Linux (preferowany, zgodny ze środowiskiem produkcyjnym), macOS, Windows (dla deweloperów).
    *   **Python:** Wersja >=3.10 (zgodnie z `pyproject.toml`).
    *   **Baza danych:** Dedykowana instancja PostgreSQL dla testów, z możliwością resetowania danych.
    *   **Serwer ASGI:** Uvicorn (do lokalnych testów i developmentu).
    *   **Zmienne środowiskowe:** Skonfigurowane `.env` dla środowiska testowego, w tym mockowane lub testowe klucze API (np. dla OpenRouter).
*   **Frontend:**
    *   **Przeglądarki:** Najnowsze wersje Chrome, Firefox, Safari, Edge.
    *   **Node.js/npm/yarn:** Wersje zgodne z `frontend/package.json` i `.nvmrc`.
*   **Narzędzia:**
    *   System kontroli wersji: Git.
    *   Środowisko CI/CD (np. GitHub Actions, GitLab CI) do automatycznego uruchamiania testów.
*   **Dane testowe:**
    *   Przygotowany zestaw danych testowych dla użytkowników, wycieczek, preferencji, aby umożliwić powtarzalne i spójne testy.

## 6. Narzędzia do Testowania

*   **Backend:**
    *   **Testy jednostkowe/integracyjne API:** `pytest` z wtyczkami (`pytest-asyncio`, `pytest-cov`), FastAPI `TestClient`.
    *   **Mockowanie:** `unittest.mock`.
    *   **Testy wydajności API:** `locust`.
    *   **Linting/Static Analysis:** Ruff, Mypy, Black (już w projekcie).
*   **Frontend:**
    *   **Testy jednostkowe/integracyjne komponentów:** `Jest`, `React Testing Library`.
    *   **Testy E2E:** `Playwright` lub `Cypress`.
    *   **Linting/Static Analysis:** ESLint, Prettier (Astro/React).
    *   **Narzędzia deweloperskie przeglądarek:** Do debugowania i analizy wydajności.
*   **Ogólne:**
    *   **Zarządzanie testami:** `TestRail`, `Xray` (jeśli budżet pozwala) lub prostsze rozwiązania jak arkusze kalkulacyjne/Markdown.
    *   **Zarządzanie błędami:** `Jira`, `Trello`, `GitHub Issues`.
    *   **Automatyzacja testów API (opcjonalnie):** `Postman` z `Newman`.
    *   **Dokumentacja API:** `Swagger UI` / `Redoc` (generowane przez FastAPI).

## 7. Harmonogram Testów

Harmonogram będzie ściśle powiązany z harmonogramem deweloperskim i kolejnymi sprintami/iteracjami. Ogólny zarys:

*   **Faza 1: Planowanie i przygotowanie (początek projektu/sprintu)**
    *   Analiza wymagań i specyfikacji.
    *   Tworzenie/aktualizacja planu testów.
    *   Przygotowanie środowiska testowego i danych testowych.
    *   Definiowanie szczegółowych przypadków testowych.
*   **Faza 2: Wykonanie testów (równolegle z developmentem)**
    *   Testy jednostkowe i integracyjne (deweloperzy i QA).
    *   Testy API (QA).
    *   Testy E2E (QA - dla stabilnych części aplikacji).
    *   Testy eksploracyjne (QA).
*   **Faza 3: Testy regresji (przed każdym wydaniem/wdrożeniem)**
    *   Uruchomienie zautomatyzowanego zestawu testów regresji.
    *   Manualne testy kluczowych ścieżek.
*   **Faza 4: Testy akceptacyjne (UAT - przed wdrożeniem produkcyjnym)**
    *   Udostępnienie wersji testowej dla interesariuszy.
*   **Faza 5: Testy post-wdrożeniowe (po wdrożeniu na produkcję)**
    *   Testy dymne (smoke tests) na środowisku produkcyjnym.

Każdy sprint/iteracja będzie obejmować cykl testowania nowych funkcjonalności oraz testy regresji dla istniejących.

## 8. Kryteria Akceptacji Testów

### 8.1. Kryteria wejścia (rozpoczęcia testów):

*   Dostępna dokumentacja funkcjonalna/techniczna dla testowanych modułów.
*   Oprogramowanie dostarczone do środowiska testowego.
*   Środowisko testowe skonfigurowane i gotowe do użycia.
*   Ukończone testy jednostkowe przez deweloperów (dla nowych funkcjonalności).
*   Zdefiniowane i zatwierdzone przypadki testowe (dla testów formalnych).

### 8.2. Kryteria wyjścia (zakończenia testów):

*   **Poziom krytyczny (Release Candidate):**
    *   100% zdefiniowanych przypadków testowych dla kluczowych funkcjonalności (P0, P1) wykonanych i zakończonych sukcesem.
    *   Brak otwartych błędów krytycznych (blokujących) i wysokiego priorytetu.
    *   Wszystkie zidentyfikowane błędy średniego priorytetu przeanalizowane; te, które nie zostaną naprawione, muszą być zaakceptowane przez Product Ownera.
    *   Zestaw testów regresji wykonany i zakończony sukcesem.
    *   Dokumentacja testowa (raporty z testów, lista znanych błędów) przygotowana.
*   **Poziom akceptowalny (np. dla wersji Alfa/Beta):**
    *   Minimum 80-90% przypadków testowych dla kluczowych funkcjonalności wykonanych.
    *   Brak otwartych błędów krytycznych.
    *   Znane błędy wysokiego priorytetu mają zaplanowane rozwiązanie.
