import { useFormContext } from "react-hook-form";
import { FormControl, FormField, FormItem, FormLabel } from "@/components/ui/form";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import type { CreateTripFormShape } from "./types";

// TODO: retrieve the options from the backend
const ACCOMMODATION_OPTIONS = [
  { value: "HOTEL", label: "Hotel" },
  { value: "APARTMENT", label: "Apartament" },
  { value: "HOSTEL", label: "Hostel" },
  { value: "CAMPING", label: "Camping" },
  { value: "OTHER", label: "Inne" },
];

//TODO: retrieve the options from the backend
const TRANSPORT_OPTIONS = [
  { value: "PLANE", label: "Samolot" },
  { value: "CAR", label: "Samochód" },
  { value: "TRAIN", label: "Pociąg" },
  { value: "BUS", label: "Autobus" },
  { value: "OTHER", label: "Inne" },
];

//TODO: retrieve the options from the backend
const SEASON_OPTIONS = [
  { value: "SUMMER", label: "Lato" },
  { value: "WINTER", label: "Zima" },
  { value: "SPRING", label: "Wiosna" },
  { value: "AUTUMN", label: "Jesień" },
];

//TODO: retrieve the options from the backend
const CATERING_OPTIONS = [
  { id: "0", label: "All-inclusive" },
  { id: "1", label: "Własne wyżywienie" },
  { id: "2", label: "Częściowe" },
];

export const Step2Preferences = () => {
  const form = useFormContext<CreateTripFormShape>();

  return (
    <div className="space-y-6">
      <FormField
        control={form.control}
        name="accommodation"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Zakwaterowanie</FormLabel>
            <Select onValueChange={field.onChange} defaultValue={field.value}>
              <FormControl>
                <SelectTrigger>
                  <SelectValue placeholder="Wybierz typ zakwaterowania" />
                </SelectTrigger>
              </FormControl>
              <SelectContent>
                <SelectItem value="hotel">Hotel</SelectItem>
                <SelectItem value="apartment">Apartament</SelectItem>
                <SelectItem value="camping">Camping</SelectItem>
                <SelectItem value="hostel">Hostel</SelectItem>
              </SelectContent>
            </Select>
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="transport"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Transport</FormLabel>
            <Select onValueChange={field.onChange} defaultValue={field.value}>
              <FormControl>
                <SelectTrigger>
                  <SelectValue placeholder="Wybierz środek transportu" />
                </SelectTrigger>
              </FormControl>
              <SelectContent>
                <SelectItem value="plane">Samolot</SelectItem>
                <SelectItem value="car">Samochód</SelectItem>
                <SelectItem value="train">Pociąg</SelectItem>
                <SelectItem value="bus">Autobus</SelectItem>
              </SelectContent>
            </Select>
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="season"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Pora roku</FormLabel>
            <Select onValueChange={field.onChange} defaultValue={field.value}>
              <FormControl>
                <SelectTrigger>
                  <SelectValue placeholder="Wybierz porę roku" />
                </SelectTrigger>
              </FormControl>
              <SelectContent>
                <SelectItem value="spring">Wiosna</SelectItem>
                <SelectItem value="summer">Lato</SelectItem>
                <SelectItem value="autumn">Jesień</SelectItem>
                <SelectItem value="winter">Zima</SelectItem>
              </SelectContent>
            </Select>
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="activities"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Planowane aktywności</FormLabel>
            <div className="space-y-2">
              {[
                { id: "swimming", label: "Pływanie" },
                { id: "hiking", label: "Wędrówki" },
                { id: "skiing", label: "Narciarstwo" },
                { id: "sightseeing", label: "Zwiedzanie" },
                { id: "beach", label: "Plaża" },
              ].map((activity) => (
                <div key={activity.id} className="flex items-center space-x-2">
                  <Checkbox
                    checked={(field.value || []).includes(activity.id)}
                    onCheckedChange={(checked: boolean) => {
                      const currentActivities = field.value || [];
                      if (checked) {
                        field.onChange([...currentActivities, activity.id]);
                      } else {
                        field.onChange(
                          currentActivities.filter((id) => id !== activity.id)
                        );
                      }
                    }}
                  />
                  <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                    {activity.label}
                  </label>
                </div>
              ))}
            </div>
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="catering"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Posiłki (liczba dziennie)</FormLabel>
            <FormControl>
              <Input
                type="number"
                min={0}
                max={5}
                {...field}
                onChange={(e) => {
                  const value = parseInt(e.target.value);
                  field.onChange(value ? [value] : []);
                }}
                value={field.value?.[0] || ""}
              />
            </FormControl>
          </FormItem>
        )}
      />
    </div>
  );
}; 