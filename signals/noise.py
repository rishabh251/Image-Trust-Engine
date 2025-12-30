# signals/noise.py

import cv2
import numpy as np
from scipy.stats import entropy


def analyze_noise(image_path: str) -> dict:
    """
    Analyze noise characteristics with phone-camera awareness.
    """

    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            return {
                "score": None,
                "confidence": 0.0,
                "reason": "Failed to load image for noise analysis"
            }

        # ---- Noise extraction (keep your method) ----
        blurred = cv2.GaussianBlur(img, (5, 5), 0)
        noise = img.astype(np.float32) - blurred.astype(np.float32)

        noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-8)

        hist, _ = np.histogram(noise, bins=256, range=(0, 1), density=True)
        noise_entropy = entropy(hist + 1e-8)

        # ---- NEW: secondary statistic for phones ----
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        noise_std = np.std(laplacian)

        # ---- Phone-aware interpretation ----
        if 4.5 <= noise_entropy <= 5.5:
            score = 1.0
            confidence = 0.85
            reason = "Natural sensor-like noise detected"

        elif noise_entropy < 3.8 and noise_std < 10:
            score = 0.6
            confidence = 0.75
            reason = "Low-entropy noise consistent with phone-camera denoising"

        elif 3.8 <= noise_entropy < 4.5 or 5.5 < noise_entropy <= 6.2:
            score = 0.5
            confidence = 0.7
            reason = "Moderately atypical noise (possible processing)"

        else:
            score = 0.3
            confidence = 0.6
            reason = "Unnatural noise pattern (possible synthetic origin)"

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
