import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import type { CreateTripCommand, TripDTO, GeneratePackingListResponseDTO } from '@/types';
import type { CreateTripFormShape } from './new-trip/types';
import { StepIndicator } from './new-trip/StepIndicator';
import { Step1BasicInfo } from './new-trip/Step1BasicInfo';
import { Step2Preferences } from './new-trip/Step2Preferences';
import { Step3Luggage } from './new-trip/Step3Luggage';
import { FormNavigation } from './new-trip/FormNavigation';

// Form validation schema
const createTripFormSchema = z.object({
  destination: z.string().min(1, "Cel podróży jest wymagany"),
  startDate: z.string().optional(),
  durationDays: z.number().int().positive("Czas trwania musi być liczbą dodatnią"),
  numAdults: z.number().int().min(0, "Liczba dorosłych nie może być ujemna"),
  childrenAges: z.array(z.number().int().min(0)).optional(),
  accommodation: z.string().optional(),
  catering: z.array(z.number()).optional(),
  transport: z.string().optional(),
  activities: z.array(z.string()).optional(),
  season: z.string().optional(),
  availableLuggage: z.array(z.object({
    maxWeight: z.number().positive().optional(),
    dimensions: z.string().optional()
  })).optional()
});

export const NewTripPage = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const form = useForm<CreateTripFormShape>({
    resolver: zodResolver(createTripFormSchema),
    defaultValues: {
      numAdults: 1,
      durationDays: 1,
      childrenAges: [],
      availableLuggage: []
    }
  });

  const onSubmit = async (data: CreateTripFormShape) => {
    try {
      setIsLoading(true);
      setApiError(null);

      // Transform form data to API command
      const firstLuggage = data.availableLuggage?.[0];
      const command: CreateTripCommand = {
        ...data,
        availableLuggage: firstLuggage ? {
          maxWeight: firstLuggage.maxWeight ?? 0,
          dimensions: firstLuggage.dimensions ?? ''
        } : undefined
      };

      // Create trip
      const response = await fetch('/api/trips', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(command),
      });

      if (!response.ok) {
        throw new Error('Wystąpił błąd podczas zapisywania podróży');
      }

      const trip: TripDTO = await response.json();

      // Generate packing list
      const listResponse = await fetch(`/api/trips/${trip.id}/generate-list`, {
        method: 'POST',
      });

      if (!listResponse.ok) {
        throw new Error('Wystąpił błąd podczas generowania listy');
      }

      const generatedList: GeneratePackingListResponseDTO = await listResponse.json();

      // Redirect to the generated list
      window.location.href = `/trips/${trip.id}/lists/${generatedList.generatedListId}`;

    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Wystąpił błąd podczas zapisywania podróży');
    } finally {
      setIsLoading(false);
    }
  };

  const handleNext = async () => {
    const isValid = await form.trigger();
    if (isValid && currentStep < 3) {
      setCurrentStep(prev => prev + 1);
      return true;
    }
    return false;
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(prev => prev - 1);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Zaplanuj nową podróż</h1>
      
      <StepIndicator currentStep={currentStep} totalSteps={3} />

      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8 mt-8">
        {currentStep === 1 && <Step1BasicInfo form={form} />}
        {currentStep === 2 && <Step2Preferences form={form} />}
        {currentStep === 3 && <Step3Luggage form={form} />}

        {apiError && (
          <div className="bg-destructive/15 text-destructive px-4 py-3 rounded-md">
            {apiError}
          </div>
        )}

        <FormNavigation
          currentStep={currentStep}
          totalSteps={3}
          onBack={handleBack}
          onNext={handleNext}
          isSubmitting={isLoading}
        />
      </form>
    </div>
  );
}; 