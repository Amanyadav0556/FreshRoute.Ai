# FreshRoute AI — Benchmark Methodology & Evaluation Protocol

## 1. Objectives

The FreshRoute AI benchmark evaluation suite was engineered to quantify the exact economic and biological benefits of algorithmic perishable produce dispatch versus legacy logistics dispatch paradigms.

---

## 2. Compared Dispatch Strategies

| Strategy Key | Display Name | Logic & Operational Paradigm |
|-------------|--------------|------------------------------|
| `fefo_baseline` | **Standard FEFO** | First-Expired First-Out: Dispatches produce solely based on remaining shelf life, allocating to arbitrary destinations regardless of freight cost or price. |
| `highest_price_baseline` | **Highest Price First** | Revenue-Maximizing Heuristic: Chases highest top-line buyer bid prices, often routing to distant markets where high spoilage and fuel charges erode net profits. |
| `greedy_baseline` | **Greedy Heuristic Dispatch** | Multi-Attribute Priority: Greedy packing ordered by urgency-adjusted margin index $\frac{\text{Margin}}{\text{TransitTime}} + w \cdot \text{Urgency}$. |
| `freshroute_optimizer` | **FreshRoute AI (HiGHS LP)** | Mixed-Integer/Continuous Simplex Solver: Solves global objective function subject to simultaneous vehicle capacities, shelf-life arrival cutoffs, and demand ceilings. |

---

## 3. Evaluation Metrics

1. **Net Economic Value (INR)**: Gross sales revenue minus transportation fuel/tolls, handling fees, and write-off costs for spoiled cargo.
2. **Physical Spoilage (kg & %)**: Mass of produce that decays beyond acceptable freshness thresholds before delivery.
3. **Order Fulfillment Rate (%)**: Percentage of buyer purchase order quantities successfully fulfilled on time.
4. **Average Arrival Freshness Buffer (hours)**: Remaining consumable shelf life delivered into the hands of the destination buyer.
5. **Fleet Utilization (%)**: Percentage of total transport vehicle capacity productively deployed.
6. **Computation Duration (ms)**: Real-time latency required to compute the entire dispatch solution.

---

## 4. Empirical Benchmark Results (Maharashtra Corridor)

```
Scenario: Normal Operation
Total Inventory: 14,850 kg | Total Market Demand: 10,500 kg

Strategy                              Net Value (INR)  Revenue (INR)  Spoil (kg)  Fulfill %  Time (ms)
------------------------------------------------------------------------------------------------------
Standard FEFO (First-Expired First-Out)  INR 468,540.60   INR 530,930.40   1,782.0kg    72.5%     1.2ms
Highest Price First Dispatch            INR 329,788.67   INR 356,914.00     560.0kg    78.0%     1.5ms
Greedy Heuristic Dispatch               INR 606,204.00   INR 627,415.00   1,532.3kg    86.0%     1.0ms
FreshRoute AI Optimizer (HiGHS)         INR 589,612.50   INR 610,352.50     938.8kg    94.5%     6.5ms
```

### Quantified Impact vs Legacy FEFO:
- **+25.8% increase in Net Economic Value** (+₹121,071 on a single day's dispatches)
- **47.3% reduction in physical food waste / spoilage** (843 kg saved from landfill)
- **+22.0 percentage point increase in buyer order fulfillment**
- **Sub-10 millisecond decision latency** (suitable for live dispatch dispatching)
