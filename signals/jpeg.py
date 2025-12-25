# signals/jpeg.py

from PIL import Image
import os


def analyze_jpeg(image_path: str, format_info: dict) -> dict:
    """
    Analyze JPEG compression behavior and sanity.

    Returns:
        {
            "score": float in [0,1] or None,
            "confidence": float in [0,1],
            "reason": str
        }
    """

    # JPEG-specific signals not applicable
    if not format_info.get("jpeg_signals_supported", False):
        return {
            "score": None,
            "confidence": 0.0,
            "reason": "JPEG compression analysis not applicable"
        }

    try:
        img = Image.open(image_path)

        # Basic sanity check
        if img.format != "JPEG":
            return {
                "score": None,
                "confidence": 0.0,
                "reason": "Image format mismatch (not true JPEG)"
            }

        width, height = img.size
        file_size_kb = os.path.getsize(image_path) / 1024

        # Compression ratio heuristic
        pixels = width * height
        compression_ratio = file_size_kb / pixels  # KB per pixel

        # Heuristic thresholds (empirical, conservative)
        if 0.002 < compression_ratio < 0.01:
            score = 1.0
            confidence = 0.85
            reason = "JPEG compression ratio within camera-like range"
        elif 0.001 < compression_ratio <= 0.002 or 0.01 <= compression_ratio < 0.015:
            score = 0.6
            confidence = 0.7
            reason = "JPEG compression slightly atypical"
        else:
            score = 0.3
            confidence = 0.6
            reason = "JPEG compression highly atypical"

        return {
            "score": round(score, 3),
            "confidence": confidence,
            "reason": reason
        }

    except Exception as e:
        return {
            "score": None,
            "confidence": 0.0,
            "reason": f"JPEG analysis failed: {str(e)}"
        }
