export interface CreateTripFormShape {
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
  availableLuggage?: {
    maxWeight?: number;
    width?: number;
    height?: number;
    depth?: number;
  }[];
}
