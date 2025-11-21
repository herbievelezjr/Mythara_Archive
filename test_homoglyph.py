#!/usr/bin/env python3
"""Test homoglyph normalization"""
import unicodedata

def normalize_unicode(s: str) -> str:
    homoglyph_map = {
        'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O', 'Р': 'P', 'С': 'C', 'Т': 'T', 'Х': 'X',
        'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x',
        'Α': 'A', 'Β': 'B', 'Ε': 'E', 'Ζ': 'Z', 'Η': 'H', 'Ι': 'I', 'Κ': 'K', 'Μ': 'M', 'Ν': 'N', 'Ο': 'O', 'Ρ': 'P', 'Τ': 'T', 'Υ': 'Y', 'Χ': 'X',
        'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'ζ': 'z', 'η': 'h', 'θ': 'th', 'ι': 'i', 'κ': 'k', 'λ': 'l', 'μ': 'm', 'ν': 'n', 'ξ': 'x', 'ο': 'o', 'π': 'p', 'ρ': 'r', 'σ': 's', 'ς': 's', 'τ': 't', 'υ': 'y', 'φ': 'f', 'χ': 'ch', 'ψ': 'ps', 'ω': 'o'
    }
    
    for homoglyph, ascii_char in homoglyph_map.items():
        s = s.replace(homoglyph, ascii_char)
    
    nfd = unicodedata.normalize('NFD', s)
    ascii_text = ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')
    return ascii_text.lower()

# Test the problematic case
text = "We collect data from children without parental consent".replace('o', chr(0x03BF), 1)
print(f"Original text: {text}")
for i, char in enumerate(text):
    if ord(char) > 127:
        print(f"Position {i}: '{char}' = U+{ord(char):04X}")
normalized = normalize_unicode(text)
print(f"Normalized: {normalized}")
print(f"Contains 'collect data from children': {'collect data from children' in normalized}")
