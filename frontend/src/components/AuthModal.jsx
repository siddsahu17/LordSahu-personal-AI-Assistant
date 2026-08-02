import React, { useState } from 'react';
import { X, Sparkles, LogIn, Mail, Lock } from 'lucide-react';

export default function AuthModal({ isOpen, onClose, onLoginSuccess }) {
  const [email, setEmail] = useState('siddhant@lordsahu.ai');
  const [password, setPassword] = useState('••••••••');
  const [isSignUp, setIsSignUp] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    onLoginSuccess();
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="neo-card p-6 md:p-8 bg-white max-w-md w-full space-y-6 relative shadow-[8px_8px_0px_0px_#000]">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg border-2 border-black bg-slate-100 hover:bg-slate-200"
        >
          <X className="w-4 h-4 text-black" />
        </button>

        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 bg-blue-100 text-blue-900 border-2 border-black px-2.5 py-0.5 rounded-full text-xs font-black">
            <Sparkles className="w-3.5 h-3.5" />
            AUTHENTICATION
          </div>
          <h2 className="text-2xl font-black text-black">
            {isSignUp ? 'Create LordSahu Account' : 'Welcome Back, Siddhant'}
          </h2>
          <p className="text-xs text-slate-700 font-medium">
            Sign in to access your personal AI operating system timeline.
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4 text-xs font-bold">
          <div>
            <label className="block text-black mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full bg-slate-50 text-black border-2 border-black rounded-xl pl-9 pr-3 py-2.5 focus:outline-none focus:bg-white"
              />
            </div>
          </div>

          <div>
            <label className="block text-black mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full bg-slate-50 text-black border-2 border-black rounded-xl pl-9 pr-3 py-2.5 focus:outline-none focus:bg-white"
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full neo-btn bg-blue-600 hover:bg-blue-500 text-white py-3 text-sm font-black flex items-center justify-center gap-2 shadow-[4px_4px_0px_0px_#000]"
          >
            <LogIn className="w-4 h-4" /> {isSignUp ? 'Sign Up' : 'Continue to LordSahu'}
          </button>
        </form>

        <div className="relative border-t-2 border-black my-4 text-center">
          <span className="bg-white px-2 text-[10px] font-black text-slate-500 absolute -top-2 left-1/2 -translate-x-1/2">
            OR
          </span>
        </div>

        {/* Google Login Button */}
        <button
          onClick={() => { onLoginSuccess(); onClose(); }}
          className="w-full neo-btn bg-white hover:bg-slate-50 text-black py-2.5 text-xs font-black flex items-center justify-center gap-2 shadow-[3px_3px_0px_0px_#000]"
        >
          <svg className="w-4 h-4" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
          </svg>
          Continue with Google
        </button>

        <p className="text-center text-xs font-bold text-slate-700">
          {isSignUp ? 'Already have an account?' : "Don't have an account?"}{' '}
          <button
            onClick={() => setIsSignUp(!isSignUp)}
            className="text-blue-700 underline font-black"
          >
            {isSignUp ? 'Sign In' : 'Sign Up'}
          </button>
        </p>
      </div>
    </div>
  );
}
