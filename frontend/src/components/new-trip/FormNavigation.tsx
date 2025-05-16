import { Button } from "@/components/ui/button";
import type { UseFormReturn } from "react-hook-form";

interface FormNavigationProps {
  currentStep: number;
  totalSteps: number;
  onBack: () => void;
  onNext: () => Promise<boolean>;
  isSubmitting: boolean;
}

export const FormNavigation = ({
  currentStep,
  totalSteps,
  onBack,
  onNext,
  isSubmitting,
}: FormNavigationProps) => {
  const handleNextClick = async (e: React.MouseEvent) => {
    e.preventDefault();
    await onNext();
  };

  return (
    <div className="flex justify-between pt-6">
      {currentStep > 1 ? (
        <Button type="button" variant="outline" onClick={onBack}>
          Wstecz
        </Button>
      ) : (
        <div></div> // Placeholder for flex spacing
      )}

      {currentStep === totalSteps ? (
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? (
            <span className="flex items-center gap-2">
              <svg
                className="animate-spin h-4 w-4"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Przetwarzanie...
            </span>
          ) : (
            "Generuj listę"
          )}
        </Button>
      ) : (
        <Button type="button" onClick={handleNextClick} disabled={isSubmitting}>
          Dalej
        </Button>
      )}
    </div>
  );
};
