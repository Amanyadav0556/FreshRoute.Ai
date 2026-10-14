import React from 'react';
import { AlertTriangle, Clock, Truck, XCircle, CheckCircle } from 'lucide-react';
import { formatKg, formatHours, formatINR } from '@/lib/utils';

interface AlertBatch {
  id: string;
  batch_code: string;
  commodity: string;
  quantity_kg: number;
  remaining_shelf_life_hours: number;
  risk_level: 'high' | 'medium';
  alternatives: Alternative[];
}

interface Alternative {
  destination: string;
  vehicle_code: string;
  vehicle_type: string;
  travel_hours: number;
  handling_hours: number;
  total_hours: number;
  feasible: boolean;
  net_value_inr: number;
  infeasibility_reason?: string;
}

const SAMPLE_ALERTS: AlertBatch[] = [
  {
    id: 'b1', batch_code: 'TOM-2024-001', commodity: 'Tomatoes', quantity_kg: 500, remaining_shelf_life_hours: 18, risk_level: 'high',
    alternatives: [
      { destination: 'Pune Market', vehicle_code: 'VH-001', vehicle_type: 'normal', travel_hours: 1.0, handling_hours: 1.0, total_hours: 2.0, feasible: true, net_value_inr: 4800 },
      { destination: 'Mumbai APMC', vehicle_code: 'VH-002', vehicle_type: 'refrigerated', travel_hours: 4.5, handling_hours: 2.0, total_hours: 6.5, feasible: true, net_value_inr: 6200 },
      { destination: 'Nashik Mandi', vehicle_code: 'VH-003', vehicle_type: 'normal', travel_hours: 20.0, handling_hours: 1.5, total_hours: 21.5, feasible: false, net_value_inr: 0, infeasibility_reason: 'Travel time (20h) + handling (1.5h) = 21.5h exceeds remaining shelf life (18h)' },
    ],
  },
  {
    id: 'b4', batch_code: 'GRD-2024-004', commodity: 'Grapes', quantity_kg: 200, remaining_shelf_life_hours: 8, risk_level: 'high',
    alternatives: [
      { destination: 'Pune Market', vehicle_code: 'VH-001', vehicle_type: 'normal', travel_hours: 1.0, handling_hours: 1.0, total_hours: 2.0, feasible: true, net_value_inr: 3200 },
      { destination: 'Mumbai APMC', vehicle_code: 'VH-002', vehicle_type: 'refrigerated', travel_hours: 4.5, handling_hours: 2.0, total_hours: 6.5, feasible: false, net_value_inr: 0, infeasibility_reason: 'Demand at Mumbai APMC already fulfilled for this commodity' },
    ],
  },
];

export function AlertsPage() {
  return (
    <div className="animate-fade-in space-y-6">
      <div className="section-header">
        <div>
          <h1 className="text-2xl font-bold">Spoilage Alerts</h1>
          <p className="text-sm text-muted-foreground mt-1">High-risk batches and emergency redistribution options</p>
        </div>
        <span className="badge-risk-high">{SAMPLE_ALERTS.length} Critical Alerts</span>
      </div>

      {SAMPLE_ALERTS.map(batch => (
        <div key={batch.id} className="glass-card overflow-hidden border-red-500/20">
          <div className="flex items-center gap-3 border-b border-border bg-red-500/5 px-5 py-4">
            <AlertTriangle className="h-5 w-5 text-red-400" />
            <div className="flex-1">
              <p className="font-semibold">{batch.batch_code} — {batch.commodity}</p>
              <p className="text-xs text-muted-foreground">
                {formatKg(batch.quantity_kg)} · <span className="text-red-400 font-medium">{formatHours(batch.remaining_shelf_life_hours)} remaining</span>
              </p>
            </div>
            <span className="badge-risk-high">HIGH RISK</span>
          </div>

          <div className="p-5">
            <p className="text-sm font-medium mb-3 text-muted-foreground">Emergency Redistribution Options</p>
            <div className="space-y-3">
              {batch.alternatives.map((alt, i) => (
                <div key={i} className={`rounded-lg border p-4 ${alt.feasible ? 'border-primary/20 bg-primary/5' : 'border-red-500/20 bg-red-500/5 opacity-70'}`}>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-2">
                      {alt.feasible ? (
                        <CheckCircle className="h-4 w-4 text-primary" />
                      ) : (
                        <XCircle className="h-4 w-4 text-red-400" />
                      )}
                      <div>
                        <p className="font-medium text-sm">{alt.destination}</p>
                        <p className="text-xs text-muted-foreground">
                          <Truck className="inline h-3 w-3 mr-1" />
                          {alt.vehicle_code} ({alt.vehicle_type}) · {formatHours(alt.travel_hours)} travel + {formatHours(alt.handling_hours)} handling = {formatHours(alt.total_hours)} total
                        </p>
                      </div>
                    </div>
                    {alt.feasible ? (
                      <p className="font-bold text-primary tabular-nums">{formatINR(alt.net_value_inr)}</p>
                    ) : (
                      <span className="badge-risk-high text-xs">Infeasible</span>
                    )}
                  </div>
                  {!alt.feasible && alt.infeasibility_reason && (
                    <p className="mt-2 text-xs text-red-400 ml-6">↳ {alt.infeasibility_reason}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
