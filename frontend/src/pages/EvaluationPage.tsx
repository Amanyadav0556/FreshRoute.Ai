import React, { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { BarChart3, Play, Download } from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
} from 'recharts';
import { evaluationService } from '@/services/api';
import { formatINR, formatKg, formatPercent } from '@/lib/utils';
import type { Evaluation } from '@/types';

const STRATEGY_LABELS: Record<string, string> = {
  freshroute: 'FreshRoute',
  fefo: 'FEFO',
  highest_price: 'Highest Price',
  greedy: 'Greedy',
};

const STRATEGY_COLORS: Record<string, string> = {
  freshroute: '#22c55e',
  fefo: '#3b82f6',
  highest_price: '#f59e0b',
  greedy: '#a855f7',
};

const SAMPLE_EVALS: Evaluation[] = [
  { id: 'e1', plan_id: 'p1', strategy: 'freshroute', spoilage_percent: 3.2, demand_fulfilment_percent: 91.5, unmet_demand_kg: 103, net_value_inr: 195200, transport_cost_inr: 22500, discount_cost_inr: 4800, violation_count: 0, runtime_seconds: 1.24, created_at: new Date().toISOString() },
  { id: 'e2', plan_id: 'p2', strategy: 'fefo', spoilage_percent: 5.8, demand_fulfilment_percent: 84.2, unmet_demand_kg: 196, net_value_inr: 164300, transport_cost_inr: 21000, discount_cost_inr: 2100, violation_count: 0, runtime_seconds: 0.08, created_at: new Date().toISOString() },
  { id: 'e3', plan_id: 'p3', strategy: 'highest_price', spoilage_percent: 7.1, demand_fulfilment_percent: 79.3, unmet_demand_kg: 257, net_value_inr: 172800, transport_cost_inr: 20000, discount_cost_inr: 1500, violation_count: 0, runtime_seconds: 0.05, created_at: new Date().toISOString() },
  { id: 'e4', plan_id: 'p4', strategy: 'greedy', spoilage_percent: 6.3, demand_fulfilment_percent: 82.7, unmet_demand_kg: 215, net_value_inr: 158600, transport_cost_inr: 19500, discount_cost_inr: 3200, violation_count: 0, runtime_seconds: 0.12, created_at: new Date().toISOString() },
];

export function EvaluationPage() {
  const [scenarioId, setScenarioId] = useState('');
  const { data, refetch } = useQuery({ queryKey: ['evaluations'], queryFn: evaluationService.getAll });

  const runMutation = useMutation({
    mutationFn: () => evaluationService.run(scenarioId || undefined),
    onSuccess: () => refetch(),
  });

  const evals = data ?? SAMPLE_EVALS;

  const barData = evals.map(e => ({
    name: STRATEGY_LABELS[e.strategy] ?? e.strategy,
    'Net Value (₹)': e.net_value_inr,
    strategy: e.strategy,
  }));

  const radarData = [
    { metric: 'Demand Fill', ...Object.fromEntries(evals.map(e => [STRATEGY_LABELS[e.strategy], e.demand_fulfilment_percent])) },
    { metric: 'Low Spoilage', ...Object.fromEntries(evals.map(e => [STRATEGY_LABELS[e.strategy], 100 - e.spoilage_percent])) },
    { metric: 'Net Value', ...Object.fromEntries(evals.map(e => [STRATEGY_LABELS[e.strategy], (e.net_value_inr / 200000) * 100])) },
    { metric: 'Speed', ...Object.fromEntries(evals.map(e => [STRATEGY_LABELS[e.strategy], Math.max(0, 100 - e.runtime_seconds * 10)])) },
    { metric: 'No Violations', ...Object.fromEntries(evals.map(e => [STRATEGY_LABELS[e.strategy], e.violation_count === 0 ? 100 : 0])) },
  ];

  return (
    <div className="animate-fade-in space-y-6">
      <div className="section-header">
        <div>
          <h1 className="text-2xl font-bold">Evaluation & Scoreboard</h1>
          <p className="text-sm text-muted-foreground mt-1">Compare strategies using the same dataset and cost model</p>
        </div>
        <button
          onClick={() => runMutation.mutate()}
          disabled={runMutation.isPending}
          className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:bg-primary/90 disabled:opacity-60"
        >
          <Play className="h-4 w-4" />
          {runMutation.isPending ? 'Running…' : 'Run All Strategies'}
        </button>
      </div>

      {/* Charts */}
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="glass-card p-5">
          <h2 className="text-sm font-semibold mb-4">Net Economic Value (INR)</h2>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={barData} margin={{ top: 0, right: 10, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(220,13%,18%)" />
              <XAxis dataKey="name" tick={{ fontSize: 12, fill: 'hsl(215,20%,60%)' }} />
              <YAxis tickFormatter={v => `₹${(v/1000).toFixed(0)}k`} tick={{ fontSize: 11, fill: 'hsl(215,20%,60%)' }} />
              <Tooltip formatter={(v) => formatINR(Number(v))} contentStyle={{ background: 'hsl(220,16%,10%)', border: '1px solid hsl(220,13%,18%)' }} />
              <Bar dataKey="Net Value (₹)" fill="#22c55e" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="glass-card p-5">
          <h2 className="text-sm font-semibold mb-4">Multi-Metric Radar</h2>
          <ResponsiveContainer width="100%" height={220}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="hsl(220,13%,18%)" />
              <PolarAngleAxis dataKey="metric" tick={{ fontSize: 11, fill: 'hsl(215,20%,60%)' }} />
              <PolarRadiusAxis tick={false} domain={[0, 100]} />
              {evals.map(e => (
                <Radar
                  key={e.strategy}
                  name={STRATEGY_LABELS[e.strategy]}
                  dataKey={STRATEGY_LABELS[e.strategy]}
                  stroke={STRATEGY_COLORS[e.strategy]}
                  fill={STRATEGY_COLORS[e.strategy]}
                  fillOpacity={0.1}
                />
              ))}
              <Legend wrapperStyle={{ fontSize: 11 }} />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Scoreboard table */}
      <div className="glass-card overflow-hidden">
        <div className="flex items-center gap-2 border-b border-border px-4 py-3">
          <BarChart3 className="h-4 w-4 text-primary" />
          <h2 className="font-semibold text-sm">Scoreboard</h2>
          <span className="ml-2 text-xs text-muted-foreground italic">(Same dataset, same constraints)</span>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Strategy</th>
              <th>Net Value</th>
              <th>Demand Fill %</th>
              <th>Spoilage %</th>
              <th>Unmet Demand</th>
              <th>Transport Cost</th>
              <th>Discount Cost</th>
              <th>Violations</th>
              <th>Runtime</th>
            </tr>
          </thead>
          <tbody>
            {evals
              .sort((a, b) => b.net_value_inr - a.net_value_inr)
              .map((e, i) => (
                <tr key={e.id} className={i === 0 ? 'bg-primary/5' : ''}>
                  <td>
                    <div className="flex items-center gap-2">
                      <span className="h-2 w-2 rounded-full" style={{ background: STRATEGY_COLORS[e.strategy] }} />
                      <span className="font-medium">{STRATEGY_LABELS[e.strategy]}</span>
                      {i === 0 && <span className="badge-risk-low">Best</span>}
                    </div>
                  </td>
                  <td className="tabular-nums font-bold">{formatINR(e.net_value_inr)}</td>
                  <td className="tabular-nums">{formatPercent(e.demand_fulfilment_percent)}</td>
                  <td className="tabular-nums">{formatPercent(e.spoilage_percent)}</td>
                  <td className="tabular-nums">{formatKg(e.unmet_demand_kg)}</td>
                  <td className="tabular-nums text-muted-foreground">{formatINR(e.transport_cost_inr)}</td>
                  <td className="tabular-nums text-muted-foreground">{formatINR(e.discount_cost_inr)}</td>
                  <td className={e.violation_count > 0 ? 'text-red-400 font-bold' : 'text-primary'}>{e.violation_count}</td>
                  <td className="tabular-nums text-muted-foreground">{e.runtime_seconds.toFixed(2)}s</td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      <div className="glass-card p-4 text-xs text-muted-foreground">
        <p className="font-medium text-foreground mb-1">Metric Definitions</p>
        <ul className="space-y-0.5 list-disc list-inside">
          <li>Spoilage % = spoiled kg / starting inventory kg × 100</li>
          <li>Demand Fulfilment % = fulfilled demand kg / total demand kg × 100</li>
          <li>Net Value = Revenue − Transport − Handling − Discount costs</li>
          <li>All strategies use the same input dataset and hard constraints</li>
          {(data === undefined) && <li className="text-yellow-400">⚠ Showing sample data — run the backend to see real evaluation results</li>}
        </ul>
      </div>
    </div>
  );
}
