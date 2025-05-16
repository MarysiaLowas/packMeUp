import * as React from "react";
import { cn } from "@/lib/utils";

export interface LinkProps
  extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
  href: string;
  className?: string;
  children: React.ReactNode;
}

const Link = React.forwardRef<HTMLAnchorElement, LinkProps>(
  ({ className, children, ...props }, ref) => {
    return (
      <a
        ref={ref}
        className={cn(
          "font-medium underline-offset-4 hover:underline",
          className,
        )}
        {...props}
      >
        {children}
      </a>
    );
  },
);
Link.displayName = "Link";

export { Link };
