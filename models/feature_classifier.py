# models/feature_classifier.py

from sklearn.linear_model import LogisticRegression
from features.simulator import generate_dataset


class FeatureClassifier:
    def __init__(self):
        self.model = LogisticRegression()

    def train(self):
        X, y = generate_dataset()
        self.model.fit(X, y)

    def predict_proba(self, features):
        return float(self.model.predict_proba([features])[0][1])
