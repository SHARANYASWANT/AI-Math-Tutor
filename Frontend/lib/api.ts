// Simulated API functions for backend integration

interface VideoResult {
  videoUrl: string;
  transcript: string;
  title: string;
}

export async function generateVideoExplanation(query: string): Promise<VideoResult> {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 5000));
  
  // Simulate video generation response
  const mockTranscript = `
Welcome to your personalized math explanation for: "${query}"

In this video, we'll break down this concept step by step to ensure you understand every part of the process.

First, let's establish the foundational concepts you'll need to understand. We'll start with the basic definitions and principles that apply to this mathematical concept.

Next, we'll walk through a simple example to demonstrate how these principles work in practice. This will help you see the pattern and logic behind the mathematical operations.

Then, we'll tackle a more complex example that builds on what we've learned. This will show you how to apply the same principles to more challenging problems.

Throughout this explanation, we'll highlight common mistakes that students make and show you how to avoid them. We'll also provide tips and tricks that can help you solve similar problems more efficiently.

Finally, we'll wrap up with a summary of the key points and provide you with practice problems you can work on to reinforce your understanding.

Remember, mathematics is all about practice and understanding the underlying patterns. Don't worry if it doesn't click immediately - keep practicing and you'll master this concept!
  `.trim();

  return {
    videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
    transcript: mockTranscript,
    title: `Step-by-Step: ${query}`
  };
}

export async function authenticateUser(email: string, password: string): Promise<{ success: boolean; token?: string; error?: string }> {
  // Simulate authentication API call
  await new Promise(resolve => setTimeout(resolve, 1500));
  
  // Mock authentication logic
  if (email === 'demo@mathvid.com' && password === 'password123') {
    return {
      success: true,
      token: 'mock_jwt_token_' + Date.now()
    };
  }
  
  return {
    success: false,
    error: 'Invalid email or password'
  };
}

export async function createUser(name: string, email: string, password: string): Promise<{ success: boolean; token?: string; error?: string }> {
  // Simulate user creation API call
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  // Mock user creation (always succeeds for demo)
  return {
    success: true,
    token: 'mock_jwt_token_' + Date.now()
  };
}