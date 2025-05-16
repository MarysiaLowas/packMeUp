#!/bin/bash

# Run frontend unit tests
echo "Running frontend unit tests..."
cd frontend && npm test
FRONTEND_UNIT_RESULT=$?
cd ..

# Run frontend E2E tests with a timeout to prevent hanging
echo "Running frontend E2E tests..."
cd frontend
# Run the tests with a timeout and capture the process ID
timeout 60s npm run test:e2e &
E2E_PID=$!
# Wait for the process to finish
wait $E2E_PID
FRONTEND_E2E_RESULT=$?
# Make sure to kill any background processes that might be running
pkill -f "astro dev" || true
cd ..

# Run backend tests
echo "Running backend tests..."
cd backend && uv run pytest tests/unit/
BACKEND_RESULT=$?
cd ..

# Check if any tests failed
if [ $FRONTEND_UNIT_RESULT -ne 0 ] || [ $FRONTEND_E2E_RESULT -ne 0 ] || [ $BACKEND_RESULT -ne 0 ]; then
  echo "Some tests failed."
  exit 1
else
  echo "All tests passed!"
  exit 0
fi 