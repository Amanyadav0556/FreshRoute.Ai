import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Package,
  MapPin,
  Truck,
  Zap,
  Tag,
  AlertTriangle,
  BarChart3,
  FlaskConical,
  Info,
  Settings,
  LogOut,
  Leaf,
} from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { cn } from '@/lib/utils';

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Overview' },
  { to: '/inventory', icon: Package, label: 'Inventory' },
  { to: '/destinations', icon: MapPin, label: 'Destinations & Orders' },
  { to: '/vehicles', icon: Truck, label: 'Vehicles & Routes' },
  { to: '/planner', icon: Zap, label: 'Optimization Planner' },
  { to: '/discounts', icon: Tag, label: 'Discount Engine' },
  { to: '/alerts', icon: AlertTriangle, label: 'Spoilage Alerts' },
  { to: '/evaluation', icon: BarChart3, label: 'Evaluation & Scoreboard' },
  { to: '/scenarios', icon: FlaskConical, label: 'Scenarios' },
  { to: '/assumptions', icon: Info, label: 'Assumptions & Provenance' },
  { to: '/settings', icon: Settings, label: 'Settings' },
];

export function Sidebar() {
  const { profile, signOut, configured } = useAuth();

  return (
    <aside className="flex h-screen w-64 flex-col border-r border-border bg-card">
      {/* Logo */}
      <div className="flex items-center gap-2.5 px-5 py-5 border-b border-border">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/20">
          <Leaf className="h-4 w-4 text-primary" />
        </div>
        <div>
          <p className="text-sm font-bold tracking-tight text-foreground">FreshRoute</p>
          <p className="text-[10px] text-muted-foreground font-medium">AI • Distribution Engine</p>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-0.5">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              cn(
                'nav-item',
                isActive && 'active',
              )
            }
          >
            <Icon className="h-4 w-4 flex-shrink-0" />
            <span className="truncate">{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* User footer */}
      <div className="border-t border-border p-4">
        {!configured && (
          <div className="mb-3 rounded-md border border-yellow-500/30 bg-yellow-500/10 px-3 py-2 text-xs text-yellow-400">
            ⚠ Sample data mode
          </div>
        )}
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/20 text-xs font-bold text-primary">
            {profile?.display_name?.[0]?.toUpperCase() ?? 'D'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="truncate text-xs font-medium text-foreground">
              {profile?.display_name ?? 'Distributor'}
            </p>
            <p className="truncate text-[10px] text-muted-foreground capitalize">
              {profile?.role ?? 'distributor'}
            </p>
          </div>
          {configured && (
            <button
              onClick={signOut}
              className="rounded-md p-1.5 text-muted-foreground hover:bg-accent hover:text-foreground transition-colors"
              title="Sign out"
            >
              <LogOut className="h-3.5 w-3.5" />
            </button>
          )}
        </div>
      </div>
    </aside>
  );
}
