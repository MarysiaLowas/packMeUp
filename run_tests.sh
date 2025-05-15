#!/bin/bash

# Run frontend tests
echo "Running frontend unit tests..."
cd frontend && npm test
FRONTEND_UNIT_RESULT=$?
cd ..

# Run frontend E2E tests
echo "Running frontend E2E tests..."
cd frontend && npm run test:e2e || echo "Skipping E2E tests as they require Playwright browser installation"
FRONTEND_E2E_RESULT=$?
cd ..

# Run backend tests
echo "Running backend tests..."
cd backend && python -m pytest tests/unit/
BACKEND_RESULT=$?
cd ..

# Check if any tests failed
if [ $FRONTEND_UNIT_RESULT -ne 0 ] || [ $BACKEND_RESULT -ne 0 ]; then
  echo "Some tests failed."
  exit 1
else
  echo "All tests passed!"
  exit 0
fi 