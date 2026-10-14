import { api } from '@/lib/api-client';
import type {
  DashboardSummary,
  Batch,
  Destination,
  Vehicle,
  Route,
  Order,
  Plan,
  Evaluation,
  Scenario,
  DiscountRecommendation,
  AssumptionItem,
  PaginatedResponse,
  PlanStrategy,
} from '@/types';

// ─── Dashboard ────────────────────────────────────────────────────────────────

export const dashboardService = {
  getSummary: () => api.get<DashboardSummary>('/api/dashboard/summary'),
};

// ─── Batches ─────────────────────────────────────────────────────────────────

export const batchService = {
  getAll: (params?: { page?: number; size?: number; risk?: string; commodity?: string }) => {
    const qs = new URLSearchParams();
    if (params?.page) qs.set('page', String(params.page));
    if (params?.size) qs.set('size', String(params.size));
    if (params?.risk) qs.set('risk', params.risk);
    if (params?.commodity) qs.set('commodity', params.commodity);
    return api.get<PaginatedResponse<Batch>>(`/api/batches?${qs}`);
  },
  getById: (id: string) => api.get<Batch>(`/api/batches/${id}`),
  create: (data: Partial<Batch>) => api.post<Batch>('/api/batches', data),
  update: (id: string, data: Partial<Batch>) => api.patch<Batch>(`/api/batches/${id}`, data),
};

// ─── Destinations ─────────────────────────────────────────────────────────────

export const destinationService = {
  getAll: () => api.get<Destination[]>('/api/destinations'),
  getById: (id: string) => api.get<Destination>(`/api/destinations/${id}`),
};

// ─── Vehicles ─────────────────────────────────────────────────────────────────

export const vehicleService = {
  getAll: () => api.get<Vehicle[]>('/api/vehicles'),
  getById: (id: string) => api.get<Vehicle>(`/api/vehicles/${id}`),
};

// ─── Routes ──────────────────────────────────────────────────────────────────

export const routeService = {
  getAll: () => api.get<Route[]>('/api/routes'),
};

// ─── Orders ──────────────────────────────────────────────────────────────────

export const orderService = {
  getAll: () => api.get<Order[]>('/api/orders'),
};

// ─── Plans ───────────────────────────────────────────────────────────────────

export const planService = {
  create: (data: { strategy: PlanStrategy; scenario_id?: string }) =>
    api.post<Plan>('/api/plans', data),
  getById: (id: string) => api.get<Plan>(`/api/plans/${id}`),
  validate: (id: string) => api.post<Plan>(`/api/plans/${id}/validate`, {}),
  replan: (data: { scenario_id?: string; disruption?: Record<string, unknown> }) =>
    api.post<Plan>('/api/replans', data),
};

// ─── Evaluations ─────────────────────────────────────────────────────────────

export const evaluationService = {
  run: (scenario_id?: string) => api.post<Evaluation[]>('/api/evaluations/run', { scenario_id }),
  getAll: () => api.get<Evaluation[]>('/api/evaluations'),
};

// ─── Scenarios ───────────────────────────────────────────────────────────────

export const scenarioService = {
  getAll: () => api.get<Scenario[]>('/api/scenarios'),
};

// ─── Discounts ───────────────────────────────────────────────────────────────

export const discountService = {
  getRecommendations: () => api.get<DiscountRecommendation[]>('/api/discounts'),
};

// ─── Assumptions ─────────────────────────────────────────────────────────────

export const assumptionService = {
  getAll: () => api.get<AssumptionItem[]>('/api/assumptions'),
};
