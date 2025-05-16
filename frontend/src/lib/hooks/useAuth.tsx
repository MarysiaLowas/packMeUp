import { useContext } from "react";
import { AuthContext } from "../providers/AuthProvider";
import type { AuthContextType } from "@/lib/types/auth";

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);

  if (context === null) {
    throw new Error(
      "useAuth must be used within an AuthProvider. " +
        "Make sure you have wrapped your component tree with AuthProvider.",
    );
  }

  return context;
}
