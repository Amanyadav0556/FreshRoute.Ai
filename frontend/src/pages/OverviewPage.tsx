import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Package, AlertTriangle, TrendingUp, CheckCircle, XCircle, Zap, Leaf, BarChart3 } from 'lucide-react';
import { dashboardService } from '@/services/api';
import { formatINR, formatKg, formatPercent } from '@/lib/utils';

interface StatCardProps {
  icon: React.ElementType;
  label: string;
  value: string;
  sub?: string;
  color?: string;
}

function StatCard({ icon: Icon, label, value, sub, color = 'text-primary' }: StatCardProps) {
  return (
    <div className="stat-card animate-slide-up">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs text-muted-foreground font-medium uppercase tracking-wider">{label}</p>
          <p className={`mt-2 text-2xl font-bold tabular-nums ${color}`}>{value}</p>
          {sub && <p className="mt-1 text-xs text-muted-foreground">{sub}</p>}
        </div>
        <div className={`rounded-lg p-2.5 bg-current/10 ${color}`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>
    </div>
  );
}

const SAMPLE: import('@/types').DashboardSummary = {
  total_inventory_kg: 4250,
  high_risk_batch_count: 3,
  expired_batch_count: 1,
  planned_dispatch_count: 8,
  demand_fulfilment_percent: 87.4,
  spoilage_percent: 4.2,
  net_economic_value_inr: 182500,
  constraint_violations: 0,
  data_mode: 'sample',
};

export function OverviewPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['dashboard-summary'],
    queryFn: dashboardService.getSummary,
  });

  const summary = data ?? SAMPLE;

  return (
    <div className="animate-fade-in space-y-6">
      {/* Header */}
      <div className="section-header">
        <div>
          <h1 className="text-2xl font-bold text-foreground">
            <span className="gradient-text">FreshRoute AI</span> — Overview
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Real-time perishable produce distribution intelligence
          </p>
        </div>
        {summary.data_mode === 'sample' && (
          <span className="rounded-full border border-yellow-500/30 bg-yellow-500/10 px-3 py-1 text-xs font-medium text-yellow-400">
            ⚠ Sample Data Mode
          </span>
        )}
      </div>

      {/* KPI grid */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard
          icon={Package}
          label="Total Inventory"
          value={formatKg(summary.total_inventory_kg)}
          sub="across all batches"
        />
        <StatCard
          icon={AlertTriangle}
          label="High-Risk Batches"
          value={String(summary.high_risk_batch_count)}
          sub={`${summary.expired_batch_count} expired`}
          color="text-orange-400"
        />
        <StatCard
          icon={Zap}
          label="Planned Dispatches"
          value={String(summary.planned_dispatch_count)}
          sub="active recommendations"
          color="text-blue-400"
        />
        <StatCard
          icon={TrendingUp}
          label="Net Economic Value"
          value={formatINR(summary.net_economic_value_inr)}
          sub="from optimizer plan"
          color="text-primary"
        />
      </div>

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard
          icon={BarChart3}
          label="Demand Fulfilment"
          value={formatPercent(summary.demand_fulfilment_percent)}
          sub="of total demand met"
          color="text-primary"
        />
        <StatCard
          icon={Leaf}
          label="Spoilage Rate"
          value={formatPercent(summary.spoilage_percent)}
          sub="of starting inventory"
          color={summary.spoilage_percent > 10 ? 'text-red-400' : 'text-primary'}
        />
        <StatCard
          icon={summary.constraint_violations === 0 ? CheckCircle : XCircle}
          label="Constraint Violations"
          value={String(summary.constraint_violations)}
          sub={summary.constraint_violations === 0 ? 'All constraints satisfied' : 'Plan marked INVALID'}
          color={summary.constraint_violations === 0 ? 'text-primary' : 'text-red-400'}
        />
        <StatCard
          icon={AlertTriangle}
          label="Expired Stock"
          value={String(summary.expired_batch_count)}
          sub="batches past shelf life"
          color="text-red-400"
        />
      </div>

      {/* Status banner */}
      {isError && (
        <div className="alert-warning">
          <AlertTriangle className="h-4 w-4 flex-shrink-0 mt-0.5" />
          <span>Backend unreachable — showing sample data. Start the FastAPI server at localhost:8000.</span>
        </div>
      )}

      {/* Data provenance note */}
      <div className="glass-card p-4 text-sm text-muted-foreground">
        <p className="font-medium text-foreground mb-1">Data Provenance</p>
        <p>
          Dashboard metrics are sourced from the FreshRoute AI optimizer.
          {summary.data_mode === 'sample'
            ? ' Currently displaying simulated sample data — connect Supabase and start the backend to see live data.'
            : ' Live data from Supabase database.'}
        </p>
      </div>
    </div>
  );
}
