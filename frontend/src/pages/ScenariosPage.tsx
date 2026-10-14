import React from 'react';
import { FlaskConical, Info } from 'lucide-react';
import type { Scenario } from '@/types';

const SAMPLE_SCENARIOS: Scenario[] = [
  { id: 's1', name: 'Normal Operation', description: 'Baseline scenario with standard parameters.', scenario_type: 'normal', parameter_overrides: {}, is_held_out: false, provenance: 'simulated' },
  { id: 's2', name: 'Shelf Life −20%', description: 'All batch shelf lives reduced by 20% to simulate hotter conditions.', scenario_type: 'shelf_life_reduced', parameter_overrides: { shelf_life_multiplier: 0.8 }, is_held_out: false, provenance: 'simulated' },
  { id: 's3', name: 'Demand +30%', description: 'All destination demand increased by 30%.', scenario_type: 'demand_increased', parameter_overrides: { demand_multiplier: 1.3 }, is_held_out: false, provenance: 'simulated' },
  { id: 's4', name: 'Demand −30%', description: 'All destination demand reduced by 30%.', scenario_type: 'demand_decreased', parameter_overrides: { demand_multiplier: 0.7 }, is_held_out: false, provenance: 'simulated' },
  { id: 's5', name: 'Travel Time +25%', description: 'All route travel times increased by 25%.', scenario_type: 'travel_time_increased', parameter_overrides: { travel_time_multiplier: 1.25 }, is_held_out: false, provenance: 'simulated' },
  { id: 's6', name: 'One Vehicle Unavailable', description: 'Largest-capacity vehicle marked unavailable.', scenario_type: 'vehicle_unavailable', parameter_overrides: { unavailable_vehicle: 'VH-003' }, is_held_out: false, provenance: 'simulated' },
  { id: 's7', name: 'Emergency New Order', description: 'New urgent order arrives mid-plan, triggering re-planning.', scenario_type: 'new_order', parameter_overrides: { new_order_qty: 300, new_order_destination: 'd1' }, is_held_out: false, provenance: 'simulated' },
  { id: 's8', name: 'Held-Out Test Scenario', description: 'Reserved for organizer-provided evaluation scenario.', scenario_type: 'custom', parameter_overrides: {}, is_held_out: true, provenance: 'simulated' },
];

const TYPE_LABELS: Record<string, string> = {
  normal: 'Normal', shelf_life_reduced: 'Shelf Life Stress', demand_increased: 'Demand Surge', demand_decreased: 'Demand Drop', travel_time_increased: 'Logistics Stress', vehicle_unavailable: 'Fleet Disruption', new_order: 'Emergency Order', custom: 'Custom',
};

export function ScenariosPage() {
  return (
    <div className="animate-fade-in space-y-6">
      <div className="section-header">
        <div>
          <h1 className="text-2xl font-bold">Scenarios</h1>
          <p className="text-sm text-muted-foreground mt-1">8 configurable disruption and stress-test scenarios</p>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {SAMPLE_SCENARIOS.map(s => (
          <div key={s.id} className={`glass-card p-5 ${s.is_held_out ? 'border-yellow-500/30' : ''}`}>
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-2">
                <FlaskConical className="h-4 w-4 text-primary" />
                <p className="font-semibold text-sm">{s.name}</p>
              </div>
              {s.is_held_out && <span className="badge-risk-medium text-xs">Held-out</span>}
            </div>
            <p className="text-xs text-muted-foreground mb-3">{s.description}</p>
            <div className="flex items-center gap-2">
              <span className="rounded-full bg-accent px-2 py-0.5 text-xs text-muted-foreground">{TYPE_LABELS[s.scenario_type]}</span>
              <span className="rounded-full bg-accent px-2 py-0.5 text-xs text-muted-foreground italic">{s.provenance}</span>
            </div>
            {Object.keys(s.parameter_overrides).length > 0 && (
              <div className="mt-3 rounded-md bg-accent/50 p-2 font-mono text-xs text-muted-foreground">
                {JSON.stringify(s.parameter_overrides, null, 2)}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="alert-warning">
        <Info className="h-4 w-4 flex-shrink-0 mt-0.5" />
        <span>Fixed random seeds are used for all generated scenarios. Organizer-provided scenarios will be loaded separately and never fabricated.</span>
      </div>
    </div>
  );
}
