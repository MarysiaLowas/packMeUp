/*
 * DTO and Command Model Definitions for PackMeUp Application
 * These types reflect the API plan and are based on the underlying database models.
 */

// User-related DTOs and Commands
export interface UserDTO {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  createdAt: string;
}

export interface RegisterUserCommand {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
}

export interface LoginCommand {
  email: string;
  password: string;
}

export interface AuthResponseDTO {
  token: string;
  user: UserDTO;
}

export interface ForgotPasswordCommand {
  email: string;
}

export interface ResetPasswordCommand {
  token: string;
  newPassword: string;
}

export interface UpdateUserProfileCommand {
  firstName: string;
  lastName: string;
  email: string;
}

// Trip-related DTOs and Commands
export interface LuggageDTO {
  maxWeight: number;
  dimensions: string;
}

export interface CreateTripCommand {
  destination: string;
  startDate?: string; // ISO date string (YYYY-MM-DD)
  durationDays: number;
  numAdults: number;
  childrenAges?: number[];
  accommodation?: string;
  catering?: number[];
  transport?: string;
  activities?: string[];
  season?: string;
  availableLuggage?: LuggageDTO;
}

export interface UpdateTripCommand {
  destination?: string;
  startDate?: string;
  durationDays?: number;
  numAdults?: number;
  childrenAges?: number[];
  accommodation?: string;
  catering?: number[];
  transport?: string;
  activities?: string[];
  season?: string;
  availableLuggage?: LuggageDTO[];
}

export interface TripDTO {
  id: string;
  userId: string;
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
  availableLuggage?: LuggageDTO[];
  createdAt: string;
  updatedAt?: string;
}

export interface ListTripsResponseDTO {
  trips: TripDTO[];
  total: number;
}

// Generate Packing List
export interface GeneratedListItemDTO {
  id: string;
  itemName: string;
  quantity: number;
  isPacked: boolean;
  createdAt?: string;
  updatedAt?: string;
}

export interface GeneratePackingListResponseDTO {
  generatedListId: string;
  name: string;
  items: GeneratedListItemDTO[];
  createdAt: string;
}

export interface GeneratePackingListCommand {
  // Optional overrides for generating a packing list based on trip details
  overrides?: Partial<CreateTripCommand>;
}

export interface GeneratedListDTO {
  id: string;
  userId: string;
  tripId: string;
  name: string;
  createdAt: string;
  updatedAt?: string;
  items: GeneratedListItemDTO[];
}

export interface UpdateGeneratedListItemCommand {
  isPacked?: boolean;
  quantity?: number;
}

// Special Lists and their Items
export interface SpecialListDTO {
  id: string;
  userId: string;
  name: string;
  category: string;
  createdAt: string;
  updatedAt?: string;
}

export interface CreateSpecialListCommand {
  name: string;
  category: string;
}

export interface UpdateSpecialListCommand {
  name?: string;
  category?: string;
}

export interface SpecialListItemDTO {
  itemId: string;
  quantity: number;
}

export interface SpecialListDetailDTO extends SpecialListDTO {
  items: Array<{
    itemId: string;
    quantity: number;
    item: ItemDTO;
  }>;
}

export interface AddItemToSpecialListCommand {
  itemId: string;
  quantity: number;
}

// Item and Tag DTOs
export interface ItemDTO {
  id: string;
  name: string;
  weight?: number;
  dimensions?: string;
  category?: string;
  createdAt: string;
  updatedAt?: string;
}

export interface TagDTO {
  id: string;
  name: string;
  createdAt: string;
  updatedAt?: string;
} 