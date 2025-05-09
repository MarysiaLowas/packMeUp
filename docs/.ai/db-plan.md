# PackMeUp - PostgreSQL Database Schema

This document outlines the database schema for the PackMeUp application based on the PRD, session notes, and technical stack.

## 1. Tables

### `users`
Stores user account information.

| Column          | Type                     | Constraints                                  | Description                       |
|-----------------|--------------------------|----------------------------------------------|-----------------------------------|
| `id`            | `UUID PRIMARY KEY`       | `DEFAULT gen_random_uuid()`                  | Unique identifier for the user    |
| `email`         | `TEXT`                   | `NOT NULL, UNIQUE`                           | User's email address (login)    |
| `hashed_password`| `TEXT`                   | `NOT NULL`                                   | Hashed user password              |
| `first_name`    | `TEXT`                   |                                              | User's first name                 |
| `last_name`    | `TEXT`                   |                                              | User's last name                 |
| `is_admin`      | `BOOLEAN`                | `NOT NULL, DEFAULT FALSE`                    | Flag indicating admin privileges  |
| `created_at`    | `TIMESTAMPTZ`            | `NOT NULL, DEFAULT NOW()`                    | Timestamp of account creation     |
| `updated_at`    | `TIMESTAMPTZ`            | `NOT NULL, DEFAULT NOW()`                    | Timestamp of last update          |

*Note: Password hashing (e.g., using `pgcrypto` extension) should be handled application-side before storing.*

### `items`
Global list of packable items.

| Column         | Type            | Constraints                 | Description                             |
|----------------|-----------------|-----------------------------|-----------------------------------------|
| `id`           | `UUID PRIMARY KEY`| `DEFAULT gen_random_uuid()` | Unique identifier for the item          |
| `name`         | `TEXT`          | `NOT NULL, UNIQUE`          | Name of the item                        |
| `weight`       | `NUMERIC(5,3)`  | `CHECK (weight >= 0)`       | Weight of the item in kg (optional)     |
| `dimensions`   | `TEXT`          |                             | Dimensions "WxHxD" in cm (optional)        |
| `category`     | `TEXT`          |                             | Item category (app-managed, optional) |
| `created_at`   | `TIMESTAMPTZ`   | `NOT NULL, DEFAULT NOW()`   | Timestamp of item creation            |
| `updated_at`   | `TIMESTAMPTZ`   | `NOT NULL, DEFAULT NOW()`   | Timestamp of last item update         |

*Note: Validation of `dimensions` format happens in the application.*

### `tags`
Global list of tags for categorizing trips and special lists.

| Column       | Type            | Constraints                 | Description                       |
|--------------|-----------------|-----------------------------|-----------------------------------|
| `id`         | `UUID PRIMARY KEY`| `DEFAULT gen_random_uuid()` | Unique identifier for the tag     |
| `name`       | `TEXT`          | `NOT NULL, UNIQUE`          | Name of the tag                   |
| `created_at` | `TIMESTAMPTZ`   | `NOT NULL, DEFAULT NOW()`   | Timestamp of tag creation       |
| `updated_at` | `TIMESTAMPTZ`   | `NOT NULL, DEFAULT NOW()`   | Timestamp of last tag update    |

### `trips`
Stores details about planned trips.

| Column             | Type            | Constraints                             | Description                                     |
|--------------------|-----------------|-----------------------------------------|-------------------------------------------------|
| `id`               | `UUID PRIMARY KEY`| `DEFAULT gen_random_uuid()`             | Unique identifier for the trip                  |
| `user_id`          | `UUID`          | `NOT NULL, REFERENCES users(id) ON DELETE CASCADE` | Foreign key to the user who owns the trip     |
| `destination`      | `TEXT`          |`NOT NULL`                               | Trip destination                                |
| `start_date`       | `DATE`          |                                         | Start date of the trip                          |
| `end_date`         | `DATE`          |                                         | End date of the trip                            |
| `duration_days`    | `INTEGER`       | `NOT NULL, CHECK (duration_days > 0)`     | Duration of the trip in days                    |
| `num_adults`       | `INTEGER`       | `NOT NULL, DEFAULT 1, CHECK (num_adults >= 0)` | Number of adults on the trip                  |
| `children_ages`    | `INTEGER[]`     |                                         | Array of children's ages                        |
| `accommodation`    | `TEXT`          |                                         | Type of accommodation (app-managed enum)        |
| `catering`         | `INTEGER[]`     |                                         | Type of catering (app-managed list selection) |
| `transport`        | `TEXT`          |                                         | Mode of transport (app-managed enum)            |
| `activities`       | `TEXT[]`        |                                         | Planned activities                              |
| `season`           | `TEXT`          |                                         | Season of the trip (app-managed enum)           |
| `available_luggage`| `JSONB`         |                                         | Details about available luggage (app-validated) |
| `created_at`       | `TIMESTAMPTZ`   | `NOT NULL, DEFAULT NOW()`               | Timestamp of trip creation                    |
| `updated_at`       | `TIMESTAMPTZ`   | `NOT NULL, DEFAULT NOW()`               | Timestamp of last trip update                 |

*Note: Trip name is constructed dynamically by the application. `available_luggage` schema validation is handled by the application.*

### `special_lists`
User-defined lists for specific contexts (e.g., activities, item types).

| Column       | Type            | Constraints                                           | Description                                       |
|--------------|-----------------|-------------------------------------------------------|---------------------------------------------------|
| `id`         | `UUID PRIMARY KEY`| `DEFAULT gen_random_uuid()`                           | Unique identifier for the special list            |
| `user_id`    | `UUID`          | `NOT NULL, REFERENCES users(id) ON DELETE CASCADE`    | Foreign key to the user who owns the list       |
| `name`       | `TEXT`          | `NOT NULL`                                            | Name of the special list                          |
| `category`   | `TEXT`          | `NOT NULL`                                            | Category of the list (app-managed enum)           |
| `created_at` | `TIMESTAMPTZ`   | `NOT NULL, DEFAULT NOW()`                             | Timestamp of list creation                      |
| `updated_at` | `TIMESTAMPTZ`   | `NOT NULL, DEFAULT NOW()`                             | Timestamp of last list update                   |

### `generated_lists`
Packing lists generated by the AI based on trip details and special lists.

| Column       | Type            | Constraints                                           | Description                                       |
|--------------|-----------------|-------------------------------------------------------|---------------------------------------------------|
| `id`         | `UUID PRIMARY KEY`| `DEFAULT gen_random_uuid()`                           | Unique identifier for the generated list        |
| `user_id`    | `UUID`          | `NOT NULL, REFERENCES users(id) ON DELETE CASCADE`    | Foreign key to the user who owns the list       |
| `trip_id`    | `UUID`          | `NOT NULL, UNIQUE, REFERENCES trips(id) ON DELETE CASCADE` | Foreign key to the associated trip (1:1 link) |
| `name`       | `TEXT`          | `NOT NULL`                                            | Name of the generated list (can be based on trip) |
| `created_at` | `TIMESTAMPTZ`   | `NOT NULL, DEFAULT NOW()`                             | Timestamp of list generation                    |
| `updated_at` | `TIMESTAMPTZ`   | `NOT NULL, DEFAULT NOW()`                             | Timestamp of last list update                   |

### `trip_tags` (Junction Table)
Associates tags with trips (Many-to-Many).

| Column    | Type   | Constraints                                     | Description                    |
|-----------|--------|-------------------------------------------------|--------------------------------|
| `trip_id` | `UUID` | `NOT NULL, REFERENCES trips(id) ON DELETE CASCADE` | Foreign key to the trip        |
| `tag_id`  | `UUID` | `NOT NULL, REFERENCES tags(id) ON DELETE CASCADE`  | Foreign key to the tag         |
|           |        | `PRIMARY KEY (trip_id, tag_id)`                 | Composite primary key          |

### `special_list_tags` (Junction Table)
Associates tags with special lists (Many-to-Many).

| Column            | Type   | Constraints                                                 | Description                        |
|-------------------|--------|-------------------------------------------------------------|------------------------------------|
| `special_list_id` | `UUID` | `NOT NULL, REFERENCES special_lists(id) ON DELETE CASCADE`  | Foreign key to the special list  |
| `tag_id`          | `UUID` | `NOT NULL, REFERENCES tags(id) ON DELETE CASCADE`           | Foreign key to the tag             |
|                   |        | `PRIMARY KEY (special_list_id, tag_id)`                     | Composite primary key              |

### `special_list_items` (Junction Table)
Associates items with special lists (Many-to-Many), including quantity.

| Column            | Type    | Constraints                                                | Description                             |
|-------------------|---------|------------------------------------------------------------|-----------------------------------------|
| `special_list_id` | `UUID`  | `NOT NULL, REFERENCES special_lists(id) ON DELETE CASCADE` | Foreign key to the special list       |
| `item_id`         | `UUID`  | `NOT NULL, REFERENCES items(id) ON DELETE CASCADE`         | Foreign key to the item               |
| `quantity`        | `INTEGER`| `NOT NULL, DEFAULT 1, CHECK (quantity > 0)`              | Quantity of the item in this list     |
|                   |         | `PRIMARY KEY (special_list_id, item_id)`                   | Composite primary key                   |

### `generated_list_items`
Stores items included in a generated list, their packed status, quantity, and *copied* item details at the time of generation.

| Column              | Type            | Constraints                                                   | Description                                               |
|---------------------|-----------------|---------------------------------------------------------------|-----------------------------------------------------------|
| `id`                | `UUID PRIMARY KEY`| `DEFAULT gen_random_uuid()`                                   | Unique identifier for this list item entry              |
| `generated_list_id` | `UUID`          | `NOT NULL, REFERENCES generated_lists(id) ON DELETE CASCADE`  | Foreign key to the generated list                       |
| `item_id`           | `UUID`          | `REFERENCES items(id) ON DELETE RESTRICT`                     | Foreign key to the original item (optional, for reference)|
| `quantity`          | `INTEGER`       | `NOT NULL, CHECK (quantity > 0)`                              | Quantity of the item to pack                            |
| `is_packed`         | `BOOLEAN`       | `NOT NULL, DEFAULT FALSE`                                     | Packing status of the item                              |
| `item_name`         | `TEXT`          | `NOT NULL`                                                    | Copied item name at generation time                     |
| `item_weight`       | `NUMERIC(5,3)`  | `CHECK (item_weight >= 0)`                                    | Copied item weight at generation time (kg)              |
| `item_dimensions`   | `TEXT`          |                                                               | Copied item dimensions at generation time               |
| `item_category`     | `TEXT`          |                                                               | Copied item category at generation time                 |
| `created_at`        | `TIMESTAMPTZ`   | `NOT NULL, DEFAULT NOW()`                                     | Timestamp of item addition to list                    |
| `updated_at`        | `TIMESTAMPTZ`   | `NOT NULL, DEFAULT NOW()`                                     | Timestamp of last item update (e.g., packing status) |

*Note: `ON DELETE RESTRICT` for `item_id` prevents deleting an item from the global `items` table if it's referenced in any generated list. Application logic should handle this case.*

## 2. Relationships Summary

*   **`users` <-> `trips`**: One-to-Many (A user can have multiple trips)
*   **`users` <-> `special_lists`**: One-to-Many (A user can have multiple special lists)
*   **`users` <-> `generated_lists`**: One-to-Many (A user can have multiple generated lists)
*   **`trips` <-> `generated_lists`**: One-to-One (A trip results in exactly one generated list, linked via `generated_lists.trip_id`)
*   **`trips` <-> `tags`**: Many-to-Many (via `trip_tags`)
*   **`special_lists` <-> `tags`**: Many-to-Many (via `special_list_tags`)
*   **`special_lists` <-> `items`**: Many-to-Many (via `special_list_items`, includes quantity)
*   **`generated_lists` <-> `items`**: Many-to-Many (via `generated_list_items`, includes quantity, packed status, and copied item details. Direct FK to `items` is for reference and has `ON DELETE RESTRICT`)

## 3. Indexes

Standard indexes are typically created automatically for PRIMARY KEY and UNIQUE constraints. Additionally, create indexes on:

*   All Foreign Key columns (`user_id`, `trip_id`, `special_list_id`, `generated_list_id`, `item_id`, `tag_id` in relevant tables).
*   `users(email)`
*   `tags(name)`
*   `special_lists(name)`
*   `generated_list_items(generated_list_id)`

Example Index Creation:
```sql
CREATE INDEX idx_trips_user_id ON trips(user_id);
CREATE INDEX idx_special_lists_user_id ON special_lists(user_id);
CREATE INDEX idx_generated_lists_user_id ON generated_lists(user_id);
CREATE INDEX idx_generated_lists_trip_id ON generated_lists(trip_id); -- Already unique, but explicit index can be useful
CREATE INDEX idx_trip_tags_tag_id ON trip_tags(tag_id);
CREATE INDEX idx_special_list_tags_tag_id ON special_list_tags(tag_id);
CREATE INDEX idx_special_list_items_item_id ON special_list_items(item_id);
CREATE INDEX idx_generated_list_items_item_id ON generated_list_items(item_id);
-- Indexes on frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_tags_name ON tags(name);
CREATE INDEX idx_special_lists_name ON special_lists(name);
```

## 4. Row-Level Security (RLS)

RLS should be enabled on tables containing user-specific data to ensure users can only access their own information. Administrators (`is_admin = true`) should bypass these policies.

**Tables to Enable RLS On:**
*   `trips`
*   `special_lists`
*   `generated_lists`
*   `trip_tags`
*   `special_list_tags`
*   `special_list_items`
*   `generated_list_items`

**Example Policy (using Supabase JWT context):**
(Replace `auth.uid()` or `current_setting(...)` with the actual mechanism used for identifying the current user ID).

```sql
-- Enable RLS
ALTER TABLE trips ENABLE ROW LEVEL SECURITY;
ALTER TABLE special_lists ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_lists ENABLE ROW LEVEL SECURITY;
-- ... enable for other relevant tables

-- Policy for users on 'trips'
CREATE POLICY "Allow user access to own trips"
ON trips FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Policy for admins on 'trips'
CREATE POLICY "Allow admin full access to trips"
ON trips FOR ALL
USING (EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND is_admin))
WITH CHECK (EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND is_admin));

-- Similar policies should be created for special_lists, generated_lists, and junction tables based on user_id linkage.
-- For junction tables like trip_tags, the policy might check ownership of the related trip:
-- CREATE POLICY "Allow user access to own trip_tags"
-- ON trip_tags FOR ALL
-- USING (EXISTS (SELECT 1 FROM trips WHERE trips.id = trip_tags.trip_id AND trips.user_id = auth.uid()))
-- WITH CHECK (EXISTS (SELECT 1 FROM trips WHERE trips.id = trip_tags.trip_id AND trips.user_id = auth.uid()));
```

*Note: The exact RLS implementation depends on the authentication mechanism.*

## 5. Additional Considerations

*   **Enums/Allowed Values:** Values for fields like `trips.accommodation`, `trips.transport`, `trips.season`, `trips.catering`, `special_lists.category`, and `items.category` are managed and validated by the backend application (FastAPI).
*   **Application-Level Validation:** Complex validation (e.g., `items.dimensions` format, `trips.available_luggage` JSON schema) is handled by the application.
*   **Password Hashing:** Ensure strong password hashing (e.g., using `bcrypt` via `passlib` in Python) is implemented in the application before storing the hash in `users.hashed_password`. Consider using the `pgcrypto` extension for some operations if needed.
*   **Migrations:** Use a migration tool like Alembic (mentioned in the tech stack) to manage schema changes over time.
*   **UUID Generation:** The schema assumes the `pgcrypto` extension is available for `gen_random_uuid()`. If not, adjust the default UUID generation method.
*   **ON DELETE RESTRICT Handling:** The application needs logic to gracefully handle potential errors when deleting an `item` that is still referenced in `generated_list_items`.
``` 