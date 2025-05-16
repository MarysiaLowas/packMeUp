# Frontend Testing Guide

This project uses two primary testing approaches:

1. **Unit/Component Testing** - Using Vitest and React Testing Library
2. **End-to-End Testing** - Using Playwright

## Unit and Component Testing

Unit and component tests are located in `__tests__` directories next to the code they test.

### Running Unit Tests

```bash
# Run tests once
npm test

# Run tests in watch mode during development
npm run test:watch

# Run tests with UI for better debugging
npm run test:ui

# Generate test coverage report
npm run test:coverage
```

### Creating Unit Tests

- All test files should follow the pattern `*.test.ts` or `*.test.tsx`
- Use the testing libraries as shown in the examples
- Follow the testing patterns demonstrated in the sample tests

### Key Testing Patterns

- Use `describe` blocks to group related tests
- Use `it` for individual test cases with clear descriptions
- Use React Testing Library for component testing
- Use `vi.fn()` and `vi.mock()` for mocking

## End-to-End Testing with Playwright

E2E tests are located in the `playwright/tests` directory.

### Running E2E Tests

```bash
# Run E2E tests
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui
```

### Creating E2E Tests

- Follow the Page Object Model pattern for maintainable tests
- Test real user workflows and journeys
- Focus on critical paths in the application

## Best Practices

1. **Test Pyramid** - Write more unit tests than integration tests, and more integration tests than E2E tests
2. **Clean Tests** - Follow AAA pattern (Arrange, Act, Assert)
3. **Isolation** - Tests should not depend on each other
4. **Meaningful Assertions** - Test behavior, not implementation
5. **Mocks and Stubs** - Use them to isolate units of code
6. **Coverage** - Aim for meaningful coverage, not just numbers
