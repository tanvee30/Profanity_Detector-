"""
Profanity Detection and Censoring Module
Detects TRULY abusive/offensive words (not mild words like damn/hell)
"""

import re
from typing import List, Tuple, Set

class ProfanityDetector:
    def __init__(self, custom_words: List[str] = None):
        """
        Initialize the profanity detector with STRICT offensive words only
        
        Args:
            custom_words: Additional words to consider as profanity
        """
        # STRICT list - only truly offensive/abusive words
        self.offensive_words = {
            'fuck', 'fucking', 'fucked', 'fucker', 'motherfucker',
            'shit', 'bullshit', 'shitty',
            'bitch', 'bitches', 'bitching',
            'asshole', 'bastard',
            'dick', 'dickhead', 'cock',
            'pussy', 'cunt',
            'whore', 'slut',
            'nigger', 'nigga',  # Racial slurs
            'fag', 'faggot',    # Homophobic slurs
        }
        
        # Add custom words if provided
        if custom_words:
            self.offensive_words.update(word.lower() for word in custom_words)
        
        # Patterns for variations and misspellings
        self.patterns = [
            r'\bf+u+c+k+\w*\b',      # fuck, fuuuck, etc.
            r'\bs+h+i+t+\w*\b',      # shit, shiit, etc.
            r'\bb+i+t+c+h+\w*\b',    # bitch, biitch, etc.
            r'\ba+s+s+h+o+l+e+\b',   # asshole variations
        ]
    
    def detect_profanity(self, text: str) -> Tuple[bool, List[str]]:
        """
        Detect if text contains TRULY offensive profanity
        
        Args:
            text: Input text to check
            
        Returns:
            Tuple of (has_profanity: bool, detected_words: List[str])
        """
        detected_words = set()
        text_lower = text.lower()
        
        # Check for exact word matches (with word boundaries)
        words = re.findall(r'\b\w+\b', text_lower)
        for word in words:
            if word in self.offensive_words:
                detected_words.add(word)
        
        # Check patterns for variations
        for pattern in self.patterns:
            matches = re.findall(pattern, text_lower)
            detected_words.update(matches)
        
        has_profanity = len(detected_words) > 0
        return has_profanity, list(detected_words)
    
    def censor_text(self, text: str, censor_char: str = '*') -> str:
        """
        Censor offensive words in text with asterisks
        
        Args:
            text: Input text to censor
            censor_char: Character to use for censoring (default: *)
            
        Returns:
            Censored text
        """
        censored = text
        
        # Censor exact matches
        words = re.findall(r'\b\w+\b', text.lower())
        for word in words:
            if word in self.offensive_words:
                # Use word boundaries to replace whole words only
                pattern = r'\b' + re.escape(word) + r'\b'
                replacement = censor_char * len(word)
                censored = re.sub(pattern, replacement, censored, flags=re.IGNORECASE)
        
        # Censor pattern matches
        for pattern in self.patterns:
            def replace_match(match):
                return censor_char * len(match.group(0))
            censored = re.sub(pattern, replace_match, censored, flags=re.IGNORECASE)
        
        return censored
    
    def analyze_text(self, text: str) -> dict:
        """
        Complete analysis of text for profanity
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with analysis results
        """
        has_profanity, detected_words = self.detect_profanity(text)
        censored_text = self.censor_text(text) if has_profanity else text
        
        return {
            'original_text': text,
            'censored_text': censored_text,
            'has_profanity': has_profanity,
            'detected_words': detected_words,
            'profanity_count': len(detected_words)
        }


if __name__ == "__main__":
    # Test the detector
    detector = ProfanityDetector()
    
    test_texts = [
        "This is a normal sentence.",
        "Hello, how are you?",
        "What the hell are you doing?",  # Should be CLEAN now
        "This is damn good!",             # Should be CLEAN now
        "This fucking code is awesome!",  # Should detect
        "You're such a bitch!",           # Should detect
        "Stop being an asshole.",         # Should detect
        "This shit is broken.",           # Should detect
    ]
    
    print("=" * 60)
    print("PROFANITY DETECTION TEST - OPTIMIZED")
    print("=" * 60)
    
    for text in test_texts:
        result = detector.analyze_text(text)
        print(f"\nOriginal: {result['original_text']}")
        
        if result['has_profanity']:
            print(f"Status: ⚠️  OFFENSIVE")
            print(f"Censored: {result['censored_text']}")
            print(f"Detected: {', '.join(result['detected_words'])}")
        else:
            print(f"Status: ✓ CLEAN")
        print("-" * 60)