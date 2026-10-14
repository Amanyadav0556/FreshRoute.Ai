/** Format a number as Indian Rupees (INR). */
export function formatINR(value: number, decimals = 0): string {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: decimals,
    minimumFractionDigits: decimals,
  }).format(value);
}

/** Format kg with unit label. */
export function formatKg(value: number, decimals = 1): string {
  return `${value.toLocaleString('en-IN', { maximumFractionDigits: decimals })} kg`;
}

/** Format hours with unit. */
export function formatHours(value: number): string {
  if (value < 1) return `${Math.round(value * 60)} min`;
  return `${value.toFixed(1)} hr`;
}

/** Format percentage. */
export function formatPercent(value: number, decimals = 1): string {
  return `${value.toFixed(decimals)}%`;
}

/** Relative time label for shelf life. */
export function shelfLifeLabel(hours: number): string {
  if (hours <= 0) return 'Expired';
  if (hours < 6) return `${hours.toFixed(1)}h (Critical)`;
  if (hours < 24) return `${hours.toFixed(1)}h`;
  const days = hours / 24;
  return `${days.toFixed(1)} days`;
}

/** Compute risk level from remaining shelf life and min feasible delivery time. */
export function computeRiskLevel(
  remainingHours: number,
  minDeliveryHours: number,
): 'low' | 'medium' | 'high' | 'expired' {
  if (remainingHours <= 0) return 'expired';
  const buffer = remainingHours - minDeliveryHours;
  if (buffer <= 0) return 'high';
  if (buffer <= remainingHours * 0.3) return 'high';
  if (buffer <= remainingHours * 0.5) return 'medium';
  return 'low';
}

/** Clamp a number between min and max. */
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

/** Truncate long text. */
export function truncate(text: string, maxLen = 80): string {
  return text.length > maxLen ? `${text.slice(0, maxLen)}…` : text;
}

/** Format ISO date string as readable date. */
export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });
}

/** Format ISO datetime string. */
export function formatDateTime(iso: string): string {
  return new Date(iso).toLocaleString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

/** cn utility (clsx + tailwind-merge). */
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
