import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  variant?: "default" | "primary" | "secondary" | "accent";
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, variant = "default", type, ...props }, ref) => {
    const variantClasses = {
      default:
        "border-grayPurple/15 focus-visible:border-brandGreen focus-visible:ring-brandGreen/25 bg-white/80 focus-visible:bg-white",
      primary:
        "border-brandGreen/20 focus-visible:border-brandGreen focus-visible:ring-brandGreen/30 bg-brandGreen/5 focus-visible:bg-white",
      secondary:
        "border-brandLime/20 focus-visible:border-brandLime focus-visible:ring-brandLime/30 bg-brandLime/5 focus-visible:bg-white",
      accent:
        "border-brandPink/20 focus-visible:border-brandPink focus-visible:ring-brandPink/30 bg-brandPink/5 focus-visible:bg-white",
    };

    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-md border bg-background px-3 py-2 text-sm ring-offset-background",
          "placeholder:text-muted-foreground/70",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
          "disabled:cursor-not-allowed disabled:opacity-50",
          "transition-all duration-200 ease-in-out",
          "hover:border-opacity-80",
          variantClasses[variant],
          className,
        )}
        ref={ref}
        {...props}
      />
    );
  },
);
Input.displayName = "Input";

// Create FormLabel component for consistent styling
interface FormLabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
  variant?: "default" | "primary" | "secondary" | "accent";
  htmlFor?: string;
}

const FormLabel = React.forwardRef<HTMLLabelElement, FormLabelProps>(
  ({ className, variant = "default", htmlFor, ...props }, ref) => {
    const variantClasses = {
      default: "after:bg-brandGreen",
      primary: "after:bg-brandGreen",
      secondary: "after:bg-brandLime",
      accent: "after:bg-brandPink",
    };

    return (
      <label
        ref={ref}
        htmlFor={htmlFor}
        className={cn(
          "font-medium text-grayPurple relative inline-block mb-2",
          "after:absolute after:left-0 after:bottom-[-2px] after:w-6 after:h-0.5 after:rounded-full",
          variantClasses[variant],
          className,
        )}
        {...props}
      />
    );
  },
);
FormLabel.displayName = "FormLabel";

export { Input, FormLabel };
