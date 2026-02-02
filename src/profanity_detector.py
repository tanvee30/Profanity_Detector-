"""
IMPROVED Profanity Detection - Simple but Effective
Catches ALL variations: leetspeak, spacing, symbols, etc.
"""

import re
from typing import List, Tuple, Dict

class ProfanityDetector:
    def __init__(self, custom_words: List[str] = None, sensitivity: str = "moderate"):
        """
        Initialize profanity detector
        
        Args:
            custom_words: Additional words to consider as profanity
            sensitivity: 'low', 'moderate', 'high'
        """
        self.sensitivity = sensitivity
        
        # Severity-based word lists
        # self.severe_words = {
        #     'fuck', 'fucking', 'fucked', 'fucker', 'motherfucker',
        #     'cunt', 'pussy', 'cock', 'dick', 'dickhead',
        #     'nigger', 'nigga', 'fag', 'faggot', 'retard',
        #     'whore', 'slut',
        # }
        
        # self.moderate_words = {
        #     'shit', 'shitty', 'bullshit',
        #     'bitch', 'bitches', 'bitching',
        #     'ass', 'asshole', 'asses',
        #     'bastard', 'piss',
        # }
        
        # self.mild_words = {
        #     'damn', 'dammit', 'hell', 'crap',
        # }
        # Severity-based word lists
        
        # SEVERE - Highly offensive words
        self.severe_words = {
            # English - Sexual/Explicit
            'fuck', 'fucking', 'fucked', 'fucker', 'motherfucker', 'fucks',
            'cunt', 'cunts', 'pussy', 'pussies',
            'cock', 'cocks', 'dick', 'dicks', 'dickhead',
            'penis', 'vagina', 'boobs', 'tits',
            
            # English - Racial slurs
            'nigger', 'nigga', 'negro', 'chink', 'gook', 'wetback',
            
            # English - Homophobic slurs
            'fag', 'faggot', 'faggots', 'dyke',
            
            # English - Ableist slurs
            'retard', 'retarded', 'retards',
            
            # English - Misogynistic
            'whore', 'whores', 'slut', 'sluts',
            
            # Hindi/Hinglish (Roman script) - SEVERE
            'chutiya', 'chutiye', 'chutiyapa',  # Idiot/moron (vulgar)
            'madarchod', 'mc', 'mkc',            # Motherfucker
            'behenchod', 'bc', 'bkl',            # Sister-fucker
            'bhosdi', 'bhosdk', 'bsdk',          # Vulgar insult
            'lavde', 'lund', 'lauda',            # Penis (vulgar)
            'gaand', 'gand',                     # Ass (vulgar)
            'chod', 'chodna',                    # Fuck
            'harami', 'haramzada',               # Bastard
            'kamina', 'kamine',                  # Scoundrel
            'kutte', 'kutta',                    # Dog (insult)
            'saale', 'sala',                     # Brother-in-law (insult)
            'randi', 'rundi',                    # Prostitute
            'chakka', 'hijra',                   # Transgender slur
            
            # Spanish
            'puta', 'puto', 'pendejo', 'cabron', 'cono', 'verga',
            'pinche', 'chingada', 'chingar', 'joder',
            
            # French  
            'putain', 'merde', 'connard', 'salope',
            
            # German
            'scheiße', 'scheisse', 'arschloch', 'hurensohn',
            
            # Portuguese
            'porra', 'caralho', 'foda', 'puta',
            
            # Arabic (Roman)
            'kuss', 'sharmouta', 'kalb',
            
            # Italian
            'cazzo', 'merda', 'stronzo', 'puttana',
        }
        
        # MODERATE - Offensive but less severe
        self.moderate_words = {
            # English
            'shit', 'shits', 'shitty', 'bullshit', 'shite', 'crap',
            'bitch', 'bitches', 'bitching', 'bitchy',
            'ass', 'asses', 'asshole', 'assholes', 'arse',
            'bastard', 'bastards',
            'piss', 'pissed', 'pissing', 'pisser',
            'wanker', 'tosser', 'twat', 'prick',
            
            # Hindi/Hinglish - MODERATE
            'chup', 'chapri',                    # Shut up / trashy
            'bewakoof', 'bevkoof',               # Stupid
            'pagal', 'paagal',                   # Crazy (mild insult)
            'gadha', 'gadhe',                    # Donkey (fool)
            'ullu', 'ullu ka pattha',           # Owl / son of owl (fool)
            'jhatu', 'jhaatu',                   # Pubic hair (insult)
            'bhadwa', 'bhadwe',                  # Pimp
            'gandu',                             # Asshole
            
            # Other languages - moderate
            'culo', 'mierda', 'idiota',         # Spanish
            'merde', 'con',                      # French
        }
        
        # MILD - Common mild expletives
        self.mild_words = {
            # English
            'damn', 'damned', 'dammit', 'dang',
            'hell', 'hells',
            'crap', 'crappy', 'craps',
            'suck', 'sucks', 'sucked',
            'bloody', 'blimey', 'bollocks',
            
            # Hindi - MILD
            'yaar', 'abe', 'oye',  # These are NOT offensive, just casual
            'pagal',                # Crazy (context-dependent)
        }
        
        # # Character substitution map - includes common obfuscations
        # self.substitutions = {
        #     'a': r'[a@4\*]',
        #     'e': r'[e3€\*]',
        #     'i': r'[i1!|\*]',
        #     'o': r'[o0\*]',
        #     'u': r'[uv4\*]',  # Added 4 for 'u' (F4ck)
        #     's': r'[s$5z\*]',
        #     'c': r'[ck©\*]',
        #     'b': r'[b8\*]',
        #     'f': r'[f\*]',
        #     'g': r'[g9\*]',
        #     't': r'[t7\*]',
        #     'h': r'[h\*]',
        #     'k': r'[k\*]',
        # Character substitution map - includes common obfuscations
        self.substitutions = {
            'a': r'[a@4\*]',
            'e': r'[e3€\*]',
            'i': r'[i1!|\*]',
            'o': r'[o0\*]',
            'u': r'[uv4\*]',
            's': r'[s$5z\*]',
            'c': r'[ck©\*]',
            'b': r'[b8\*]',
            'f': r'[f\*]',
            'g': r'[g9\*]',
            't': r'[t7\*]',
            'h': r'[h\*]',
            'k': r'[k\*]',
            'd': r'[d\*]',
            'n': r'[n\*]',
            'l': r'[l\*]',
            'm': r'[m\*]',
            'p': r'[p\*]',
            'r': r'[r\*]',
            'w': r'[w\*]',
            'y': r'[y\*]',
        }
        
        
        # Set active words based on sensitivity
        if sensitivity == "high":
            self.offensive_words = self.severe_words | self.moderate_words | self.mild_words
        elif sensitivity == "moderate":
            self.offensive_words = self.severe_words | self.moderate_words
        else:
            self.offensive_words = self.severe_words
        
        if custom_words:
            self.offensive_words.update(word.lower() for word in custom_words)
    
    def _create_pattern(self, word: str) -> str:
        """
        Create flexible regex pattern for a word
        Handles: f u c k, f-u-c-k, f.u.c.k, f4ck, fuuuck, @sshole, F**k, etc.
        """
        # Allow @ or other symbols at the start for words starting with 'a'
        if word[0] == 'a':
            pattern = r'[@a4\*]+'
        else:
            pattern = r'\b'
            char = word[0]
            if char in self.substitutions:
                pattern += self.substitutions[char] + r'+'
            else:
                pattern += char + r'+'
        
        pattern += r'[\s\-_\.\*]*'
        
        # Rest of the word
        for char in word[1:].lower():
            if char in self.substitutions:
                pattern += self.substitutions[char] + r'+[\s\-_\.\*]*'
            else:
                pattern += char + r'+[\s\-_\.\*]*'
        
        pattern = pattern.rstrip(r'[\s\-_\.\*]*')
        pattern += r'\b'
        
        return pattern
    
    def _normalize_text(self, text: str) -> str:
        """Remove excessive separators for better matching"""
        # Keep the text but make it easier to match
        normalized = text.lower()
        # Replace multiple spaces/symbols with single space
        normalized = re.sub(r'[\s\-_\.]+', ' ', normalized)
        return normalized
    
    def _get_severity(self, word: str) -> str:
        """Get severity level of detected word"""
        word_lower = word.lower()
        if word_lower in self.severe_words:
            return "severe"
        elif word_lower in self.moderate_words:
            return "moderate"
        elif word_lower in self.mild_words:
            return "mild"
        return "moderate"  # default
    
    def detect_profanity(self, text: str) -> Tuple[bool, List[Dict]]:
        """
        Detect all profanity including obfuscated versions
        
        Returns:
            (has_profanity, list of detected word details)
        """
        detected = []
        seen_words = set()
        
        text_lower = text.lower()
        normalized = self._normalize_text(text)
        
        # Check each offensive word
        for word in self.offensive_words:
            pattern = self._create_pattern(word)
            
            # Search in both original and normalized text
            for search_text in [text_lower, normalized]:
                matches = re.finditer(pattern, search_text, re.IGNORECASE)
                
                for match in matches:
                    if word not in seen_words:
                        detected.append({
                            'word': word,
                            'matched_text': match.group(0).strip(),
                            'severity': self._get_severity(word),
                            'position': match.start()
                        })
                        seen_words.add(word)
                        break  # Move to next word once found
        
        has_profanity = len(detected) > 0
        return has_profanity, detected
    
    def censor_text(self, text: str, censor_char: str = '*', 
                   reveal_first_last: bool = False) -> str:
        """
        Censor profane words including all obfuscated versions
        """
        censored = text
        has_profanity, detected = self.detect_profanity(text)
        
        if not has_profanity:
            return censored
        
        # Sort by word length (longest first to avoid partial replacements)
        detected = sorted(detected, key=lambda x: len(x['word']), reverse=True)
        
        for item in detected:
            word = item['word']
            pattern = self._create_pattern(word)
            
            def replace_func(match):
                matched_text = match.group(0)
                if reveal_first_last and len(matched_text) > 2:
                    return matched_text[0] + (censor_char * (len(matched_text) - 2)) + matched_text[-1]
                else:
                    return censor_char * len(matched_text)
            
            censored = re.sub(pattern, replace_func, censored, flags=re.IGNORECASE)
        
        return censored
    
    def analyze_text(self, text: str, detailed: bool = False) -> dict:
        """
        Complete profanity analysis
        """
        has_profanity, detected = self.detect_profanity(text)
        censored_text = self.censor_text(text) if has_profanity else text
        
        result = {
            'original_text': text,
            'censored_text': censored_text,
            'has_profanity': has_profanity,
            'profanity_count': len(detected),
            'detected_words': [d['word'] for d in detected],
        }
        
        if detailed:
            result['detailed_detection'] = detected
            result['severity_breakdown'] = {
                'severe': len([d for d in detected if d['severity'] == 'severe']),
                'moderate': len([d for d in detected if d['severity'] == 'moderate']),
                'mild': len([d for d in detected if d['severity'] == 'mild']),
            }
        
        return result
    
    def get_statistics(self, text: str) -> dict:
        """Get detailed statistics"""
        has_profanity, detected = self.detect_profanity(text)
        
        total_words = len(text.split())
        profanity_percentage = (len(detected) / total_words * 100) if total_words > 0 else 0
        
        severity_counts = {
            'severe': len([d for d in detected if d['severity'] == 'severe']),
            'moderate': len([d for d in detected if d['severity'] == 'moderate']),
            'mild': len([d for d in detected if d['severity'] == 'mild']),
        }
        
        return {
            'total_words': total_words,
            'profane_words': len(detected),
            'profanity_percentage': round(profanity_percentage, 2),
            'severity_breakdown': severity_counts,
            'is_offensive': has_profanity,
            'risk_level': 'high' if severity_counts['severe'] > 0 else 
                         'medium' if severity_counts['moderate'] > 0 else 'low'
        }


if __name__ == "__main__":
    print("=" * 80)
    print("MULTILINGUAL PROFANITY DETECTOR - TESTING")
    print("=" * 80)
    
    detector = ProfanityDetector(sensitivity="moderate")
    
    test_cases = [
        # English
        ("This fucking code rocks!", True, "English"),
        ("You're an asshole", True, "English"),
        ("Hello how are you?", False, "English"),
        
        # Hindi/Hinglish
        ("Tu chutiya hai", True, "Hindi"),
        ("Abe saale madarchod", True, "Hindi"),
        ("Bhosdi ke stop it", True, "Hindi"),
        ("Kya baat hai yaar", False, "Hindi - casual"),
        ("Tu bahut bewakoof hai", True, "Hindi"),
        ("MC BC yaar", True, "Hindi abbreviations"),
        
        # Spanish
        ("Eres un pendejo", True, "Spanish"),
        ("Que pasa amigo?", False, "Spanish"),
        ("Pinche cabron", True, "Spanish"),
        
        # Mixed/Hinglish
        ("This is chutiyapa bro", True, "Hinglish"),
        ("Sala behenchod fuck off", True, "Mixed"),
        ("Abe yaar what the fuck", True, "Mixed"),
        
        # Edge cases
        ("ch*t!ya", True, "Hindi obfuscated"),
        ("m@d@rch0d", True, "Hindi leetspeak"),
        ("b c spacing", True, "Hindi abbreviation with spacing"),
    ]
    
    passed = 0
    failed = 0
    
    for text, should_detect, language in test_cases:
        result = detector.analyze_text(text, detailed=True)
        
        is_correct = result['has_profanity'] == should_detect
        status_symbol = "✓" if is_correct else "✗"
        
        if is_correct:
            passed += 1
        else:
            failed += 1
        
        print(f"\n{status_symbol} [{language}] '{text}'")
        print(f"   Expected: {'DETECT' if should_detect else 'CLEAN'} | "
              f"Got: {'DETECT' if result['has_profanity'] else 'CLEAN'}")
        
        if result['has_profanity']:
            print(f"   Detected: {', '.join(result['detected_words'])}")
            print(f"   Censored: '{result['censored_text']}'")
    
    print("\n" + "=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)