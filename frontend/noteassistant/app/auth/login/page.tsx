// app/auth/login/page.tsx

import LoginForm from '@/app/components/LoginForm';
import React from 'react';

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="w-full max-w-md p-8 bg-white shadow-lg rounded-lg">
        <h2 className="text-2xl font-semibold text-center text-gray-700 mb-6">Login</h2>
        <LoginForm />
      </div>
    </div>
  );
}
