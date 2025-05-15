import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  variant?: "default" | "primary" | "secondary" | "accent";
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, variant = "default", type, ...props }, ref) => {
    const variantClasses = {
      default: "border-input focus-visible:ring-ring",
      primary: "border-primary focus-visible:ring-primary",
      secondary: "border-secondary focus-visible:ring-secondary",
      accent: "border-accent focus-visible:ring-accent",
    };

    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-md border bg-background px-3 py-2 text-sm ring-offset-background",
          "placeholder:text-muted-foreground",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
          "disabled:cursor-not-allowed disabled:opacity-50",
          "transition-colors duration-200",
          variantClasses[variant],
          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);
Input.displayName = "Input";

export { Input };
