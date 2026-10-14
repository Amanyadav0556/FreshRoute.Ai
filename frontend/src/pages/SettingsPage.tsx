import React from 'react';
import { Settings, Info } from 'lucide-react';

export function SettingsPage() {
  return (
    <div className="animate-fade-in space-y-6">
      <div className="section-header">
        <h1 className="text-2xl font-bold">Settings</h1>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="glass-card p-5 space-y-4">
          <h2 className="font-semibold text-sm text-muted-foreground uppercase tracking-wider">Connection</h2>
          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-muted-foreground">Backend URL</label>
              <input readOnly className="mt-1 w-full rounded-lg border border-border bg-accent px-3 py-2 text-sm font-mono" value={import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'} />
            </div>
            <div>
              <label className="text-xs font-medium text-muted-foreground">Supabase URL</label>
              <input readOnly className="mt-1 w-full rounded-lg border border-border bg-accent px-3 py-2 text-sm font-mono" value={import.meta.env.VITE_SUPABASE_URL ?? '(not configured)'} />
            </div>
          </div>
        </div>

        <div className="glass-card p-5 space-y-4">
          <h2 className="font-semibold text-sm text-muted-foreground uppercase tracking-wider">Optimizer</h2>
          <div className="space-y-3 text-sm text-muted-foreground">
            <p>Solver timeout: <span className="text-foreground font-mono">30s</span> (configurable via <code>SOLVER_TIMEOUT_SECONDS</code>)</p>
            <p>Fallback: <span className="text-foreground font-mono">greedy</span></p>
            <p>Demand response elasticity: <span className="text-foreground font-mono">0.2 per 10% discount</span> (simulated)</p>
          </div>
        </div>
      </div>

      <div className="alert-success">
        <Info className="h-4 w-4 flex-shrink-0 mt-0.5" />
        <span>Edit <code>.env</code> in the project root to configure Supabase and backend connections. Never commit real credentials.</span>
      </div>
    </div>
  );
}
