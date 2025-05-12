import { useFormContext } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { FormControl, FormField, FormItem, FormLabel } from "@/components/ui/form";
import { Card, CardContent } from "@/components/ui/card";
import type { CreateTripFormShape } from "./types";

type LuggageItem = {
  maxWeight?: number;
  width?: number;
  height?: number;
  depth?: number;
};

export const Step3Luggage = () => {
  const form = useFormContext<CreateTripFormShape>();

  const handleAddLuggage = () => {
    const currentLuggage = form.getValues("availableLuggage") || [];
    form.setValue("availableLuggage", [
      ...currentLuggage,
      { maxWeight: undefined, width: undefined, height: undefined, depth: undefined },
    ]);
  };

  const handleRemoveLuggage = (index: number) => {
    const currentLuggage = form.getValues("availableLuggage") || [];
    form.setValue(
      "availableLuggage",
      currentLuggage.filter((_: LuggageItem, i: number) => i !== index)
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium">Dostępny bagaż</h3>
        <Button type="button" variant="outline" size="sm" onClick={handleAddLuggage}>
          Dodaj bagaż
        </Button>
      </div>

      {(form.watch("availableLuggage") || []).map((luggage: LuggageItem, index: number) => (
        <Card key={index}>
          <CardContent className="space-y-4 pt-6">
            <FormField
              control={form.control}
              name={`availableLuggage.${index}.maxWeight`}
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Maksymalna waga (kg)</FormLabel>
                  <FormControl>
                    <Input
                      type="number"
                      min={0}
                      step={0.1}
                      placeholder="np. 20"
                      {...field}
                      onChange={(e) =>
                        field.onChange(e.target.value ? parseFloat(e.target.value) : undefined)
                      }
                      value={field.value || ""}
                    />
                  </FormControl>
                </FormItem>
              )}
            />

            <div className="grid grid-cols-3 gap-4">
              <FormField
                control={form.control}
                name={`availableLuggage.${index}.width`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Szerokość (cm)</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        min={0}
                        step={1}
                        placeholder="np. 55"
                        {...field}
                        onChange={(e) =>
                          field.onChange(e.target.value ? parseInt(e.target.value) : undefined)
                        }
                        value={field.value || ""}
                      />
                    </FormControl>
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name={`availableLuggage.${index}.height`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Wysokość (cm)</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        min={0}
                        step={1}
                        placeholder="np. 40"
                        {...field}
                        onChange={(e) =>
                          field.onChange(e.target.value ? parseInt(e.target.value) : undefined)
                        }
                        value={field.value || ""}
                      />
                    </FormControl>
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name={`availableLuggage.${index}.depth`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Głębokość (cm)</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        min={0}
                        step={1}
                        placeholder="np. 20"
                        {...field}
                        onChange={(e) =>
                          field.onChange(e.target.value ? parseInt(e.target.value) : undefined)
                        }
                        value={field.value || ""}
                      />
                    </FormControl>
                  </FormItem>
                )}
              />
            </div>

            <Button
              type="button"
              variant="destructive"
              size="sm"
              onClick={() => handleRemoveLuggage(index)}
            >
              Usuń
            </Button>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}; 