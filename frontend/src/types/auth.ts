export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  name: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterResponse {
  id: string;
  email: string;
  name: string;
}

export interface ApiError {
  code: string;
  message: string;
}

export interface User {
  id: string;
  email: string;
  first_name: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  first_name: string;
}

export interface Token {
  access_token: string;
  token_type: string;
  expires_in: number;
} 