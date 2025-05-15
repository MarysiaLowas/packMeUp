# Plan Testów dla Projektu PackMeUp

## 1. Wprowadzenie i cele testowania

PackMeUp to aplikacja webowa pomagająca użytkownikom efektywnie pakować się na wyjazdy poprzez generowanie spersonalizowanych list rzeczy do spakowania. Głównym celem testowania jest zapewnienie wysokiej jakości, stabilności oraz użyteczności aplikacji, ze szczególnym uwzględnieniem dokładności generowanych list pakowania oraz ogólnego doświadczenia użytkownika.

### Cele testowania:
- Weryfikacja poprawności działania funkcjonalności generowania list pakowania
- Zapewnienie responsywności i dostępności interfejsu użytkownika
- Potwierdzenie integralności danych między frontendem a backendem
- Sprawdzenie wydajności aplikacji pod różnym obciążeniem
- Weryfikacja bezpieczeństwa danych użytkownika

## 2. Zakres testów

### W zakresie:
- Interfejs użytkownika (frontend Astro z React)
- Logika biznesowa (generowanie list pakowania)
- API backend (FastAPI)
- Operacje bazodanowe (PostgreSQL, SQLAlchemy)
- Integracja z usługami AI (OpenRouter.ai)
- Mechanizmy uwierzytelniania i autoryzacji
- Dostępność i responsywność na różnych urządzeniach

### Poza zakresem:
- Testy infrastruktury CI/CD (GitHub Actions)
- Testy platformy hostingowej (Render)
- Testowanie zewnętrznych modeli AI (dostarczane przez OpenRouter.ai)

## 3. Typy testów do przeprowadzenia

### Testy jednostkowe
- **Frontend**: Testy komponentów React (React Testing Library)
- **Backend**: Testy funkcji i metod w FastAPI (pytest)
- **Pokrycie testami**: Cel minimalny 80% dla kluczowych komponentów

### Testy integracyjne
- Interakcje między frontendem a backendem
- Poprawność działania API
- Integracja z bazą danych
- Integracja z usługami AI

### Testy end-to-end
- Przepływ pracy użytkownika od rejestracji do wygenerowania listy pakowania
- Scenariusze wielokrokowe obejmujące pełny cykl użytkowania aplikacji

### Testy UI/UX
- Testy responsywności na różnych urządzeniach
- Testy dostępności (WCAG)
- Testy użyteczności z udziałem rzeczywistych użytkowników

### Testy wydajnościowe
- Testy obciążeniowe API
- Testy czasu odpowiedzi aplikacji
- Testy wydajności bazy danych

### Testy bezpieczeństwa
- Testy penetracyjne
- Testy ochrony danych
- Analiza kodu pod kątem podatności

## 4. Scenariusze testowe dla kluczowych funkcjonalności

### Generowanie list pakowania
1. **Weryfikacja generowania listy dla różnych typów podróży**
   - Precondition: Użytkownik jest zalogowany
   - Kroki:
     1. Wybierz typ podróży (biznesowa, wakacyjna, sportowa)
     2. Określ liczbę dni
     3. Wybierz uczestników
     4. Wybierz planowane aktywności
     5. Określ dostępną pojemność bagażu
     6. Wygeneruj listę
   - Oczekiwany rezultat: Lista dostosowana do wybranych parametrów

2. **Edycja wygenerowanej listy**
   - Precondition: Użytkownik ma wygenerowaną listę
   - Kroki:
     1. Usuń wybrany element z listy
     2. Dodaj własny element do listy
     3. Zmień kategorię elementu
     4. Zapisz zmiany
   - Oczekiwany rezultat: Lista jest zaktualizowana zgodnie z wprowadzonymi zmianami

### Zarządzanie kontem użytkownika
1. **Rejestracja nowego użytkownika**
   - Kroki:
     1. Przejdź do strony rejestracji
     2. Wprowadź dane (email, hasło)
     3. Potwierdź rejestrację
   - Oczekiwany rezultat: Konto zostaje utworzone, użytkownik otrzymuje potwierdzenie

2. **Logowanie i wylogowanie**
   - Kroki:
     1. Wprowadź dane logowania
     2. Kliknij przycisk logowania
     3. Wyloguj się
   - Oczekiwany rezultat: Użytkownik zostaje zalogowany i ma dostęp do funkcji aplikacji, po wylogowaniu dostęp jest ograniczony

### Integracja z AI
1. **Generowanie sugestii opartych na AI**
   - Precondition: Użytkownik wprowadził parametry podróży
   - Kroki:
     1. Zażądaj sugestii AI dla wybranych parametrów
     2. Poczekaj na odpowiedź
     3. Sprawdź sugestie
   - Oczekiwany rezultat: System zwraca sensowne i adekwatne do kontekstu sugestie

## 5. Środowisko testowe

### Środowisko deweloperskie
- Lokalne środowisko z kontenerami Docker
- Baza danych: PostgreSQL w kontenerze
- Mocking usług zewnętrznych (OpenRouter.ai)

### Środowisko testowe
- Dedykowana instancja na platformie Render
- Testowa baza danych
- Izolowane od produkcji klucze API do usług zewnętrznych

### Środowisko stagingowe
- Konfiguracja identyczna z produkcyjną
- Ograniczony dostęp dla zespołu testowego
- Pełna integracja ze wszystkimi usługami

## 6. Narzędzia do testowania

### Frontend
- Vitest / React Testing Library - testy jednostkowe komponentów React
- Playwright - testy end-to-end
- Lighthouse - testy wydajności i dostępności
- Storybook - testowanie izolowanych komponentów UI

### Backend
- pytest - testy jednostkowe i integracyjne
- pytest-cov - pokrycie kodu testami
- Postman/Newman - testy API
- Locust - testy obciążeniowe

### Baza danych
- pytest-postgresql - testowanie interakcji z bazą danych
- SQLAlchemy test fixtures - testowanie modeli i zapytań

### Monitoring i raportowanie
- GitHub Actions - automatyczne uruchamianie testów

## 7. Harmonogram testów

### Faza 1: Testy deweloperskie (równolegle z rozwojem)
- Testy jednostkowe pisane przez deweloperów
- Podstawowe testy integracyjne
- Czas trwania: Przez cały cykl rozwoju

### Faza 2: Alpha testing (po zakończeniu głównych funkcjonalności)
- Pełne testy integracyjne
- Pierwsze testy end-to-end
- Testy UI/UX
- Czas trwania: 2 tygodnie

### Faza 3: Beta testing (przed premierą)
- Testy z udziałem rzeczywistych użytkowników
- Testy wydajnościowe
- Testy bezpieczeństwa
- Czas trwania: 3 tygodnie

### Faza 4: Testy regresji (po każdej większej aktualizacji)
- Zautomatyzowane testy regresji
- Selektywne testy manualne
- Czas trwania: 1 tydzień po każdej aktualizacji

## 8. Kryteria akceptacji testów

### Kryteria ilościowe
- Pokrycie kodu testami: minimum 80% dla kodu produkcyjnego
- Wszystkie krytyczne ścieżki pokryte testami end-to-end
- Zero błędów o wysokim priorytecie
- Maksymalnie 5 błędów o średnim priorytecie
- Czas ładowania strony poniżej 2 sekund

### Kryteria jakościowe
- Wszystkie główne funkcjonalności działają zgodnie ze specyfikacją
- Interfejs użytkownika jest intuicyjny i przyjazny dla użytkowników
- Aplikacja działa poprawnie na wszystkich głównych przeglądarkach (Chrome, Firefox, Safari, Edge)
- Aplikacja jest responsywna na urządzeniach mobilnych i tabletach
- Generowane listy pakowania są praktyczne i dostosowane do podanych parametrów

## 9. Role i odpowiedzialności w procesie testowania

### Kierownik ds. jakości
- Nadzorowanie całego procesu testowania
- Zarządzanie zespołem testowym
- Raportowanie wyników testów interesariuszom

### Inżynierowie testów automatycznych
- Projektowanie i implementacja testów automatycznych
- Utrzymanie infrastruktury testowej
- Analiza wyników testów automatycznych

### Testerzy manualni
- Przeprowadzanie testów eksploracyjnych
- Weryfikacja napraw błędów
- Testowanie UX i dostępności

### Deweloperzy
- Pisanie i utrzymywanie testów jednostkowych
- Naprawianie zgłoszonych błędów
- Współpraca z testerami przy testach integracyjnych