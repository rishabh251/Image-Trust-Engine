from signals.format_detector import detect_format
from signals.exif import analyze_exif
from signals.jpeg import analyze_jpeg
from signals.frequency import analyze_frequency
from signals.noise import analyze_noise

IMAGE_PATH = "testimages/img9.jpg"   # change if needed


def run_option1(image_path):
    print("\n=== OPTION 1 TEST START ===\n")

    # 1. Detect format
    format_info = detect_format(image_path)
    print("Format Info:")
    print(format_info, "\n")

    # 2. EXIF analysis
    exif_result = analyze_exif(image_path, format_info)
    print("EXIF Analysis:")
    print(exif_result, "\n")

    # 3. JPEG analysis
    jpeg_result = analyze_jpeg(image_path, format_info)
    print("JPEG Analysis:")
    print(jpeg_result, "\n")

    # 4. Frequency analysis
    freq_result = analyze_frequency(image_path)
    print("Frequency Analysis:")
    print(freq_result, "\n")

    # 5. Noise analysis
    noise_result = analyze_noise(image_path)
    print("Noise Analysis:")
    print(noise_result, "\n")

    print("=== OPTION 1 TEST END ===")


if __name__ == "__main__":
    run_option1(IMAGE_PATH)
