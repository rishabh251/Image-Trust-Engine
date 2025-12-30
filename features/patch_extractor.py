# features/patch_extractor.py

import cv2
import numpy as np


def extract_patches(
    image_path: str,
    patch_size: int = 64,
    stride: int = 32
):
    """
    Splits image into overlapping patches.

    Returns:
        List of dicts:
        {
            "patch": np.ndarray,
            "x": int,
            "y": int
        }
    """

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Failed to load image for patch extraction")

    h, w = img.shape
    patches = []

    for y in range(0, h - patch_size + 1, stride):
        for x in range(0, w - patch_size + 1, stride):
            patch = img[y:y + patch_size, x:x + patch_size]

            patches.append({
                "patch": patch,
                "x": x,
                "y": y
            })

    return patches
