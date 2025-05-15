import React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90 shadow hover:shadow-md hover:-translate-y-0.5",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90 shadow hover:shadow-md hover:-translate-y-0.5",
        outline: "border border-grayPurple/20 hover:bg-brandGreen/10 hover:border-brandGreen transition-all duration-200 hover:-translate-y-0.5",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/90 shadow hover:shadow-md hover:-translate-y-0.5",
        ghost: "hover:bg-brandGreen/10 transition-all duration-200",
        link: "underline-offset-4 hover:underline text-primary hover:text-primary/80",
        accent: "bg-accent text-accent-foreground hover:bg-accent/90 shadow hover:shadow-md hover:-translate-y-0.5",
        muted: "bg-muted text-muted-foreground hover:bg-muted/90 shadow-sm hover:shadow hover:-translate-y-0.5",
        success: "bg-success text-success-foreground hover:bg-success/90 shadow hover:shadow-md hover:-translate-y-0.5",
        warning: "bg-warning text-warning-foreground hover:bg-warning/90 shadow hover:shadow-md hover:-translate-y-0.5",
        gradient: "text-white shadow hover:shadow-md hover:-translate-y-0.5 bg-gradient-to-r from-brandGreen to-brandLime border-none",
        gradientAccent: "text-white shadow hover:shadow-md hover:-translate-y-0.5 bg-gradient-to-r from-brandPink to-brandPink/90 border-none",
      },
      size: {
        default: "h-10 py-2 px-4",
        sm: "h-9 px-3 rounded-md",
        lg: "h-11 px-8 rounded-md",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants }
