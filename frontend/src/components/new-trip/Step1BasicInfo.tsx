import { useFormContext } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Card, CardContent } from "@/components/ui/card";
import type { CreateTripFormShape } from "./types";

export const Step1BasicInfo = () => {
  const form = useFormContext<CreateTripFormShape>();

  const handleAddChild = () => {
    const currentChildren = form.getValues("childrenAges") || [];
    form.setValue("childrenAges", [...currentChildren, 0]);
  };

  const handleRemoveChild = (index: number) => {
    const currentChildren = form.getValues("childrenAges") || [];
    form.setValue(
      "childrenAges",
      currentChildren.filter((_: number, i: number) => i !== index)
    );
  };

  return (
    <div className="space-y-6">
      <FormField
        control={form.control}
        name="destination"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Cel podróży</FormLabel>
            <FormControl>
              <Input placeholder="np. Paryż, Francja" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="startDate"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Data rozpoczęcia</FormLabel>
            <FormControl>
              <Input type="date" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="durationDays"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Czas trwania (dni)</FormLabel>
            <FormControl>
              <Input
                type="number"
                min={1}
                {...field}
                onChange={(e) => field.onChange(parseInt(e.target.value))}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="numAdults"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Liczba dorosłych</FormLabel>
            <FormControl>
              <Input
                type="number"
                min={1}
                {...field}
                onChange={(e) => field.onChange(parseInt(e.target.value))}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <Label>Dzieci (wiek)</Label>
          <Button type="button" variant="outline" size="sm" onClick={handleAddChild}>
            Dodaj dziecko
          </Button>
        </div>

        {(form.watch("childrenAges") || []).map((age: number, index: number) => (
          <Card key={index}>
            <CardContent className="flex items-center gap-4 pt-6">
              <FormField
                control={form.control}
                name={`childrenAges.${index}`}
                render={({ field }) => (
                  <FormItem className="flex-1">
                    <FormControl>
                      <Input
                        type="number"
                        min={0}
                        placeholder="Wiek dziecka"
                        {...field}
                        onChange={(e) => field.onChange(parseInt(e.target.value))}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button
                type="button"
                variant="destructive"
                size="sm"
                onClick={() => handleRemoveChild(index)}
              >
                Usuń
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}; 