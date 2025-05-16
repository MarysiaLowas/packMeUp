import { Suspense, lazy } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useParams,
} from "react-router-dom";
import { AuthProvider } from "@/lib/providers/AuthProvider";
import { Layout } from "./components/layout/Layout";
import { ProtectedRoute } from "./components/auth/ProtectedRoute";
import { ThemeProvider } from "./components/ui/theme-provider";

// Lazy loading komponentów
const DashboardLayout = lazy(
  () => import("./components/dashboard/DashboardLayout"),
);
const DashboardHome = lazy(
  () => import("./components/dashboard/DashboardHome"),
);
const LoginForm = lazy(() => import("./components/auth/LoginForm"));
const RegisterForm = lazy(() => import("./components/auth/RegisterForm"));
const ResetPasswordForm = lazy(
  () => import("./components/auth/ResetPasswordForm"),
);
const NewTripPage = lazy(() => import("./components/new-trip/NewTripPage"));
const PackingList = lazy(() => import("./components/packing-list/PackingList"));
const ThemeGuide = lazy(() =>
  import("./components/ui/theme-guide").then((module) => ({
    default: module.ThemeGuide,
  })),
);

// Komponent ładowania
const LoadingSpinner = () => (
  <div className="flex items-center justify-center min-h-[400px]">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
  </div>
);

// Komponent dla strony 404
const NotFound = () => (
  <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
    <h1 className="text-4xl font-bold">404 - Strona nie znaleziona</h1>
    <p className="text-muted-foreground">
      Przepraszamy, ale strona której szukasz nie istnieje.
    </p>
  </div>
);

// Wrapper dla PackingList, który dostarcza parametry z URL
const PackingListWrapper = () => {
  const { listId = "" } = useParams();
  return <PackingList listId={listId} />;
};

export function App() {
  return (
    <BrowserRouter>
      <ThemeProvider defaultTheme="light">
        <AuthProvider>
          <Layout>
            <Suspense fallback={<LoadingSpinner />}>
              <Routes>
                <Route path="/login" element={<LoginForm />} />
                <Route path="/register" element={<RegisterForm />} />
                <Route path="/reset-password" element={<ResetPasswordForm />} />
                <Route path="/theme-guide" element={<ThemeGuide />} />
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute>
                      <DashboardLayout />
                    </ProtectedRoute>
                  }
                >
                  <Route index element={<DashboardHome />} />
                  <Route path="new-trip" element={<NewTripPage />} />
                </Route>
                <Route
                  path="/trips/:tripId/lists/:listId"
                  element={
                    <ProtectedRoute>
                      <PackingListWrapper />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/"
                  element={<Navigate to="/dashboard" replace />}
                />
                {/* Catch-all route for 404 */}
                <Route path="*" element={<NotFound />} />
              </Routes>
            </Suspense>
          </Layout>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
}
