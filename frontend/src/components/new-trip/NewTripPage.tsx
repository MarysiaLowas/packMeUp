import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import type { CreateTripCommand, TripDTO, GeneratePackingListResponseDTO, LuggageDTO } from '@/types';
import type { CreateTripFormShape } from './types';
import { Form } from "@/components/ui/form";
import { StepIndicator } from './StepIndicator';
import { Step1BasicInfo } from './Step1BasicInfo';
import { Step2Preferences } from './Step2Preferences';
import { Step3Luggage } from './Step3Luggage';
import { FormNavigation } from './FormNavigation';
import { apiClient } from '@/lib/api-client';

// Form validation schema
const createTripFormSchema = z.object({
  destination: z.string().min(1, "Cel podróży jest wymagany"),
  startDate: z.string().optional(),
  durationDays: z.number().int().positive("Czas trwania musi być liczbą dodatnią"),
  numAdults: z.number().int().min(0, "Liczba dorosłych nie może być ujemna"),
  childrenAges: z.array(z.number().int().min(0)).optional(),
  accommodation: z.string().optional(),
  catering: z.array(z.number().int().min(0).max(2)).optional()
    .refine(
      (values) => !values?.length || values.every((val) => [0, 1, 2].includes(val)),
      "Nieprawidłowe opcje wyżywienia"
    ),
  transport: z.string().optional(),
  activities: z.array(z.string()).optional(),
  season: z.string().optional(),
  availableLuggage: z.array(
    z.object({
      maxWeight: z.number().positive().optional(),
      width: z.number().positive().optional(),
      height: z.number().positive().optional(),
      depth: z.number().positive().optional()
    }).refine(
      (data) => {
        // If any dimension is provided, all dimensions must be provided
        const hasSomeDimension = data.width || data.height || data.depth;
        const hasAllDimensions = data.width && data.height && data.depth;
        
        if (hasSomeDimension && !hasAllDimensions) {
          return false; // If any dimension is provided, all must be provided
        }

        // Must have either weight or all dimensions
        return !!data.maxWeight || hasAllDimensions;
      },
      {
        message: "Musisz podać albo wagę, albo wszystkie wymiary (szerokość, wysokość, głębokość), albo oba"
      }
    )
  ).optional()
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
    // Prevent form submission if not on the last step
    if (currentStep !== 3) {
      console.log('Form submission prevented - not on last step');
      return;
    }

    console.log('Form submitted with data:', data);
    try {
      setIsLoading(true);
      setApiError(null);

      // Transform form data to API command
      const luggageItems = data.availableLuggage
        ?.filter(item => 
          // Include items that have either weight or all dimensions
          item.maxWeight || (item.width && item.height && item.depth)
        )
        .map(item => {
          const luggageDTO: LuggageDTO = {};
          
          // Only include maxWeight if it's specified
          if (item.maxWeight) {
            luggageDTO.maxWeight = item.maxWeight;
          }

          // Only include dimensions if all dimensions are specified
          if (item.width && item.height && item.depth) {
            luggageDTO.dimensions = `${item.width}x${item.height}x${item.depth}`;
          }

          return luggageDTO;
        });

      const command: CreateTripCommand = {
        ...data,
        availableLuggage: luggageItems?.length ? luggageItems : undefined
      };

      console.log('Sending command to API:', command);

      // Create trip
      const trip = await apiClient.post<TripDTO>('/api/trips', command);
      console.log('Trip created:', trip);

      // Generate packing list
      const generatedList = await apiClient.post<GeneratePackingListResponseDTO>(
        `/api/trips/${trip.id}/generate-list`
      );
      console.log('List generated:', generatedList);

      // Redirect to the generated list
      window.location.href = `/trips/${trip.id}/lists/${generatedList.id}`;

    } catch (error) {
      console.error('Error in form submission:', error);
      setApiError(error instanceof Error ? error.message : 'Wystąpił błąd podczas zapisywania podróży');
    } finally {
      setIsLoading(false);
    }
  };

  const handleNext = async () => {
    try {
      const isValid = await form.trigger();
      if (isValid && currentStep < 3) {
        setCurrentStep(prev => prev + 1);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error in handleNext:', error);
      return false;
    }
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

      <Form {...form}>
        <form 
          onSubmit={(e) => {
            if (currentStep !== 3) {
              e.preventDefault();
              return;
            }
            form.handleSubmit(onSubmit)(e);
          }} 
          className="space-y-8 mt-8"
          noValidate
        >
          {currentStep === 1 && <Step1BasicInfo />}
          {currentStep === 2 && <Step2Preferences />}
          {currentStep === 3 && <Step3Luggage />}

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
      </Form>
    </div>
  );
}; 