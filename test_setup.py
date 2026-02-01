# Test if all libraries are installed correctly
import sys

def test_imports():
    try:
        import speech_recognition as sr
        print("✓ SpeechRecognition installed")
    except ImportError as e:
        print(f"✗ SpeechRecognition not installed: {e}")
    
    try:
        import torch
        print(f"✓ PyTorch installed (version {torch.__version__})")
    except ImportError:
        print("✗ PyTorch not installed")
    
    try:
        import transformers
        print("✓ Transformers installed")
    except ImportError:
        print("✗ Transformers not installed")
    
    try:
        import sklearn
        print("✓ Scikit-learn installed")
    except ImportError:
        print("✗ Scikit-learn not installed")
    
    try:
        import pandas
        print("✓ Pandas installed")
    except ImportError:
        print("✗ Pandas not installed")
    
    try:
        from better_profanity import profanity
        print("✓ Better-profanity installed")
    except ImportError:
        print("✗ Better-profanity not installed")
    
    print("\n✓ Setup complete!")

if __name__ == "__main__":
    test_imports()