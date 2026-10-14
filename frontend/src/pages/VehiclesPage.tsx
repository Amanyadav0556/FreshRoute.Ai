import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Truck, Route } from 'lucide-react';
import { vehicleService, routeService } from '@/services/api';
import { formatKg, formatINR, formatHours } from '@/lib/utils';

const STATUS_BADGE: Record<string, string> = {
  available: 'badge-risk-low',
  in_transit: 'badge-risk-medium',
  maintenance: 'badge-risk-high',
  unavailable: 'badge-risk-high',
};

export function VehiclesPage() {
  const { data: vehicles } = useQuery({ queryKey: ['vehicles'], queryFn: vehicleService.getAll });
  const { data: routes } = useQuery({ queryKey: ['routes'], queryFn: routeService.getAll });

  const vehs = vehicles ?? SAMPLE_VEHICLES;
  const rts = routes ?? SAMPLE_ROUTES;

  return (
    <div className="animate-fade-in space-y-6">
      <div className="section-header">
        <div>
          <h1 className="text-2xl font-bold">Vehicles & Routes</h1>
          <p className="text-sm text-muted-foreground mt-1">Fleet status, capacities and route costs</p>
        </div>
      </div>

      <div className="glass-card overflow-hidden">
        <div className="flex items-center gap-2 border-b border-border px-4 py-3">
          <Truck className="h-4 w-4 text-primary" />
          <h2 className="font-semibold text-sm">Vehicles</h2>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Code</th>
              <th>Type</th>
              <th>Capacity</th>
              <th>Cost / Trip</th>
              <th>Temperature</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {vehs.map(v => (
              <tr key={v.id}>
                <td className="font-mono text-xs font-medium">{v.vehicle_code}</td>
                <td className="capitalize">{v.vehicle_type}</td>
                <td className="tabular-nums">{formatKg(v.capacity_kg)}</td>
                <td className="tabular-nums">{formatINR(v.cost_per_trip_inr)}</td>
                <td className="text-xs text-muted-foreground">
                  {v.cabin_temperature_c != null ? `${v.cabin_temperature_c}°C` : 'Ambient'}
                </td>
                <td><span className={STATUS_BADGE[v.status]}>{v.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="glass-card overflow-hidden">
        <div className="flex items-center gap-2 border-b border-border px-4 py-3">
          <Route className="h-4 w-4 text-primary" />
          <h2 className="font-semibold text-sm">Routes</h2>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Origin</th>
              <th>Destination</th>
              <th>Travel Time</th>
              <th>Transport Cost</th>
            </tr>
          </thead>
          <tbody>
            {rts.map(r => (
              <tr key={r.id}>
                <td>{r.origin?.name ?? r.origin_id}</td>
                <td>{r.destination?.name ?? r.destination_id}</td>
                <td className="tabular-nums">{formatHours(r.travel_time_hours)}</td>
                <td className="tabular-nums">{formatINR(r.transport_cost_inr)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const SAMPLE_VEHICLES: import('@/types').Vehicle[] = [
  { id: 'v1', vehicle_code: 'VH-001', vehicle_type: 'normal', capacity_kg: 1000, cost_per_trip_inr: 3500, status: 'available' },
  { id: 'v2', vehicle_code: 'VH-002', vehicle_type: 'refrigerated', capacity_kg: 800, cost_per_trip_inr: 5500, cabin_temperature_c: 4, status: 'available' },
  { id: 'v3', vehicle_code: 'VH-003', vehicle_type: 'normal', capacity_kg: 1500, cost_per_trip_inr: 4000, status: 'in_transit' },
];

const SAMPLE_ROUTES: import('@/types').Route[] = [
  { id: 'r1', origin_id: 'cc1', origin: { id: 'cc1', name: 'Nasik CC', location_description: 'Nasik', created_at: '' }, destination_id: 'd1', destination: { id: 'd1', name: 'Mumbai APMC', location_description: 'Mumbai', demand_kg: 1200, confirmed_order_kg: 800, predicted_demand_kg: 1200, base_price_inr_per_kg: 28, handling_time_hours: 2, handling_cost_inr_per_kg: 1.5, provenance: 'simulated' }, travel_time_hours: 4.5, transport_cost_inr: 3500 },
  { id: 'r2', origin_id: 'cc2', origin: { id: 'cc2', name: 'Pune CC', location_description: 'Pune', created_at: '' }, destination_id: 'd2', destination: { id: 'd2', name: 'Pune Market', location_description: 'Pune', demand_kg: 600, confirmed_order_kg: 400, predicted_demand_kg: 600, base_price_inr_per_kg: 25, handling_time_hours: 1, handling_cost_inr_per_kg: 1.2, provenance: 'simulated' }, travel_time_hours: 1.0, transport_cost_inr: 1500 },
];
