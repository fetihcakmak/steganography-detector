"""
Chi-Square Analyzer - Statistical analysis to detect structural anomalies
"""
import math
from collections import Counter
from typing import List, Tuple

def calculate_shannon_entropy(data: bytes) -> float:
    """Calculates the Shannon entropy of a byte sequence."""
    if not data:
        return 0.0
    entropy = 0
    length = len(data)
    counts = Counter(data)
    for count in counts.values():
        p_x = count / length
        entropy += - p_x * math.log2(p_x)
    return entropy

def chi_square_test(data: bytes, block_size: int = 1024) -> List[Tuple[int, float]]:
    """
    Performs a Chi-Square test on blocks of data.
    Steganography (especially LSB) tends to make the byte distribution 
    closer to uniform. We compare the distribution against an expected uniform distribution.
    """
    results = []
    expected = block_size / 256.0
    
    # We only test if expected > 0
    if expected == 0:
        return results
        
    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        if len(block) < block_size:
            continue
            
        counts = Counter(block)
        chi_sq = 0.0
        
        for byte_val in range(256):
            observed = counts.get(byte_val, 0)
            chi_sq += ((observed - expected) ** 2) / expected
            
        results.append((i, chi_sq))
        
    return results

def analyze_anomalies(data: bytes) -> Tuple[float, float, bool]:
    """
    Returns (entropy, avg_chi_square, is_suspicious)
    """
    if not data:
        return 0.0, 0.0, False
        
    entropy = calculate_shannon_entropy(data)
    
    chi_results = chi_square_test(data)
    if not chi_results:
        return entropy, 0.0, entropy > 7.9
        
    avg_chi = sum(val for _, val in chi_results) / len(chi_results)
    
    # Lower chi-square means closer to uniform (suspicious for images)
    # Very high entropy (> 7.9) is also suspicious
    is_suspicious = (avg_chi < 200) or (entropy > 7.9)
    
    return entropy, avg_chi, is_suspicious
