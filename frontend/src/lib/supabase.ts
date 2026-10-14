import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL as string;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string;

const isConfigured =
  supabaseUrl &&
  supabaseUrl !== 'https://YOUR_PROJECT_REF.supabase.co' &&
  supabaseAnonKey;

if (!isConfigured) {
  console.warn(
    '[FreshRoute] Supabase environment variables not configured.\n' +
    'Copy .env.example to .env and fill in VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.\n' +
    'Running in SAMPLE DATA mode — authentication is disabled.',
  );
}

export const supabase = isConfigured
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null;

export const supabaseConfigured = isConfigured;
