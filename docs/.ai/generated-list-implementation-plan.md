# Plan implementacji funkcjonalności list pakowania

## Opis problemu

Obecnie funkcjonalność list pakowania w aplikacji PackMeUp ma następujące problemy:

1. Istnieją dwa dublujące się endpointy do pobierania pojedynczej listy pakowania:
   - `/api/generated-lists/{list_id}` (w pliku `generated_lists.py`)
   - `/api/trips/{trip_id}/lists/{list_id}` (w pliku `trips.py`)

2. Brakuje endpointu do listowania wszystkich list pakowania użytkownika.

3. Frontend używa endpointu `/api/generated-lists/{list_id}`, ale nawigacja po utworzeniu listy wykorzystuje ścieżkę URL zawierającą ID wycieczki (`/trips/:tripId/lists/:listId`).

## Plan implementacji

### 1. Weryfikacja i rozszerzenie endpointu `/api/generated-lists/{list_id}`

1. **Weryfikacja działania**:
   - Upewnić się, że endpoint `/api/generated-lists/{list_id}` zwraca wszystkie niezbędne dane.
   - Sprawdzić obsługę błędów i kwestie autoryzacji.

2. **Rozszerzenie funkcjonalności**:
   - Dodać konieczne parametry z endpointu `/api/trips/{trip_id}/lists/{list_id}` do endpointu `/api/generated-lists/{list_id}`.
   - Upewnić się, że wszystkie funkcje z usuwanego endpointu są w pełni obsługiwane.

### 2. Stworzenie endpointu do listowania list pakowania

Dodać nowy endpoint `/api/generated-lists` w pliku `generated_lists.py` z następującą funkcjonalnością:

```python
@router.get(
    "/",
    response_model=PaginatedGeneratedListResponse,
    summary="List user's packing lists",
    response_description="List of packing lists with pagination",
)
async def list_generated_lists(
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=100),
    search: Optional[str] = None,
    trip_id: Optional[UUID] = None,
    sort_field: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    current_user_id: UUID = Depends(get_current_user_id),
) -> PaginatedGeneratedListResponse:
    """Get all packing lists for the current user with pagination, filtering, and sorting."""
    try:
        # Construct the base query
        query = (
            select(GeneratedList)
            .where(GeneratedList.user_id == current_user_id)
        )
        
        # Apply filters
        if search:
            query = query.where(GeneratedList.name.ilike(f"%{search}%"))
        
        if trip_id:
            query = query.where(GeneratedList.trip_id == trip_id)
        
        # Count total matching records
        count_query = select(func.count()).select_from(query.subquery())
        total = await GeneratedList.execute_scalar(count_query)
        
        # Apply sorting
        if sort_field == "name":
            sort_column = GeneratedList.name
        elif sort_field == "trip_id":
            sort_column = GeneratedList.trip_id
        else:  # default to created_at
            sort_column = GeneratedList.created_at
            
        if sort_order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())
        
        # Apply pagination
        query = query.offset((page - 1) * page_size).limit(page_size)
        
        # Fetch the lists
        lists = await GeneratedList.select_all(query)
        
        # Calculate total pages
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        
        # Prepare the response
        return PaginatedGeneratedListResponse(
            items=[GeneratedListSummaryDTO.from_orm(lst) for lst in lists],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get packing lists",
        )
```

### 3. Tworzenie niezbędnych DTO

Dodać niezbędne DTO do pliku `backend/app/api/dto.py`:

```python
class GeneratedListSummaryDTO(BaseModel):
    id: UUID
    name: str
    trip_id: UUID
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    items_count: int = Field(..., alias="itemsCount")
    packed_items_count: int = Field(..., alias="packedItemsCount")
    
    @validator("items_count", "packed_items_count", pre=True)
    def compute_counts(cls, v, values, **kwargs):
        return v

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class PaginatedGeneratedListResponse(BaseModel):
    items: List[GeneratedListSummaryDTO]
    total: int
    page: int
    page_size: int = Field(..., alias="pageSize")
    total_pages: int = Field(..., alias="totalPages")

    model_config = ConfigDict(populate_by_name=True)
```

### 4. Usunięcie redundantnego endpointu

Usunąć endpoint `/api/trips/{trip_id}/lists/{list_id}` z pliku `trips.py`.

### 5. Aktualizacja typów w TypeScript

Zaktualizować plik `frontend/src/types.ts`, dodając nowe typy:

```typescript
export interface GeneratedListSummaryDTO {
  id: string;
  name: string;
  tripId: string;
  createdAt: string;
  updatedAt?: string;
  itemsCount: number;
  packedItemsCount: number;
}

export interface PaginatedGeneratedListResponse {
  items: GeneratedListSummaryDTO[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}
```

### 6. Stworzenie komponentu do wyświetlania listy list pakowania

Stworzyć nowy komponent `frontend/src/components/packing-list/PackingLists.tsx`:

```tsx
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { apiClient } from "@/lib/api-client";
import type { PaginatedGeneratedListResponse, GeneratedListSummaryDTO } from "@/types";
import { Card, CardContent, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { 
  Pagination, 
  PaginationContent, 
  PaginationItem, 
  PaginationNext, 
  PaginationPrevious 
} from "@/components/ui/pagination";

export function PackingLists() {
  const navigate = useNavigate();
  const [lists, setLists] = useState<GeneratedListSummaryDTO[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  
  // Fetch lists when component loads or when page/search changes
  useEffect(() => {
    const fetchLists = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const params = new URLSearchParams({
          page: page.toString(),
          page_size: "10",
        });
        
        if (search) {
          params.append("search", search);
        }
        
        const response = await apiClient.get<PaginatedGeneratedListResponse>(
          `/api/generated-lists?${params.toString()}`
        );
        
        setLists(response.items);
        setTotalPages(response.totalPages);
      } catch (err) {
        console.error("Error fetching lists:", err);
        setError(err instanceof Error ? err.message : "Failed to load lists");
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchLists();
  }, [page, search]);
  
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
    setPage(1); // Reset to first page when search changes
  };
  
  const handlePageChange = (newPage: number) => {
    setPage(newPage);
  };
  
  const handleViewList = (list: GeneratedListSummaryDTO) => {
    navigate(`/trips/${list.tripId}/lists/${list.id}`);
  };
  
  if (isLoading && page === 1) {
    return <div>Ładowanie list pakowania...</div>;
  }
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Twoje listy pakowania</h1>
        <div className="w-1/3">
          <Input
            type="text"
            placeholder="Szukaj listy..."
            value={search}
            onChange={handleSearchChange}
          />
        </div>
      </div>
      
      {error && <div className="text-red-500">{error}</div>}
      
      {lists.length === 0 ? (
        <div className="text-center py-10">
          <p className="text-muted-foreground">Nie masz jeszcze żadnych list pakowania.</p>
          <Button 
            className="mt-4" 
            onClick={() => navigate('/dashboard/new-trip')}
          >
            Stwórz nową podróż
          </Button>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {lists.map((list) => (
            <Card key={list.id} className="cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => handleViewList(list)}>
              <CardContent className="p-4">
                <CardTitle className="text-lg mb-2">{list.name}</CardTitle>
                <div className="text-sm text-muted-foreground mb-3">
                  Utworzono: {new Date(list.createdAt).toLocaleDateString()}
                </div>
                <div className="flex justify-between items-center">
                  <div className="text-sm">
                    Spakowano: {list.packedItemsCount} z {list.itemsCount} przedmiotów
                  </div>
                  <div>
                    {Math.round((list.packedItemsCount / Math.max(list.itemsCount, 1)) * 100)}%
                  </div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
                  <div 
                    className="bg-primary h-2.5 rounded-full" 
                    style={{
                      width: `${Math.round((list.packedItemsCount / Math.max(list.itemsCount, 1)) * 100)}%`
                    }}
                  />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
      
      {totalPages > 1 && (
        <Pagination className="mt-8">
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious 
                onClick={() => page > 1 && handlePageChange(page - 1)}
                className={page === 1 ? "pointer-events-none opacity-50" : "cursor-pointer"}
              />
            </PaginationItem>
            
            {/* Generate page numbers */}
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((pageNum) => (
              <PaginationItem key={pageNum}>
                <Button
                  variant={pageNum === page ? "default" : "outline"}
                  size="sm"
                  onClick={() => handlePageChange(pageNum)}
                >
                  {pageNum}
                </Button>
              </PaginationItem>
            ))}
            
            <PaginationItem>
              <PaginationNext 
                onClick={() => page < totalPages && handlePageChange(page + 1)}
                className={page === totalPages ? "pointer-events-none opacity-50" : "cursor-pointer"}
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      )}
    </div>
  );
}

export default PackingLists;
```

### 7. Aktualizacja routingu

Dodać nową ścieżkę w komponencie `App.tsx`:

```tsx
<Route 
  path="/dashboard/packing-lists" 
  element={
    <ProtectedRoute>
      <PackingLists />
    </ProtectedRoute>
  } 
/>
```

### 8. Aktualizacja nawigacji

Zaktualizować komponent `DashboardLayout.tsx`, zmieniając:

```tsx
<div className="flex items-center gap-3 px-3 py-2 text-sm font-medium text-muted-foreground">
  Listy pakowania (wkrótce)
</div>
```

na:

```tsx
<NavLink
  to="/dashboard/packing-lists"
  className={({ isActive }) =>
    cn(
      "flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg hover:bg-muted",
      isActive && "bg-muted",
    )
  }
>
  Listy pakowania
</NavLink>
```

### 9. Dodanie karty w dashboardzie

Zaktualizować komponent `DashboardHome.tsx`, dodając wywołanie API dla liczby list:

```tsx
const [listCount, setListCount] = useState(0);

useEffect(() => {
  const fetchListCount = async () => {
    try {
      const response = await apiClient.get<PaginatedGeneratedListResponse>(
        `/api/generated-lists?page=1&page_size=1`
      );
      setListCount(response.total);
    } catch (error) {
      console.error("Error fetching list count:", error);
    }
  };
  
  fetchListCount();
}, []);
```

Następnie zaktualizować kartę "Aktywne listy":

```tsx
<ThemedCard variant="secondary">
  <CardHeader>
    <CardTitle>Aktywne listy</CardTitle>
    <CardDescription>Listy pakowania w przygotowaniu</CardDescription>
  </CardHeader>
  <CardContent>
    <div className="text-3xl font-bold text-brandLime">{listCount}</div>
    <Button
      variant="ghost"
      className="mt-4 text-xs w-full justify-start hover:bg-brandLime/10 border border-transparent hover:border-brandLime/20"
      onClick={() => navigate("/dashboard/packing-lists")}
    >
      Zobacz listy →
    </Button>
  </CardContent>
</ThemedCard>
```

## Harmonogram implementacji

1. **Dzień 1**: Weryfikacja i rozszerzenie endpointu `/api/generated-lists/{list_id}`
2. **Dzień 2**: Implementacja endpointu do listowania list pakowania i stworzenie niezbędnych DTO
3. **Dzień 3**: Usunięcie redundantnego endpointu i aktualizacja typu w TypeScript
4. **Dzień 4**: Implementacja komponentu PackingLists i integracja z dashboardem
5. **Dzień 5**: Testowanie, poprawki i dokumentacja

## Potencjalne ryzyka i ich mitygacja

1. **Ryzyko**: Niektóre funkcje endpointu `/api/trips/{trip_id}/lists/{list_id}` mogą być pominięte podczas konsolidacji.
   **Mitygacja**: Dokładne przeanalizowanie kodu obu endpointów i upewnienie się, że wszystkie funkcje zostały uwzględnione.

2. **Ryzyko**: Usunięcie endpointu może wpłynąć na inne części aplikacji.
   **Mitygacja**: Przeprowadzenie gruntownych testów przed i po usunięciu, z możliwością szybkiego przywrócenia endpointu w razie problemów.

3. **Ryzyko**: Niezgodność typów między frontendem a backendem.
   **Mitygacja**: Testy integracyjne sprawdzające poprawność komunikacji między frontendem a backendem. 