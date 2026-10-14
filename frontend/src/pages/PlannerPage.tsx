import React, { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Zap, Play, CheckCircle, XCircle, AlertTriangle, ChevronDown, ChevronUp } from 'lucide-react';
import { planService, scenarioService } from '@/services/api';
import { formatINR, formatKg } from '@/lib/utils';
import type { Plan, PlanStrategy } from '@/types';

const STRATEGIES: { value: PlanStrategy; label: string; description: string }[] = [
  { value: 'freshroute', label: 'FreshRoute Optimizer', description: 'LP optimization via SciPy/HiGHS maximizing net economic value' },
  { value: 'fefo', label: 'FEFO Baseline', description: 'First Expired, First Out — dispatch closest-to-expiry batches first' },
  { value: 'highest_price', label: 'Highest Price First', description: 'Prefer destinations with highest base price per kg' },
  { value: 'greedy', label: 'Greedy Heuristic', description: 'Greedy shelf-life heuristic — deterministic fallback' },
];

export function PlannerPage() {
  const [strategy, setStrategy] = useState<PlanStrategy>('freshroute');
  const [scenarioId, setScenarioId] = useState('');
  const [plan, setPlan] = useState<Plan | null>(null);
  const [expandedRec, setExpandedRec] = useState<string | null>(null);

  const { data: scenarios } = useQuery({ queryKey: ['scenarios'], queryFn: scenarioService.getAll });

  const runMutation = useMutation({
    mutationFn: () => planService.create({ strategy, scenario_id: scenarioId || undefined }),
    onSuccess: (data) => setPlan(data),
  });

  const validateMutation = useMutation({
    mutationFn: () => planService.validate(plan!.id),
    onSuccess: (data) => setPlan(data),
  });

  return (
    <div className="animate-fade-in space-y-6">
      <div className="section-header">
        <div>
          <h1 className="text-2xl font-bold">Optimization Planner</h1>
          <p className="text-sm text-muted-foreground mt-1">Generate and validate dispatch plans</p>
        </div>
      </div>

      {/* Configuration */}
      <div className="glass-card p-6 space-y-5">
        <h2 className="font-semibold text-sm text-muted-foreground uppercase tracking-wider">Configuration</h2>

        <div className="grid gap-4 lg:grid-cols-2">
          {/* Strategy */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Strategy</label>
            <div className="grid gap-2">
              {STRATEGIES.map(s => (
                <label key={s.value} className={`flex cursor-pointer items-start gap-3 rounded-lg border p-3 transition-colors ${strategy === s.value ? 'border-primary/50 bg-primary/5' : 'border-border hover:bg-accent'}`}>
                  <input type="radio" name="strategy" value={s.value} checked={strategy === s.value} onChange={() => setStrategy(s.value)} className="mt-0.5" />
                  <div>
                    <p className="text-sm font-medium">{s.label}</p>
                    <p className="text-xs text-muted-foreground">{s.description}</p>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Scenario */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Scenario (optional)</label>
            <select
              className="w-full rounded-lg border border-border bg-card px-3 py-2 text-sm"
              value={scenarioId}
              onChange={e => setScenarioId(e.target.value)}
            >
              <option value="">Normal Operation</option>
              {(scenarios ?? []).map(s => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
            <p className="text-xs text-muted-foreground">Select a disruption scenario to test robustness</p>
          </div>
        </div>

        <button
          onClick={() => runMutation.mutate()}
          disabled={runMutation.isPending}
          className="flex items-center gap-2 rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground hover:bg-primary/90 disabled:opacity-60 transition-all"
        >
          <Play className="h-4 w-4" />
          {runMutation.isPending ? 'Running optimizer…' : 'Run Optimizer'}
        </button>
      </div>

      {/* Results */}
      {plan && (
        <div className="space-y-4 animate-slide-up">
          {/* Status bar */}
          <div className="glass-card p-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              {plan.status === 'valid' ? (
                <CheckCircle className="h-5 w-5 text-primary" />
              ) : plan.status === 'invalid' ? (
                <XCircle className="h-5 w-5 text-red-400" />
              ) : (
                <AlertTriangle className="h-5 w-5 text-yellow-400" />
              )}
              <div>
                <p className="font-semibold text-sm">Plan {plan.id.slice(0, 8)}…</p>
                <p className="text-xs text-muted-foreground">
                  {plan.optimizer_method} · Status: <span className="capitalize font-medium">{plan.solver_status}</span>
                </p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-lg font-bold text-primary tabular-nums">{formatINR(plan.objective_value_inr)}</p>
              <p className="text-xs text-muted-foreground">objective value</p>
            </div>
            <button
              onClick={() => validateMutation.mutate()}
              disabled={!plan.id || validateMutation.isPending}
              className="ml-4 rounded-lg border border-border px-3 py-1.5 text-xs font-medium hover:bg-accent transition-colors"
            >
              {validateMutation.isPending ? 'Validating…' : 'Re-validate'}
            </button>
          </div>

          {/* Violations */}
          {plan.violations && plan.violations.length > 0 && (
            <div className="alert-danger">
              <XCircle className="h-4 w-4 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-medium mb-1">Constraint Violations — Plan is INVALID</p>
                {plan.violations.map((v, i) => (
                  <p key={i} className="text-xs">{v.constraint_id}: {v.reason} (actual {v.actual_value} vs allowed {v.allowed_value})</p>
                ))}
              </div>
            </div>
          )}

          {/* Recommendations */}
          <div className="glass-card overflow-hidden">
            <div className="border-b border-border px-4 py-3 flex items-center gap-2">
              <Zap className="h-4 w-4 text-primary" />
              <h2 className="font-semibold text-sm">Dispatch Recommendations</h2>
              <span className="ml-auto text-xs text-muted-foreground">{plan.recommendations?.length ?? 0} allocations</span>
            </div>
            <div className="divide-y divide-border">
              {(plan.recommendations ?? []).map(rec => (
                <div key={rec.id} className="p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-medium text-sm">
                        Batch {rec.batch?.batch_code ?? rec.batch_id.slice(0, 8)} → {rec.destination?.name ?? rec.destination_id}
                      </p>
                      <p className="text-xs text-muted-foreground mt-0.5">
                        {formatKg(rec.quantity_kg)} · {rec.vehicle?.vehicle_code ?? rec.vehicle_id} · {rec.discount_percent}% discount
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-primary tabular-nums">{formatINR(rec.estimated_net_value_inr)}</p>
                      <p className="text-xs text-muted-foreground">net value</p>
                    </div>
                    <button
                      onClick={() => setExpandedRec(expandedRec === rec.id ? null : rec.id)}
                      className="ml-4 text-muted-foreground hover:text-foreground"
                    >
                      {expandedRec === rec.id ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                    </button>
                  </div>
                  {expandedRec === rec.id && (
                    <div className="mt-3 rounded-lg bg-accent/50 p-3 text-xs text-muted-foreground">
                      <p className="mb-1 font-medium text-foreground">Explanation</p>
                      <p>{rec.explanation}</p>
                      <div className="mt-2 grid grid-cols-3 gap-2 text-xs">
                        <div><span className="text-muted-foreground">Revenue: </span><span className="tabular-nums">{formatINR(rec.estimated_revenue_inr)}</span></div>
                        <div><span className="text-muted-foreground">Cost: </span><span className="tabular-nums">{formatINR(rec.estimated_cost_inr)}</span></div>
                        <div><span className="text-muted-foreground">Price: </span><span className="tabular-nums">{formatINR(rec.recommended_price_inr_per_kg, 2)}/kg</span></div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
              {(plan.recommendations ?? []).length === 0 && (
                <p className="px-4 py-6 text-sm text-center text-muted-foreground">No feasible allocations found for this configuration.</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
