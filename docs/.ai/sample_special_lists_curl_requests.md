# Sample Curl Requests for Special Lists API

Below are some sample curl commands to test the endpoints in special_lists.py. Replace YOUR_TOKEN with your actual authentication token as needed.

## 1. Create Special List

Create a new special list.

```bash
curl -X POST http://localhost:8000/api/special-lists/ \
     -H "Content-Type: application/json" \
     -d '{
           "name": "My Special List",
           "category": "Travel",
           "description": "Packing list for summer vacation"
         }'
```

## 2. Get Special Lists (Paginated)

Retrieve special lists with pagination, filters, and sorting.

```bash
curl -X GET "http://localhost:8000/api/special-lists/?page=1&page_size=10&category=Travel&search=vacation&sort_field=CREATED_AT&sort_order=DESC" \
     -H "Authorization: Bearer YOUR_TOKEN"
```

## 3. Get Special List Details

Get details of a specific special list by ID.

```bash
curl -X GET http://localhost:8000/api/special-lists/123e4567-e89b-12d3-a456-426614174000 \
     -H "Authorization: Bearer YOUR_TOKEN"
```

## 4. Update Special List

Update an existing special list by ID.

```bash
curl -X PUT http://localhost:8000/api/special-lists/123e4567-e89b-12d3-a456-426614174000 \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d '{
           "name": "Updated List Name",
           "category": "Updated Category",
           "description": "Updated description"
         }'
```

## 5. Delete Special List

Delete a special list by ID.

```bash
curl -X DELETE http://localhost:8000/api/special-lists/123e4567-e89b-12d3-a456-426614174000 \
     -H "Authorization: Bearer YOUR_TOKEN"
```

## 6. Add Item to Special List

Add an item to a special list.

```bash
curl -X POST http://localhost:8000/api/special-lists/123e4567-e89b-12d3-a456-426614174000/items \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d '{
           "item_id": "abcdef12-3456-7890-abcd-ef1234567890",
           "quantity": 2
         }'
```

## 7. Remove Item from Special List

Remove an item from a special list by list ID and item ID.

```bash
curl -X DELETE http://localhost:8000/api/special-lists/123e4567-e89b-12d3-a456-426614174000/items/abcdef12-3456-7890-abcd-ef1234567890 \
     -H "Authorization: Bearer YOUR_TOKEN"
```

## 8. Update Item Quantity in Special List

Update the quantity of an item in a special list.

```bash
curl -X PUT http://localhost:8000/api/special-lists/123e4567-e89b-12d3-a456-426614174000/items/abcdef12-3456-7890-abcd-ef1234567890 \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d '{
           "quantity": 3
         }'
```

## 9. Add Tag to Special List

Add a tag to a special list.

```bash
curl -X POST http://localhost:8000/api/special-lists/123e4567-e89b-12d3-a456-426614174000/tags \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d '{
           "name": "Urgent"
         }'
```

## 10. Remove Tag from Special List

Remove a tag from a special list by list ID and tag ID.

```bash
curl -X DELETE http://localhost:8000/api/special-lists/123e4567-e89b-12d3-a456-426614174000/tags/123e4567-e89b-12d3-a456-426614174001 \
     -H "Authorization: Bearer YOUR_TOKEN"
``` 