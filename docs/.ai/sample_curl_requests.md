# Sample Curl Requests for Testing Trips API

Below are some sample curl commands to test the list_trips and create_trip endpoints in trips.py.

## Create Trip with Full Details

```bash
curl -X POST http://localhost:8000/api/trips/ \
     -H "Content-Type: application/json" \
     -d '{
       "destination": "Paris, France",
       "start_date": "2024-06-15",
       "duration_days": 10,
       "num_adults": 2,
       "children_ages": [5, 8],
       "accommodation": "hotel",
       "catering": [0],
       "transport": "plane",
       "activities": ["sightseeing", "museums"],
       "season": "summer",
       "available_luggage": {
         "max_weight": 23.0,
         "dimensions": "55x40x20"
       }
     }'
```

## Create Trip with Minimal Fields

```bash
curl -X POST http://localhost:8000/api/trips/ \
     -H "Content-Type: application/json" \
     -d '{
       "destination": "Rome, Italy",
       "duration_days": 5,
       "num_adults": 1
     }'
```

## List Trips with Default Pagination and Sorting by Creation Date

```bash
curl -X GET "http://localhost:8000/api/trips/?limit=10&offset=0&sort=created_at"
```

## List Trips with Custom Pagination

```bash
curl -X GET "http://localhost:8000/api/trips/?limit=5&offset=10"
``` 