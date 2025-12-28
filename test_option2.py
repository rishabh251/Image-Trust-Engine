from features.simulator import generate_sample
from models.feature_classifier import FeatureClassifier

clf = FeatureClassifier()
clf.train()

# Simulated AI-like sample
ai_sample = generate_sample(1)
real_sample = generate_sample(0)

print("AI sample:", ai_sample)
print("AI probability:", clf.predict_proba(ai_sample))

print("Real sample:", real_sample)
print("AI probability:", clf.predict_proba(real_sample))
