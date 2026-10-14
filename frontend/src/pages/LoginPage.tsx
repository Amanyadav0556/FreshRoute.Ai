import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Leaf, LogIn, UserPlus, AlertTriangle } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useNavigate } from 'react-router-dom';

const loginSchema = z.object({
  email: z.string().email('Enter a valid email'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

const signupSchema = loginSchema.extend({
  displayName: z.string().min(2, 'Name must be at least 2 characters'),
});

type LoginData = z.infer<typeof loginSchema>;
type SignupData = z.infer<typeof signupSchema>;

export function LoginPage() {
  const [mode, setMode] = useState<'login' | 'signup'>('login');
  const [serverError, setServerError] = useState('');
  const { signIn, signUp, configured } = useAuth();
  const navigate = useNavigate();

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<SignupData>({
    resolver: zodResolver(mode === 'login' ? loginSchema : signupSchema),
  });

  async function onSubmit(data: SignupData) {
    setServerError('');
    const { error } = mode === 'login'
      ? await signIn(data.email, data.password)
      : await signUp(data.email, data.password, data.displayName ?? '');
    if (error) setServerError(error.message);
    else navigate('/');
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="w-full max-w-sm space-y-6 animate-slide-up">
        {/* Logo */}
        <div className="flex flex-col items-center gap-3 text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/20">
            <Leaf className="h-6 w-6 text-primary" />
          </div>
          <div>
            <h1 className="text-2xl font-bold gradient-text">FreshRoute AI</h1>
            <p className="text-sm text-muted-foreground">Perishable Distribution Intelligence</p>
          </div>
        </div>

        {!configured && (
          <div className="alert-warning">
            <AlertTriangle className="h-4 w-4 flex-shrink-0 mt-0.5" />
            <div className="text-xs">
              <p className="font-medium">Supabase not configured</p>
              <p>Authentication is disabled. <a href="/" className="underline">Continue in sample data mode →</a></p>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="glass-card p-6 space-y-4">
          <div className="flex rounded-lg border border-border overflow-hidden">
            <button type="button" onClick={() => setMode('login')} className={`flex-1 py-2 text-sm font-medium transition-colors ${mode === 'login' ? 'bg-primary text-primary-foreground' : 'text-muted-foreground hover:bg-accent'}`}>Sign In</button>
            <button type="button" onClick={() => setMode('signup')} className={`flex-1 py-2 text-sm font-medium transition-colors ${mode === 'signup' ? 'bg-primary text-primary-foreground' : 'text-muted-foreground hover:bg-accent'}`}>Sign Up</button>
          </div>

          {mode === 'signup' && (
            <div className="space-y-1">
              <label className="text-xs font-medium">Display Name</label>
              <input {...register('displayName')} placeholder="Rajesh Kumar" className="w-full rounded-lg border border-border bg-card px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary" />
              {errors.displayName && <p className="text-xs text-red-400">{errors.displayName.message}</p>}
            </div>
          )}

          <div className="space-y-1">
            <label className="text-xs font-medium">Email</label>
            <input {...register('email')} type="email" placeholder="you@example.com" className="w-full rounded-lg border border-border bg-card px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary" />
            {errors.email && <p className="text-xs text-red-400">{errors.email.message}</p>}
          </div>

          <div className="space-y-1">
            <label className="text-xs font-medium">Password</label>
            <input {...register('password')} type="password" placeholder="••••••••" className="w-full rounded-lg border border-border bg-card px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary" />
            {errors.password && <p className="text-xs text-red-400">{errors.password.message}</p>}
          </div>

          {serverError && <p className="text-xs text-red-400">{serverError}</p>}

          <button type="submit" disabled={isSubmitting || !configured} className="flex w-full items-center justify-center gap-2 rounded-lg bg-primary py-2.5 text-sm font-semibold text-primary-foreground hover:bg-primary/90 disabled:opacity-60 transition-all">
            {mode === 'login' ? <LogIn className="h-4 w-4" /> : <UserPlus className="h-4 w-4" />}
            {isSubmitting ? 'Please wait…' : mode === 'login' ? 'Sign In' : 'Create Account'}
          </button>
        </form>
      </div>
    </div>
  );
}
