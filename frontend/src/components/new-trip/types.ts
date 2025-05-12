import type { CreateTripCommand } from "@/types";

export type CreateTripFormShape = {
  destination: string;
  startDate?: string;
  durationDays: number;
  numAdults: number;
  childrenAges?: number[];
  accommodation?: string;
  catering?: number[];
  transport?: string;
  activities?: string[];
  season?: string;
  availableLuggage?: Array<{
    maxWeight?: number;
    dimensions?: string;
  }>;
}; 