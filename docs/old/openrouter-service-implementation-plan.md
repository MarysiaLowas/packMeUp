# Implementacja usługi OpenRouter – Przewodnik wdrożenia

## 1. Opis usługi
Usługa OpenRouter stanowi warstwę integracji umożliwiającą komunikację z API OpenRouter, której zadaniem jest wspieranie funkcjonalności czatów opartych o LLM. Usługa odpowiada za:

1. Autentykację i autoryzację żądań do API.
2. Formatowanie i wysyłanie zapytań zawierających:
   - Komunikat systemowy
   - Komunikat użytkownika
   - Zdefiniowany response_format (schemat JSON)
   - Nazwę modelu
   - Parametry modelu
3. Odbieranie i walidację odpowiedzi, w tym parsowanie ustrukturyzowanych danych.
4. Obsługę błędów oraz wdrożenie mechanizmów bezpieczeństwa.

## 2. Opis konstruktora
Konstruktor usługi (np. klasa OpenRouterService) inicjuje wszystkie niezbędne komponenty i przyjmuje ustawienia konfiguracyjne, takie jak:

1. Klucz API i dane autoryzacyjne.
2. Domyślne komunikaty systemowe oraz ustawienia formatu response_format.
3. Konfigurację parametrów modelu (np. temperature, max_tokens, top_p).
4. Callbacki lub hooki do logowania błędów i monitorowania.

## 3. Publiczne metody i pola
Usługa powinna udostępniać następujące publiczne metody:

1. **set_system_message(message: str)** – Ustawienie komunikatu systemowego.
2. **set_user_message(message: str)** – Ustawienie komunikatu użytkownika.
3. **set_response_format(format: dict)** – Zdefiniowanie schematu odpowiedzi. Przykład:
   - { type: 'json_schema', json_schema: { name: 'PackingListResponse', strict: true, schema: { items: { type: 'array', items: { type: 'string' } } } } }
4. **set_model_name(name: str)** – Ustawienie nazwy modelu (np. "gpt-4").
5. **set_model_parameters(params: dict)** – Ustawienie parametrów modelu (np. { temperature: 0.2, max_tokens: 1024, top_p: 0.9 }).
6. **send_request()** – Metoda łącząca przygotowanie żądania, wysyłkę do OpenRouter API oraz przetwarzanie odpowiedzi.

Pola publiczne mogą obejmować:

- Konfigurację API (endpoint, tokeny).
- Aktualne ustawienia zapytań i odpowiedzi.

## 4. Prywatne metody i pola
Prywatne elementy usługi odpowiadają za wewnętrzne operacje:

1. **_build_request_payload()** – Składa ładunek żądania, łącząc komunikaty systemowy, użytkownika, response_format, model name i model parameters.
2. **_parse_response(response: any)** – Analizuje odpowiedź z API, weryfikując zgodność z zadanym schematem.
3. **_handle_api_error(error: any)** – Centralny moduł do obsługi błędów, który loguje problemy oraz podejmuje próby ponowienia (retry) w razie potrzeby.
4. Pola pomocnicze, np. przechowywanie konfiguracji tymczasowej, liczby prób, timeouty etc.

## 5. Obsługa błędów
Obsługa błędów obejmuje następujące scenariusze:

1. **Błąd autentykacji**
   - Wyzwanie: Nieprawidłowe lub wygasłe tokeny.
   - Rozwiązanie: Weryfikacja kluczy API przy starcie usługi oraz regularna ich aktualizacja.

2. **Błąd sieci / timeout**
   - Wyzwanie: Opóźnienia lub brak odpowiedzi od API.
   - Rozwiązanie: Mechanizm retry z backoffem oraz timeouty na poziomie żądania.

3. **Niepoprawny format odpowiedzi**
   - Wyzwanie: Odpowiedź niezgodna z zadanym schema response_format.
   - Rozwiązanie: Walidacja zwróconych danych przy użyciu dedykowanego walidatora schematu; fallback do wartości domyślnych.

4. **Błąd serwerowy OpenRouter**
   - Wyzwanie: Błąd po stronie API.
   - Rozwiązanie: Wyświetlanie przyjaznych komunikatów oraz logowanie błędów do systemu monitoringu.

## 6. Kwestie bezpieczeństwa
Przy wdrażaniu usługi należy zwrócić uwagę na:

1. **Bezpieczne przechowywanie kluczy API:**
   - Użycie zmiennych środowiskowych oraz mechanizmów szyfrowania.
2. **Ograniczenie liczby prób (rate limiting):**
   - Zapobieganie nadużyciom poprzez limitowanie żądań.
3. **Walidacja wejścia i wyjścia:**
   - Upewnienie się, że wszystkie dane są odpowiednio walidowane przed wysłaniem i po otrzymaniu odpowiedzi.
4. **Monitoring i logowanie:**
   - Implementacja mechanizmów wykrywania nieautoryzowanych prób oraz śledzenia błędów.

## 7. Plan wdrożenia krok po kroku
1. **Analiza wymagań i specyfikacja:**
   - Pozyskanie pełnych wymagań dotyczących interakcji z OpenRouter API.
   - Określenie niezbędnych komunikatów (systemowy, użytkownika) i formatów odpowiedzi.

2. **Projektowanie architektury usługi:**
   - Zdefiniowanie kluczowych komponentów: integracji API, formatera wiadomości, parsowania odpowiedzi oraz modułu obsługi błędów.
   - Szkic interfejsu publicznego i prywatnych metod.

3. **Implementacja komponentu integracji:**
   - Utworzenie konstruktora z konfiguracją API.
   - Implementacja metody _build_request_payload(), która łączy komunikaty systemowy, użytkownika, response_format, model name i model parameters.

4. **Implementacja formatera zapytań:**
   - Upewnienie się o poprawnym formatowaniu komunikatów.
   - Przykłady konfiguracji:
     1. System Message: "System: Ustal protokół komunikacji oraz priorytety w odpowiedziach."
     2. User Message: "Użytkownik: Proszę wygenerować spersonalizowaną listę pakowania." 
     3. Response Format: { type: 'json_schema', json_schema: { name: 'PackingListResponse', strict: true, schema: { items: { type: 'array', items: { type: 'string' } } } } }
     4. Model Name: "gpt-4"
     5. Model Parameters: { temperature: 0.2, max_tokens: 1024, top_p: 0.9 }

5. **Implementacja parsowania odpowiedzi:**
   - Rozwój metody _parse_response(response) z walidacją zgodności odpowiedzi z zadanym schema.

6. **Integracja modułu obsługi błędów:**
   - Stworzenie centralnego mechanizmu _handle_api_error() do wychwytywania i logowania błędów.
   - Implementacja mechanizmu retry dla scenariuszy timeout i błędów sieciowych.

7. **Wdrożenie mechanizmów bezpieczeństwa:**
   - Implementacja bezpiecznego przechowywania kluczy API,
   - Konfiguracja limitowania żądań i monitoringu.

---

Przewodnik implementacji powyżej stanowi kompleksowy plan wdrożenia usługi OpenRouter, odpowiadający na wymagania interfejsu API i wytyczne projektu, w tym aspekty bezpieczeństwa, obsługi błędów oraz integracji z pozostałymi komponentami systemu. 