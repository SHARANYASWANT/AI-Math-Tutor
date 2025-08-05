'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { RotateCcw, Plus, Volume2, VolumeX } from 'lucide-react';

interface VideoResult {
  videoUrl: string;
  transcript: string;
  title: string;
}

interface VideoPlayerProps {
  videoResult: VideoResult;
  onNewQuery: () => void;
  onRegenerate: () => void;
  isRegenerating: boolean;
}

export function VideoPlayer({
  videoResult,
  onNewQuery,
  onRegenerate,
  isRegenerating,
}: VideoPlayerProps) {
  const [isMuted, setIsMuted] = useState(false);

  return (
    <div className="animate-fade-in">
      <Card className="shadow-2xl border-0 bg-white/95 backdrop-blur-sm">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl text-gray-900">{videoResult.title}</CardTitle>
          <div className="flex justify-center gap-4 mt-4">
            {/* Regenerate button */}
            <Button
              onClick={onRegenerate}
              disabled={isRegenerating}
              variant="outline"
              className="flex items-center gap-2"
            >
              {isRegenerating ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                  Regenerating...
                </>
              ) : (
                <>
                  <RotateCcw className="h-4 w-4" />
                  Regenerate Video
                </>
              )}
            </Button>

            {/* New Query button */}
            <Button
              onClick={onNewQuery}
              className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700"
            >
              <Plus className="h-4 w-4" />
              New Query
            </Button>
          </div>
        </CardHeader>

        <CardContent>
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Video Section */}
            <div className="lg:col-span-2">
              <div className="video-container bg-black rounded-xl overflow-hidden shadow-lg">
                <video
                  controls
                  muted={isMuted}
                  className="w-full h-full object-cover"
                  
                >
                  <source src={videoResult.videoUrl} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
              </div>

              {/* Video Controls */}
              <div className="flex items-center justify-between mt-4 p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => setIsMuted(!isMuted)}
                    className="flex items-center gap-2"
                  >
                    {isMuted ? <VolumeX className="h-4 w-4" /> : <Volume2 className="h-4 w-4" />}
                    {isMuted ? 'Unmute' : 'Mute'}
                  </Button>
                </div>
                <div className="text-sm text-gray-500">Generated with AI</div>
              </div>
            </div>

            {/* Transcript Section */}
            <div className="lg:col-span-1">
              <Tabs defaultValue="transcript" className="w-full">
                <TabsList className="grid w-full grid-cols-1">
                  <TabsTrigger value="transcript">Transcript</TabsTrigger>
                </TabsList>
                <TabsContent value="transcript" className="mt-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Video Transcript</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ScrollArea className="h-80">
                        <div className="text-sm text-gray-700 leading-relaxed space-y-3">
                          {videoResult.transcript
                            ? videoResult.transcript.split('\n').map((paragraph, index) => (
                                <p key={index} className="text-justify">
                                  {paragraph}
                                </p>
                              ))
                            : 'No transcript available.'}
                        </div>
                      </ScrollArea>
                    </CardContent>
                  </Card>
                </TabsContent>
              </Tabs>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
