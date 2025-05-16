export interface User {
  id: string; // UUID z backendu
  email: string;
  first_name: string | null; // Może być null, jeśli nie ustawione
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  first_name: string; // Przy rejestracji zakładamy, że imię jest wymagane
  password: string;
}

// Typ dla odpowiedzi z endpointu /api/auth/login
export interface TokenResponse {
  access_token: string;
  token_type: string; // np. "bearer"
  expires_in: number; // Czas życia access_token w sekundach
  refresh_token: string;
  // Możliwe, że ten endpoint zwraca też od razu dane użytkownika,
  // jeśli tak, trzeba je tu dodać. Na razie zakładam, że nie.
}

// Usunięto interfejs UserDetails, ponieważ był pusty i nieużywany aktywnie.
// Jeśli w przyszłości endpoint /api/users/me będzie potrzebny i będzie zwracał
// inną strukturę niż User, można go będzie przywrócić.
// export interface UserDetails extends User {}

// Typ dla pełnych danych przechowywanych w sesji przez setSession/getSession
// Łączy informacje o tokenach i użytkowniku
export interface FullSessionData extends TokenResponse {
  // Dane użytkownika, które chcemy przechowywać bezpośrednio w sesji
  // aby uniknąć ponownego zapytania do /api/users/me przy każdym odświeżeniu,
  // jeśli `getSession` ma zwracać "pełne dane użytkownika".
  userId: string; // id użytkownika, może być to samo co User.id
  email: string; // email użytkownika
  user_first_name: string | null; // first_name użytkownika, unikamy konfliktu nazw z User.first_name
}

// Stary typ AuthResponse, może być przestarzały jeśli /api/auth/login nie zwraca usera
// export interface AuthResponse {
//   access_token: string;
//   user: User;
// }

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  resetPassword: (email: string) => Promise<void>;
}
