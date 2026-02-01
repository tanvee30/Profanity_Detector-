"""
Profanity Detector Demo
Main script to demonstrate speech-to-text + profanity detection
"""

import os
import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from profanity_detector import ProfanityDetector
from speech_to_text import SpeechToText


def process_audio_file(audio_path: str, detector: ProfanityDetector, stt: SpeechToText):
    """Process an audio file for profanity detection"""
    print("\n" + "=" * 70)
    print("🎤 PROCESSING AUDIO FILE")
    print("=" * 70)
    
    # Convert speech to text
    print(f"\n📁 Audio file: {audio_path}")
    result = stt.transcribe_audio(audio_path)
    
    print(f"\n📝 Transcribed text:")
    print(f"   '{result['text']}'")
    print(f"   Language: {result['language']}")
    
    # Analyze for profanity
    analysis = detector.analyze_text(result['text'])
    
    print(f"\n🔍 Profanity Analysis:")
    print(f"   Contains profanity: {'YES ⚠️' if analysis['has_profanity'] else 'NO ✓'}")
    
    if analysis['has_profanity']:
        print(f"   Detected words: {', '.join(analysis['detected_words'])}")
        print(f"\n✏️ Censored text:")
        print(f"   '{analysis['censored_text']}'")
    
    print("\n" + "=" * 70)
    
    return analysis


def process_text_directly(text: str, detector: ProfanityDetector):
    """Process text directly for profanity detection"""
    print("\n" + "=" * 70)
    print("📝 PROCESSING TEXT")
    print("=" * 70)
    
    print(f"\nOriginal text:")
    print(f"   '{text}'")
    
    analysis = detector.analyze_text(text)
    
    print(f"\n🔍 Profanity Analysis:")
    print(f"   Contains profanity: {'YES ⚠️' if analysis['has_profanity'] else 'NO ✓'}")
    
    if analysis['has_profanity']:
        print(f"   Detected words: {', '.join(analysis['detected_words'])}")
        print(f"   Total count: {analysis['profanity_count']}")
        print(f"\n✏️ Censored text:")
        print(f"   '{analysis['censored_text']}'")
    
    print("\n" + "=" * 70)
    
    return analysis


def run_demo_tests(detector: ProfanityDetector):
    """Run demo tests with sample texts"""
    print("\n" + "=" * 70)
    print("🧪 RUNNING DEMO TESTS")
    print("=" * 70)
    
    test_cases = [
        "Hello, this is a clean sentence!",
        "This is damn impressive work!",
        "What the hell is going on here?",
        "This fucking code is so cool!",
        "You absolute genius, this rocks!",
        "Stop being such a bitch about it.",
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n--- Test {i} ---")
        print(f"Input: '{text}'")
        
        analysis = detector.analyze_text(text)
        
        if analysis['has_profanity']:
            print(f"⚠️  PROFANITY DETECTED")
            print(f"Words: {', '.join(analysis['detected_words'])}")
            print(f"Censored: '{analysis['censored_text']}'")
        else:
            print(f"✓ Clean text")
    
    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Profanity Detection System with Speech-to-Text"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["audio", "text", "demo"],
        default="demo",
        help="Mode to run: audio (process audio file), text (process text), demo (run tests)"
    )
    parser.add_argument(
        "--audio",
        type=str,
        help="Path to audio file (required for audio mode)"
    )
    parser.add_argument(
        "--text",
        type=str,
        help="Text to analyze (required for text mode)"
    )
    parser.add_argument(
        "--custom-words",
        type=str,
        nargs="+",
        help="Additional words to consider as profanity"
    )
    
    args = parser.parse_args()
    
    # Initialize profanity detector
    print("🚀 Initializing Profanity Detector...")
    detector = ProfanityDetector(custom_words=args.custom_words)
    print("✓ Detector ready!\n")
    
    # Run based on mode
    if args.mode == "demo":
        run_demo_tests(detector)
    
    elif args.mode == "text":
        if not args.text:
            print("❌ Error: --text argument required for text mode")
            print("Example: python demo.py --mode text --text 'your text here'")
            sys.exit(1)
        process_text_directly(args.text, detector)
    
    elif args.mode == "audio":
        if not args.audio:
            print("❌ Error: --audio argument required for audio mode")
            print("Example: python demo.py --mode audio --audio audio.wav")
            sys.exit(1)
        
        if not os.path.exists(args.audio):
            print(f"❌ Error: Audio file not found: {args.audio}")
            sys.exit(1)
        
        print("🎤 Initializing Speech-to-Text...")
        stt = SpeechToText(model_size="base")
        print("✓ Speech-to-Text ready!\n")
        
        process_audio_file(args.audio, detector, stt)


if __name__ == "__main__":
    main()