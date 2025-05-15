# API Endpoint Implementation Plan: Special Lists API

## 1. Przegląd punktu końcowego
Implementacja zestawu endpointów REST API do zarządzania specjalnymi listami pakowania. API umożliwia tworzenie, odczytywanie, aktualizowanie i usuwanie list oraz zarządzanie elementami w tych listach.

## 2. Szczegóły żądania

### Endpointy podstawowe:

#### Tworzenie listy
- Metoda: POST
- URL: `/api/special-lists`
- Body:
```json
{
  "name": "string",
  "category": "string"
}
```

#### Pobieranie list
- Metoda: GET
- URL: `/api/special-lists`
- Parametry query: brak
- Response:
```json
{
  "items": [
    {
      "id": "uuid",
      "userId": "uuid",
      "name": "string",
      "category": "string",
      "createdAt": "datetime",
      "updatedAt": "datetime"
    }
  ],
  "total": 0
}
```

#### Szczegóły listy
- Metoda: GET
- URL: `/api/special-lists/{listId}`
- Parametry path: listId (UUID)
- Response:
```json
{
  "id": "uuid",
  "userId": "uuid",
  "name": "string",
  "category": "string",
  "createdAt": "datetime",
  "updatedAt": "datetime",
  "items": [
    {
      "itemId": "uuid",
      "quantity": 1,
      "item": {
        "id": "uuid",
        "name": "string",
        "weight": 0.0,
        "dimensions": "string",
        "category": "string"
      }
    }
  ],
  "tags": [
    {
      "id": "uuid",
      "name": "string"
    }
  ]
}
```

#### Aktualizacja listy
- Metoda: PUT
- URL: `/api/special-lists/{listId}`
- Parametry path: listId (UUID)
- Body:
```json
{
  "name": "string",
  "category": "string"
}
```

#### Usuwanie listy
- Metoda: DELETE
- URL: `/api/special-lists/{listId}`
- Parametry path: listId (UUID)

### Endpointy zarządzania elementami:

#### Dodawanie elementu
- Metoda: POST
- URL: `/api/special-lists/{listId}/items`
- Parametry path: listId (UUID)
- Body:
```json
{
  "itemId": "uuid?",
  "name": "string",
  "quantity": 1,
  "weight": 0.0,
  "dimensions": "string?",
  "category": "string?"
}
```
- Response:
```json
{
  "itemId": "uuid",
  "quantity": 1,
  "item": {
    "id": "uuid",
    "name": "string",
    "weight": 0.0,
    "dimensions": "string",
    "category": "string"
  }
}
```

#### Usuwanie elementu
- Metoda: DELETE
- URL: `/api/special-lists/{listId}/items/{itemId}`
- Parametry path: listId (UUID), itemId (UUID)

## 3. Wykorzystywane typy

```python
# Pydantic models dla API
from pydantic import BaseModel, Field, constr
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class TagDTO(BaseModel):
    id: UUID
    name: str

class ItemDTO(BaseModel):
    id: UUID
    name: str
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    category: Optional[str] = None

class SpecialListItemWithDetailsDTO(BaseModel):
    itemId: UUID
    quantity: int
    item: ItemDTO

class SpecialListDTO(BaseModel):
    id: UUID
    userId: UUID
    name: str
    category: str
    createdAt: datetime
    updatedAt: datetime

class SpecialListDetailDTO(SpecialListDTO):
    items: List[SpecialListItemWithDetailsDTO]
    tags: List[TagDTO]

class CreateSpecialListCommand(BaseModel):
    name: str
    category: str

class UpdateSpecialListCommand(BaseModel):
    name: str
    category: str

class CreateItemCommand(BaseModel):
    name: constr(min_length=1, max_length=255)
    weight: Optional[float] = Field(None, ge=0)
    dimensions: Optional[str] = None
    category: Optional[str] = None

class AddSpecialListItemCommand(BaseModel):
    itemId: Optional[UUID] = None
    name: constr(min_length=1, max_length=255)
    quantity: int = Field(gt=0)
    weight: Optional[float] = Field(None, ge=0)
    dimensions: Optional[str] = None
    category: Optional[str] = None

    @validator('itemId', always=True)
    def validate_item_data(cls, v, values):
        if v is None and 'name' not in values:
            raise ValueError('name is required when itemId is not provided')
        return v
```

## 4. Przepływ danych

1. Warstwa kontrolera:
   - Walidacja wejścia przez Pydantic models
   - Autoryzacja użytkownika przez JWT token
   - Przekazanie do serwisu

2. Warstwa serwisu:
   ```python
   class SpecialListService:
       def __init__(self, db: Session):
           self.db = db
           self.repo = SpecialListRepository(db)
           self.item_repo = ItemRepository(db)

       async def create_special_list(
           self, user_id: UUID, data: CreateSpecialListCommand
       ) -> SpecialList:
           # Sprawdzenie limitów użytkownika
           await self._check_user_lists_limit(user_id)
           
           special_list = SpecialList(
               user_id=user_id,
               name=data.name,
               category=data.category
           )
           return await self.repo.create(special_list)

       async def add_item(
           self, list_id: UUID, user_id: UUID, data: AddSpecialListItemCommand
       ) -> SpecialListItem:
           # Sprawdzenie czy lista należy do użytkownika
           special_list = await self._get_user_list(list_id, user_id)
           
           # Pobranie lub utworzenie itemu
           item = None
           if data.itemId:
               item = await self.item_repo.get(data.itemId)
               if not item:
                   raise SpecialListError("Item not found", 404)
           else:
               # Sprawdzenie czy item o takiej nazwie już istnieje
               item = await self.item_repo.get_by_name(data.name)
               if not item:
                   # Utworzenie nowego itemu
                   item = Item(
                       name=data.name,
                       weight=data.weight,
                       dimensions=data.dimensions,
                       category=data.category
                   )
                   item = await self.item_repo.create(item)
           
           # Sprawdzenie czy item już istnieje w liście
           if await self.repo.item_exists(list_id, item.id):
               raise SpecialListError("Item already exists in list", 409)
           
           special_list_item = SpecialListItem(
               special_list_id=list_id,
               item_id=item.id,
               quantity=data.quantity
           )
           return await self.repo.add_item(special_list_item)

       async def _get_user_list(self, list_id: UUID, user_id: UUID) -> SpecialList:
           special_list = await self.repo.get(list_id)
           if not special_list:
               raise SpecialListError("Special list not found", 404)
           if special_list.user_id != user_id:
               raise SpecialListError("Access denied", 403)
           return special_list
   ```

3. Warstwa repozytorium:
   ```python
   class ItemRepository:
       def __init__(self, db: Session):
           self.db = db

       async def get_by_name(self, name: str) -> Optional[Item]:
           return await self.db.query(Item).filter(Item.name == name).first()
   ```

## 5. Względy bezpieczeństwa

1. Uwierzytelnianie:
   - Wykorzystanie istniejącego middleware JWT
   - Walidacja tokenu w każdym żądaniu

2. Autoryzacja:
   - Sprawdzanie właściciela listy przez user_id
   - Izolacja danych między użytkownikami przez filtrowanie po user_id
   - Walidacja uprawnień przed każdą operacją modyfikacji

3. Walidacja danych:
   - Pydantic models z walidatorami
   - Sprawdzanie limitów (ilość list, ilość elementów)
   - Walidacja relacji (istnienie elementów, unikalność w liście)

## 6. Obsługa błędów

```python
class SpecialListError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

@app.exception_handler(SpecialListError)
async def special_list_exception_handler(request: Request, exc: SpecialListError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message}
    )
```

Kody błędów:
- 400: Nieprawidłowe dane wejściowe (np. nieprawidłowa ilość)
- 401: Brak autoryzacji (brak lub nieprawidłowy token)
- 403: Brak uprawnień (próba dostępu do cudzej listy)
- 404: Lista/element nie znaleziony
- 409: Konflikt (element już istnieje w liście)
- 500: Błąd serwera

## 7. Rozważania dotyczące wydajności

1. Indeksowanie:
   - Wykorzystanie istniejących indeksów z modeli:
     - user_id w special_lists
     - item_id w special_list_items
     - name w special_lists

2. Paginacja:
   - Implementacja dla list długich (limit/offset)
   - Limit rozmiaru odpowiedzi (max 50 elementów na stronę)
   - Sortowanie po created_at domyślnie

3. Optymalizacja zapytań:
   - Eager loading dla items i tags w szczegółach listy
   - Lazy loading dla list podstawowych
   - Cachowanie częstych zapytań

## 8. Etapy wdrożenia

1. Implementacja serwisu:
   - SpecialListService z metodami CRUD
   - Metody zarządzania elementami
   - Walidacja biznesowa

2. Implementacja endpointów:
```python
@router.post("/", response_model=SpecialListDTO)
async def create_special_list(
    data: CreateSpecialListCommand,
    current_user: User = Depends(get_current_user),
    service: SpecialListService = Depends()
):
    """Tworzy nową listę specjalną."""
    return await service.create_special_list(current_user.id, data)

@router.get("/{list_id}", response_model=SpecialListDetailDTO)
async def get_special_list(
    list_id: UUID,
    current_user: User = Depends(get_current_user),
    service: SpecialListService = Depends()
):
    """Pobiera szczegóły listy specjalnej."""
    return await service.get_list_with_details(list_id, current_user.id)
```

3. Dokumentacja API:
   - OpenAPI/Swagger dokumentacja
   - Przykłady użycia
   - Opis kodów błędów 