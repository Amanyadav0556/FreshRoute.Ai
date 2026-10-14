import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Package, Search, Filter, Clock, AlertTriangle } from 'lucide-react';
import { batchService } from '@/services/api';
import { formatKg, formatHours, formatDate } from '@/lib/utils';
import type { RiskLevel } from '@/types';

const RISK_BADGE: Record<RiskLevel, string> = {
  low: 'badge-risk-low',
  medium: 'badge-risk-medium',
  high: 'badge-risk-high',
  expired: 'badge-risk-high',
};

export function InventoryPage() {
  const [search, setSearch] = useState('');
  const [riskFilter, setRiskFilter] = useState('');

  const { data, isLoading, isError } = useQuery({
    queryKey: ['batches', riskFilter],
    queryFn: () => batchService.getAll({ risk: riskFilter || undefined, size: 100 }),
  });

  const batches = (data?.items ?? SAMPLE_BATCHES).filter(b =>
    !search ||
    b.batch_code.toLowerCase().includes(search.toLowerCase()) ||
    b.commodity?.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="animate-fade-in space-y-6">
      <div className="section-header">
        <div>
          <h1 className="text-2xl font-bold">Inventory</h1>
          <p className="text-sm text-muted-foreground mt-1">All produce batches with shelf-life monitoring</p>
        </div>
        <span className="text-sm text-muted-foreground">{batches.length} batches</span>
      </div>

      {/* Filters */}
      <div className="flex gap-3">
        <div className="relative flex-1 max-w-xs">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            className="w-full rounded-lg border border-border bg-card pl-9 pr-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary"
            placeholder="Search batches, commodities…"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
        <select
          className="rounded-lg border border-border bg-card px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
          value={riskFilter}
          onChange={e => setRiskFilter(e.target.value)}
        >
          <option value="">All Risk Levels</option>
          <option value="high">High Risk</option>
          <option value="medium">Medium Risk</option>
          <option value="low">Low Risk</option>
          <option value="expired">Expired</option>
        </select>
      </div>

      {/* Table */}
      <div className="glass-card overflow-hidden">
        <table className="data-table">
          <thead>
            <tr>
              <th>Batch Code</th>
              <th>Commodity</th>
              <th>Collection Centre</th>
              <th>Quantity</th>
              <th>Shelf Life</th>
              <th>Quality</th>
              <th>Risk</th>
              <th>Arrived</th>
              <th>Provenance</th>
            </tr>
          </thead>
          <tbody>
            {isLoading && (
              <tr><td colSpan={9} className="text-center py-8 text-muted-foreground">Loading batches…</td></tr>
            )}
            {batches.map(batch => (
              <tr key={batch.id}>
                <td className="font-mono text-xs font-medium text-primary">{batch.batch_code}</td>
                <td>{batch.commodity?.name ?? '—'}</td>
                <td className="text-muted-foreground text-xs">{batch.collection_centre?.name ?? '—'}</td>
                <td className="tabular-nums">{formatKg(batch.quantity_kg)}</td>
                <td className="tabular-nums">
                  <span className={batch.remaining_shelf_life_hours <= 12 ? 'text-red-400 font-medium' : ''}>
                    {formatHours(batch.remaining_shelf_life_hours)}
                  </span>
                </td>
                <td>
                  <span className="rounded-full bg-primary/10 px-2 py-0.5 text-xs font-medium text-primary">
                    {batch.quality_grade}
                  </span>
                </td>
                <td>
                  <span className={RISK_BADGE[batch.risk_level ?? 'low']}>
                    {batch.risk_level ?? 'low'}
                  </span>
                </td>
                <td className="text-xs text-muted-foreground">{formatDate(batch.arrival_time)}</td>
                <td>
                  <span className="text-xs text-muted-foreground italic">{batch.provenance}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// Sample data for development / backend-offline mode
const SAMPLE_BATCHES: import('@/types').Batch[] = [
  { id: '1', batch_code: 'TOM-2024-001', commodity_id: 'c1', commodity: { id: 'c1', name: 'Tomatoes', base_shelf_life_hours: 72, provenance: 'simulated' }, collection_centre_id: 'cc1', collection_centre: { id: 'cc1', name: 'Nasik CC', location_description: 'Nasik, MH', created_at: '' }, quantity_kg: 500, remaining_shelf_life_hours: 18, quality_grade: 'A', arrival_time: new Date().toISOString(), provenance: 'simulated', risk_level: 'high', created_at: '', updated_at: '' },
  { id: '2', batch_code: 'ONI-2024-002', commodity_id: 'c2', commodity: { id: 'c2', name: 'Onions', base_shelf_life_hours: 120, provenance: 'simulated' }, collection_centre_id: 'cc1', collection_centre: { id: 'cc1', name: 'Nasik CC', location_description: 'Nasik, MH', created_at: '' }, quantity_kg: 800, remaining_shelf_life_hours: 96, quality_grade: 'B', arrival_time: new Date().toISOString(), provenance: 'simulated', risk_level: 'low', created_at: '', updated_at: '' },
  { id: '3', batch_code: 'POT-2024-003', commodity_id: 'c3', commodity: { id: 'c3', name: 'Potatoes', base_shelf_life_hours: 168, provenance: 'simulated' }, collection_centre_id: 'cc2', collection_centre: { id: 'cc2', name: 'Pune CC', location_description: 'Pune, MH', created_at: '' }, quantity_kg: 1200, remaining_shelf_life_hours: 48, quality_grade: 'A', arrival_time: new Date().toISOString(), provenance: 'simulated', risk_level: 'medium', created_at: '', updated_at: '' },
];
