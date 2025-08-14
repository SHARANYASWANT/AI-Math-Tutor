import os
from gtts import gTTS
from pydub import AudioSegment

def generate_audio_from_transcript(transcript: str, output_path: str = "output_audio.mp3", speed: float = 1.2):
    if not transcript.strip():
        raise ValueError("Transcript is empty, cannot generate audio.")

    temp_path = "temp_audio.mp3"

    # Generate TTS
    tts = gTTS(text=transcript, lang='en', slow=False)
    tts.save(temp_path)

    # Adjust speed using pydub
    audio = AudioSegment.from_file(temp_path)
    faster_audio = audio.speedup(playback_speed=speed)
    # Export final audio
    faster_audio.export(output_path, format="mp3")

    # Remove temp file
    os.remove(temp_path)

    return output_path