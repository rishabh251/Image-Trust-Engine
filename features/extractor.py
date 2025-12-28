# features/extractor.py

def extract_features(exif, jpeg, frequency, noise):
    """
    Convert Option 1 signal outputs into a numeric feature vector.
    None values are replaced with -1.
    """

    def safe_score(result):
        return -1 if result["score"] is None else float(result["score"])

    features = [
        safe_score(exif),
        safe_score(jpeg),
        safe_score(frequency),
        safe_score(noise)
    ]

    return features
