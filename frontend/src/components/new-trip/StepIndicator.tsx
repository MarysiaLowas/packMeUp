import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface StepIndicatorProps {
  currentStep: number;
}

export const StepIndicator = ({ currentStep }: StepIndicatorProps) => {
  const steps = [
    { value: "1", label: "Podstawowe informacje" },
    { value: "2", label: "Preferencje" },
    { value: "3", label: "Bagaż" },
  ];

  return (
    <Tabs value={currentStep.toString()} className="w-full">
      <TabsList className="grid w-full grid-cols-3">
        {steps.map((step) => (
          <TabsTrigger
            key={step.value}
            value={step.value}
            disabled
            className={`data-[state=active]:bg-primary data-[state=active]:text-primary-foreground ${
              parseInt(step.value) < currentStep ? "bg-muted" : ""
            }`}
          >
            {step.label}
          </TabsTrigger>
        ))}
      </TabsList>
    </Tabs>
  );
};
