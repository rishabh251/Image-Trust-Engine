# signals/noise.py

import cv2
import numpy as np
from scipy.stats import entropy


# =========================================================
# GLOBAL IMAGE-LEVEL NOISE ANALYSIS (KEEP AS IS)
# =========================================================

def analyze_noise(image_path: str) -> dict:
    """
    Analyze global noise characteristics with phone-camera awareness.
    """

    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            return {
                "score": 0.0,
                "confidence": 0.0,
                "reason": "Failed to load image for noise analysis"
            }

        # ---- Noise extraction ----
        blurred = cv2.GaussianBlur(img, (5, 5), 0)
        noise = img.astype(np.float32) - blurred.astype(np.float32)

        noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-8)

        hist, _ = np.histogram(noise, bins=256, range=(0, 1), density=True)
        noise_entropy = entropy(hist + 1e-8)

        # ---- Secondary statistic (phone cameras) ----
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        noise_std = np.std(laplacian)

        # ---- Interpretation ----
        if 4.5 <= noise_entropy <= 5.5:
            score = 0.2
            confidence = 0.85
            reason = "Natural sensor-like noise detected"

        elif noise_entropy < 3.8 and noise_std < 10:
            score = 0.3
            confidence = 0.75
            reason = "Low-entropy noise consistent with phone-camera denoising"

        elif 3.8 <= noise_entropy < 4.5 or 5.5 < noise_entropy <= 6.2:
            score = 0.45
            confidence = 0.7
            reason = "Moderately atypical noise (possible processing)"

        else:
            score = 0.6
            confidence = 0.6
            reason = "Unnatural noise pattern (possible synthetic origin)"

        return {
            "score": round(float(score), 3),
            "confidence": float(confidence),
            "reason": reason
        }

    except Exception as e:
        return {
            "score": 0.0,
            "confidence": 0.0,
            "reason": f"Noise analysis failed: {str(e)}"
        }


# =========================================================
# PATCH-LEVEL NOISE ANALYSIS (NEW – CRITICAL)
# =========================================================

def analyze_noise_patch(patch: np.ndarray) -> float:
    """
    Analyze noise characteristics of a single image patch.

    Returns:
        score in range [0, 1]
        Higher score => more suspicious (AI-like)
    """

    if patch is None or patch.size == 0:
        return 0.0

    # Ensure float
    patch = patch.astype(np.float32)

    # Remove low-frequency content
    blurred = cv2.GaussianBlur(patch, (5, 5), 0)
    noise = patch - blurred

    # Noise statistics
    noise_std = float(np.std(noise))

    # Heuristic:
    # - Natural camera noise → higher variance
    # - AI / inpainted regions → overly smooth or inconsistent noise
    #
    # Typical patch noise_std ~ 2–6 (depends on scale)
    # We convert this to a suspicion score

    if noise_std < 1.5:
        score = 0.9   # very suspicious (over-smoothed / synthetic)
    elif noise_std < 3.0:
        score = 0.6   # moderately suspicious
    else:
        score = 0.2   # natural noise

    return float(score)
