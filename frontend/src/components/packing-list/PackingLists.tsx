import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { apiClient } from "@/lib/api-client";
import type { PaginatedGeneratedLists, GeneratedListSummary } from "@/types";
import { Card, CardContent, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
  PaginationLink,
} from "@/components/ui/pagination";
import { useDebounce } from "@/components/hooks/useDebounce";

export function PackingLists() {
  const navigate = useNavigate();
  const [lists, setLists] = useState<GeneratedListSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [pageSize] = useState(10);

  const debouncedSearch = useDebounce(search, 300);

  // Fetch lists when component loads or when page/search changes
  useEffect(() => {
    const fetchLists = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const params = new URLSearchParams({
          page: page.toString(),
          page_size: pageSize.toString(),
        });

        if (debouncedSearch) {
          params.append("search", debouncedSearch);
        }

        const response = await apiClient.get<PaginatedGeneratedLists>(
          `/api/generated-lists?${params.toString()}`,
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
  }, [page, debouncedSearch, pageSize]);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
    setPage(1); // Reset to first page when search changes
  };

  const handlePageChange = (newPage: number) => {
    setPage(newPage);
  };

  const handleViewList = (list: GeneratedListSummary) => {
    navigate(`/trips/${list.tripId}/lists/${list.id}`);
  };

  const handleCreateList = () => {
    navigate("/dashboard/new-trip");
  };

  if (isLoading && page === 1) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Twoje listy pakowania</h1>
        <div className="flex gap-4 items-center">
          <Input
            type="text"
            placeholder="Szukaj listy..."
            value={search}
            onChange={handleSearchChange}
            className="w-64"
          />
          <Button onClick={handleCreateList}>Nowa lista</Button>
        </div>
      </div>

      {error && (
        <div className="bg-destructive/10 text-destructive p-4 rounded-lg">
          {error}
        </div>
      )}

      {!isLoading && lists.length === 0 && (
        <div className="text-center py-12">
          <h3 className="text-lg font-semibold mb-2">
            Nie masz jeszcze żadnych list pakowania
          </h3>
          <p className="text-muted-foreground mb-6">
            Stwórz swoją pierwszą listę pakowania, aby zacząć planować podróż.
          </p>
          <Button onClick={handleCreateList}>Stwórz pierwszą listę</Button>
        </div>
      )}

      {lists.length > 0 && (
        <>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {lists.map((list) => (
              <Card
                key={list.id}
                className="cursor-pointer hover:shadow-md transition-shadow"
                onClick={() => handleViewList(list)}
              >
                <CardContent className="p-4">
                  <CardTitle className="text-lg mb-2">{list.name}</CardTitle>
                  <div className="text-sm text-muted-foreground mb-3">
                    Utworzono: {new Date(list.createdAt).toLocaleDateString()}
                  </div>
                  <div className="flex justify-between items-center">
                    <div className="text-sm">
                      Spakowano: {list.packedItemsCount} z {list.itemsCount}{" "}
                      przedmiotów
                    </div>
                    <div>
                      {Math.round(
                        (list.packedItemsCount / Math.max(list.itemsCount, 1)) *
                          100,
                      )}
                      %
                    </div>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
                    <div
                      className="bg-primary h-2.5 rounded-full"
                      style={{
                        width: `${Math.round((list.packedItemsCount / Math.max(list.itemsCount, 1)) * 100)}%`,
                      }}
                    />
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {totalPages > 1 && (
            <Pagination>
              <PaginationContent>
                <PaginationItem>
                  <PaginationPrevious
                    onClick={() => handlePageChange(page - 1)}
                    disabled={page === 1}
                  />
                </PaginationItem>
                {Array.from({ length: totalPages }, (_, i) => i + 1).map(
                  (pageNum) => (
                    <PaginationItem key={pageNum}>
                      <PaginationLink
                        isActive={pageNum === page}
                        onClick={() => handlePageChange(pageNum)}
                      >
                        {pageNum}
                      </PaginationLink>
                    </PaginationItem>
                  ),
                )}
                <PaginationItem>
                  <PaginationNext
                    onClick={() => handlePageChange(page + 1)}
                    disabled={page === totalPages}
                  />
                </PaginationItem>
              </PaginationContent>
            </Pagination>
          )}
        </>
      )}
    </div>
  );
}

export default PackingLists;
