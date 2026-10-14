import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { MapPin, ShoppingCart } from 'lucide-react';
import { destinationService, orderService } from '@/services/api';
import { formatKg, formatINR } from '@/lib/utils';

export function DestinationsPage() {
  const { data: destinations } = useQuery({ queryKey: ['destinations'], queryFn: destinationService.getAll });
  const { data: orders } = useQuery({ queryKey: ['orders'], queryFn: orderService.getAll });

  const dests = destinations ?? SAMPLE_DESTINATIONS;
  const ords = orders ?? SAMPLE_ORDERS;

  return (
    <div className="animate-fade-in space-y-6">
      <div className="section-header">
        <div>
          <h1 className="text-2xl font-bold">Destinations & Orders</h1>
          <p className="text-sm text-muted-foreground mt-1">Mandis, markets and confirmed/predicted demand</p>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Destinations */}
        <div className="glass-card overflow-hidden">
          <div className="flex items-center gap-2 border-b border-border px-4 py-3">
            <MapPin className="h-4 w-4 text-primary" />
            <h2 className="font-semibold text-sm">Destinations / Mandis</h2>
            <span className="ml-auto text-xs text-muted-foreground">{dests.length} total</span>
          </div>
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Demand</th>
                <th>Confirmed</th>
                <th>Price / kg</th>
                <th>Handling</th>
              </tr>
            </thead>
            <tbody>
              {dests.map(d => (
                <tr key={d.id}>
                  <td className="font-medium">{d.name}</td>
                  <td className="tabular-nums">{formatKg(d.demand_kg)}</td>
                  <td className="tabular-nums text-primary">{formatKg(d.confirmed_order_kg)}</td>
                  <td className="tabular-nums">{formatINR(d.base_price_inr_per_kg, 2)}</td>
                  <td className="text-xs text-muted-foreground">{d.handling_time_hours}h</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Orders */}
        <div className="glass-card overflow-hidden">
          <div className="flex items-center gap-2 border-b border-border px-4 py-3">
            <ShoppingCart className="h-4 w-4 text-primary" />
            <h2 className="font-semibold text-sm">Orders</h2>
            <span className="ml-auto text-xs text-muted-foreground">{ords.length} total</span>
          </div>
          <table className="data-table">
            <thead>
              <tr>
                <th>Destination</th>
                <th>Commodity</th>
                <th>Quantity</th>
                <th>Confirmed</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {ords.map(o => (
                <tr key={o.id}>
                  <td>{o.destination?.name ?? '—'}</td>
                  <td>{o.commodity?.name ?? '—'}</td>
                  <td className="tabular-nums">{formatKg(o.quantity_kg)}</td>
                  <td>
                    <span className={o.confirmed ? 'badge-risk-low' : 'text-xs text-muted-foreground'}>
                      {o.confirmed ? 'Yes' : 'Predicted'}
                    </span>
                  </td>
                  <td className="capitalize text-xs">{o.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

const SAMPLE_DESTINATIONS: import('@/types').Destination[] = [
  { id: 'd1', name: 'Mumbai APMC', location_description: 'Mumbai, MH', demand_kg: 1200, confirmed_order_kg: 800, predicted_demand_kg: 1200, base_price_inr_per_kg: 28, handling_time_hours: 2, handling_cost_inr_per_kg: 1.5, provenance: 'simulated' },
  { id: 'd2', name: 'Pune Market', location_description: 'Pune, MH', demand_kg: 600, confirmed_order_kg: 400, predicted_demand_kg: 600, base_price_inr_per_kg: 25, handling_time_hours: 1, handling_cost_inr_per_kg: 1.2, provenance: 'simulated' },
  { id: 'd3', name: 'Nashik Mandi', location_description: 'Nashik, MH', demand_kg: 900, confirmed_order_kg: 500, predicted_demand_kg: 900, base_price_inr_per_kg: 22, handling_time_hours: 1.5, handling_cost_inr_per_kg: 1.0, provenance: 'simulated' },
];

const SAMPLE_ORDERS: import('@/types').Order[] = [
  { id: 'o1', destination_id: 'd1', destination: SAMPLE_DESTINATIONS[0], commodity_id: 'c1', commodity: { id: 'c1', name: 'Tomatoes', base_shelf_life_hours: 72, provenance: 'simulated' }, quantity_kg: 400, confirmed: true, status: 'confirmed', created_at: new Date().toISOString() },
  { id: 'o2', destination_id: 'd2', destination: SAMPLE_DESTINATIONS[1], commodity_id: 'c2', commodity: { id: 'c2', name: 'Onions', base_shelf_life_hours: 120, provenance: 'simulated' }, quantity_kg: 300, confirmed: false, status: 'pending', created_at: new Date().toISOString() },
];
