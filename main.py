# main.py

import argparse
import os

# Import forensic signals
from signals.noise import analyze_noise
from signals.frequency import analyze_frequency
from signals.format_detector import analyze_format

# Import decision engine
from fusion.decision_engine import decide_authenticity
from features.noise_patch_analyzer import analyze_noise_patches

def run_forensic_pipeline(image_path: str) -> dict:
    """
    Runs all forensic analyzers on the given image
    and returns the final authenticity decision.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # -------- Step 1: Collect forensic signals -------- #

    signals = {}

    try:
        signals["noise"] = analyze_noise_patches(image_path)
    except Exception as e:
        signals["noise"] = {
            "score": 0.0,
            "confidence": 0.0,
            "reason": f"Noise analysis failed: {str(e)}"
        }

    try:
        signals["frequency"] = analyze_frequency(image_path)
    except Exception as e:
        signals["frequency"] = {
            "score": 0.0,
            "confidence": 0.0,
            "reason": f"Frequency analysis failed: {str(e)}"
        }

    try:
        signals["format"] = analyze_format(image_path)
    except Exception as e:
        signals["format"] = {
            "score": 0.0,
            "confidence": 0.0,
            "reason": f"Format analysis failed: {str(e)}"
        }

    # -------- Step 2: Decision making -------- #

    decision = decide_authenticity(signals)

    return {
        "image": image_path,
        "signals": signals,
        "decision": decision
    }


def main():
    parser = argparse.ArgumentParser(
        description="AI Image Forensic Authenticity Analyzer"
    )

    parser.add_argument(
        "--image",
        type=str,
        required=True,
        help="Path to input image"
    )

    args = parser.parse_args()

    result = run_forensic_pipeline(args.image)

    # -------- Step 3: Final user-facing output -------- #

    print("\n========== IMAGE AUTHENTICITY REPORT ==========\n")
    print(f"Image: {result['image']}\n")

    print("Forensic Signals:")
    for name, res in result["signals"].items():
        print(
            f" - {name.upper():10s} | "
            f"score={res['score']:.2f} | "
            f"confidence={res['confidence']:.2f}"
        )

    print("\nFinal Decision:")
    print(f" Label      : {result['decision']['label']}")
    print(f" Confidence : {result['decision']['confidence']}")
    print(f" Reason     : {result['decision']['reason']}")
    print("\n=============================================\n")


if __name__ == "__main__":
    main()
