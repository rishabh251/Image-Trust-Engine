# main.py
# Image Trust Engine – Final Pipeline

from signals.format_detector import detect_format
from signals.exif import analyze_exif
from signals.jpeg import analyze_jpeg
from signals.frequency import analyze_frequency
from signals.noise import analyze_noise

from features.extractor import extract_features
from models.feature_classifier import FeatureClassifier
from fusion.decision_engine import fuse_signals


def predict(image_path: str):
    print("\n=== Running Image Trust Engine ===\n")

    # ---------- OPTION 1: Forensic signals ----------
    format_info = detect_format(image_path)

    exif = analyze_exif(image_path, format_info)
    jpeg = analyze_jpeg(image_path, format_info)
    frequency = analyze_frequency(image_path)
    noise = analyze_noise(image_path)

    # ---------- OPTION 2: Feature-level ML ----------
    features = extract_features(exif, jpeg, frequency, noise)

    clf = FeatureClassifier()
    clf.train()   # synthetic training for now
    ai_prob_ml = clf.predict_proba(features)

    # ---------- OPTION 3: Decision fusion ----------
    final_decision = fuse_signals(
        exif_result=exif,
        jpeg_result=jpeg,
        frequency_result=frequency,
        noise_result=noise
    )

    # Replace rule-based probability with ML probability
    final_decision["ai_probability"] = round(ai_prob_ml, 3)

    return final_decision


if __name__ == "__main__":
    # 👇 PUT YOUR IMAGE HERE
    IMAGE_PATH = "testimages/img4.jpg"   # change to any image you want

    result = predict(IMAGE_PATH)

    print("=== FINAL RESULT ===")
    for key, value in result.items():
        print(f"{key}: {value}")
