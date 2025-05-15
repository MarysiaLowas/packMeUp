# Backend Testing Guide

This project uses pytest and its plugins for testing backend functionality.

## Test Structure

The tests are organized in the following structure:

- `tests/unit/` - Unit tests for individual functions, classes, and modules
- `tests/integration/` - Integration tests for API endpoints and database functionality
- `conftest.py` - Shared fixtures and configuration

## Running Tests

To run all tests:
```bash
pytest
```

To run specific test categories:
```bash
# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run tests with the 'slow' marker
pytest -m slow
```

To run tests with coverage:
```bash
pytest --cov=app
```

## Fixtures

Common fixtures are defined in `conftest.py`:

- `test_client` - A FastAPI TestClient for API testing
- `async_engine` - Async SQLAlchemy engine for database testing
- `async_session` - Async SQLAlchemy session for database operations
- `mock_db_session` - Mock session for testing without database access

## Test Markers

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow tests that might be skipped in quick runs

## Best Practices

1. **Keep tests isolated** - Each test should be able to run independently
2. **Use fixtures** - For common setup and teardown
3. **Follow AAA pattern** - Arrange, Act, Assert
4. **Mock external dependencies** - Use pytest-mock to create mocks and stubs
5. **Use parametrization** - For testing multiple inputs with the same test logic
6. **Test both success and error cases** - Ensure proper error handling

## Async Testing

Use the `@pytest.mark.asyncio` decorator for async tests and `async_session` fixture for database operations. 