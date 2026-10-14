import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Tag, TrendingDown, TrendingUp, Info } from 'lucide-react';
import { discountService } from '@/services/api';
import { formatINR, formatKg, formatPercent } from '@/lib/utils';
import type { DiscountRecommendation } from '@/types';

const ACTION_STYLES: Record<string, { label: string; className: string }> = {
  sell_full: { label: 'Sell at Full Price', className: 'badge-risk-low' },
  discount: { label: 'Apply Discount', className: 'badge-risk-medium' },
  redirect: { label: 'Redirect', className: 'badge-risk-medium' },
  salvage: { label: 'Salvage', className: 'badge-risk-high' },
  no_option: { label: 'No Option', className: 'badge-risk-high' },
};

const SAMPLE_DISCOUNTS: DiscountRecommendation[] = [
  {
    batch_id: 'b1',
    destination_id: 'd1',
    recommended_action: 'discount',
    recommended_discount_percent: 15,
    options: [
      { discount_percent: 0, recommended_price_inr_per_kg: 28, expected_quantity_kg: 300, estimated_revenue_inr: 8400, transport_cost_inr: 3500, handling_cost_inr: 450, net_value_inr: 4450, demand_response_assumption: 'Base demand, no price sensitivity' },
      { discount_percent: 10, recommended_price_inr_per_kg: 25.2, expected_quantity_kg: 360, estimated_revenue_inr: 9072, transport_cost_inr: 3500, handling_cost_inr: 540, net_value_inr: 5032, demand_response_assumption: 'Simulated: 20% demand uplift per 10% discount' },
      { discount_percent: 15, recommended_price_inr_per_kg: 23.8, expected_quantity_kg: 390, estimated_revenue_inr: 9282, transport_cost_inr: 3500, handling_cost_inr: 585, net_value_inr: 5197, demand_response_assumption: 'Simulated: 30% demand uplift per 10% discount' },
      { discount_percent: 20, recommended_price_inr_per_kg: 22.4, expected_quantity_kg: 420, estimated_revenue_inr: 9408, transport_cost_inr: 3500, handling_cost_inr: 630, net_value_inr: 5278, demand_response_assumption: 'Simulated: 40% demand uplift per 10% discount' },
    ],
    explanation: 'Batch TOM-2024-001 has 18 hours remaining. At full price, only 300kg can be sold before expiry. A 15% discount is projected to increase demand by 30%, improving net value by ₹747.',
    assumptions: ['Demand response elasticity is simulated — no historical transaction data available', 'Walk-away price not configured — minimum price floor not enforced'],
    uncertainty_note: 'Demand response estimates are assumptions. Actual uplift may vary significantly.',
    walk_away_price_available: false,
  },
];

export function DiscountsPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['discounts'],
    queryFn: discountService.getRecommendations,
  });

  const recs = data ?? SAMPLE_DISCOUNTS;

  return (
    <div className="animate-fade-in space-y-6">
      <div className="section-header">
        <div>
          <h1 className="text-2xl font-bold">Discount Engine</h1>
          <p className="text-sm text-muted-foreground mt-1">Compare pricing strategies for at-risk batches</p>
        </div>
      </div>

      {recs.map((rec, i) => (
        <div key={i} className="glass-card overflow-hidden">
          <div className="flex items-center justify-between border-b border-border px-5 py-4">
            <div className="flex items-center gap-3">
              <Tag className="h-4 w-4 text-primary" />
              <div>
                <p className="font-semibold">Batch {rec.batch?.batch_code ?? rec.batch_id.slice(0,8)}</p>
                <p className="text-xs text-muted-foreground">→ {rec.destination?.name ?? rec.destination_id}</p>
              </div>
            </div>
            <span className={ACTION_STYLES[rec.recommended_action]?.className}>
              {ACTION_STYLES[rec.recommended_action]?.label} — {rec.recommended_discount_percent}% discount
            </span>
          </div>

          <div className="p-5 space-y-4">
            {/* Options comparison table */}
            <div className="overflow-x-auto">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Discount</th>
                    <th>Price / kg</th>
                    <th>Qty Sold</th>
                    <th>Revenue</th>
                    <th>Cost</th>
                    <th>Net Value</th>
                    <th>Best?</th>
                  </tr>
                </thead>
                <tbody>
                  {rec.options.map((opt, j) => {
                    const isBest = opt.discount_percent === rec.recommended_discount_percent;
                    return (
                      <tr key={j} className={isBest ? 'bg-primary/5' : ''}>
                        <td className="tabular-nums font-medium">{opt.discount_percent === 0 ? 'Full Price' : `${opt.discount_percent}%`}</td>
                        <td className="tabular-nums">{formatINR(opt.recommended_price_inr_per_kg, 2)}</td>
                        <td className="tabular-nums">{formatKg(opt.expected_quantity_kg)}</td>
                        <td className="tabular-nums">{formatINR(opt.estimated_revenue_inr)}</td>
                        <td className="tabular-nums text-muted-foreground">{formatINR(opt.transport_cost_inr + opt.handling_cost_inr)}</td>
                        <td className={`tabular-nums font-bold ${isBest ? 'text-primary' : ''}`}>{formatINR(opt.net_value_inr)}</td>
                        <td>{isBest && <span className="badge-risk-low">✓ Recommended</span>}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            {/* Explanation */}
            <div className="rounded-lg bg-accent/50 p-4 text-sm">
              <p className="font-medium mb-1">Explanation</p>
              <p className="text-muted-foreground">{rec.explanation}</p>
            </div>

            {/* Assumptions */}
            <div className="flex items-start gap-2 text-xs text-yellow-400">
              <Info className="h-4 w-4 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-medium mb-1">Assumptions & Uncertainty</p>
                {rec.assumptions.map((a, k) => <p key={k}>• {a}</p>)}
                <p className="mt-1 italic">{rec.uncertainty_note}</p>
                {!rec.walk_away_price_available && (
                  <p className="mt-1 text-orange-400">⚠ Walk-away price not configured — no minimum price floor enforced.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
