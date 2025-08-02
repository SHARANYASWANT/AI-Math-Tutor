'use client';

import { useState } from 'react';
import Link from 'next/link';
import { AuthForm } from '@/components/AuthForm';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Calculator } from 'lucide-react';

export default function SignupPage() {
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (data: { email: string; password: string; name?: string }) => {
    setIsLoading(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    console.log('Signup attempt:', data);
    setIsLoading(false);
    // In a real app, handle successful signup here
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-2 font-bold text-2xl text-gray-900 hover:text-blue-600 transition-colors">
            <Calculator className="h-7 w-7 text-blue-600" />
            MathVid
          </Link>
        </div>

        <Card className="shadow-xl border-0 bg-white/90 backdrop-blur-sm">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl text-gray-900">Create your account</CardTitle>
            <CardDescription className="text-gray-600">
              Join thousands of students learning math visually
            </CardDescription>
          </CardHeader>
          <CardContent>
            <AuthForm
              type="signup"
              onSubmit={handleSubmit}
              isLoading={isLoading}
            />
            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                Already have an account?{' '}
                <Link href="/login" className="font-medium text-blue-600 hover:text-blue-500 transition-colors">
                  Sign in
                </Link>
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}