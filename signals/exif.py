# signals/exif.py

from PIL import Image
from PIL.ExifTags import TAGS

# Common EXIF tags typically present in camera images
COMMON_CAMERA_TAGS = {
    "Make",
    "Model",
    "DateTime",
    "DateTimeOriginal",
    "ExifImageWidth",
    "ExifImageHeight"
}


def analyze_exif(image_path: str, format_info: dict) -> dict:
    """
    Analyze EXIF metadata presence and basic consistency.

    Returns:
        {
            "score": float in [0,1] or None,
            "confidence": float in [0,1],
            "reason": str
        }
    """

    # EXIF not applicable for this format
    if not format_info.get("exif_supported", False):
        return {
            "score": None,
            "confidence": 0.0,
            "reason": "EXIF not supported for detected format"
        }

    try:
        img = Image.open(image_path)
        exif_raw = img._getexif()

        # No EXIF metadata at all
        if not exif_raw:
            return {
                "score": 0.0,
                "confidence": 0.7,
                "reason": "No EXIF metadata found"
            }

        # Decode EXIF tags
        exif = {
            TAGS.get(tag, tag): value
            for tag, value in exif_raw.items()
        }

        present_tags = COMMON_CAMERA_TAGS.intersection(exif.keys())
        coverage_ratio = len(present_tags) / len(COMMON_CAMERA_TAGS)

        # Heuristic scoring (conservative)
        if coverage_ratio >= 0.7:
            score = 1.0
            confidence = 0.9
            reason = "Rich and consistent EXIF metadata"
        elif coverage_ratio >= 0.4:
            score = 0.6
            confidence = 0.7
            reason = "Partial EXIF metadata present"
        else:
            score = 0.3
            confidence = 0.6
            reason = "Sparse or suspicious EXIF metadata"

        return {
            "score": round(score, 3),
            "confidence": confidence,
            "reason": reason
        }

    except Exception as e:
        return {
            "score": None,
            "confidence": 0.0,
            "reason": f"EXIF analysis failed: {str(e)}"
        }
