# REST API Plan

## 1. Resources

- **Users** (maps to the `users` table)
- **Items** (maps to the `items` table)
- **Tags** (maps to the `tags` table)
- **Trips** (maps to the `trips` table)
- **Special Lists** (maps to the `special_lists` table)
- **Generated Lists** (maps to the `generated_lists` table)
- **Special List Items** (junction table: `special_list_items`)
- **Generated List Items** (junction table: `generated_list_items`)
- **Trip Tags** and **Special List Tags** (junction tables for many-to-many associations)

## 2. Endpoints

### 2.1. Authentication & User Management

#### 2.1.1. Registration
- **Method:** POST
- **URL:** /api/auth/register
- **Description:** Registers a new user.
- **Request Payload:**
  ```json
  {
    "email": "user@example.com",
    "password": "SecretPass123!",
    "firstName": "John",
    "lastName": "Doe"
  }
  ```
- **Response Payload:**
  ```json
  {
    "id": "uuid",
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "createdAt": "timestamp"
  }
  ```
- **Success Codes:** 201 Created
- **Error Codes:** 400 Bad Request, 409 Conflict (if email already exists)

#### 2.1.2. Login
- **Method:** POST
- **URL:** /api/auth/login
- **Description:** Authenticates a user and returns a JWT token.
- **Request Payload:**
  ```json
  {
    "email": "user@example.com",
    "password": "SecretPass123!"
  }
  ```
- **Response Payload:**
  ```json
  {
    "token": "jwt-token",
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe"
    }
  }
  ```
- **Success Codes:** 200 OK
- **Error Codes:** 401 Unauthorized, 400 Bad Request

#### 2.1.3. Password Reset
- **Endpoints:**
  - **POST** /api/auth/forgot-password
    - **Request:** `{ "email": "user@example.com" }`
    - **Response:** `{ "message": "Reset link sent" }`
  - **POST** /api/auth/reset-password
    - **Request:** `{ "token": "reset-token", "newPassword": "NewSecret123!" }`
    - **Response:** `{ "message": "Password updated" }`
- **Success Codes:** 200 OK
- **Error Codes:** 400 Bad Request, 404 Not Found

#### 2.1.4. Profile Management
- **GET** /api/users/me
  - **Description:** Retrieve current user's profile.
- **PUT** /api/users/me
  - **Description:** Update current user's profile.
  - **Request Payload Example:**
    ```json
    {
      "firstName": "Jane",
      "lastName": "Doe",
      "email": "newemail@example.com"
    }
    ```
- **DELETE** /api/users/me
  - **Description:** Delete current user's account.
- **Success Codes:** 200 OK or 204 No Content
- **Error Codes:** 400 Bad Request

### 2.2. Trips (Survey & Trip Management)

#### 2.2.1. Create Trip (Survey Submission)
- **Method:** POST
- **URL:** /api/trips
- **Description:** Creates a new trip based on survey input.
- **Request Payload:**
  ```json
  {
    "destination": "Paris, France",
    "startDate": "2023-12-01",
    "durationDays": 10,
    "numAdults": 2,
    "childrenAges": [5],
    "accommodation": "Hotel",
    "catering": [1, 2],
    "transport": "Plane",
    "activities": ["sightseeing", "museum"],
    "season": "Winter",
    "availableLuggage": [
      {
        "maxWeight": 20,
        "dimensions": "50x40x30"
      },
      {
        "maxWeight": 15
      }
    ]
  }
  ```
- **Response Payload:**
  ```json
  {
    "id": "uuid",
    "userId": "uuid",
    "destination": "Paris, France",
    "startDate": "2023-12-01",
    "durationDays": 10,
    "numAdults": 2,
    "childrenAges": [5],
    "accommodation": "Hotel",
    "catering": [1, 2],
    "transport": "Plane",
    "activities": ["sightseeing", "museum"],
    "season": "Winter",
    "availableLuggage": [
      { "maxWeight": 20, "dimensions": "50x40x30" },
      { "maxWeight": 15 }
    ],
    "createdAt": "timestamp"
  }
  ```
- **Success Codes:** 201 Created
- **Error Codes:** 400 Bad Request

#### 2.2.2. List Trips
- **Method:** GET
- **URL:** /api/trips
- **Description:** Retrieves a paginated list of trips for the authenticated user.
- **Query Parameters:**
  - `limit` (default: 10)
  - `offset` (default: 0)
  - `sort` (e.g., by startDate)
- **Response Payload:**
  ```json
  {
    "trips": [ /* array of trip objects */ ],
    "total": 25
  }
  ```
- **Success Codes:** 200 OK

#### 2.2.3. Get Trip Details
- **Method:** GET
- **URL:** /api/trips/{tripId}
- **Description:** Retrieves detailed information for a specific trip.
- **Success Codes:** 200 OK
- **Error Codes:** 404 Not Found, 403 Forbidden

#### 2.2.4. Update Trip
- **Method:** PUT
- **URL:** /api/trips/{tripId}
- **Description:** Updates a trip's details.
- **Request Payload:** Similar to the creation payload, with fields to update.
- **Success Codes:** 200 OK
- **Error Codes:** 400 Bad Request, 404 Not Found

#### 2.2.5. Delete Trip
- **Method:** DELETE
- **URL:** /api/trips/{tripId}
- **Description:** Deletes a trip.
- **Success Codes:** 204 No Content
- **Error Codes:** 404 Not Found, 403 Forbidden

#### 2.2.6. Generate Packing List for Trip
- **Method:** POST
- **URL:** /api/trips/{tripId}/generate-list
- **Description:** Triggers generation of a packing list using AI based on trip details and user special lists.
- **Request Payload:** May optionally include overrides or additional parameters.
- **Response Payload:**
  ```json
  {
    "generatedListId": "uuid",
    "name": "Packing List for Paris, France",
    "items": [
      {
        "id": "uuid",
        "itemName": "Toothbrush",
        "quantity": 1,
        "isPacked": false
      }
    ],
    "createdAt": "timestamp"
  }
  ```
- **Success Codes:** 201 Created
- **Error Codes:** 400 Bad Request, 404 Not Found

### 2.3. Special Lists

#### 2.3.1. Create Special List
- **Method:** POST
- **URL:** /api/special-lists
- **Description:** Creates a new special list.
- **Request Payload:**
  ```json
  {
    "name": "Beach Essentials",
    "category": "Leisure"
  }
  ```
- **Response Payload:**
  ```json
  {
    "id": "uuid",
    "userId": "uuid",
    "name": "Beach Essentials",
    "category": "Leisure",
    "createdAt": "timestamp"
  }
  ```
- **Success Codes:** 201 Created

#### 2.3.2. List Special Lists
- **Method:** GET
- **URL:** /api/special-lists
- **Description:** Retrieves a list of special lists for the user.
- **Success Codes:** 200 OK

#### 2.3.3. Get Special List Details
- **Method:** GET
- **URL:** /api/special-lists/{listId}
- **Description:** Retrieves details of a specific special list, including its items.
- **Success Codes:** 200 OK

#### 2.3.4. Update Special List
- **Method:** PUT
- **URL:** /api/special-lists/{listId}
- **Description:** Updates the special list's name or category.
- **Request Payload:**
  ```json
  {
    "name": "Updated List Name",
    "category": "Updated Category"
  }
  ```
- **Success Codes:** 200 OK

#### 2.3.5. Delete Special List
- **Method:** DELETE
- **URL:** /api/special-lists/{listId}
- **Description:** Deletes a special list.
- **Success Codes:** 204 No Content

#### 2.3.6. Manage Items in a Special List
- **Add Item**:
  - **Method:** POST
  - **URL:** /api/special-lists/{listId}/items
  - **Request Payload:**
    ```json
    {
      "itemId": "uuid",
      "quantity": 2
    }
    ```
  - **Success Codes:** 201 Created
- **Remove Item**:
  - **Method:** DELETE
  - **URL:** /api/special-lists/{listId}/items/{itemId}
  - **Success Codes:** 204 No Content

### 2.4. Generated Lists & List Items

#### 2.4.1. List Generated Lists
- **Method:** GET
- **URL:** /api/generated-lists
- **Description:** Retrieves a list of AI-generated packing lists for the user.
- **Success Codes:** 200 OK

#### 2.4.2. Get Generated List Details
- **Method:** GET
- **URL:** /api/generated-lists/{listId}
- **Description:** Retrieves details of a specific generated packing list, including its items.
- **Success Codes:** 200 OK

#### 2.4.3. Update Generated List Item (Mark as Packed/Update Quantity)
- **Method:** PATCH
- **URL:** /api/generated-lists/{listId}/items/{itemId}
- **Description:** Updates the status (e.g., marking an item as packed) or edits quantity of an item in the generated list.
- **Request Payload:**
  ```json
  {
    "isPacked": true,
    "quantity": 1
  }
  ```- **Success Codes:** 200 OK

### 2.5. Items and Tags (Global Resources)

#### 2.5.1. List Items
- **Method:** GET
- **URL:** /api/items
- **Description:** Retrieves a list of all items with optional filtering (e.g., by category).
- **Query Parameters:**
  - `category` (optional)
- **Success Codes:** 200 OK

#### 2.5.2. Get Item Details
- **Method:** GET
- **URL:** /api/items/{itemId}
- **Description:** Retrieves details of a specific item.
- **Success Codes:** 200 OK

#### 2.5.3. List Tags
- **Method:** GET
- **URL:** /api/tags
- **Description:** Retrieves a list of tags.
- **Success Codes:** 200 OK

## 3. Authentication and Authorization

- The API uses JWT (JSON Web Tokens) for authentication. All endpoints (except registration, login, and password reset) require a valid JWT in the Authorization header (Bearer token).
- Role-based access: Admin users (`is_admin = true`) may have elevated privileges (e.g., managing global items and tags).
- Row-Level Security (RLS) policies are enforced at the database level to ensure that users can access only their own data.
- Additional measures include rate limiting and secure headers implemented at the API gateway or middleware level.

## 4. Validation and Business Logic

- **Validation:**
  - All incoming payloads are validated against defined JSON schemas.
  - Business rules such as `durationDays` must be greater than 0 and item `weight` must be non-negative are enforced.
  - Unique constraints (e.g., unique email for users, unique item names) are validated on the server side.

- **Business Logic:**
  - **Trip Generation:** The endpoint POST `/api/trips/{tripId}/generate-list` uses AI services to generate a personalized packing list by combining trip details and the user's special lists.
  - **Packed Status Management:** Users can update the `isPacked` status of items in their generated lists to track packing progress.
  - **Pagination, Filtering & Sorting:** All list endpoints support query parameters (e.g., `limit`, `offset`, `sort`, and filtering criteria) to refine responses.
  - **Error Handling:** Consistent error responses include clear messages and appropriate HTTP status codes (e.g., 400 for validation errors, 403 for access violations, 404 for not found).

## Security and Performance Considerations

- **Security:**
  - All API communications must occur over HTTPS.
  - Input validation and sanitation prevent injection attacks.
  - JWT authentication and RLS in the database ensure that users access only their permitted data.
  - Rate limiting and logging help protect against abuse.

- **Performance:**
  - Database indexing on frequently queried fields (e.g., `user_id`, `trip_id`, etc.) supports efficient queries.
  - API responses are designed to minimize payload sizes and include pagination metadata for large result sets. 

