# Architektura UI dla PackMeUp

## 1. Przegląd struktury UI

Architektura interfejsu użytkownika (UI) dla aplikacji PackMeUp została zaprojektowana w celu zapewnienia intuicyjnej i efektywnej obsługi kluczowych funkcjonalności: zarządzania kontem użytkownika, tworzenia spersonalizowanych list pakowania za pomocą ankiet i AI, zarządzania własnymi listami specjalnymi oraz śledzenia postępów pakowania. System opiera się na podejściu mobile-first, wykorzystując nowoczesne technologie takie jak React, TypeScript, Tailwind CSS oraz bibliotekę komponentów Shadcn/ui. Nawigacja jest prosta i scentralizowana, a przepływy użytkownika zoptymalizowane pod kątem minimalizacji kroków potrzebnych do osiągnięcia celu. Nacisk położono na jasny, minimalistyczny design z elementami seledynowymi/miętowymi, responsywność oraz dostarczanie użytkownikowi informacji zwrotnej poprzez notyfikacje toast i wskaźniki ładowania.

## 2. Lista widoków

Poniżej znajduje się lista kluczowych widoków aplikacji wraz z ich celami, informacjami i komponentami.

---

### 2.1. Strona Główna / Landing Page (Publiczny)
-   **Nazwa widoku:** Strona Główna
-   **Ścieżka widoku:** `/` (jeśli użytkownik nie jest zalogowany, inaczej `/dashboard`)
-   **Główny cel:** Przedstawienie aplikacji PackMeUp i zachęcenie do rejestracji lub logowania.
-   **Kluczowe informacje do wyświetlenia:**
    -   Nazwa i logo aplikacji.
    -   Krótki opis wartości aplikacji (np. "Pakuj się mądrze, podróżuj lekko").
    -   Główne korzyści.
-   **Kluczowe komponenty widoku:**
    -   Sekcja "Hero" z chwytliwym hasłem.
    -   Przyciski CTA: "Zarejestruj się", "Zaloguj się" (komponenty `Button` Shadcn/ui).
-   **UX, dostępność i względy bezpieczeństwa:**
    -   UX: Jasny i zachęcający design, szybkie przejście do akcji.
    -   Dostępność: Podstawowa, wynikająca z użytych komponentów.
    -   Bezpieczeństwo: Widok publiczny, brak przetwarzania wrażliwych danych.

---

### 2.2. Logowanie (Publiczny)
-   **Nazwa widoku:** Logowanie
-   **Ścieżka widoku:** `/login`
-   **Główny cel:** Umożliwienie istniejącym użytkownikom zalogowania się do aplikacji.
-   **Kluczowe informacje do wyświetlenia:**
    -   Formularz logowania.
    -   Link do strony rejestracji.
    -   Link do strony odzyskiwania hasła.
-   **Kluczowe komponenty widoku:**
    -   `Card` z `CardHeader` ("Logowanie"), `CardContent` (formularz), `CardFooter` (linki).
    -   Formularz: `Label` i `Input` dla adresu e-mail i hasła.
    -   Przycisk `Button` "Zaloguj się".
    -   Komunikaty o błędach (`Alert` lub `Toast`).
-   **UX, dostępność i względy bezpieczeństwa:**
    -   UX: Prosty i szybki proces logowania. Wyraźne komunikaty o błędach.
    -   Dostępność: Poprawne etykietowanie pól formularza.
    -   Bezpieczeństwo: Przesyłanie danych formularza przez HTTPS. API endpoint: `POST /api/auth/login`.

---

### 2.3. Rejestracja (Publiczny)
-   **Nazwa widoku:** Rejestracja
-   **Ścieżka widoku:** `/register`
-   **Główny cel:** Umożliwienie nowym użytkownikom założenia konta w aplikacji.
-   **Kluczowe informacje do wyświetlenia:**
    -   Formularz rejestracyjny.
    -   Wymagania dotyczące hasła.
    -   Link do strony logowania.
    -   Informacje o zgodzie na przetwarzanie danych (RODO).
-   **Kluczowe komponenty widoku:**
    -   `Card` z formularzem rejestracyjnym.
    -   Formularz: `Label` i `Input` dla imienia, adresu e-mail, hasła, potwierdzenia hasła.
    -   `Checkbox` dla zgód RODO.
    -   Przycisk `Button` "Zarejestruj się".
    -   Komunikaty o błędach/sukcesie.
-   **UX, dostępność i względy bezpieczeństwa:**
    -   UX: Jasno określone wymagania, walidacja na bieżąco.
    -   Dostępność: Poprawne etykietowanie pól i informacji o wymaganiach.
    -   Bezpieczeństwo: Przesyłanie danych przez HTTPS. Weryfikacja unikalności emaila. API endpoint: `POST /api/auth/register`.

---

### 2.4. Zapomniałem Hasła (Publiczny)
-   **Nazwa widoku:** Zapomniałem Hasła
-   **Ścieżka widoku:** `/forgot-password`
-   **Główny cel:** Inicjacja procesu odzyskiwania zapomnianego hasła.
-   **Kluczowe informacje do wyświetlenia:**
    -   Formularz do wprowadzenia adresu e-mail.
    -   Instrukcje dotyczące dalszych kroków.
-   **Kluczowe komponenty widoku:**
    -   `Card` z formularzem.
    -   Formularz: `Label` i `Input` dla adresu e-mail.
    -   Przycisk `Button` "Wyślij link do resetowania hasła".
-   **UX, dostępność i względy bezpieczeństwa:**
    -   UX: Prosty proces, jasne instrukcje.
    -   Bezpieczeństwo: API endpoint: `POST /api/auth/forgot-password`. Link resetujący wysyłany na email.

---

### 2.5. Resetowanie Hasła (Publiczny)
-   **Nazwa widoku:** Resetowanie Hasła
-   **Ścieżka widoku:** `/reset-password/:token`
-   **Główny cel:** Umożliwienie użytkownikowi ustawienia nowego hasła po przejściu procedury odzyskiwania.
-   **Kluczowe informacje do wyświetlenia:**
    -   Formularz do wprowadzenia nowego hasła i jego potwierdzenia.
    -   Wymagania dotyczące nowego hasła.
-   **Kluczowe komponenty widoku:**
    -   `Card` z formularzem.
    -   Formularz: `Label` i `Input` dla nowego hasła i jego potwierdzenia.
    -   Przycisk `Button` "Ustaw Nowe Hasło".
-   **UX, dostępność i względy bezpieczeństwa:**
    -   UX: Zapewnienie, że użytkownik wie, iż token jest ważny.
    -   Bezpieczeństwo: Token weryfikowany po stronie serwera. API endpoint: `POST /api/auth/reset-password`.

---

### 2.6. Dashboard (Prywatny)
-   **Nazwa widoku:** Dashboard / Panel Główny
-   **Ścieżka widoku:** `/dashboard` lub `/` (po zalogowaniu)
-   **Główny cel:** Centralny punkt nawigacyjny po zalogowaniu, wyświetlanie przeglądu aktywności (ostatnie listy pakowania) i inicjowanie nowych działań.
-   **Kluczowe informacje do wyświetlenia:**
    -   Przegląd ostatnio wygenerowanych list pakowania (np. nazwa, cel podróży, data).
    -   Wyraźnie widoczny przycisk CTA do tworzenia nowej podróży/ankiety.
    -   Stan pusty, jeśli użytkownik nie ma jeszcze żadnych list.
-   **Kluczowe komponenty widoku:**
    -   Nagłówek np. "Witaj, [Imię Użytkownika]!" lub "Twoje Listy Pakowania".
    -   Główny przycisk `Button` (np. "Stwórz Nową Podróż" lub "Rozpocznij Ankietę").
    -   Sekcja list: lista komponentów `Card`, każdy reprezentujący wygenerowaną listę, z linkiem do jej szczegółów.
    -   Komponent stanu pustego z CTA.
    -   `Skeleton` loader podczas ładowania list.
-   **UX, dostępność i względy bezpieczeństwa:**
    -   UX: Szybki dostęp do kluczowych funkcji i informacji.
    -   Dostępność: Nagłówki, linki opisowe.
    -   Bezpieczeństwo: Dostęp tylko dla zalogowanych użytkowników. Dane pobierane przez `GET /api/generated-lists`.

---

### 2.7. Tworzenie Nowej Podróży / Ankieta (Prywatny)
-   **Nazwa widoku:** Ankieta Podróży
-   **Ścieżka widoku:** `/new-trip`
-   **Główny cel:** Zebranie od użytkownika wszystkich niezbędnych informacji o planowanej podróży w celu wygenerowania spersonalizowanej listy pakowania.
-   **Kluczowe informacje do wyświetlenia:**
    -   Formularz (potencjalnie wieloetapowy) zbierający dane: cel podróży, daty, liczba osób (dorośli, dzieci - wiek), rodzaj noclegu, rodzaj wyżywienia, środek transportu, planowane aktywności, dostępny bagaż.
-   **Kluczowe komponenty widoku:**
    -   Formularz z polami: `Input` (tekst, data, liczba), `Select`, `Checkbox`, `RadioGroup`, `Textarea`.
    -   Logika kroków (np. komponenty `Tabs` lub przyciski "Dalej"/"Wstecz").
    -   Przycisk `Button` "Wygeneruj Listę Rzeczy do Zabraia".
    -   Wskaźnik ładowania (`Spinner` lub `Skeleton`) po kliknięciu generowania.
-   **UX, dostępność i względy bezpieczeństwa:**
    -   UX: Przejrzysty formularz, podział na logiczne sekcje/kroki. Walidacja na bieżąco.
    -   Dostępność: Etykiety dla wszystkich pól, instrukcje.
    -   Bezpieczeństwo: Dane przesyłane przez `POST /api/trips`, następnie `POST /api/trips/{tripId}/generate-list`.

---

### 2.8. Widok Wygenerowanej Listy Pakowania (Prywatny)
-   **Nazwa widoku:** Szczegóły Wygenerowanej Listy
-   **Ścieżka widoku:** `/generated-lists/:listId`
-   **Główny cel:** Wyświetlanie, zarządzanie i modyfikowanie wygenerowanej przez AI listy przedmiotów do spakowania.
-   **Kluczowe informacje do wyświetlenia:**
    -   Nazwa listy (edytowalna).
    -   Lista przedmiotów: nazwa, ilość, kategoria, status spakowania (checkbox).
    -   Procentowy postęp pakowania.
    -   Opcje filtrowania listy (np. po kategoriach przedmiotów).
-   **Kluczowe komponenty widoku:**
    -   Edytowalna nazwa listy (`Input` po kliknięciu).
    -   `Progress` bar dla postępu pakowania.
    -   Filtry: `Select` lub `DropdownMenu`.
    -   Lista przedmiotów: `Table` lub dynamiczna lista komponentów `Card`. Każdy przedmiot: `Checkbox`, `Input` (ilość), opcje edycji/usunięcia (np. `DropdownMenu` per item).
    -   Przycisk `Button` "Dodaj Przedmiot" otwierający `Dialog` / `Modal`.
        -   W Dialogu: Formularz dodawania przedmiotu (wyszukiwarka `GET /api/items?q=...`, tworzenie nowego z nazwą, kategorią `Select` z `GET /api/item-categories`, wymiarami, ilością).
    -   `Toast` notifications dla auto-zapisu i innych akcji.
    -   `Skeleton` loader podczas ładowania.
-   **UX, dostępność i względy bezpieczeństwa:**
    -   UX: Łatwe zarządzanie listą, szybkie oznaczanie przedmiotów. Optimistic updates dla checkboxów.
    -   Dostępność: Interaktywne elementy dostępne z klawiatury.
    -   Bezpieczeństwo: API calls: `GET /api/generated-lists/{listId}`, `PUT /api/generated-lists/{listId}` (dla nazwy i pełnej listy przedmiotów), `PATCH /api/generated-lists/{listId}/items/{itemId}` (dla statusu `isPacked` i ilości).

---

### 2.9. Moje Listy Specjalne (Prywatny)
-   **Nazwa widoku:** Moje Listy Specjalne
-   **Ścieżka widoku:** `/special-lists`
-   **Główny cel:** Umożliwienie użytkownikowi przeglądania, tworzenia i zarządzania własnymi, predefiniowanymi listami specjalnymi (np. "Apteczka", "Sprzęt fotograficzny").
-   **Kluczowe informacje do wyświetlenia:**
    -   Lista wszystkich list specjalnych użytkownika (nazwa, kategoria/tagi).
    -   Przycisk CTA do tworzenia nowej listy specjalnej.
    -   Stan pusty, jeśli brak list.
-   **Kluczowe komponenty widoku:**
    -   Nagłówek "Moje Listy Specjalne".
    *   Przycisk `Button` "Stwórz Nową Listę Specjalną".
    *   Lista komponentów `Card`, każdy reprezentujący listę specjalną, z linkami do edycji i opcją usunięcia (`AlertDialog` do potwierdzenia).
    -   `Skeleton` loader podczas ładowania.
-   **UX, dostępność i względy bezpieczeństwa:**
    -   UX: Centralne miejsce do zarządzania szablonami list.
    -   Bezpieczeństwo: API calls: `GET /api/special-lists`, `DELETE /api/special-lists/{listId}`.

---

### 2.10. Tworzenie / Edycja Listy Specjalnej (Prywatny)
-   **Nazwa widoku:** Formularz Listy Specjalnej
-   **Ścieżka widoku:** `/special-lists/new` lub `/special-lists/:listId/edit`
-   **Główny cel:** Tworzenie nowej listy specjalnej lub edycja istniejącej, w tym zarządzanie jej nazwą, kategorią/tagami i przedmiotami.
-   **Kluczowe informacje do wyświetlenia:**
    -   Formularz do edycji nazwy listy i jej kategorii/tagów.
    -   Interfejs do dodawania, edytowania i usuwania przedmiotów z listy.
-   **Kluczowe komponenty widoku:**
    -   Formularz: `Input` (nazwa listy), `Input` lub `MultiSelect` (kategorie/tagi - `GET /api/tags` dla tagów).
    -   Zarządzanie przedmiotami: Podobnie jak w widoku wygenerowanej listy - `Input` do wyszukiwania (`GET /api/items?q=...`), `Dialog` do tworzenia nowego przedmiotu (`POST /api/items`, kategorie z `GET /api/item-categories`), lista przedmiotów z opcjami edycji ilości i usuwania.
    -   Przyciski `Button`: "Zapisz Zmiany", "Usuń Listę" (dla edycji, z `AlertDialog`).
-   **UX, dostępność i względy bezpieczeństwa:**
    -   UX: Elastyczność w definiowaniu własnych zestawów przedmiotów.
    -   Bezpieczeństwo: API calls: `POST /api/special-lists` (tworzenie), `GET /api/special-lists/{listId}` (ładowanie), `PUT /api/special-lists/{listId}` (aktualizacja nazwy/kategorii), `PUT /api/special-lists/{listId}/items` (aktualizacja pełnego zestawu przedmiotów).

---

### 2.11. Profil Użytkownika / Ustawienia (Prywatny)
-   **Nazwa widoku:** Profil Użytkownika
-   **Ścieżka widoku:** `/profile`
-   **Główny cel:** Umożliwienie użytkownikowi zarządzania danymi swojego konta, zmianą hasła i usunięciem konta.
-   **Kluczowe informacje do wyświetlenia:**
    -   Formularz edycji danych osobowych (imię, e-mail).
    -   Opcja zmiany hasła.
    -   Opcja usunięcia konta.
    -   Informacje dotyczące RODO.
-   **Kluczowe komponenty widoku:**
    -   `Card` dla edycji profilu: `Input` (imię, e-mail), `Button` "Zapisz Zmiany".
    -   `Card` dla zmiany hasła: `Input` (stare hasło, nowe hasło, potwierdzenie), `Button` "Zmień Hasło".
    -   Sekcja usuwania konta: `Button` "Usuń Konto" z `AlertDialog` do potwierdzenia.
    -   Tekstowa informacja o RODO.
-   **UX, dostępność i względy bezpieczeństwa:**
    -   UX: Jasne opcje zarządzania kontem.
    -   Bezpieczeństwo: Potwierdzenia dla krytycznych akcji (zmiana hasła, usunięcie konta). API calls: `GET /api/users/me`, `PUT /api/users/me`, `DELETE /api/users/me`.

## 3. Mapa podróży użytkownika

### 3.1. Główny przepływ: Rejestracja -> Pierwsza lista pakowania
1.  **Użytkownik (nowy):** Odwiedza Landing Page (`/`).
2.  Kliknięcie "Zarejestruj się" -> Przejście do Widoku Rejestracji (`/register`).
3.  Wypełnienie formularza rejestracyjnego -> `POST /api/auth/register`.
4.  Po sukcesie (automatyczne lub manualne) -> Przejście do Widoku Logowania (`/login`).
5.  Wypełnienie formularza logowania -> `POST /api/auth/login`.
6.  Po sukcesie -> Przejście do Dashboardu (`/dashboard`).
7.  **Użytkownik (zalogowany):** Na Dashboardzie klika "Stwórz Nową Podróż".
8.  Przejście do Widoku Ankiety Podróży (`/new-trip`).
9.  Wypełnienie ankiety -> Kliknięcie "Wygeneruj Listę Rzeczy do Zabraia".
    *   Frontend: `POST /api/trips` (wysyła dane ankiety).
    *   Frontend (po sukcesie): `POST /api/trips/{tripId}/generate-list` (używa `tripId` z odpowiedzi).
10. Po sukcesie generowania -> Przekierowanie do Widoku Wygenerowanej Listy Pakowania (`/generated-lists/:listId`).
11. Użytkownik zarządza listą: oznacza przedmioty jako spakowane (`PATCH .../items/{itemId}`), edytuje nazwę listy (`PUT /generated-lists/{listId}`), dodaje/usuwa przedmioty (`PUT /generated-lists/{listId}` z pełną listą).

### 3.2. Zarządzanie listami specjalnymi
1.  **Użytkownik (zalogowany):** W nawigacji wybiera "Moje Listy Specjalne".
2.  Przejście do Widoku "Moje Listy Specjalne" (`/special-lists`).
3.  Kliknięcie "Stwórz Nową Listę Specjalną" -> Przejście do Widoku Formularza Listy Specjalnej (`/special-lists/new`).
4.  Wypełnienie nazwy, kategorii/tagów. Dodanie przedmiotów (wyszukanie `GET /api/items?q=...` lub utworzenie nowych `POST /api/items`, kategorie z `GET /api/item-categories`).
5.  Zapisanie listy: `POST /api/special-lists` (dla nowej listy), a następnie `PUT /api/special-lists/{listId}/items` (dla przedmiotów).
6.  Lub: Na widoku "/special-lists" klika na istniejącą listę -> Przejście do edycji (`/special-lists/:listId/edit`).
7.  Modyfikacja danych listy i przedmiotów, zapis przez odpowiednie `PUT` endpointy.

### 3.3. Zarządzanie profilem
1.  **Użytkownik (zalogowany):** W nawigacji wybiera "Profil" lub "Ustawienia".
2.  Przejście do Widoku Profilu Użytkownika (`/profile`).
3.  Użytkownik edytuje dane, zmienia hasło lub inicjuje usunięcie konta, co wywołuje odpowiednie endpointy API.

## 4. Układ i struktura nawigacji

### 4.1. Układ ogólny
-   **Mobile-first:** Interfejs projektowany z myślą o urządzeniach mobilnych, skalujący się na większe ekrany.
-   **Główna treść:** Centralna część ekranu, zawierająca dynamiczne treści danego widoku.
-   **Nawigacja górna (Top Menu):** Widoczna na większości ekranów po zalogowaniu.

### 4.2. Elementy nawigacji
-   **Nawigacja Publiczna (przed zalogowaniem):**
    -   Linki na Landing Page: "Zarejestruj się", "Zaloguj się".
    -   Linki w formularzach: np. "Masz już konto? Zaloguj się", "Zapomniałeś hasła?".
-   **Nawigacja Prywatna (po zalogowaniu - Top Menu):**
    -   **Logo aplikacji / Link do Dashboardu:** Zawsze widoczne, powrót do `/dashboard`.
    -   **"Dashboard" / "Moje Listy Pakowania":** Link do `/dashboard`.
    -   **"Moje Listy Specjalne":** Link do `/special-lists`.
    -   **Ikona Profilu / Nazwa Użytkownika (rozwijane menu):**
        -   "Profil / Ustawienia": Link do `/profile`.
        -   "Wyloguj się": Akcja wylogowania (kończy sesję, usuwa token, przekierowuje do `/login`).
-   **Nawigacja Kontekstowa:**
    -   Przyciski "Wstecz" w przeglądarce powinny działać zgodnie z oczekiwaniami.
    -   Przyciski akcji prowadzące do kolejnych kroków (np. "Dalej" w ankiecie, "Zapisz").
    -   Linki wewnątrz list (np. kliknięcie na kartę listy prowadzi do jej szczegółów).
    -   Breadcrumbs (okruszki): Mogą być rozważone dla bardziej zagnieżdżonych widoków w przyszłości.

## 5. Kluczowe komponenty (współdzielone)

Wiele komponentów z biblioteki Shadcn/ui będzie używanych wielokrotnie. Poniżej kilka kluczowych, które zdefiniują wygląd i działanie aplikacji:

-   **`Button`:** Dla wszystkich akcji klikalnych (CTA, wysyłanie formularzy, nawigacja). Style: primary, secondary, destructive, ghost, link.
-   **`Card`, `CardHeader`, `CardContent`, `CardFooter`:** Do grupowania informacji i tworzenia modułowych sekcji (np. listy, formularze).
-   **`Input`, `Label`:** Podstawowe elementy formularzy.
-   **`Select`, `Checkbox`, `RadioGroup`:** Do wyboru opcji w formularzach.
-   **`Dialog` / `Modal`:** Do wyświetlania dodatkowych informacji lub formularzy bez opuszczania bieżącego widoku (np. dodawanie przedmiotu).
-   **`Toast` (z `useToast`):** Do wyświetlania krótkich, nieinwazyjnych powiadomień (np. "Zmiany zapisano", błędy).
-   **`Alert`, `AlertDescription`, `AlertTitle`:** Do wyświetlania ważniejszych komunikatów, w tym błędów.
-   **`Skeleton`:** Do wskazywania ładowania treści, poprawiając odczucie płynności.
-   **`Progress`:** Do wizualizacji postępu (np. pakowania).
-   **`Table`, `TableHeader`, `TableBody`, `TableRow`, `TableCell`:** Do wyświetlania danych tabelarycznych (np. listy przedmiotów).
-   **`DropdownMenu`:** Dla menu kontekstowych przy elementach list.
-   **`AlertDialog`:** Do potwierdzania krytycznych akcji (np. usuwanie).

Architektura ta ma na celu stworzenie solidnych podstaw pod MVP aplikacji PackMeUp, z możliwością dalszej rozbudowy i iteracji. 