'use client';

import { useState } from 'react';
import { VideoPlayer } from '@/components/VideoPlayer';
import { PopularConcepts } from '@/components/PopularConcepts';
import { generateVideoExplanation } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertCircle } from 'lucide-react';

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

  /** Generate video explanation (called for both initial & regenerate) */
  const fetchVideo = async (customQuery?: string) => {
    const finalQuery = customQuery ?? query;

    if (!finalQuery.trim()) {
      setError('Please enter a mathematical concept or question.');
      return;
    }

    setError('');
    setIsLoading(true);

    try {
      const result = await generateVideoExplanation(finalQuery);
      setVideoResult(result);
    } catch {
      setError('Failed to generate video explanation. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  /** Handle form submit (initial generation) */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetchVideo();
  };

  /** Handle regenerate using same query */
  const handleRegenerate = async () => {
    await fetchVideo();
  };

  /** Reset state for new query */
  const handleNewQuery = () => {
    setQuery('');
    setVideoResult(null);
    setError('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Input Section */}
      <section className="pt-20 pb-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Transform Math Into
            <span className="text-blue-600 block">Visual Learning</span>
          </h1>

          <Card className="max-w-2xl mx-auto shadow-xl border-0 bg-white/80 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-2xl text-gray-800">Ask Your Math Question</CardTitle>
              <CardDescription className="text-gray-600">
                Describe the mathematical concept you'd like explained in a video
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <Textarea
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="e.g., Explain the quadratic formula step by step"
                  className="min-h-[120px] text-base"
                  disabled={isLoading}
                />
                {error && (
                  <div className="flex items-center gap-2 text-red-600 text-sm mt-2">
                    <AlertCircle className="h-4 w-4" />
                    {error}
                  </div>
                )}
                <Button
                  type="submit"
                  disabled={isLoading || !query.trim()}
                  className="w-full h-12 text-lg font-semibold bg-blue-600 hover:bg-blue-700"
                >
                  {isLoading ? 'Generating Video...' : 'Generate Video Explanation'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Video Section */}
      {videoResult && (
        <section className="py-16 px-4">
          <div className="max-w-6xl mx-auto">
            <VideoPlayer
              videoResult={videoResult}
              onNewQuery={handleNewQuery}
              onRegenerate={handleRegenerate}
              isRegenerating={isLoading}
            />
          </div>
        </section>
      )}

      {/* Popular Concepts */}
      {!videoResult && (
        <section className="py-16 px-4">
          <div className="max-w-6xl mx-auto">
            <PopularConcepts onConceptSelect={(concept) => setQuery(concept)} />
          </div>
        </section>
      )}
    </div>
  );
}
