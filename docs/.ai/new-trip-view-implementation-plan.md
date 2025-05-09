# Plan Implementacji Widoku: Ankieta Podróży

## 1. Przegląd
Widok "Ankieta Podróży" (`/new-trip`) umożliwia użytkownikom wprowadzenie szczegółowych informacji dotyczących planowanej podróży. Zebrane dane są następnie wykorzystywane do wygenerowania spersonalizowanej listy rzeczy do spakowania. Proces zbierania danych jest podzielony na logiczne kroki, aby ułatwić użytkownikowi wypełnienie formularza. Po wypełnieniu ankiety i jej przesłaniu, system najpierw tworzy zasób podróży, a następnie generuje dla niej listę pakowania.

## 2. Routing widoku
Widok będzie dostępny pod ścieżką: `/new-trip`.

## 3. Struktura komponentów
```
NewTripPage (View Container)
├── Header (np. "Zaplanuj nową podróż")
├── StepIndicator (np. komponent Tabs z Shadcn/ui lub dedykowany wskaźnik kroków)
├── FormContainer (obsługiwany przez react-hook-form)
│   ├── Step1BasicInfo (Komponent dla kroku 1: Podstawowe informacje)
│   │   ├── InputField (dla celu podróży)
│   │   ├── DatePicker (dla daty rozpoczęcia)
│   │   ├── InputField (dla czasu trwania podróży w dniach)
│   │   ├── InputField (dla liczby dorosłych)
│   │   └── ChildrenAgesInput (dynamiczne pola dla wieku dzieci)
│   ├── Step2Preferences (Komponent dla kroku 2: Preferencje)
│   │   ├── SelectField (dla rodzaju zakwaterowania)
│   │   ├── CheckboxGroup/MultiSelect (dla opcji wyżywienia)
│   │   ├── SelectField (dla środka transportu)
│   │   ├── TextareaField/TagInput (dla planowanych aktywności)
│   │   └── SelectField (dla pory roku)
│   ├── Step3Luggage (Komponent dla kroku 3: Bagaż)
│   │   ├── Button "Dodaj Bagaż" 
│   │   └── Dynamiczna lista pól dla każdego bagażu (używająca useFieldArray)
│   │       ├── InputField (dla maxWeight - opcjonalne, typ number)
│   │       ├── InputField (dla dimensions - opcjonalne, typ string, np. "SZERxWYSxGŁ")
│   │       └── Button "Usuń Bagaż" (dla każdego elementu listy)
│   └── FormNavigation
│       ├── Button "Wstecz" (widoczny od kroku 2)
│       ├── Button "Dalej" (widoczny na kroku 1 i 2)
│       └── Button "Generuj Listę" (widoczny na kroku 3)
└── LoadingSpinner (wyświetlany podczas operacji API)
```

## 4. Szczegóły komponentów

### `NewTripPage`
-   **Opis komponentu:** Główny kontener widoku `/new-trip`. Zarządza logiką kroków formularza, stanem formularza (przy użyciu `react-hook-form`), obsługą ładowania i błędów oraz procesem wysyłania danych do API.
-   **Główne elementy:** `StepIndicator`, `FormContainer` (z dynamicznie renderowanymi komponentami kroków), `FormNavigation`, `LoadingSpinner`.
-   **Obsługiwane interakcje:** Nawigacja między krokami, finalne przesłanie formularza.
-   **Obsługiwana walidacja:** Koordynuje walidację na poziomie całego formularza przed wysłaniem.
-   **Typy:** `CreateTripCommand` (do przechowywania danych formularza), `GeneratedListDTO` (oczekiwany typ po pomyślnym wygenerowaniu listy).
-   **Propsy:** Brak (jest to komponent-strona).

### `StepIndicator`
-   **Opis komponentu:** Wizualnie reprezentuje aktualny krok oraz całkowitą liczbę kroków w formularzu. Może być zaimplementowany przy użyciu komponentu `Tabs` z Shadcn/ui lub jako niestandardowy komponent.
-   **Główne elementy:** Elementy graficzne wskazujące kroki (np. kropki, liczby, zakładki).
-   **Obsługiwane interakcje:** Potencjalnie kliknięcie na krok, aby do niego przejść (jeśli dozwolone i krok został już odwiedzony/jest dostępny).
-   **Typy:** `currentStep: number`, `totalSteps: number`.
-   **Propsy:** `currentStep: number`, `totalSteps: number`, `onStepSelect?: (step: number) => void`.

### `FormContainer`
-   **Opis komponentu:** Opakowuje formularz i integruje się z `react-hook-form` do zarządzania stanem i walidacją. Renderuje odpowiedni komponent kroku.
-   **Główne elementy:** Element `<form>` HTML.
-   **Obsługiwane interakcje:** Przesłanie formularza.
-   **Typy:** `UseFormReturn<CreateTripFormShape>` (gdzie `CreateTripFormShape` może zawierać numeryczne `width`, `height`, `depth` dla bagażu, zamiast `dimensions: string`).
-   **Propsy:** `onSubmit: (data: CreateTripFormShape) => Promise<void>`.

### `Step1BasicInfo`
-   **Opis komponentu:** Formularz dla pierwszego kroku ankiety: podstawowe informacje o podróży.
-   **Główne elementy HTML i komponenty dzieci:**
    -   `InputField` (Shadcn `Input` + `Label` + `FormMessage`) dla `destination` (Cel podróży).
    -   `DatePicker` (Shadcn `DatePicker` lub odpowiednik) dla `startDate` (Data rozpoczęcia).
    -   `InputField` (typ `number`) dla `durationDays` (Czas trwania w dniach).
    -   `InputField` (typ `number`) dla `numAdults` (Liczba dorosłych).
    -   `ChildrenAgesInput` (dynamiczny komponent używający `useFieldArray` z `react-hook-form` do zarządzania listą pól `Input` dla wieku dzieci).
-   **Obsługiwane interakcje:** Wprowadzanie danych.
-   **Warunki walidacji:**
    -   `destination`: Wymagane, minimum 1 znak.
    -   `startDate`: Opcjonalne, poprawny format daty.
    -   `durationDays`: Wymagane, liczba całkowita większa od 0.
    -   `numAdults`: Wymagane, liczba całkowita nieujemna (>= 0).
    -   `childrenAges`: Opcjonalne; jeśli podane, każda wartość musi być liczbą całkowitą nieujemną (>= 0).
-   **Typy:** Pola z `CreateTripFormShape` (lub `CreateTripCommand`): `destination`, `startDate`, `durationDays`, `numAdults`, `childrenAges`.
-   **Propsy:** `form: UseFormReturn<CreateTripFormShape>`.

### `Step2Preferences`
-   **Opis komponentu:** Formularz dla drugiego kroku ankiety: preferencje dotyczące podróży.
-   **Główne elementy HTML i komponenty dzieci:**
    -   `SelectField` (Shadcn `Select`) dla `accommodation` (Rodzaj zakwaterowania). Opcje pobrane z `AccommodationType`.
    -   `CheckboxGroup` lub `MultiSelect` dla `catering` (Opcje wyżywienia). Opcje pobrane z `CATERING_OPTIONS`.
    -   `SelectField` dla `transport` (Środek transportu). Opcje pobrane z `TransportType`.
    -   `TextareaField` (Shadcn `Textarea`) lub `TagInput` dla `activities` (Planowane aktywności).
    -   `SelectField` dla `season` (Pora roku). Opcje pobrane z `SeasonType`.
-   **Obsługiwane interakcje:** Wybór opcji, wprowadzanie tekstu.
-   **Warunki walidacji:**
    -   `accommodation`: Opcjonalne; jeśli podane, musi być jedną z dozwolonych wartości (`AccommodationType`).
    -   `catering`: Opcjonalne; jeśli podane, wartości muszą być poprawnymi identyfikatorami z `CATERING_OPTIONS`.
    -   `transport`: Opcjonalne; jeśli podane, musi być jedną z dozwolonych wartości (`TransportType`).
    -   `activities`: Opcjonalne.
    -   `season`: Opcjonalne; jeśli podane, musi być jedną z dozwolonych wartości (`SeasonType`).
-   **Typy:** Pola z `CreateTripFormShape` (lub `CreateTripCommand`): `accommodation`, `catering`, `transport`, `activities`, `season`.
-   **Propsy:** `form: UseFormReturn<CreateTripFormShape>`.

### `Step3Luggage`
-   **Opis komponentu:** Formularz dla trzeciego kroku ankiety: informacje o dostępnym bagażu. Umożliwia użytkownikowi dodanie jednego lub więcej elementów bagażu, każdy z opcjonalną maksymalną wagą i wymiarami.
-   **Główne elementy HTML i komponenty dzieci:**
    -   `Button` (Shadcn `Button`) "Dodaj Bagaż" do dynamicznego dodawania nowego formularza bagażu.
    -   Lista dynamicznie generowanych sekcji formularza (zarządzana przez `useFieldArray` z `react-hook-form`), gdzie każda sekcja reprezentuje jeden bagaż i zawiera:
        -   `InputField` (typ `number`, Shadcn `Input`) dla `availableLuggage[index].maxWeight` (Maksymalna waga bagażu w kg, opcjonalne).
        -   `InputField` (typ `text`, Shadcn `Input`) dla `availableLuggage[index].dimensions` (Wymiary bagażu w formacie "SZERxWYSxGŁ", np. "50x40x20", opcjonalne). Helper text wskazujący format.
        -   `Button` (Shadcn `Button`, wariant `destructive` lub ikona kosza) "Usuń Bagaż" do usunięcia danej pozycji bagażu z listy.
-   **Obsługiwane interakcje:** Dodawanie nowych pozycji bagażu, usuwanie istniejących, wprowadzanie danych dla każdej pozycji.
-   **Warunki walidacji (dla każdego elementu `availableLuggage` jeśli tablica nie jest pusta):**
    -   Co najmniej jedno z pól `maxWeight` lub `dimensions` musi być podane dla każdego dodanego bagażu.
    -   `maxWeight`: Jeśli podane, musi być liczbą większą od 0.
    -   `dimensions`: Jeśli podane, powinno być stringiem (format "SZERxWYSxGŁ" jest sugerowany, ale walidacja formatu po stronie backendu).
-   **Typy:** Pole `availableLuggage` w `CreateTripFormShape` będzie tablicą obiektów: `{ maxWeight?: number; dimensions?: string; }[]`.
-   **Propsy:** `form: UseFormReturn<CreateTripFormShape>`, `fieldArray: UseFieldArrayReturn<CreateTripFormShape, "availableLuggage", "id">`.

### `FormNavigation`
-   **Opis komponentu:** Zawiera przyciski do nawigacji między krokami formularza oraz do jego przesłania.
-   **Główne elementy HTML i komponenty dzieci:** Shadcn `Button`.
-   **Obsługiwane interakcje:** Kliknięcie przycisków "Wstecz", "Dalej", "Generuj Listę".
-   **Warunki walidacji:** Przycisk "Dalej" i "Generuj Listę" powinien być aktywny tylko jeśli bieżący krok jest poprawny (lub cały formularz w przypadku "Generuj Listę").
-   **Propsy:**
    -   `currentStep: number`
    -   `totalSteps: number`
    -   `onBack: () => void`
    -   `onNext: () => Promise<boolean>` (zwraca `true` jeśli walidacja kroku przeszła pomyślnie)
    -   `isSubmitting: boolean`

## 5. Typy
Główne typy danych wykorzystywane w widoku to:

-   **`CreateTripCommand` (z `frontend/src/types.ts`):** Typ danych wysyłanych do API.
    ```typescript
    export interface CreateTripCommand {
      destination: string;
      startDate?: string; // ISO date string (YYYY-MM-DD)
      durationDays: number;
      numAdults: number;
      childrenAges?: number[];
      accommodation?: string;
      catering?: number[];
      transport?: string;
      activities?: string[];
      season?: string;
      availableLuggage?: LuggageDTO[]; // Zmienione na tablicę LuggageDTO
    }

    export interface LuggageDTO { // Ten DTO jest częścią CreateTripCommand
      maxWeight?: number; // Opcjonalne
      dimensions?: string; // Opcjonalne, Format "SZERxWYSxGŁ", np. "50x40x20"
    }
    ```
-   **`CreateTripFormShape` (ViewModel dla formularza):** Reprezentuje strukturę danych zarządzaną przez `react-hook-form`.
    ```typescript
    // Przykład ViewModelu dla formularza, używanego z react-hook-form i Zod
    export interface CreateTripFormShape {
      destination: string;
      startDate?: string;
      durationDays: number;
      numAdults: number;
      childrenAges?: number[];
      accommodation?: string;
      catering?: number[];
      transport?: string;
      activities?: string[];
      season?: string;
      availableLuggage?: { // Zmienione na tablicę obiektów
        maxWeight?: number;    // Opcjonalne
        dimensions?: string; // Opcjonalne, string np. "SZERxWYSxGŁ"
      }[];
    }
    ```
-   **`TripDTO` (z `frontend/src/types.ts`):** Typ odpowiedzi po pomyślnym utworzeniu podróży (`POST /api/trips`). Powinien również odzwierciedlać `availableLuggage` jako `LuggageDTO[]`.
-   **`GeneratePackingListResponseDTO` (z `frontend/src/types.ts`):** Typ odpowiedzi po pomyślnym wygenerowaniu listy (`POST /api/trips/{tripId}/generate-list`).
-   **Typy dla opcji `Select`:** Należy zdefiniować typy lub stałe dla opcji wyboru (zakwaterowanie, transport, pora roku, wyżywienie), np.:
    ```typescript
    // Przykładowe opcje, docelowo powinny być zsynchronizowane z backend/app/services/constants.py
    export const ACCOMMODATION_OPTIONS = [
      { value: "HOTEL", label: "Hotel" },
      { value: "APARTMENT", label: "Apartament" },
      // ... inne
    ];
    // ... (TRANSPORT_OPTIONS, SEASON_OPTIONS, CATERING_OPTIONS_FRONTEND jak poprzednio)
    export const TRANSPORT_OPTIONS = [
      { value: "PLANE", label: "Samolot" },
      { value: "CAR", label: "Samochód" },
      // ... inne
    ];

    export const SEASON_OPTIONS = [
      { value: "SUMMER", label: "Lato" },
      { value: "WINTER", label: "Zima" },
      // ... inne
    ];
    
    export const CATERING_OPTIONS_FRONTEND = [ // Na podstawie CATERING_OPTIONS z backendu
        { value: 0, label: "All-inclusive" },
        { value: 1, label: "Własne wyżywienie" },
        { value: 2, label: "Częściowe" },
    ];
    ```

## 6. Zarządzanie stanem
-   **Główny stan formularza:** Zarządzany przez `react-hook-form`.
    -   Użycie `useForm<CreateTripFormShape>()`.
    -   Użycie `useFieldArray` dla pola `availableLuggage` do dynamicznego zarządzania listą bagaży.
    -   Schemat walidacji Zod dla `CreateTripFormShape` przekazany do `resolver` w `useForm`.
-   **Stan kroków:** Prosta zmienna stanu React `currentStep: number` w komponencie `NewTripPage`.
-   **Stan ładowania API:** Zmienna stanu React `isLoading: boolean` w `NewTripPage`.
-   **Stan błędów API:** Zmienna stanu React `apiError: string | null` w `NewTripPage`.
-   Transformacja z `CreateTripFormShape` do `CreateTripCommand` będzie teraz prostsza dla `availableLuggage`, ponieważ struktura jest już tablicą obiektów z opcjonalnymi `maxWeight` i `dimensions`. Należy jedynie upewnić się, że puste obiekty lub obiekty bez `maxWeight` i `dimensions` są odpowiednio obsługiwane (np. odfiltrowane, jeśli API tego wymaga, lub backend obsługuje takie przypadki zgodnie z walidatorem `root_validator` w `LuggageModel`).

## 7. Integracja API
Widok będzie komunikował się z dwoma endpointami API:

1.  **Tworzenie podróży:**
    -   **Endpoint:** `POST /api/trips`
    -   **Żądanie (Request Body):** Obiekt typu `CreateTripCommand`. Dane z `CreateTripFormShape.availableLuggage` (tablica obiektów `{maxWeight?: number, dimensions?: string}`) będą bezpośrednio mapowane do `CreateTripCommand.availableLuggage` (tablica `LuggageDTO`).
        ```json
        // Przykład payloadu CreateTripCommand po transformacji
        {
          "destination": "Paryż, Francja",
          "startDate": "2024-12-01",
          "durationDays": 10,
          "numAdults": 2,
          "childrenAges": [5],
          "accommodation": "HOTEL",
          "catering": [0, 2],
          "transport": "PLANE",
          "activities": ["zwiedzanie", "muzea"],
          "season": "WINTER",
          "availableLuggage": [ // Przykładowa tablica bagaży
            {
              "maxWeight": 20.5,
              "dimensions": "50x40x20"
            },
            {
              "maxWeight": 10.0
            },
            {
              "dimensions": "30x20x10"
            }
          ]
        }
        ```
    -   **Odpowiedź (Sukces - 201 Created):** Obiekt typu `TripDTO` (z `availableLuggage` jako tablicą `LuggageDTO`).

2.  **Generowanie listy pakowania:** (Bez zmian w stosunku do poprzedniej wersji planu)
    -   **Endpoint:** `POST /api/trips/{tripId}/generate-list`
    -   **Odpowiedź (Sukces - 201 Created):** Obiekt typu `GeneratePackingListResponseDTO`.

**Przepływ:** (Bez zmian w stosunku do poprzedniej wersji planu, z uwzględnieniem transformacji danych przed pierwszym wywołaniem API)

## 8. Interakcje użytkownika
(Bez zmian w ogólnym przepływie; walidacja dotyczy `CreateTripFormShape`)

## 9. Warunki i walidacja
Walidacja będzie realizowana na frontendzie przy użyciu `react-hook-form` i Zod, na podstawie typu `CreateTripFormShape`.

**Kluczowe reguły walidacji (per pole z `CreateTripFormShape`):**
-   `destination`: Wymagane (np. `z.string().min(1, "Cel podróży jest wymagany")`).
-   `startDate`: Opcjonalne, poprawny format daty.
-   `durationDays`: Wymagane, liczba całkowita dodatnia (np. `z.number().int().positive("Czas trwania musi być liczbą dodatnią")`).
-   `numAdults`: Wymagane, liczba całkowita nieujemna (np. `z.number().int().min(0, "Liczba dorosłych nie może być ujemna")`).
-   `childrenAges`: Opcjonalna tablica liczb całkowitych nieujemnych.
-   `accommodation`, `catering`, `transport`, `activities`, `season`: Jak poprzednio.
-   `availableLuggage`: Opcjonalny obiekt. Jeśli istnieje:
    -   `maxWeight`: Wymagane, liczba dodatnia (np. `z.number().positive()`).
    -   `dimensions`: Wymagane, poprawny format stringa "SZERxWYSxGŁ".

Komunikaty o błędach walidacji będą wyświetlane przy odpowiednich polach.

## 10. Obsługa błędów
(Bez zmian w stosunku do poprzedniej wersji planu)

## 11. Kroki implementacji
1.  **Przygotowanie środowiska:** (Bez zmian)
2.  **Definicja typów:** Zdefiniowanie `CreateTripCommand`, `LuggageDTO` (dla API) oraz `CreateTripFormShape` (dla formularza) i stałych opcji Select.
3.  **Stworzenie komponentu `NewTripPage`:**
    -   Inicjalizacja `react-hook-form` z `useForm<CreateTripFormShape>()` i schematem walidacji Zod dla `CreateTripFormShape`.
    -   Implementacja funkcji `onSubmit`, która transformuje `CreateTripFormShape` do `CreateTripCommand` przed wysłaniem do API.
4.  **Implementacja komponentu `StepIndicator`**. (Bez zmian)
5.  **Implementacja komponentów kroków (`Step1BasicInfo`, `Step2Preferences`, `Step3Luggage`):**
    -   `Step3Luggage` będzie zawierał trzy numeryczne pola Input dla `width`, `height`, `depth`.
6.  **Implementacja komponentu `FormNavigation`:** (Bez zmian)
7.  **Implementacja logiki przesyłania danych:**
    -   Funkcja `onSubmit` w `NewTripPage` wykonuje transformację danych bagażu przed wywołaniem `POST /api/trips`.
8.  **Styling:** (Bez zmian)
9.  **Testowanie:**
    -   Testowanie walidacji dla `CreateTripFormShape`, w tym numerycznych pól wymiarów bagażu.
    -   Testowanie transformacji danych bagażu i poprawnego formatu stringa `dimensions` wysyłanego do API.
10. **Refaktoryzacja i optymalizacja:** (Bez zmian)
``` 