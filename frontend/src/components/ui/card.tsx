import * as React from "react";

import { cn } from "@/lib/utils";

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-lg border border-grayPurple/10 bg-card text-card-foreground shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1 relative overflow-hidden",
      className,
    )}
    {...props}
  />
));
Card.displayName = "Card";

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
));
CardHeader.displayName = "CardHeader";

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, children, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-xl font-semibold leading-none tracking-tight relative pb-2 after:absolute after:left-0 after:bottom-0 after:w-8 after:h-0.5 after:bg-brandGreen after:rounded-full",
      className,
    )}
    {...props}
  >
    {children || <span style={{ display: "none" }}>Card Title</span>}
  </h3>
));
CardTitle.displayName = "CardTitle";

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
));
CardDescription.displayName = "CardDescription";

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
));
CardContent.displayName = "CardContent";

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
));
CardFooter.displayName = "CardFooter";

// Themed card variants
const ThemedCard = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & {
    variant?: "primary" | "secondary" | "accent" | "muted" | "default";
  }
>(({ className, variant = "default", ...props }, ref) => {
  const variantClasses = {
    primary:
      "before:absolute before:top-0 before:left-0 before:w-full before:h-1 before:bg-gradient-to-r before:from-brandGreen before:to-brandLime border-brandGreen/20 hover:border-brandGreen/40 bg-brandGreen/5",
    secondary:
      "before:absolute before:top-0 before:left-0 before:w-full before:h-1 before:bg-gradient-to-r before:from-brandLime before:to-brandLime/70 border-brandLime/20 hover:border-brandLime/40 bg-brandLime/5",
    accent:
      "before:absolute before:top-0 before:left-0 before:w-full before:h-1 before:bg-gradient-to-r before:from-brandPink before:to-grayPurple border-brandPink/20 hover:border-brandPink/40 bg-brandPink/5",
    muted:
      "before:absolute before:top-0 before:left-0 before:w-full before:h-1 before:bg-gradient-to-r before:from-grayPurple before:to-grayGreen border-grayPurple/20 hover:border-grayPurple/30 bg-grayPurple/5",
    default:
      "before:absolute before:top-0 before:left-0 before:w-full before:h-1 before:bg-gradient-to-r before:from-brandGreen/40 before:to-transparent",
  };

  return (
    <Card
      ref={ref}
      className={cn(
        "transition-all duration-300",
        variantClasses[variant],
        className,
      )}
      {...props}
    />
  );
});
ThemedCard.displayName = "ThemedCard";

export {
  Card,
  CardHeader,
  CardFooter,
  CardTitle,
  CardDescription,
  CardContent,
  ThemedCard,
};
