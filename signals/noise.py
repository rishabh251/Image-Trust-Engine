# signals/noise.py

import cv2
import numpy as np
from scipy.stats import entropy


def analyze_noise(image_path: str) -> dict:
    """
    Analyze noise entropy to estimate whether noise
    resembles natural camera sensor noise.

    Returns:
        {
            "score": float in [0,1],
            "confidence": float in [0,1],
            "reason": str
        }
    """

    try:
        # Load image in grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            return {
                "score": None,
                "confidence": 0.0,
                "reason": "Failed to load image for noise analysis"
            }

        # Extract noise using a simple blur subtraction
        blurred = cv2.GaussianBlur(img, (5, 5), 0)
        noise = img.astype(np.float32) - blurred.astype(np.float32)

        # Normalize noise
        noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-8)

        # Histogram of noise values
        hist, _ = np.histogram(noise, bins=256, range=(0, 1), density=True)

        noise_entropy = entropy(hist + 1e-8)

        # Heuristic scoring (camera-like entropy range)
        if 4.5 <= noise_entropy <= 5.5:
            score = 1.0
            confidence = 0.85
            reason = "Natural sensor-like noise entropy detected"
        elif 3.8 <= noise_entropy < 4.5 or 5.5 < noise_entropy <= 6.2:
            score = 0.6
            confidence = 0.7
            reason = "Slightly atypical noise entropy"
        else:
            score = 0.3
            confidence = 0.6
            reason = "Unnatural noise entropy detected"

        return {
            "score": round(score, 3),
            "confidence": confidence,
            "reason": reason
        }

    except Exception as e:
        return {
            "score": None,
            "confidence": 0.0,
            "reason": f"Noise analysis failed: {str(e)}"
        }
