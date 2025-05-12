import { useFormContext } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { FormControl, FormField, FormItem, FormLabel } from "@/components/ui/form";
import { Card, CardContent } from "@/components/ui/card";
import type { CreateTripFormShape } from "./types";

type LuggageItem = {
  maxWeight?: number;
  dimensions?: string;
};

export const Step3Luggage = () => {
  const form = useFormContext<CreateTripFormShape>();

  const handleAddLuggage = () => {
    const currentLuggage = form.getValues("availableLuggage") || [];
    form.setValue("availableLuggage", [
      ...currentLuggage,
      { maxWeight: undefined, dimensions: "" },
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

            <FormField
              control={form.control}
              name={`availableLuggage.${index}.dimensions`}
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Wymiary</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="np. 55x40x20"
                      {...field}
                      onChange={(e) => {
                        const value = e.target.value;
                        // Allow only numbers, 'x' and whitespace
                        if (!value || value.match(/^[\dx\s]*$/)) {
                          field.onChange(value);
                        }
                      }}
                    />
                  </FormControl>
                </FormItem>
              )}
            />

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