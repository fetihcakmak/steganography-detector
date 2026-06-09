"""
LSB Analyzer - Pure Python Least Significant Bit analysis (specifically for BMP)
"""
import struct
from typing import Tuple, List, Optional

def analyze_bmp_lsb(filepath: str) -> Tuple[bool, str, Optional[bytes]]:
    """
    Reads an uncompressed BMP file, extracts the LSB of each pixel byte, 
    and checks if it contains readable text or high entropy data.
    """
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
    except Exception:
        return False, "Dosya okunamadi", None

    if len(data) < 54:
        return False, "Gecersiz dosya boyutu", None

    # Check BMP magic bytes
    if not data.startswith(b'BM'):
        return False, "BMP formati degil (Sadece uncompressed BMP desteklenir)", None

    # Parse basic BMP header
    pixel_offset = struct.unpack('<I', data[10:14])[0]
    
    if pixel_offset >= len(data):
        return False, "Gecersiz pixel offset", None

    pixels = data[pixel_offset:]
    
    # Extract LSB from each byte
    lsb_bits = [str(b & 1) for b in pixels]
    
    # Group into bytes (8 bits = 1 byte)
    extracted_bytes = bytearray()
    for i in range(0, len(lsb_bits) - 7, 8):
        byte_str = "".join(lsb_bits[i:i+8])
        extracted_bytes.append(int(byte_str, 2))
        
    # Analyze the extracted bytes
    # Look for a streak of printable characters (potential hidden message)
    longest_string = ""
    current_string = ""
    
    for b in extracted_bytes:
        if 32 <= b <= 126: # Printable ASCII
            current_string += chr(b)
        else:
            if len(current_string) > len(longest_string):
                longest_string = current_string
            current_string = ""
            
    if len(longest_string) > 8:
        return True, f"Olası metin bulundu: {longest_string[:50]}...", extracted_bytes
        
    return False, "Temiz (LSB anormalligi bulunmadi)", extracted_bytes
