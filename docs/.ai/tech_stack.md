Frontend - Astro z React dla komponentów interaktywnych:
    Astro 5 dostarcza podstawowego layoutu dla Reacta
    React 19 zapewni interaktywność tam, gdzie jest potrzebna
    TypeScript 5 dla statycznego typowania kodu i lepszego wsparcia IDE
    Tailwind 4 pozwala na wygodne stylowanie aplikacji
    Shadcn/ui zapewnia bibliotekę dostępnych komponentów React, na których oprzemy UI

Backend - FastAPI + SQLAlchemy:

    Zapewnia bazę danych PostgreSQL.
    Do migracji użyjemy paczki Alembik.

Testing - Framework'i i narzędzia testujące:

    Vitest / React Testing Library do testów jednostkowych komponentów React
    pytest do testów jednostkowych i integracyjnych backendu (FastAPI)
    Playwright do kompleksowych testów end-to-end
    Storybook do testowania izolowanych komponentów UI
    Lighthouse do testów wydajności i dostępności

Linters i narzędzia do jakości kodu:

    Frontend:
        ESLint z pluginami dla TypeScript, React, React Hooks, JSX A11y i Astro
        Prettier zintegrowany z ESLint do formatowania kodu

    Backend:
        Ruff - nowoczesny linter dla Pythona z wyselekcjonowanymi regułami
        Black - formatter kodu Python
        MyPy - narzędzie do statycznej analizy typów
        isort - organizacja importów w Pythonie

    Pre-commit hooks dla automatycznej weryfikacji jakości kodu przed commitami (Ruff, Black, isort, MyPy)

AI - Komunikacja z modelami przez usługę Openrouter.ai:

    Dostęp do szerokiej gamy modeli (OpenAI, Anthropic, Google i wiele innych), które pozwolą nam znaleźć rozwiązanie zapewniające wysoką efektywność i niskie koszta
    Pozwala na ustawianie limitów finansowych na klucze API

CI/CD i Hosting:

    Github Actions do tworzenia pipeline'ów CI/CD
    Render do hostowania aplikacji

