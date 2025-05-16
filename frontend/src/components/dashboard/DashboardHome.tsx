import { useState, useEffect } from "react";
import {
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  ThemedCard,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/hooks/useAuth";
import { useNavigate } from "react-router-dom";
import { apiClient } from "@/lib/api-client";
import type { PaginatedGeneratedLists } from "@/types";

const DashboardHome = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [listCount, setListCount] = useState(0);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchListCount = async () => {
      try {
        const response = await apiClient.get<PaginatedGeneratedLists>(
          "/api/generated-lists?page=1&page_size=1",
        );
        setListCount(response.total);
      } catch (error) {
        console.error("Error fetching list count:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchListCount();
  }, []);

  const handleStartTrip = () => {
    navigate("/dashboard/new-trip");
  };

  return (
    <div className="space-y-8">
      <div className="relative pb-3 after:absolute after:left-0 after:bottom-0 after:h-0.5 after:w-20 after:bg-gradient-to-r after:from-brandGreen after:to-brandLime after:rounded-full">
        <h1 className="text-3xl font-bold tracking-tight">Panel główny</h1>
        <p className="text-muted-foreground mt-2">
          Witaj z powrotem,{" "}
          <span className="text-brandGreen font-medium">
            {user?.first_name}
          </span>
          ! Oto przegląd Twoich podróży i list pakowania.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <ThemedCard variant="primary">
          <CardHeader>
            <CardTitle>Nadchodzące podróże</CardTitle>
            <CardDescription>
              Lista Twoich zaplanowanych podróży
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-brandGreen">0</div>
            <Button
              variant="ghost"
              className="mt-4 text-xs w-full justify-start hover:bg-brandGreen/10 border border-transparent hover:border-brandGreen/20"
              onClick={handleStartTrip}
            >
              Zaplanuj podróż →
            </Button>
          </CardContent>
        </ThemedCard>

        <ThemedCard variant="secondary">
          <CardHeader>
            <CardTitle>Aktywne listy</CardTitle>
            <CardDescription>Listy pakowania w przygotowaniu</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-brandLime">
              {isLoading ? (
                <div className="animate-pulse w-6 h-8 bg-brandLime/20 rounded" />
              ) : (
                listCount
              )}
            </div>
            <Button
              variant="ghost"
              className="mt-4 text-xs w-full justify-start hover:bg-brandLime/10 border border-transparent hover:border-brandLime/20"
              onClick={() => navigate("/dashboard/packing-lists")}
            >
              Zobacz listy →
            </Button>
          </CardContent>
        </ThemedCard>

        <ThemedCard variant="accent">
          <CardHeader>
            <CardTitle>Ukończone podróże</CardTitle>
            <CardDescription>Historia Twoich podróży</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-brandPink">0</div>
            <Button
              variant="ghost"
              className="mt-4 text-xs w-full justify-start hover:bg-brandPink/10 border border-transparent hover:border-brandPink/20"
            >
              Zobacz historię →
            </Button>
          </CardContent>
        </ThemedCard>
      </div>

      <ThemedCard variant="muted">
        <CardHeader>
          <CardTitle>Ostatnia aktywność</CardTitle>
          <CardDescription>Historia Twoich ostatnich działań</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="rounded-md bg-grayPurple/5 border border-grayPurple/10 p-4 flex items-center">
            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-brandGreen/20 to-brandLime/20 flex items-center justify-center mr-4">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="text-brandGreen"
              >
                <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"></path>
              </svg>
            </div>
            <div>
              <p className="text-sm">Brak ostatniej aktywności</p>
              <p className="text-xs text-muted-foreground mt-1">
                Tutaj będą wyświetlane Twoje ostatnie działania
              </p>
            </div>
          </div>
        </CardContent>
      </ThemedCard>

      <div className="h-px bg-gradient-to-r from-transparent via-brandGreen/30 to-transparent border-0 my-8"></div>

      <div className="text-center">
        <Button
          variant="gradient"
          size="lg"
          className="px-8"
          onClick={handleStartTrip}
        >
          Rozpocznij nową podróż
        </Button>
      </div>
    </div>
  );
};

export default DashboardHome;
