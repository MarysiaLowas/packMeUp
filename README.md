# Pack Me Up

A web application to help users pack efficiently for trips.

## Features

- Generate personalized packing lists
- Tailor to trip type, number of people, planned activities
- Optimize for available luggage capacity

## Tech Stack

- **Frontend:** Astro, TypeScript, React, Tailwind, Shadcn/ui
- **Backend:** FastAPI, SQLAlchemy

## Development

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pack-me-up.git
   cd pack-me-up
   ```

2. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

3. Set up the backend:
   ```bash
   cd backend
   pip install -e ".[dev]"
   ```

### Running the application

1. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

2. Start the backend:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

## Testing

This project has a comprehensive testing setup for both frontend and backend.

### Frontend Testing

Frontend uses Vitest for unit/component testing and Playwright for E2E testing.

```bash
# In the frontend directory
# Run unit tests
npm test

# Run in watch mode
npm run test:watch

# Run with UI
npm run test:ui

# Generate coverage report
npm run test:coverage

# Run E2E tests
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui
```

### Backend Testing

Backend uses pytest with plugins for testing.

```bash
# In the backend directory
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run with coverage
pytest --cov=app
```

### Running all tests

A script is provided to run all tests in one go:

```bash
./run_tests.sh
```

## Project Structure

- `frontend/` - Frontend application
  - `src/` - Source code
    - `components/` - React components
    - `pages/` - Astro pages
    - `layouts/` - Astro layouts
    - `lib/` - Utilities and services
    - `types.ts` - Shared types
  - `tests/` - Test setup and utilities
  - `playwright/` - E2E tests

- `backend/` - Backend application
  - `app/` - Source code
    - `api/` - API endpoints
    - `models.py` - Database models
    - `services/` - Business logic
    - `crud.py` - Database operations
  - `tests/` - Test directory
    - `unit/` - Unit tests
    - `integration/` - Integration tests

## Contributing

Please read the testing guides in `frontend/tests/README.md` and `backend/tests/README.md` before contributing. 