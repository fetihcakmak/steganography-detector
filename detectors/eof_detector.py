"""
EOF Detector - Identifies appended data after the logical End Of File
"""
import os
from typing import Tuple, Optional

def detect_eof_data(filepath: str) -> Tuple[bool, int, Optional[bytes]]:
    """
    Checks for data appended to files (like JPG, PNG) after their logical end.
    Returns (has_appended_data, appended_size, appended_bytes)
    """
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
    except Exception:
        return False, 0, None

    if len(data) == 0:
        return False, 0, None

    # Check for JPEG EOF (FF D9)
    if data.startswith(b'\xff\xd8'):
        eof_index = data.rfind(b'\xff\xd9')
        if eof_index != -1:
            appended = data[eof_index + 2:]
            if len(appended) > 0:
                return True, len(appended), appended
                
    # Check for PNG EOF (IEND chunk)
    elif data.startswith(b'\x89PNG\r\n\x1a\n'):
        iend_index = data.rfind(b'IEND\xaeB`\x82')
        if iend_index != -1:
            appended = data[iend_index + 8:]
            if len(appended) > 0:
                return True, len(appended), appended
                
    # Check for GIF EOF (3B)
    elif data.startswith(b'GIF87a') or data.startswith(b'GIF89a'):
        if data[-1] != 0x3B:
            # Finding the exact EOF for GIF can be complex without full parsing,
            # but if it doesn't end with 3B, it might have appended data.
            # We'll do a simple check.
            eof_index = data.rfind(b'\x3b')
            if eof_index != -1:
                appended = data[eof_index + 1:]
                if len(appended) > 0:
                    return True, len(appended), appended

    return False, 0, None
