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
  name: string;
} 