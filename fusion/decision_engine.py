# fusion/decision_engine.py

def fuse_signals(
    exif_result: dict,
    jpeg_result: dict,
    frequency_result: dict,
    noise_result: dict
) -> dict:
    """
    Fuse Option 1 signals into a final decision.

    Returns:
        {
            "verdict": str,
            "ai_probability": float,
            "confidence": float,
            "explanation": str
        }
    """

    signals = {
        "exif": exif_result,
        "jpeg": jpeg_result,
        "frequency": frequency_result,
        "noise": noise_result
    }

    weights = {
        "exif": 0.2,
        "jpeg": 0.3,
        "frequency": 0.25,
        "noise": 0.25
    }

    weighted_score = 0.0
    weight_sum = 0.0
    explanations = []

    for name, result in signals.items():
        score = result.get("score")
        reason = result.get("reason", "")

        if score is None:
            explanations.append(f"{name}: not applicable")
            continue

        weighted_score += weights[name] * score
        weight_sum += weights[name]
        explanations.append(f"{name}: {reason}")

    # Safety check
    if weight_sum == 0:
        return {
            "verdict": "Indeterminate",
            "ai_probability": 0.5,
            "confidence": 0.2,
            "explanation": "Insufficient forensic signals available"
        }

    final_score = weighted_score / weight_sum

    # Interpretation logic (VERY IMPORTANT)
    if final_score < 0.35:
        verdict = "Likely reprocessed real image"
        ai_probability = 0.25
        confidence = 0.7
    elif final_score < 0.55:
        verdict = "Indeterminate (reprocessed or AI)"
        ai_probability = 0.5
        confidence = 0.5
    else:
        verdict = "Likely AI-generated image"
        ai_probability = 0.75
        confidence = 0.7

    return {
        "verdict": verdict,
        "ai_probability": round(ai_probability, 2),
        "confidence": round(confidence, 2),
        "explanation": " | ".join(explanations)
    }
