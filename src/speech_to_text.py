"""
Speech-to-Text Module
Converts audio files to text using OpenAI Whisper
"""

import os
import whisper
import warnings
warnings.filterwarnings("ignore")

class SpeechToText:
    def __init__(self, model_size: str = "base"):
        """
        Initialize Speech-to-Text converter
        
        Args:
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
                       'base' is recommended for speed/accuracy balance
        """
        print(f"Loading Whisper model '{model_size}'...")
        self.model = whisper.load_model(model_size)
        print("Model loaded successfully!")
    
    def transcribe_audio(self, audio_path: str, language: str = "en") -> dict:
        """
        Convert audio file to text
        
        Args:
            audio_path: Path to audio file (mp3, wav, m4a, etc.)
            language: Language code (default: 'en' for English)
            
        Returns:
            Dictionary with transcription results
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"Transcribing audio: {audio_path}")
        
        # Transcribe
        result = self.model.transcribe(
            audio_path,
            language=language,
            fp16=False  # Use FP32 for CPU compatibility
        )
        
        return {
            'text': result['text'].strip(),
            'language': result['language'],
            'segments': result['segments']
        }
    
    def transcribe_with_timestamps(self, audio_path: str) -> list:
        """
        Transcribe audio with word-level timestamps
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            List of segments with timestamps
        """
        result = self.transcribe_audio(audio_path)
        
        segments = []
        for segment in result['segments']:
            segments.append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text'].strip()
            })
        
        return segments


if __name__ == "__main__":
    # Test the speech-to-text converter
    print("=" * 60)
    print("SPEECH-TO-TEXT TEST")
    print("=" * 60)
    
    stt = SpeechToText(model_size="base")
    
    # You'll need to provide a test audio file
    print("\nTo test, provide an audio file path:")
    print("Example: test_audio.wav")
    print("\nThis module is ready to use in the main pipeline!")