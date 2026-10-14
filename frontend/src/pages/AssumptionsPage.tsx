import React from 'react';
import { Info, AlertTriangle } from 'lucide-react';
import type { AssumptionItem } from '@/types';

const ASSUMPTIONS: AssumptionItem[] = [
  { category: 'Demand Response', parameter: 'Price elasticity', value: '20% demand uplift per 10% discount', source: 'simulated', note: 'No historical transaction data available. Sensitivity analysis recommended.' },
  { category: 'Demand Response', parameter: 'Walk-away price', value: 'Not configured', source: 'simulated', note: 'Minimum price floor not enforced. Discounts may go below viable threshold.' },
  { category: 'Shelf Life', parameter: 'Shelf life estimation method', value: 'Supplier-declared hours', source: 'estimated', note: 'Not adjusted for temperature unless realism mode is enabled.' },
  { category: 'Shelf Life', parameter: 'Temperature sensitivity', value: 'Disabled (realism mode off)', source: 'simulated', note: 'Enable realism mode to apply Q10 temperature correction.' },
  { category: 'Demand', parameter: 'Demand data source', value: 'Dataset-supplied demand_kg', source: 'simulated', note: 'Predicted demand is labelled as simulated — not a trained ML forecast.' },
  { category: 'Demand', parameter: 'Mandi price data', value: 'Not treated as confirmed demand', source: 'simulated', note: 'Mandi arrival prices are reference data only.' },
  { category: 'Costs', parameter: 'Spoilage cost', value: '100% of unsold value', source: 'simulated', note: 'Spoiled kg counted against starting inventory denominator.' },
  { category: 'Costs', parameter: 'Discount cost', value: 'Revenue difference from full price', source: 'simulated', note: 'No double-counting with spoilage cost.' },
  { category: 'Optimization', parameter: 'Solver', value: 'SciPy linprog (HiGHS backend)', source: 'real', note: 'Greedy fallback used if solver times out or returns infeasible.' },
  { category: 'Optimization', parameter: 'Solver timeout', value: '30 seconds', source: 'real', note: 'Configurable via SOLVER_TIMEOUT_SECONDS env variable.' },
  { category: 'Data', parameter: 'Inventory data', value: 'Simulated sample dataset', source: 'simulated', note: 'Not connected to real distributor stock systems.' },
  { category: 'Data', parameter: 'Vehicle tracking', value: 'Static availability windows', source: 'simulated', note: 'No real-time GPS or vehicle tracking integrated.' },
];

const CATEGORY_COLORS: Record<string, string> = {
  'Demand Response': 'text-orange-400',
  'Shelf Life': 'text-yellow-400',
  'Demand': 'text-blue-400',
  'Costs': 'text-purple-400',
  'Optimization': 'text-primary',
  'Data': 'text-muted-foreground',
};

export function AssumptionsPage() {
  const categories = [...new Set(ASSUMPTIONS.map(a => a.category))];

  return (
    <div className="animate-fade-in space-y-6">
      <div className="section-header">
        <div>
          <h1 className="text-2xl font-bold">Assumptions & Data Provenance</h1>
          <p className="text-sm text-muted-foreground mt-1">Complete transparency on simulated inputs and model assumptions</p>
        </div>
      </div>

      <div className="alert-warning">
        <AlertTriangle className="h-4 w-4 flex-shrink-0 mt-0.5" />
        <span>FreshRoute AI clearly distinguishes <strong>real</strong>, <strong>estimated</strong> and <strong>simulated</strong> data. No inputs are fabricated and presented as confirmed data.</span>
      </div>

      {categories.map(cat => (
        <div key={cat} className="glass-card overflow-hidden">
          <div className="flex items-center gap-2 border-b border-border px-4 py-3">
            <Info className={`h-4 w-4 ${CATEGORY_COLORS[cat]}`} />
            <h2 className="font-semibold text-sm">{cat}</h2>
          </div>
          <table className="data-table">
            <thead>
              <tr>
                <th>Parameter</th>
                <th>Value / Setting</th>
                <th>Source</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              {ASSUMPTIONS.filter(a => a.category === cat).map((a, i) => (
                <tr key={i}>
                  <td className="font-medium">{a.parameter}</td>
                  <td className="font-mono text-xs">{String(a.value)}</td>
                  <td>
                    <span className={`text-xs italic ${a.source === 'real' ? 'text-primary' : a.source === 'estimated' ? 'text-yellow-400' : 'text-muted-foreground'}`}>
                      {a.source}
                    </span>
                  </td>
                  <td className="text-xs text-muted-foreground">{a.note}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
}
