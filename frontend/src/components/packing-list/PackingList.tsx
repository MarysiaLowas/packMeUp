import { useState, useEffect } from 'react';
import { Checkbox } from '@/components/ui/checkbox';
import type { GeneratePackingListResponseDTO, GeneratedListItemDTO } from '@/types';
import { apiClient } from '@/lib/api-client';

interface PackingListProps {
  listId: string;
}

export function PackingList({ listId }: PackingListProps) {
  const [list, setList] = useState<GeneratePackingListResponseDTO | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchList();
  }, [listId]);

  const fetchList = async () => {
    try {
      setIsLoading(true);
      setError(null);
      console.log('Fetching list with ID:', listId);
      const response = await apiClient.get<GeneratePackingListResponseDTO>(`/api/generated-lists/${listId}`);
      console.log('API Response:', response);
      setList(response);
    } catch (err) {
      console.error('Error fetching list:', err);
      setError(err instanceof Error ? err.message : 'Failed to load list');
    } finally {
      setIsLoading(false);
    }
  };

  const handleItemCheck = async (item: GeneratedListItemDTO, checked: boolean) => {
    try {
      // Optimistic update
      setList(prev => {
        if (!prev) return prev;
        return {
          ...prev,
          items: prev.items.map(i => 
            i.id === item.id ? { ...i, isPacked: checked } : i
          )
        };
      });

      await apiClient.patch(`/api/generated-lists/${listId}/items/${item.id}`, {
        isPacked: checked
      });
    } catch (err) {
      // Revert on error
      setList(prev => {
        if (!prev) return prev;
        return {
          ...prev,
          items: prev.items.map(i => 
            i.id === item.id ? { ...i, isPacked: !checked } : i
          )
        };
      });
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  if (!list) {
    return null;
  }

  const packedCount = list.items.filter(item => item.isPacked).length;
  const progress = Math.round((packedCount / list.items.length) * 100);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">{list.name}</h1>
        <p className="text-sm text-gray-500">
          Packed: {packedCount} of {list.items.length} ({progress}%)
        </p>
      </div>

      <div className="space-y-2">
        {list.items.map(item => (
          <div 
            key={item.id} 
            className="flex items-center gap-4 p-3 rounded-lg border"
          >
            <Checkbox
              checked={item.isPacked}
              onCheckedChange={(checked) => handleItemCheck(item, checked as boolean)}
            />
            <div>
              <p className={item.isPacked ? 'line-through text-gray-500' : ''}>
                {item.itemName} ({item.quantity})
              </p>
              {item.itemCategory && (
                <p className="text-sm text-gray-500">{item.itemCategory}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
} 