# API Endpoints Implementation Plan: Trips Management

## 1. Overview
This is the implementation plan for the Trip Management endpoints in PackMeUp application. These endpoints handle trip creation, management, and packing list generation using FastAPI and SQLAlchemy.

## 2. Endpoints Details

### 2.1 Create Trip (POST /api/trips)
#### Request
- Method: POST
- Authentication: Required
- Content-Type: application/json
- Request Body: CreateTripCommand

#### Validation Rules
- destination: Required, non-empty string
- durationDays: Required, integer > 0
- numAdults: Required, integer ≥ 0
- startDate/endDate: Optional, valid ISO dates
- childrenAges: Optional array of integers
- accommodation: Optional, valid enum value
- catering: Optional array of integers
- transport: Optional, valid enum value
- activities: Optional array of strings
- season: Optional, valid enum value
- availableLuggage: Optional, valid LuggageDTO schema

### 2.2 List Trips (GET /api/trips)
#### Request
- Method: GET
- Authentication: Required
- Query Parameters:
  - limit: integer, default=10
  - offset: integer, default=0
  - sort: string, optional

#### Response
- ListTripsResponseDTO with pagination

### 2.3 Get Trip Details (GET /api/trips/{tripId})
#### Request
- Method: GET
- Authentication: Required
- Path Parameters: tripId (UUID)

#### Response
- TripDTO or 404

### 2.4 Update Trip (PUT /api/trips/{tripId})
#### Request
- Method: PUT
- Authentication: Required
- Path Parameters: tripId (UUID)
- Request Body: UpdateTripCommand

### 2.5 Delete Trip (DELETE /api/trips/{tripId})
#### Request
- Method: DELETE
- Authentication: Required
- Path Parameters: tripId (UUID)

### 2.6 Generate Packing List (POST /api/trips/{tripId}/generate-list)
#### Request
- Method: POST
- Authentication: Required
- Path Parameters: tripId (UUID)
- Request Body: GeneratePackingListCommand (optional)

## 3. Required Types

### 3.1 Pydantic Models
```python
class LuggageModel(BaseModel):
    maxWeight: float
    dimensions: str

class TripBase(BaseModel):
    destination: str
    startDate: Optional[date]
    endDate: Optional[date]
    durationDays: int
    numAdults: int
    childrenAges: Optional[List[int]]
    accommodation: Optional[str]
    catering: Optional[List[int]]
    transport: Optional[str]
    activities: Optional[List[str]]
    season: Optional[str]
    availableLuggage: Optional[LuggageModel]

class CreateTripModel(TripBase):
    class Config:
        schema_extra = {
            "example": {
                "destination": "Paris, France",
                "durationDays": 10,
                "numAdults": 2
            }
        }

class UpdateTripModel(TripBase):
    pass

class TripResponse(TripBase):
    id: UUID
    userId: UUID
    createdAt: datetime
    updatedAt: Optional[datetime]
```

### 3.2 SQLAlchemy Models
```python
class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    destination = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    duration_days = Column(Integer, nullable=False)
    num_adults = Column(Integer, nullable=False)
    children_ages = Column(ARRAY(Integer))
    accommodation = Column(String)
    catering = Column(ARRAY(Integer))
    transport = Column(String)
    activities = Column(ARRAY(String))
    season = Column(String)
    available_luggage = Column(JSONB)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
```

## 4. Data Flow

### 4.1 Create Trip Flow
1. Validate request body using Pydantic model
2. Extract user_id from auth context
3. Create Trip SQLAlchemy model
4. Commit to database
5. Return created trip

### 4.2 List Trips Flow
1. Extract pagination parameters
2. Query trips table with user_id filter
3. Apply sorting if requested
4. Return paginated results

### 4.3 Generate Packing List Flow
1. Validate trip exists and belongs to user
2. Call AI service with trip details
3. Create generated list entry
4. Create generated list items
5. Return generated list

## 5. Security Considerations

### 5.1 Authentication
- JWT token validation for all endpoints
- User ID extraction from token

### 5.2 Authorization
- Verify trip ownership for all operations
- Implement row-level security in database

### 5.3 Input Validation
- Strict type checking via Pydantic
- SQL injection prevention via SQLAlchemy
- XSS prevention via input sanitization

### 5.4 Rate Limiting
- Implement rate limiting per user
- Higher limits for premium users

## 6. Error Handling

### 6.1 HTTP Status Codes
- 200: Successful GET/PUT operations
- 201: Successful POST operations
- 204: Successful DELETE operations
- 400: Invalid input data
- 401: Missing/invalid authentication
- 403: Unauthorized access
- 404: Resource not found
- 500: Server errors

### 6.2 Error Responses
```python
class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]]
```

### 6.3 Custom Exceptions
```python
class TripNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Trip not found"
        )

class TripAccessDeniedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Access denied"
        )
```

## 7. Performance Considerations

### 7.1 Database Optimization
- Index on user_id column
- Index on created_at for sorting
- Composite index for pagination
- Partial index for active trips

### 7.2 Caching Strategy
- Cache trip details (5 minutes TTL)
- Cache user's active trips list
- Cache generated packing lists

### 7.3 Query Optimization
- Use select_from for complex queries
- Implement lazy loading for related data
- Use count() over len() for pagination

## 8. Implementation Steps

### 8.1 Database Setup
1. Create trips table migration
2. Add indexes
3. Setup test database

### 8.2 Models Implementation
1. Create Pydantic models
2. Create SQLAlchemy models
3. Implement model validators

### 8.3 Service Layer
1. Create TripService class
2. Implement CRUD operations
3. Add business logic validation
4. Implement packing list generation

### 8.4 API Layer
1. Create trips router
2. Implement endpoint handlers
3. Add authentication middleware
4. Add rate limiting

### 8.5 Error Handling
1. Create custom exceptions
2. Implement exception handlers
3. Add error logging

### 8.6 Testing
1. Unit tests for models
2. Integration tests for endpoints
3. Performance testing
4. Security testing

### 8.7 Documentation
1. Update API documentation
2. Add code comments
3. Create usage examples

### 8.8 Deployment
1. Create database migrations
2. Update CI/CD pipeline
3. Deploy to staging
4. Monitor performance 