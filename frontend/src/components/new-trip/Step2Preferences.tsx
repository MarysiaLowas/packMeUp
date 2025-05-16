import { useFormContext } from "react-hook-form";
import { FormControl, FormField, FormItem } from "@/components/ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { FormLabel } from "@/components/ui/input";
import type { CreateTripFormShape } from "./types";

// TODO: retrieve the options from the backend
const ACCOMMODATION_OPTIONS = [
  { value: "hotel", label: "Hotel" },
  { value: "apartment", label: "Apartament" },
  { value: "hostel", label: "Hostel" },
  { value: "camping", label: "Camping" },
  { value: "other", label: "Inne" },
];

//TODO: retrieve the options from the backend
const TRANSPORT_OPTIONS = [
  { value: "plane", label: "Samolot" },
  { value: "car", label: "Samochód" },
  { value: "train", label: "Pociąg" },
  { value: "bus", label: "Autobus" },
  { value: "other", label: "Inne" },
];

//TODO: retrieve the options from the backend
const SEASON_OPTIONS = [
  { value: "summer", label: "Lato" },
  { value: "winter", label: "Zima" },
  { value: "spring", label: "Wiosna" },
  { value: "autumn", label: "Jesień" },
];

//TODO: retrieve the options from the backend
const CATERING_OPTIONS = [
  { id: 0, label: "All inclusive" },
  { id: 1, label: "Tylko śniadanie" },
  { id: 2, label: "Własne wyżywienie" },
];

export const Step2Preferences = () => {
  const form = useFormContext<CreateTripFormShape>();

  return (
    <div className="space-y-8">
      <div className="relative pb-3 after:absolute after:left-0 after:bottom-0 after:h-0.5 after:w-20 after:bg-gradient-to-r after:from-brandGreen after:to-brandLime after:rounded-full mb-6">
        <h2 className="text-2xl font-bold">Preferencje podróży</h2>
        <p className="text-muted-foreground mt-1">
          Wybierz opcje dotyczące Twojej planowanej podróży
        </p>
      </div>

      <FormField
        control={form.control}
        name="accommodation"
        render={({ field }) => (
          <FormItem className="space-y-3">
            <FormLabel variant="primary">Zakwaterowanie</FormLabel>
            <Select onValueChange={field.onChange} defaultValue={field.value}>
              <FormControl>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Wybierz typ zakwaterowania" />
                </SelectTrigger>
              </FormControl>
              <SelectContent>
                {ACCOMMODATION_OPTIONS.map((option) => (
                  <SelectItem key={option.value} value={option.value}>
                    {option.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="transport"
        render={({ field }) => (
          <FormItem className="space-y-3">
            <FormLabel variant="secondary">Transport</FormLabel>
            <Select onValueChange={field.onChange} defaultValue={field.value}>
              <FormControl>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Wybierz środek transportu" />
                </SelectTrigger>
              </FormControl>
              <SelectContent>
                {TRANSPORT_OPTIONS.map((option) => (
                  <SelectItem key={option.value} value={option.value}>
                    {option.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="season"
        render={({ field }) => (
          <FormItem className="space-y-3">
            <FormLabel variant="accent">Pora roku</FormLabel>
            <Select onValueChange={field.onChange} defaultValue={field.value}>
              <FormControl>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Wybierz porę roku" />
                </SelectTrigger>
              </FormControl>
              <SelectContent>
                {SEASON_OPTIONS.map((option) => (
                  <SelectItem key={option.value} value={option.value}>
                    {option.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="activities"
        render={({ field }) => (
          <FormItem className="space-y-3">
            <FormLabel variant="primary">Planowane aktywności</FormLabel>
            <div className="space-y-3 grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
              {[
                { id: "swimming", label: "Pływanie" },
                { id: "hiking", label: "Wędrówki" },
                { id: "skiing", label: "Narciarstwo" },
                { id: "sightseeing", label: "Zwiedzanie" },
                { id: "beach", label: "Plaża" },
              ].map((activity) => (
                <div
                  key={activity.id}
                  className="flex items-center space-x-3 p-2 rounded-md border border-gray-100 hover:border-brandGreen/30 hover:bg-brandGreen/5 transition-colors"
                >
                  <Checkbox
                    checked={(field.value || []).includes(activity.id)}
                    onCheckedChange={(checked: boolean) => {
                      const currentActivities = field.value || [];
                      if (checked) {
                        field.onChange([...currentActivities, activity.id]);
                      } else {
                        field.onChange(
                          currentActivities.filter((id) => id !== activity.id),
                        );
                      }
                    }}
                    className="border-grayPurple/20 data-[state=checked]:bg-brandGreen data-[state=checked]:border-brandGreen"
                  />
                  <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer">
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
          <FormItem className="space-y-3">
            <FormLabel variant="secondary">Opcje wyżywienia</FormLabel>
            <div className="space-y-3 pt-1">
              {CATERING_OPTIONS.map((option) => (
                <div
                  key={option.id}
                  className="flex items-center space-x-3 p-2 rounded-md border border-gray-100 hover:border-brandLime/30 hover:bg-brandLime/5 transition-colors"
                >
                  <Checkbox
                    checked={(field.value || []).includes(option.id)}
                    onCheckedChange={(checked) => {
                      const currentValue = field.value || [];
                      if (checked) {
                        field.onChange([...currentValue, option.id]);
                      } else {
                        field.onChange(
                          currentValue.filter((id) => id !== option.id),
                        );
                      }
                    }}
                    className="border-grayPurple/20 data-[state=checked]:bg-brandLime data-[state=checked]:border-brandLime"
                  />
                  <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer">
                    {option.label}
                  </label>
                </div>
              ))}
            </div>
          </FormItem>
        )}
      />
    </div>
  );
};
