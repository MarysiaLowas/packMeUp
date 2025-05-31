# Project Onboarding: Pack Me Up

## Welcome

Welcome to the Pack Me Up project! This application is designed to help users efficiently pack for their trips by generating personalized packing lists tailored to trip type, number of people, planned activities, and luggage capacity.

## Project Overview & Structure

The project is a monorepo with a separate `frontend` and `backend`.

- **`frontend/`**: Contains the client-side application built with Astro, React, and TypeScript. It handles user interaction and presentation.
  - `src/pages/`: Astro files defining the routes and structure of different pages.
  - `src/components/`: Reusable React components used across the application.
  - `src/lib/`: Utility functions, API interaction logic, and potentially state management.
  - `src/styles/`: Global styles and Tailwind CSS configuration.
  - `public/`: Static assets like images and fonts.
- **`backend/`**: Contains the server-side application built with Python and FastAPI. It manages business logic, data storage, and API provision.
  - `app/api/`: FastAPI routers and endpoint definitions.
  - `app/services/`: Core business logic for packing list generation, etc.
  - `app/crud.py`: Functions for Create, Read, Update, Delete operations on the database.
  - `app/models.py`: SQLAlchemy models defining the database schema.
  - `app/schemas/`: Pydantic schemas for data validation and serialization.
  - `alembic/`: Database migration scripts.
- **`docs/`**: Intended for project documentation (currently being populated by this summary).
- **`.github/`**: Contains GitHub Actions workflows for CI/CD and potentially issue/PR templates.
- **Testing**: Comprehensive test suites exist for both frontend (`Vitest` for unit/component, `Playwright` for E2E) and backend (`pytest`).

## Core Modules

### `Backend API & Services`
- **Role:** Provides data to the frontend, handles user authentication, and executes the core logic of packing list generation.
- **Key Files/Areas:** `backend/app/main.py`, `backend/app/api/`, `backend/app/services/`, `backend/app/config.py`, `backend/app/settings.py`
- **Recent Focus:** Recent commits indicate work on CI stability for the backend.

### `Backend Data Management`
- **Role:** Defines and interacts with the database. Manages data persistence for users, trips, items, and packing lists.
- **Key Files/Areas:** `backend/app/models.py` (SQLAlchemy models), `backend/app/crud.py` (database operations), `backend/app/schemas/` (data validation), `alembic/` (migrations).
- **Recent Focus:** No specific recent commits directly to these files, but they are fundamental to any backend changes. `models.py` is notably large, indicating a complex data structure.

### `Frontend Application (Astro + React)`
- **Role:** Renders the user interface, manages user interactions, and communicates with the backend API.
- **Key Files/Areas:** `frontend/src/pages/` (Astro), `frontend/src/components/` (React), `frontend/src/layouts/`, `frontend/src/lib/` (utilities, API client), `frontend/src/types.ts`.
- **Recent Focus:** Recent commits show active development in translating UI elements, fixing item selection in packing lists, and adding features like a list of packing lists.

## Key Contributors

- **Marysia Lowas-Rzechonek:** Appears to be the primary recent contributor, with work spanning both backend (CI fixes) and frontend (feature development and fixes).

*(Further contributors can be identified by exploring the `git log` history more extensively or looking for authorship in code comments/documentation if available).*

## Overall Takeaways & Recent Focus

- The project is a well-structured web application with a clear separation of concerns between its FastAPI backend and Astro/React frontend.
- There's a strong emphasis on code quality, with linting (`Ruff`, `ESLint`), type checking (`Mypy`, `TypeScript`), and comprehensive testing (`pytest`, `Vitest`, `Playwright`) integrated into the development workflow, including pre-commit hooks.
- Recent development has focused on stabilizing backend CI processes and enhancing frontend functionality and user experience.
- The core feature revolves around generating personalized packing lists.

## Potential Complexity/Areas to Note

- **Database Schema (`backend/app/models.py`):** Given its size, understanding the relationships between different data models will be crucial.
- **Frontend State Management and Data Flow:** The interaction between Astro pages and React components, especially for managing shared state and complex UI logic, might require careful study. `frontend/src/types.ts` is extensive.
- **Packing List Generation Logic (`backend/app/services/`):** The algorithms and rules used to generate and optimize packing lists are likely to be a complex part of the backend.
- **Astro and React Integration:** For developers new to Astro, understanding its "islands architecture" and how it integrates with React components will be important.

## Questions for the Team

1.  Could you walk me through the database schema and the relationships between the main tables in `models.py`?
2.  What is the primary approach to state management on the frontend, especially for complex forms or user-specific data?
3.  Are there any specific performance considerations or optimization techniques used in the packing list generation service?
4.  What are the plans for the `.env` file? What variables need to be configured for local development?
5.  Where can I find more detailed documentation on the business rules for packing list generation?
6.  Are there any API documentation tools in use (e.g., Swagger/OpenAPI for FastAPI)?
7.  What are the current priorities for the project in the next 1-3 months?

## Next Steps

1.  **Set up the development environment:** Follow the instructions in the main `README.md` to get both the frontend and backend running locally.
2.  **Explore the codebase:** Start by examining the key files mentioned in the "Core Modules" section, particularly `backend/app/models.py`, `backend/app/services/`, `frontend/src/pages/`, and `frontend/src/components/`.
3.  **Run the tests:** Execute the test suites for both frontend and backend to see them in action and understand the expected behavior (`./run_tests.sh`).
4.  **Review `frontend/tests/README.md` and `backend/tests/README.md`** for more detailed information on testing practices.
5.  Try creating a new packing list through the UI to understand the user flow and how frontend and backend interact.

## Development Environment Setup

As per the `README.md`:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/pack-me-up.git # Replace with actual repo URL
    cd pack-me-up
    ```
2.  **Set up and run the frontend:**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
3.  **Set up and run the backend:**
    ```bash
    cd backend
    pip install -e ".[dev]" # Ensure you have Python >=3.10
    # It is recommended to use a virtual environment.
    # Create/source a .env file based on .env.example
    uvicorn app.main:app --reload
    ```
-   **Pre-commit hooks:** Run `bash setup_precommit.sh` from the root directory to install pre-commit hooks for automated linting and formatting.
-   **Environment Variables:** An `.env` file is needed, likely for database connection strings and potentially other secrets. Refer to `.env.example` and consult `backend/app/config.py` or `backend/app/settings.py` for expected variables.

## Helpful Resources

-   **Project Repository:** The Git repository where the codebase is hosted (e.g., GitHub).
-   **Issue Tracker:** Likely GitHub Issues associated with the repository.
-   **Frontend Testing Guide:** `frontend/tests/README.md` (as mentioned in the main `README.md`).
-   **Backend Testing Guide:** `backend/tests/README.md` (as mentioned in the main `README.md`).
-   **FastAPI Documentation:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
-   **Astro Documentation:** [https://docs.astro.build/](https://docs.astro.build/)
-   **React Documentation:** [https://react.dev/](https://react.dev/)
-   **SQLAlchemy Documentation:** [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)
-   **Tailwind CSS Documentation:** [https://tailwindcss.com/docs](https://tailwindcss.com/docs)
-   **Shadcn/UI:** [https://ui.shadcn.com/](https://ui.shadcn.com/)

*(Note: If there are internal wikis, Confluence pages, or specific communication channels like Slack/Discord, links to those should be added here.)* 