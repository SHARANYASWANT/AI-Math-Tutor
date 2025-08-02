'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Calculator, Triangle, FunctionSquare as Function, Circle, TrendingUp, Play } from 'lucide-react';

interface Video {
  id: string;
  title: string;
  thumbnail: string;
  videoUrl: string;
  description: string;
  duration: string;
}

const videoGallery = {
  Algebra: [
    {
      id: 'alg1',
      title: 'Quadratic Formula Explained',
      thumbnail: 'https://images.pexels.com/photos/3729557/pexels-photo-3729557.jpeg?auto=compress&cs=tinysrgb&w=400',
      videoUrl: '#',
      description: 'Learn how to solve quadratic equations using the quadratic formula with step-by-step examples.',
      duration: '8:45'
    },
    {
      id: 'alg2',
      title: 'Factoring Polynomials',
      thumbnail: 'https://images.pexels.com/photos/6256065/pexels-photo-6256065.jpeg?auto=compress&cs=tinysrgb&w=400',
      videoUrl: '#',
      description: 'Master polynomial factoring techniques including common factors and special cases.',
      duration: '12:30'
    },
    {
      id: 'alg3',
      title: 'Systems of Linear Equations',
      thumbnail: 'https://images.pexels.com/photos/3729557/pexels-photo-3729557.jpeg?auto=compress&cs=tinysrgb&w=400',
      videoUrl: '#',
      description: 'Solve systems using substitution, elimination, and graphing methods.',
      duration: '15:20'
    }
  ],
  Geometry: [
    {
      id: 'geo1',
      title: 'Pythagorean Theorem',
      thumbnail: 'https://images.pexels.com/photos/6256065/pexels-photo-6256065.jpeg?auto=compress&cs=tinysrgb&w=400',
      videoUrl: '#',
      description: 'Understand and apply the Pythagorean theorem in various geometric problems.',
      duration: '10:15'
    },
    {
      id: 'geo2',
      title: 'Circle Area and Circumference',
      thumbnail: 'https://images.pexels.com/photos/3729557/pexels-photo-3729557.jpeg?auto=compress&cs=tinysrgb&w=400',
      videoUrl: '#',
      description: 'Calculate area and circumference of circles with practical examples.',
      duration: '7:30'
    },
    {
      id: 'geo3',
      title: 'Triangle Properties',
      thumbnail: 'https://images.pexels.com/photos/6256065/pexels-photo-6256065.jpeg?auto=compress&cs=tinysrgb&w=400',
      videoUrl: '#',
      description: 'Explore different types of triangles and their unique properties.',
      duration: '11:45'
    }
  ],
  Trigonometry: [
    {
      id: 'trig1',
      title: 'Unit Circle Basics',
      thumbnail: 'https://images.pexels.com/photos/3729557/pexels-photo-3729557.jpeg?auto=compress&cs=tinysrgb&w=400',
      videoUrl: '#',
      description: 'Master the unit circle and understand trigonometric ratios.',
      duration: '14:20'
    },
    {
      id: 'trig2',
      title: 'Sine and Cosine Graphs',
      thumbnail: 'https://images.pexels.com/photos/6256065/pexels-photo-6256065.jpeg?auto=compress&cs=tinysrgb&w=400',
      videoUrl: '#',
      description: 'Visualize and understand sine and cosine function graphs.',
      duration: '9:55'
    }
  ],
  'Venn Diagrams & Set Theory': [
    {
      id: 'set1',
      title: 'Set Operations',
      thumbnail: 'https://images.pexels.com/photos/3729557/pexels-photo-3729557.jpeg?auto=compress&cs=tinysrgb&w=400',
      videoUrl: '#',
      description: 'Learn union, intersection, and complement operations with Venn diagrams.',
      duration: '8:10'
    },
    {
      id: 'set2',
      title: 'Probability with Sets',
      thumbnail: 'https://images.pexels.com/photos/6256065/pexels-photo-6256065.jpeg?auto=compress&cs=tinysrgb&w=400',
      videoUrl: '#',
      description: 'Apply set theory concepts to solve probability problems.',
      duration: '12:40'
    }
  ],
  Calculus: [
    {
      id: 'calc1',
      title: 'Limits and Continuity',
      thumbnail: 'https://images.pexels.com/photos/3729557/pexels-photo-3729557.jpeg?auto=compress&cs=tinysrgb&w=400',
      videoUrl: '#',
      description: 'Understand the fundamental concepts of limits in calculus.',
      duration: '16:25'
    },
    {
      id: 'calc2',
      title: 'Basic Derivatives',
      thumbnail: 'https://images.pexels.com/photos/6256065/pexels-photo-6256065.jpeg?auto=compress&cs=tinysrgb&w=400',
      videoUrl: '#',
      description: 'Learn to find derivatives using the power rule and basic techniques.',
      duration: '13:15'
    },
    {
      id: 'calc3',
      title: 'Integration Basics',
      thumbnail: 'https://images.pexels.com/photos/3729557/pexels-photo-3729557.jpeg?auto=compress&cs=tinysrgb&w=400',
      videoUrl: '#',
      description: 'Introduction to integration and fundamental theorem of calculus.',
      duration: '18:30'
    }
  ]
};

const topicIcons = {
  Algebra: Calculator,
  Geometry: Triangle,
  Trigonometry: Function,
  'Venn Diagrams & Set Theory': Circle,
  Calculus: TrendingUp
};

export default function GalleryPage() {
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 pt-20 pb-16">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Video Gallery
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Explore our comprehensive collection of mathematical concept explanations, 
            organized by topic for easy learning.
          </p>
        </div>

        {/* Video Gallery by Topic */}
        <div className="space-y-12">
          {Object.entries(videoGallery).map(([topic, videos]) => {
            const IconComponent = topicIcons[topic as keyof typeof topicIcons];
            
            return (
              <section key={topic} className="animate-fade-in">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <IconComponent className="h-5 w-5 text-blue-600" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900">{topic}</h2>
                </div>
                
                <div className="relative">
                  <ScrollArea className="w-full">
                    <div className="flex gap-6 pb-4 scrollbar-hide">
                      <div className="flex gap-6 min-w-max">
                        {videos.map((video) => (
                          <Card 
                            key={video.id} 
                            className="w-80 flex-shrink-0 cursor-pointer hover:shadow-xl transition-all duration-300 transform hover:scale-[1.02] border-0 bg-white"
                            onClick={() => setSelectedVideo(video)}
                          >
                            <div className="relative">
                              <img
                                src={video.thumbnail}
                                alt={video.title}
                                className="w-full h-48 object-cover rounded-t-lg"
                              />
                              <div className="absolute inset-0 bg-black/20 rounded-t-lg flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
                                <div className="w-12 h-12 bg-white/90 rounded-full flex items-center justify-center">
                                  <Play className="h-6 w-6 text-blue-600 ml-1" />
                                </div>
                              </div>
                              <div className="absolute bottom-2 right-2 bg-black/80 text-white text-xs px-2 py-1 rounded">
                                {video.duration}
                              </div>
                            </div>
                            <CardContent className="p-4">
                              <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">
                                {video.title}
                              </h3>
                              <p className="text-sm text-gray-600 line-clamp-3">
                                {video.description}
                              </p>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    </div>
                  </ScrollArea>
                </div>
              </section>
            );
          })}
        </div>
      </div>

      {/* Video Modal */}
      <Dialog open={!!selectedVideo} onOpenChange={() => setSelectedVideo(null)}>
        <DialogContent className="max-w-4xl max-h-[90vh]">
          {selectedVideo && (
            <>
              <DialogHeader>
                <DialogTitle className="text-xl">{selectedVideo.title}</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div className="video-container bg-black rounded-lg overflow-hidden">
                  <video
                    controls
                    className="w-full h-full"
                    poster={selectedVideo.thumbnail}
                  >
                    <source src={selectedVideo.videoUrl} type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <span>Duration: {selectedVideo.duration}</span>
                  </div>
                  <p className="text-gray-700">{selectedVideo.description}</p>
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}