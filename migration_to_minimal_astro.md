# Plan migracji do minimalnego wykorzystania Astro

## Obecny stan
- Aplikacja używa Astro do routingu i podstawowych layoutów
- Komponenty React obsługują interaktywne elementy i stan autoryzacji
- Istnieje już implementacja `AuthProvider` i `useAuth` do zarządzania stanem autoryzacji
- Występują problemy z przekazywaniem kontekstu autoryzacji i przekierowaniami

## Problemy do rozwiązania
1. Mieszane podejście do routingu (Astro + window.location)
2. Niepotrzebne przeładowania strony przy przekierowaniach
3. Niespójne zarządzanie stanem autoryzacji
4. Błędy typów w implementacji kontekstu autoryzacji

## Plan migracji

### 1. Naprawa istniejących problemów z TypeScript
- Poprawić definicję `AuthContext` - usunąć string z union type
- Zaktualizować typy w `useAuth` hook
- Dodać prawidłową obsługę typu `User`

### 2. Minimalizacja Astro
- Zostawić tylko jeden plik `index.astro` jako entry point
- Przenieść wszystkie layouty do komponentów React
- Usunąć zbędne pliki `.astro`:
  - `login.astro`
  - `register.astro`
  - `reset-password.astro`
  - `new-trip.astro`
  - Inne strony wymagające autoryzacji

### 3. Implementacja React Router
- Dodać `react-router-dom`
- Stworzyć główny komponent routingu
- Zaimplementować lazy loading dla stron
- Przenieść logikę protected routes do React Router

### 4. Refaktoryzacja autoryzacji
- Usunąć `window.location.reload()` z `AuthProvider`
- Wykorzystać React Router do nawigacji
- Zaimplementować persystencję stanu autoryzacji
- Dodać interceptor do obsługi wygasłego tokenu

### 5. Aktualizacja komponentów
- Przenieść `Navigation` do React Router
- Zaktualizować wszystkie formularze, aby używały `useNavigate`
- Usunąć pozostałe odwołania do Astro

### 6. Optymalizacja wydajności
- Dodać Suspense dla lazy-loaded routes
- Zaimplementować code splitting
- Zoptymalizować bundle size

## Kolejność implementacji

1. **Tydzień 1: Przygotowanie**
   - Naprawa TypeScript
   - Dodanie React Router
   - Stworzenie podstawowej struktury routingu

2. **Tydzień 2: Migracja stron**
   - Konwersja stron Astro na komponenty React
   - Implementacja lazy loading
   - Aktualizacja protected routes

3. **Tydzień 3: Autoryzacja**
   - Refaktoryzacja `AuthProvider`
   - Implementacja persystencji stanu
   - Obsługa wygasłych tokenów

4. **Tydzień 4: Finalizacja**
   - Testy end-to-end
   - Optymalizacja wydajności
   - Dokumentacja

## Przykłady implementacji

### Nowa struktura routingu
```typescript
const AppRouter = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="register" element={<RegisterPage />} />
          <Route
            path="dashboard"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
        </Route>
      </Routes>
    </Router>
  );
};
```

### Zaktualizowany Protected Route
```typescript
const ProtectedRoute = ({ children }: { children: ReactNode }) => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  
  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login', { replace: true });
    }
  }, [isAuthenticated, navigate]);
  
  return isAuthenticated ? children : null;
};
```

## Potencjalne ryzyka
1. Możliwe problemy z SEO po usunięciu SSR
2. Tymczasowe problemy z wydajnością podczas pierwszego ładowania
3. Potrzeba dodatkowej konfiguracji dla środowiska produkcyjnego

## Metryki sukcesu
1. Brak przeładowań strony podczas nawigacji
2. Poprawne działanie autoryzacji bez wycieków pamięci
3. Zmniejszony rozmiar bundle'a
4. Lepsze wyniki w Lighthouse
5. Krótszy czas do interaktywności (TTI) 