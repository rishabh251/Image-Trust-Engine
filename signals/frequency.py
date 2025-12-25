# signals/frequency.py

import cv2
import numpy as np


def analyze_frequency(image_path: str) -> dict:
    """
    Analyze frequency characteristics of the image to detect
    unnatural smoothness or sharpness.

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
                "reason": "Failed to load image for frequency analysis"
            }

        # Compute FFT
        fft = np.fft.fft2(img)
        fft_shift = np.fft.fftshift(fft)
        magnitude = np.abs(fft_shift)

        # Normalize magnitude
        magnitude /= np.max(magnitude) + 1e-8

        h, w = magnitude.shape
        center_h, center_w = h // 2, w // 2

        # High-frequency region (outer ring)
        radius = min(center_h, center_w) // 3
        high_freq_region = magnitude.copy()

        cv2.circle(
            high_freq_region,
            (center_w, center_h),
            radius,
            0,
            thickness=-1
        )

        high_freq_energy = np.mean(high_freq_region)

        # Heuristic scoring
        if 0.15 <= high_freq_energy <= 0.35:
            score = 1.0
            confidence = 0.85
            reason = "Natural frequency distribution detected"
        elif 0.08 <= high_freq_energy < 0.15 or 0.35 < high_freq_energy <= 0.45:
            score = 0.6
            confidence = 0.7
            reason = "Slightly atypical frequency characteristics"
        else:
            score = 0.3
            confidence = 0.6
            reason = "Unnatural frequency distribution detected"

        return {
            "score": round(score, 3),
            "confidence": confidence,
            "reason": reason
        }

    except Exception as e:
        return {
            "score": None,
            "confidence": 0.0,
            "reason": f"Frequency analysis failed: {str(e)}"
        }
