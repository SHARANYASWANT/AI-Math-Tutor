'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Calculator, Triangle, FunctionSquare as Function, Circle, TrendingUp } from 'lucide-react';

interface PopularConceptsProps {
  onConceptSelect: (concept: string) => void;
}

const concepts = [
  {
    icon: Calculator,
    title: 'Algebra',
    description: 'Linear equations, quadratic formulas, and polynomial operations',
    examples: [
      'Solve quadratic equations',
      'Factor polynomials step by step',
      'Systems of linear equations'
    ]
  },
  {
    icon: Triangle,
    title: 'Geometry',
    description: 'Shapes, angles, area, perimeter, and geometric proofs',
    examples: [
      'Calculate area and perimeter of triangles',
      'Pythagorean theorem applications',
      'Circle geometry and arc length'
    ]
  },
  {
    icon: Function,
    title: 'Trigonometry',
    description: 'Sine, cosine, tangent, and trigonometric identities',
    examples: [
      'Unit circle and trigonometric ratios',
      'Solving trigonometric equations',
      'Law of sines and cosines'
    ]
  },
  {
    icon: Circle,
    title: 'Venn Diagrams & Set Theory',
    description: 'Set operations, unions, intersections, and probability',
    examples: [
      'Set operations with Venn diagrams',
      'Probability using set theory',
      'De Morgan\'s laws explained'
    ]
  },
  {
    icon: TrendingUp,
    title: 'Calculus',
    description: 'Derivatives, integrals, limits, and applications',
    examples: [
      'Find derivatives using the power rule',
      'Calculate definite and indefinite integrals',
      'Limits and continuity concepts'
    ]
  }
];

export function PopularConcepts({ onConceptSelect }: PopularConceptsProps) {
  return (
    <div>
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Popular Math Concepts</h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Explore our most requested mathematical topics. Click on any example to get started.
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {concepts.map((concept, index) => {
          const IconComponent = concept.icon;
          return (
            <Card key={index} className="border-0 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-[1.02] bg-white">
              <CardHeader className="text-center">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <IconComponent className="h-6 w-6 text-blue-600" />
                </div>
                <CardTitle className="text-xl text-gray-900">{concept.title}</CardTitle>
                <p className="text-sm text-gray-600">{concept.description}</p>
              </CardHeader>
              <CardContent className="space-y-2">
                {concept.examples.map((example, exampleIndex) => (
                  <Button
                    key={exampleIndex}
                    variant="ghost"
                    className="w-full justify-start text-left text-sm h-auto p-3 hover:bg-blue-50 hover:text-blue-700 transition-colors"
                    onClick={() => onConceptSelect(example)}
                  >
                    {example}
                  </Button>
                ))}
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}