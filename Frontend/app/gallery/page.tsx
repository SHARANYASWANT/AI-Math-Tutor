'use client';

import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Calculator } from 'lucide-react';

interface Video {
  id: string;
  title: string;
  videoUrl: string;
  description: string;
  duration: string;
}

const videoGallery: Video[] = [
  {
    id: 'vid1',
    title: 'Area Model Expanding Binomials',
    videoUrl: '/AreaModelExpandingBinomials.mp4',
    description: 'Learn how to expand binomials using the area model technique.',
    duration: '5:20'
  },
  {
    id: 'vid2',
    title: 'De Morgan’s Laws',
    videoUrl: '/DeMorgansLaws.mp4',
    description: 'Understand De Morgan’s Laws with visual proofs and examples.',
    duration: '6:45'
  },
  {
    id: 'vid3',
    title: 'Difference and Complement',
    videoUrl: '/DifferenceAndComplement.mp4',
    description: 'Explore set theory concepts of difference and complement visually.',
    duration: '4:15'
  },
  {
    id: 'vid4',
    title: 'Linear Function Interpretation',
    videoUrl: '/LinearFunctionInterpretation.mp4',
    description: 'Interpret linear functions with graphical and algebraic examples.',
    duration: '7:10'
  },
  {
    id: 'vid5',
    title: 'Pet Ownership Venn Diagram',
    videoUrl: '/PetOwnershipVennDiagram.mp4',
    description: 'Analyze pet ownership data using Venn diagrams.',
    duration: '5:00'
  },
  {
    id: 'vid6',
    title: 'Pythagorean Theorem',
    videoUrl: '/PythagoreanTheorem.mp4',
    description: 'Understand and prove the Pythagorean Theorem with visuals.',
    duration: '8:30'
  },
  {
    id: 'vid7',
    title: 'Quadratic Factoring',
    videoUrl: '/QuadraticFactoring.mp4',
    description: 'Learn different methods to factor quadratic expressions.',
    duration: '9:15'
  },
  {
    id: 'vid8',
    title: 'Quadratic Formula Derivation',
    videoUrl: '/QuadraticFormulaDerivation.mp4',
    description: 'Derive the quadratic formula step-by-step with clear explanation.',
    duration: '10:00'
  },
  {
    id: 'vid9',
    title: 'Regular Polygon Morph',
    videoUrl: '/RegularPolygonMorph.mp4',
    description: 'Watch regular polygons morph dynamically to understand properties.',
    duration: '3:45'
  },
  {
    id: 'vid10',
    title: 'Systems of Equations',
    videoUrl: '/SystemsOfEquations.mp4',
    description: 'Solve systems of equations using substitution and elimination methods.',
    duration: '11:20'
  },
  {
    id: 'vid11',
    title: 'Thales Theorem',
    videoUrl: '/Thales.mp4',
    description: 'Visualize Thales theorem and its geometric applications.',
    duration: '6:55'
  },
  {
    id: 'vid12',
    title: 'Union and Intersection',
    videoUrl: '/UnionAndIntersection.mp4',
    description: 'Learn about union and intersection in set theory with visuals.',
    duration: '5:40'
  },
  {
    id: 'vid13',
    title: 'Venn Formula Derivation',
    videoUrl: '/VennFormulaDerivation.mp4',
    description: 'Derive the formula for Venn diagrams using step-by-step explanation.',
    duration: '4:50'
  },
  {
    id: 'vid14',
    title: 'WhatsApp Video',
    videoUrl: '/WhatsApp Video 2025-08-04 at 15.11.04_641ac7a4.mp4',
    description: 'Miscellaneous educational video content.',
    duration: '2:30'
  }
];


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

        {/* Single Topic (Algebra) */}
        <section className="animate-fade-in">
         

          {/* Videos Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {videoGallery.map((video) => (
              <Card
                key={video.id}
                className="w-full cursor-pointer hover:shadow-xl transition-all duration-300 transform hover:scale-[1.02] border-0 bg-white"
                onClick={() => setSelectedVideo(video)}
              >
                <div className="relative">
                  <video
                    src={video.videoUrl}
                    controls
                    className="w-full h-48 object-cover rounded-t-lg"
                  />
                  
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
        </section>
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
                    src={selectedVideo.videoUrl}
                  >
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
