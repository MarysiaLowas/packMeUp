# Plan migracji z Astro do React

## 1. Przygotowanie projektu

### 1.1. Setup nowego projektu
```bash
# Utworzenie nowego projektu
npm create vite@latest frontend-react -- --template react-ts

# Instalacja podstawowych zależności
cd frontend-react
npm install react-router-dom @tanstack/react-query axios
npm install -D tailwindcss postcss autoprefixer
```

### 1.2. Konfiguracja TypeScript
```typescript
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### 1.3. Konfiguracja Tailwind i shadcn/ui
```bash
# Inicjalizacja Tailwind
npx tailwindcss init -p

# Instalacja shadcn/ui
npx shadcn-ui@latest init
```

## 2. Struktura projektu

### 2.1. Nowa struktura katalogów
```
/frontend-react
├── src/
│   ├── components/
│   │   ├── ui/          # Komponenty z shadcn/ui
│   │   ├── auth/        # Komponenty autoryzacji
│   │   ├── trips/       # Komponenty związane z wycieczkami
│   │   └── layout/      # Komponenty layoutu
│   ├── pages/
│   │   ├── auth/
│   │   │   ├── LoginPage.tsx
│   │   │   └── RegisterPage.tsx
│   │   └── trips/
│   ├── lib/
│   │   ├── api/
│   │   │   └── client.ts
│   │   └── auth/
│   │       └── session.ts
│   ├── providers/
│   │   └── AuthProvider.tsx
│   ├── hooks/
│   │   └── useAuth.ts
│   ├── types/
│   │   └── auth.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
```

## 3. Plan migracji komponentów

### 3.1. Providers i Hooks
1. Przenieść i poprawić AuthProvider:
   - Usunąć zależności od Astro
   - Poprawić inicjalizację kontekstu
   - Dodać proper typing

2. Przenieść i dostosować hooki:
   - useAuth
   - inne custom hooki

### 3.2. Routing i Layout
1. Skonfigurować react-router:
```typescript
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route
              path="/trips/*"
              element={
                <PrivateRoute>
                  <TripsRoutes />
                </PrivateRoute>
              }
            />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
```

2. Przenieść layouty:
   - BaseLayout -> Layout
   - GuestLayout -> AuthLayout

### 3.3. Komponenty autoryzacji
1. LoginForm:
   - Usunąć zależności od Astro
   - Poprawić obsługę formularza
   - Dostosować do react-router

2. RegisterForm:
   - Podobne zmiany jak w LoginForm

3. PrivateRoute:
   - Przepisać logikę autoryzacji
   - Zintegrować z react-router

### 3.4. Komponenty biznesowe
1. Przenieść komponenty związane z wycieczkami
2. Przenieść komponenty związane z listami
3. Dostosować do nowej struktury

## 4. Kolejność migracji

### 4.1. Faza 1: Setup i podstawy (1 dzień)
- [ ] Setup nowego projektu
- [ ] Konfiguracja TypeScript
- [ ] Konfiguracja Tailwind i shadcn/ui
- [ ] Podstawowa struktura routingu

### 4.2. Faza 2: Autoryzacja (1 dzień)
- [ ] AuthProvider i useAuth
- [ ] LoginForm i LoginPage
- [ ] RegisterForm i RegisterPage
- [ ] PrivateRoute

### 4.3. Faza 3: Layouty i nawigacja (0.5 dnia)
- [ ] Layout components
- [ ] Nawigacja
- [ ] Routing dla chronionych ścieżek

### 4.4. Faza 4: Komponenty biznesowe (1-1.5 dnia)
- [ ] Trips
- [ ] Lists
- [ ] Other features

### 4.5. Faza 5: Testy i poprawki (1 dzień)
- [ ] Testy funkcjonalne
- [ ] Poprawki błędów
- [ ] Optymalizacja

## 5. Testowanie

### 5.1. Plan testów
1. Testy jednostkowe dla:
   - Hooks
   - Utils
   - Komponenty

2. Testy integracyjne dla:
   - Flow autoryzacji
   - Nawigacja
   - Protected routes

3. Testy E2E dla:
   - User journeys
   - Critical paths

### 5.2. Krytyczne ścieżki do przetestowania
- Rejestracja -> Logowanie -> Tworzenie wycieczki
- Logowanie -> Edycja profilu
- Logowanie -> Tworzenie listy -> Edycja listy
- Expired session handling
- Error handling

## 6. Deployment

### 6.1. Build
```bash
# Produkcyjny build
npm run build

# Output w /dist:
- index.html
- assets/
```

### 6.2. Konfiguracja środowiska
```typescript
// src/config.ts
export const config = {
  API_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  // inne zmienne środowiskowe
};
```

### 6.3. Nginx config
```nginx
server {
    listen 80;
    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 7. Potencjalne problemy i rozwiązania

### 7.1. Hydration
✅ Problem rozwiązany - brak SSR oznacza brak problemów z hydracją

### 7.2. Auth Context
✅ Działa natywnie w React bez dodatkowych komplikacji

### 7.3. Routing
- Potencjalny problem: Głębokie linki
- Rozwiązanie: Proper setup react-router i nginx

### 7.4. Performance
- Większy initial bundle
- Rozwiązanie: Code splitting przez React.lazy()

## 8. Rollback plan

### 8.1. Przygotowanie
- Zachować stary kod Astro
- Utrzymywać oba rozwiązania przez krótki okres
- Przygotować skrypty do szybkiego przełączania

### 8.2. Kryteria sukcesu
- Wszystkie funkcjonalności działają
- Nie ma problemów z autoryzacją
- Performance jest akceptowalne
- Nie ma regresji w UX

### 8.3. Procedura rollback
```bash
# Jeśli coś pójdzie nie tak:
git checkout main
docker-compose up -d astro-frontend
``` 