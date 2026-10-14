import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from '@/hooks/useAuth';
import { AppLayout } from '@/layouts/AppLayout';

// Pages
import { OverviewPage } from '@/pages/OverviewPage';
import { InventoryPage } from '@/pages/InventoryPage';
import { DestinationsPage } from '@/pages/DestinationsPage';
import { VehiclesPage } from '@/pages/VehiclesPage';
import { PlannerPage } from '@/pages/PlannerPage';
import { DiscountsPage } from '@/pages/DiscountsPage';
import { AlertsPage } from '@/pages/AlertsPage';
import { EvaluationPage } from '@/pages/EvaluationPage';
import { ScenariosPage } from '@/pages/ScenariosPage';
import { AssumptionsPage } from '@/pages/AssumptionsPage';
import { SettingsPage } from '@/pages/SettingsPage';
import { LoginPage } from '@/pages/LoginPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 30_000,
      refetchOnWindowFocus: false,
    },
  },
});

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route element={<AppLayout />}>
              <Route path="/" element={<OverviewPage />} />
              <Route path="/inventory" element={<InventoryPage />} />
              <Route path="/destinations" element={<DestinationsPage />} />
              <Route path="/vehicles" element={<VehiclesPage />} />
              <Route path="/planner" element={<PlannerPage />} />
              <Route path="/discounts" element={<DiscountsPage />} />
              <Route path="/alerts" element={<AlertsPage />} />
              <Route path="/evaluation" element={<EvaluationPage />} />
              <Route path="/scenarios" element={<ScenariosPage />} />
              <Route path="/assumptions" element={<AssumptionsPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}
