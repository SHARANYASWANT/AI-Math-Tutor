'use client';

import { useState } from 'react';
import { VideoPlayer } from '@/components/VideoPlayer';
import { PopularConcepts } from '@/components/PopularConcepts';
import { generateVideoExplanation } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertCircle, Sparkles, Play } from 'lucide-react';

interface VideoResult {
  videoUrl: string;
  transcript: string;
  title: string;
}

export default function Home() {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [videoResult, setVideoResult] = useState<VideoResult | null>(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a mathematical concept or question.');
      return;
    }

    setError('');
    setIsLoading(true);
    setVideoResult(null);

    try {
      const result = await generateVideoExplanation(query);
      setVideoResult(result);
    } catch (err) {
      setError('Failed to generate video explanation. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewQuery = () => {
    setQuery('');
    setVideoResult(null);
    setError('');
  };

  const handleRegenerateVideo = async () => {
    if (!query.trim()) return;
    
    setIsLoading(true);
    setVideoResult(null);
    
    try {
      const result = await generateVideoExplanation(query);
      setVideoResult(result);
    } catch (err) {
      setError('Failed to regenerate video. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleConceptSelect = (concept: string) => {
    setQuery(concept);
    setError('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Hero Section */}
      <section className="pt-20 pb-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-6">
            <Sparkles className="h-4 w-4" />
            AI-Powered Math Explanations
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Transform Math Into
            <span className="text-blue-600 block">Visual Learning</span>
          </h1>
          <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto leading-relaxed">
            Get personalized step-by-step video explanations for any mathematical concept. 
            From basic algebra to advanced calculus, we make math visual and understandable.
          </p>

          {/* Input Form */}
          <Card className="max-w-2xl mx-auto shadow-xl border-0 bg-white/80 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-2xl text-gray-800">Ask Your Math Question</CardTitle>
              <CardDescription className="text-gray-600">
                Describe the mathematical concept you'd like explained in a video
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Textarea
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="e.g., Explain the quadratic formula step by step, or How do you solve systems of linear equations?"
                    className="min-h-[120px] text-base border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                    disabled={isLoading}
                  />
                  {error && (
                    <div className="flex items-center gap-2 text-red-600 text-sm mt-2">
                      <AlertCircle className="h-4 w-4" />
                      {error}
                    </div>
                  )}
                </div>
                <Button
                  type="submit"
                  disabled={isLoading || !query.trim()}
                  className="w-full h-12 text-lg font-semibold bg-blue-600 hover:bg-blue-700 transition-all duration-200 transform hover:scale-[1.02]"
                >
                  {isLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Generating Video...
                    </>
                  ) : (
                    <>
                      <Play className="h-5 w-5 mr-2" />
                      Generate Video Explanation
                    </>
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Video Result Section */}
      {videoResult && (
        <section className="py-16 px-4 animate-slide-up">
          <div className="max-w-6xl mx-auto">
            <VideoPlayer
              videoResult={videoResult}
              onNewQuery={handleNewQuery}
              onRegenerate={handleRegenerateVideo}
              isRegenerating={isLoading}
            />
          </div>
        </section>
      )}

      {/* Popular Concepts Section */}
      {!videoResult && (
        <section className="py-16 px-4">
          <div className="max-w-6xl mx-auto">
            <PopularConcepts onConceptSelect={handleConceptSelect} />
          </div>
        </section>
      )}

      {/* Features Section */}
      <section className="py-20 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Why Choose MathVid?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Experience the future of mathematical learning with our AI-powered platform
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="text-center border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardContent className="pt-6">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Sparkles className="h-6 w-6 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">AI-Powered</h3>
                <p className="text-gray-600">
                  Advanced AI creates personalized explanations tailored to your learning style
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardContent className="pt-6">
                <div className="w-12 h-12 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Play className="h-6 w-6 text-emerald-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Visual Learning</h3>
                <p className="text-gray-600">
                  Complex concepts broken down into easy-to-follow visual explanations
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardContent className="pt-6">
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <AlertCircle className="h-6 w-6 text-purple-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Step-by-Step</h3>
                <p className="text-gray-600">
                  Every solution broken down into clear, manageable steps you can follow
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    </div>
  );
}