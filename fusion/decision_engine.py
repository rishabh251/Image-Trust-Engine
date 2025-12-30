# fusion/decision_engine.py

def decide_authenticity(signals: dict) -> dict:
    """
    Combine multiple forensic signals to decide image authenticity.

    Args:
        signals: dict of {signal_name: {score, confidence, reason}}

    Returns:
        {
            "label": str,
            "confidence": float,
            "reason": str
        }
    """

    # -------- Step 1: Weighted evidence accumulation -------- #

    weighted_sum = 0.0
    confidence_sum = 0.0
    contributing_reasons = []

    for name, result in signals.items():
        score = result.get("score", 0.0)
        confidence = result.get("confidence", 0.0)
        reason = result.get("reason", "")

        weighted_sum += score * confidence
        confidence_sum += confidence

        if score > 0.4 and confidence > 0.6:
            contributing_reasons.append(f"{name}: {reason}")

    if confidence_sum == 0:
        return {
            "label": "UNKNOWN",
            "confidence": 0.0,
            "reason": "No reliable forensic signals available"
        }

    normalized_score = weighted_sum / confidence_sum

    # -------- Step 2: Rule-based decision thresholds -------- #

    if normalized_score >= 0.75:
        label = "AI_GENERATED"
    elif 0.45 <= normalized_score < 0.75:
        label = "AI_EDITED"
    else:
        label = "REAL"

    # -------- Step 3: Final confidence estimation -------- #

    decision_confidence = min(1.0, normalized_score + 0.15)

    # -------- Step 4: Human-readable reason -------- #

    if contributing_reasons:
        reason = " | ".join(contributing_reasons[:3])
    else:
        reason = "No significant forensic inconsistencies detected"

    return {
        "label": label,
        "confidence": round(decision_confidence, 2),
        "reason": reason
    }
