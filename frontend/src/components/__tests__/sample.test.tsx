import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import React from "react";

// Simple component to test
const Counter = () => {
  const [count, setCount] = React.useState(0);
  return (
    <div>
      <h1 data-testid="count">{count}</h1>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
};

describe("Counter Component", () => {
  it("renders with initial count of 0", () => {
    render(<Counter />);
    expect(screen.getByTestId("count")).toHaveTextContent("0");
  });

  it("increments when button is clicked", () => {
    render(<Counter />);
    fireEvent.click(screen.getByRole("button", { name: /increment/i }));
    expect(screen.getByTestId("count")).toHaveTextContent("1");
  });

  it("demonstrates how to use mocks", () => {
    // Example of mocking a function
    const mockFn = vi.fn();
    mockFn();
    expect(mockFn).toHaveBeenCalledTimes(1);
  });
});

// Example of how to test components that use hooks
describe("Testing Patterns", () => {
  it("demonstrates how to test async operations", async () => {
    const asyncMock = vi.fn().mockResolvedValue("result");
    await expect(asyncMock()).resolves.toBe("result");
    expect(asyncMock).toHaveBeenCalledTimes(1);
  });
});
