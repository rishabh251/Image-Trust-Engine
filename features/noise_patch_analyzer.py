# features/noise_patch_analyzer.py

import numpy as np
from features.patch_extractor import extract_patches
from signals.noise import analyze_noise_patch


def analyze_noise_patches(image_path: str) -> dict:
    """
    Analyze noise consistency across image patches.

    Returns forensic-style signal:
    {
        "score": float,
        "confidence": float,
        "reason": str
    }
    """

    patches = extract_patches(image_path)

    patch_scores = []

    for p in patches:
        score = analyze_noise_patch(p["patch"])
        patch_scores.append(score)

    patch_scores = np.array(patch_scores)

    # How many patches look suspicious?
    suspicious_ratio = float(np.mean(patch_scores > 0.6))

    # Variance tells us inconsistency (AI edits)
    score_variance = float(np.var(patch_scores))

    # Decision heuristics
    if suspicious_ratio > 0.6:
        score = 0.8
        confidence = 0.9
        reason = "High proportion of patches show non-natural noise patterns"

    elif suspicious_ratio > 0.15 and score_variance > 0.01:
        score = 0.6
        confidence = 0.8
        reason = "Localized noise inconsistencies detected across patches"

    else:
        score = 0.2
        confidence = 0.7
        reason = "Noise patterns consistent across image"

    return {
        "score": score,
        "confidence": confidence,
        "reason": reason
    }
