# signals/format_detector.py

from pathlib import Path

# Magic byte signatures for common image formats
MAGIC_BYTES = {
    "jpeg": [b"\xFF\xD8\xFF"],
    "png": [b"\x89PNG\r\n\x1a\n"],
    "tiff": [b"II*\x00", b"MM\x00*"],
    "bmp": [b"BM"]
}


def detect_format(file_path: str, read_bytes: int = 16) -> dict:
    """
    Detect the real image format using file headers (magic bytes),
    NOT the file extension.

    Returns a dictionary describing format capabilities.
    """

    result = {
        "file_path": str(file_path),
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

        # JPEG
        if any(header.startswith(sig) for sig in MAGIC_BYTES["jpeg"]):
            result.update({
                "detected_format": "jpeg",
                "exif_supported": True,
                "jpeg_signals_supported": True,
                "block_artifacts_supported": True,
                "reason": "JPEG magic bytes detected"
            })
            return result

        # PNG
        if any(header.startswith(sig) for sig in MAGIC_BYTES["png"]):
            result.update({
                "detected_format": "png",
                "exif_supported": False,
                "jpeg_signals_supported": False,
                "block_artifacts_supported": False,
                "reason": "PNG magic bytes detected"
            })
            return result

        # WEBP (RIFF + WEBP marker)
        if header.startswith(b"RIFF") and b"WEBP" in header:
            result.update({
                "detected_format": "webp",
                "exif_supported": False,
                "jpeg_signals_supported": False,
                "block_artifacts_supported": False,
                "reason": "WEBP container detected"
            })
            return result

        # TIFF
        if any(header.startswith(sig) for sig in MAGIC_BYTES["tiff"]):
            result.update({
                "detected_format": "tiff",
                "exif_supported": True,
                "jpeg_signals_supported": False,
                "block_artifacts_supported": False,
                "reason": "TIFF magic bytes detected"
            })
            return result

        # BMP
        if any(header.startswith(sig) for sig in MAGIC_BYTES["bmp"]):
            result.update({
                "detected_format": "bmp",
                "exif_supported": False,
                "jpeg_signals_supported": False,
                "block_artifacts_supported": False,
                "reason": "BMP magic bytes detected"
            })
            return result

        result["reason"] = "Unknown or unsupported image format"
        return result

    except Exception as e:
        result["reason"] = f"Format detection failed: {str(e)}"
        return result
