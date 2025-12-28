# features/simulator.py

import random


def generate_sample(label: int):
    """
    label = 0 → real / reprocessed real
    label = 1 → AI-generated
    """

    if label == 0:
        # Real / reprocessed real image
        return [
            random.uniform(0.3, 1.0),   # EXIF (sometimes missing)
            random.uniform(0.2, 0.8),   # JPEG (varies a lot)
            random.uniform(0.25, 0.6),  # Frequency (natural-ish)
            random.uniform(0.25, 0.6)   # Noise (camera-like)
        ]
    else:
        # AI-generated image
        return [
            random.uniform(0.0, 0.2),   # EXIF absent/fake
            random.uniform(0.0, 0.3),   # JPEG weird or missing
            random.uniform(0.0, 0.3),   # Frequency flat
            random.uniform(0.0, 0.3)    # Noise unnatural
        ]


def generate_dataset(n=1000):
    X, y = [], []

    for _ in range(n // 2):
        X.append(generate_sample(0))
        y.append(0)

        X.append(generate_sample(1))
        y.append(1)

    return X, y
