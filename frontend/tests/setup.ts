import '@testing-library/jest-dom';
import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';

// Clean up after each test
afterEach(() => {
  cleanup();
});

// Setup to console.error if any React warnings are thrown
// This helps catch any potential issues in tests
const originalConsoleError = console.error;
console.error = (...args: any[]) => {
  // Check if the error is a React-related warning
  if (typeof args[0] === 'string' && args[0].includes('Warning: ')) {
    throw new Error(args[0]);
  }
  originalConsoleError(...args);
};

// Global mocks can be added here
// For example, if you need to mock fetch:
// global.fetch = vi.fn();

// Set up any global variables that might be needed 