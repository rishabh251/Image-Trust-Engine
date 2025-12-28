from signals.format_detector import detect_format
from signals.exif import analyze_exif
from signals.jpeg import analyze_jpeg
from signals.frequency import analyze_frequency
from signals.noise import analyze_noise
from fusion.decision_engine import fuse_signals

IMAGE_PATH = "img2.png"  # change if needed

format_info = detect_format(IMAGE_PATH)

exif = analyze_exif(IMAGE_PATH, format_info)
jpeg = analyze_jpeg(IMAGE_PATH, format_info)
freq = analyze_frequency(IMAGE_PATH)
noise = analyze_noise(IMAGE_PATH)

final_result = fuse_signals(exif, jpeg, freq, noise)

print("\n=== FINAL DECISION ===")
for k, v in final_result.items():
    print(f"{k}: {v}")
