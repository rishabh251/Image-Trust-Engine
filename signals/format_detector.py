# signals/format_detector.py

from pathlib import Path

# ---------- EXISTING LOGIC (KEEP IT) ---------- #

MAGIC_BYTES = {
    "jpeg": [b"\xFF\xD8\xFF"],
    "png": [b"\x89PNG\r\n\x1a\n"],
    "tiff": [b"II*\x00", b"MM\x00*"],
    "bmp": [b"BM"]
}


def detect_format_capabilities(file_path: str, read_bytes: int = 16) -> dict:
    result = {
        "extension": None,
        "detected_format": "unknown",
        "exif_supported": False,
        "jpeg_signals_supported": False,
        "block_artifacts_supported": False,
        "reason": ""
    }

    path = Path(file_path)
    result["extension"] = path.suffix.lower().replace(".", "")

    try:
        with open(file_path, "rb") as f:
            header = f.read(read_bytes)

        if any(header.startswith(sig) for sig in MAGIC_BYTES["jpeg"]):
            result.update({
                "detected_format": "jpeg",
                "exif_supported": True,
                "jpeg_signals_supported": True,
                "block_artifacts_supported": True,
                "reason": "JPEG magic bytes detected"
            })

        elif any(header.startswith(sig) for sig in MAGIC_BYTES["png"]):
            result.update({
                "detected_format": "png",
                "reason": "PNG magic bytes detected"
            })

        elif header.startswith(b"RIFF") and b"WEBP" in header:
            result.update({
                "detected_format": "webp",
                "reason": "WEBP container detected"
            })

        elif any(header.startswith(sig) for sig in MAGIC_BYTES["tiff"]):
            result.update({
                "detected_format": "tiff",
                "exif_supported": True,
                "reason": "TIFF magic bytes detected"
            })

        elif any(header.startswith(sig) for sig in MAGIC_BYTES["bmp"]):
            result.update({
                "detected_format": "bmp",
                "reason": "BMP magic bytes detected"
            })

        else:
            result["reason"] = "Unknown or unsupported image format"

        return result

    except Exception as e:
        result["reason"] = f"Format detection failed: {str(e)}"
        return result


# ---------- FORENSIC SIGNAL (NEW) ---------- #

def analyze_format(image_path: str) -> dict:
    try:
        meta = detect_format_capabilities(image_path)

        score = 0.0
        confidence = 0.5
        reason = "Image format appears consistent with standard camera pipelines"

        # Extension mismatch
        if meta["extension"] != meta["detected_format"]:
            score = 0.4
            confidence = 0.8
            reason = "File extension does not match actual image format"

        # WEBP / BMP are uncommon for native cameras
        elif meta["detected_format"] in {"webp", "bmp"}:
            score = 0.3
            confidence = 0.6
            reason = f"Uncommon image format for camera capture ({meta['detected_format']})"

        # Unknown formats
        elif meta["detected_format"] == "unknown":
            score = 0.35
            confidence = 0.7
            reason = "Unknown image format detected"

        return {
            "score": float(score),
            "confidence": float(confidence),
            "reason": reason
        }

    except Exception as e:
        return {
            "score": 0.0,
            "confidence": 0.0,
            "reason": f"Format analysis failed: {str(e)}"
        }
