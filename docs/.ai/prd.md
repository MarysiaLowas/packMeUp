# Dokument wymagań produktu (PRD) - PackMeUp

## 1. Przegląd produktu

PackMeUp to aplikacja webowa pomagająca użytkownikom efektywnie pakować się na wyjazdy. Głównym zadaniem aplikacji jest generowanie spersonalizowanych list rzeczy do zabrania, dostosowanych do typu podróży, liczby osób, planowanych aktywności oraz dostępnej ilości bagażu.

Produkt jest skierowany głównie do dwóch grup docelowych:
- Rodzin z dziećmi planujących wspólne wyjazdy
- Backpackerów potrzebujących zoptymalizować zawartość plecaka

Aplikacja wykorzystuje sztuczną inteligencję do generowania list rzeczy do spakowania na podstawie informacji podanych przez użytkownika w ankiecie oraz z uwzględnieniem stworzonych wcześniej przez użytkownika list specjalnych.

## 2. Problem użytkownika

Użytkownicy napotykają następujące problemy podczas pakowania się na wyjazdy:

1. Trudności z zapamiętaniem wszystkich niezbędnych przedmiotów
2. Problemy z optymalnym wykorzystaniem ograniczonej ilości bagażu
3. Dostosowanie zawartości bagażu do specyfiki wyjazdu (klimat, aktywności, zakwaterowanie)
4. Pakowanie dla wielu osób jednocześnie (np. rodziny z dziećmi)

Aplikacja PackMeUp rozwiązuje te problemy przez:
- Kompleksową ankietę zbierającą wszystkie istotne informacje o wyjeździe
- Generowanie spersonalizowanych list rzeczy do zabrania z wykorzystaniem AI
- Możliwość tworzenia i przechowywania własnych list specjalnych
- Zarządzanie procesem pakowania przez oznaczanie już przygotowanych przedmiotów

## 3. Wymagania funkcjonalne

### 3.1 System ankiet
- Zbieranie informacji o celu podróży (miejsce, czas trwania)
- Określanie liczby osób (dorosłych i dzieci)
- Wybór rodzaju noclegu (hotel, namiot, apartament)
- Wybór rodzaju wyżywienia (all-inclusive, własne wyżywienie, częściowe)
- Wybór środka transportu (samochód, samolot, pociąg, pieszo)
- Określanie planowanych aktywności (sporty, zwiedzanie, plażowanie)
- Informacje o dostępnym bagażu (rozmiar, waga, liczba sztuk)

### 3.2 Manualne tworzenie list specjalnych
- Możliwość nadania nazwy liście
- Przypisywanie kategorii/tagów do list (np. góry, morze, jazda na rowerze)
- Dodawanie, edytowanie i usuwanie przedmiotów z listy
- Przechowywanie wielu list w ramach konta użytkownika

### 3.3 Generowanie list przez AI
- Wykorzystanie danych z ankiety oraz list specjalnych użytkownika do wygenerowania listy
- Uwzględnianie parametrów takich jak: pogoda, długość pobytu, planowane aktywności
- Kategoryzacja przedmiotów na liście (spanie, jedzenie, transport, aktywności)

### 3.4 Zarządzanie wygenerowanymi listami
- Dodawanie i usuwanie przedmiotów z wygenerowanej listy
- Oznaczanie przedmiotów jako już przygotowane do spakowania
- Zapisywanie i edytowanie list
- Przechowywanie wielu różnych list jednocześnie

### 3.5 System kont użytkowników
- Rejestracja przy użyciu emaila, imienia, wieku i hasła
- Logowanie do konta
- Zarządzanie profilem użytkownika
- Zgodność z wymogami RODO

## 4. Granice produktu

W ramach MVP aplikacji PackMeUp NIE będą realizowane następujące funkcjonalności:

1. Własny, zaawansowany algorytm pakowania rzeczy do plecaka lub walizki
2. Obsługa multimediów (zdjęcia przedmiotów, filmy instruktażowe)
3. Współdzielenie list między użytkownikami
4. Aplikacje mobilne (tylko wersja webowa)
5. Interfejs w językach innych niż angielski
6. Funkcjonalności społecznościowe (komentarze, oceny list)

Aplikacja będzie bazować na istniejących modelach AI do generowania list, bez tworzenia własnych zaawansowanych algorytmów.

## 5. Historyjki użytkowników

### US-001: Rejestracja nowego konta
Jako nowy użytkownik, chcę zarejestrować się w systemie, aby móc korzystać z pełnej funkcjonalności aplikacji.

Kryteria akceptacji:
- Użytkownik może zarejestrować się podając email, imię, wiek i hasło
- System weryfikuje unikalność adresu email
- System wymaga silnego hasła (minimum 8 znaków, duże i małe litery, cyfra)
- Po rejestracji użytkownik otrzymuje email potwierdzający
- Rejestracja jest zgodna z wymogami RODO (zgoda na przetwarzanie danych)

### US-002: Logowanie do konta
Jako zarejestrowany użytkownik, chcę zalogować się do systemu, aby uzyskać dostęp do moich zapisanych list.

Kryteria akceptacji:
- Użytkownik może zalogować się używając emaila i hasła
- System weryfikuje poprawność danych logowania
- System oferuje opcję "Zapomniałem hasła"
- Użytkownik po zalogowaniu ma dostęp do swoich zapisanych list

### US-003: Wypełnianie ankiety o planowanym wyjeździe
Jako użytkownik, chcę wypełnić ankietę z informacjami o moim planowanym wyjeździe, aby otrzymać spersonalizowaną listę rzeczy do zabrania.

Kryteria akceptacji:
- Formularz zawiera pola dotyczące celu podróży, liczby osób, zakwaterowania, transportu i aktywności
- Użytkownik może wybrać datę i długość pobytu
- Użytkownik może określić dostępny bagaż (rozmiar/waga)
- System zachowuje dane ankiety w profilu użytkownika
- Wszystkie pola wymagane są oznaczone i nie można wysłać ankiety bez ich wypełnienia

### US-004: Tworzenie listy specjalnej
Jako użytkownik, chcę stworzyć własną listę specjalną dla konkretnej aktywności, aby wykorzystać ją podczas generowania głównej listy rzeczy do zabrania.

Kryteria akceptacji:
- Użytkownik może nadać nazwę liście specjalnej
- Użytkownik może przypisać kategorię/tag do listy (np. góry, jazda na rowerze)
- Użytkownik może dodawać, edytować i usuwać przedmioty z listy
- Lista jest zapisywana w profilu użytkownika
- Użytkownik może przeglądać wszystkie swoje listy specjalne

### US-005: Generowanie listy rzeczy do zabrania
Jako użytkownik, chcę wygenerować listę rzeczy do zabrania na podstawie wypełnionej ankiety, aby efektywnie się spakować.

Kryteria akceptacji:
- System generuje listę przedmiotów na podstawie danych z ankiety
- Lista uwzględnia liczbę osób (dorosłych i dzieci)
- Lista jest podzielona na kategorie (spanie, jedzenie, transport, aktywności)
- System uwzględnia listy specjalne użytkownika podczas generowania

### US-006: Modyfikacja wygenerowanej listy
Jako użytkownik, chcę modyfikować wygenerowaną listę rzeczy do zabrania, aby dostosować ją do moich indywidualnych potrzeb.

Kryteria akceptacji:
- Użytkownik może dodawać nowe przedmioty do listy
- Użytkownik może usuwać przedmioty z listy
- Użytkownik może edytować nazwy przedmiotów
- Zmiany są automatycznie zapisywane

### US-007: Oznaczanie spakowanych przedmiotów
Jako użytkownik, chcę oznaczać przedmioty jako już spakowane, aby śledzić postęp pakowania.

Kryteria akceptacji:
- Użytkownik może oznaczyć każdy przedmiot na liście jako spakowany
- System wizualnie odróżnia przedmioty spakowane od niespakowanych
- Użytkownik widzi procentowy postęp pakowania
- Oznaczenia są zapisywane automatycznie
- Użytkownik może cofnąć oznaczenie przedmiotu jako spakowany

### US-008: Zapisywanie listy rzeczy do zabrania
Jako użytkownik, chcę zapisać wygenerowaną listę rzeczy do zabrania, aby móc do niej wrócić później.

Kryteria akceptacji:
- Użytkownik może zapisać listę pod własną nazwą
- System automatycznie zapisuje datę utworzenia listy
- Zapisane listy są dostępne w profilu użytkownika
- Użytkownik może przeglądać wszystkie swoje zapisane listy
- Użytkownik może usuwać zapisane listy

### US-009: Zarządzanie profilem użytkownika
Jako użytkownik, chcę zarządzać moim profilem, aby aktualizować moje dane osobowe i preferencje.

Kryteria akceptacji:
- Użytkownik może zmienić imię, wiek i hasło
- Użytkownik może zaktualizować adres email z weryfikacją
- Użytkownik może usunąć swoje konto
- System potwierdza wszystkie istotne zmiany w profilu
- Użytkownik ma dostęp do informacji o przetwarzaniu swoich danych osobowych

### US-010: Przeglądanie historii list
Jako użytkownik, chcę przeglądać historię moich list rzeczy do zabrania, aby móc wykorzystać je ponownie przy podobnych wyjazdach.

Kryteria akceptacji:
- Użytkownik widzi listę wszystkich utworzonych list z datami
- Użytkownik może filtrować listy według kategorii/tagów
- Użytkownik może wyszukiwać listy według nazwy
- System wyświetla podstawowe informacje o każdej liście (cel podróży, liczba osób)

### US-011: Odzyskiwanie hasła
Jako użytkownik, który zapomniał hasła, chcę je odzyskać, aby móc zalogować się do systemu.

Kryteria akceptacji:
- Użytkownik może zainicjować proces odzyskiwania hasła podając email
- System wysyła email z linkiem do resetowania hasła
- Link do resetowania hasła jest ważny przez ograniczony czas (24h)
- Użytkownik może ustawić nowe hasło po kliknięciu w link
- System wymaga potwierdzenia nowego hasła

### US-012: Wylogowanie z systemu
Jako zalogowany użytkownik, chcę się wylogować z systemu, aby zabezpieczyć moje dane.

Kryteria akceptacji:
- Użytkownik może wylogować się z systemu jednym kliknięciem
- Po wylogowaniu użytkownik nie ma dostępu do chronionych zasobów
- System kończy sesję użytkownika
- Użytkownik jest przekierowany na stronę logowania po wylogowaniu

## 6. Metryki sukcesu

### 6.1 Metryki produktowe
- 75% list wygenerowanych przez AI jest akceptowanych przez użytkowników bez większych modyfikacji
- Użytkownicy modyfikują nie więcej niż 75% zawartości wygenerowanej listy
- Średnio każdy aktywny użytkownik tworzy przynajmniej 2 listy specjalne


### 6.2 Kryteria techniczne
- Dostępność systemu na poziomie 99.5%
- Poprawne działanie aplikacji na wszystkich popularnych przeglądarkach (Chrome, Firefox, Safari, Edge)
- Responsywny interfejs działający na różnych rozmiarach ekranów (desktop, tablet)
- Średni czas ładowania strony poniżej 5 sekund

### 6.3 Kryteria wdrożeniowe
- Aplikacja zostanie stworzona w ciągu 5 tygodni pracy po godzinach dla jednej osoby
- Aplikacja przejdzie testy na 5 różnych scenariuszach wyjazdowych:
  - Wakacje rodzinne z dziećmi
  - Backpacking
  - Wyjazd w góry
  - Wczasy nad morzem
  - Pobyt w hotelu
- Wszystkie historyjki użytkownika zostaną zrealizowane w stopniu spełniającym kryteria akceptacji 