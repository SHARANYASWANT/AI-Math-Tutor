import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export default api;

export async function generateVideoExplanation(prompt: string) {
  try {
    const response = await api.post('/generate-video', { prompt });

    return {
      videoUrl: response.data.videoUrl,
      transcript: response.data.transcript || '',
      title: response.data.title || 'Generated Video',
    };
  } catch (error) {
    console.error('Error generating video explanation:', error);
    throw error;
  }
}
