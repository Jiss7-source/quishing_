import pandas as pd
import joblib
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import resample

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from feature_extractor import extract_features

# ============================
# FEATURE COLUMNS
# These 18 columns exist in PhiUSIIL
# AND can be extracted from URL string alone
# ============================

FEATURE_COLUMNS = [
    'URLLength',
    'DomainLength',
    'IsDomainIP',
    'TLDLength',
    'NoOfSubDomain',
    'HasObfuscation',
    'NoOfObfuscatedChar',
    'ObfuscationRatio',
    'NoOfLettersInURL',
    'LetterRatioInURL',
    'NoOfDegitsInURL',
    'DegitRatioInURL',
    'NoOfEqualsInURL',
    'NoOfQMarkInURL',
    'NoOfAmpersandInURL',
    'NoOfOtherSpecialCharsInURL',
    'SpacialCharRatioInURL',
    'IsHTTPS',
]

# ============================
# LOAD DATASET
# ============================

print("Loading dataset...")
df = pd.read_csv("dataset/PhiUSIIL_Phishing_URL_Dataset.csv")

print(f"Total rows: {len(df)}")
print(f"\nOriginal label distribution:")
print(df['label'].value_counts())
print("(PhiUSIIL: 1=Legitimate, 0=Phishing)")

# Remap to standard convention
# 0 = Legitimate, 1 = Phishing
df['Label'] = df['label'].apply(lambda x: 0 if x == 1 else 1)

print(f"\nRemapped labels (0=Legitimate, 1=Phishing):")
print(df['Label'].value_counts())

# Keep only the 18 URL features and label
df = df[FEATURE_COLUMNS + ['Label']]
df = df.dropna()

print(f"\nRows after dropping nulls: {len(df)}")

# ============================
# BALANCE DATASET
# ============================

legitimate = df[df['Label'] == 0]
phishing   = df[df['Label'] == 1]

print(f"\nBefore balancing:")
print(f"  Legitimate : {len(legitimate)}")
print(f"  Phishing   : {len(phishing)}")

# Downsample the larger class to match the smaller
min_size = min(len(legitimate), len(phishing))

legitimate_sampled = resample(
    legitimate,
    replace=False,
    n_samples=min_size,
    random_state=42
)

phishing_sampled = resample(
    phishing,
    replace=False,
    n_samples=min_size,
    random_state=42
)

balanced_df = pd.concat([legitimate_sampled, phishing_sampled])
balanced_df = balanced_df.sample(
    frac=1, random_state=42
).reset_index(drop=True)

print(f"\nAfter balancing:")
print(balanced_df['Label'].value_counts())

# ============================
# TRAIN TEST SPLIT
# ============================

X = balanced_df.drop('Label', axis=1)
y = balanced_df['Label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

print(f"\nTraining samples : {len(X_train)}")
print(f"Testing samples  : {len(X_test)}")

# ============================
# TRAIN MODEL
# ============================

print("\nTraining model...")

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)
print("Training complete.")

# ============================
# SANITY CHECK
# Uses feature_extractor.py to simulate
# real prediction on known URLs
# ============================

print("\n--- Sanity Check ---")

sanity_tests = [
    ("https://www.google.com",                     "LEGITIMATE"),
    ("https://www.youtube.com",                    "LEGITIMATE"),
    ("https://www.amazon.com",                     "LEGITIMATE"),
    ("http://192.168.1.1/login-verify",            "PHISHING"),
    ("http://secure-login-verify@evil.xyz/update", "PHISHING"),
]

all_passed = True
for test_url, expected in sanity_tests:
    feats   = extract_features(test_url)
    test_df = pd.DataFrame([feats], columns=FEATURE_COLUMNS)
    pred    = model.predict(test_df)[0]
    actual  = "LEGITIMATE" if pred == 0 else "PHISHING"
    status  = "✓" if actual == expected else "✗ WRONG"
    print(f"  {status}  {test_url:<55} -> {actual}")
    if actual != expected:
        all_passed = False

if all_passed:
    print("\n  All sanity checks passed!")
else:
    print("\n  Some checks failed.")

# ============================
# EVALUATION
# ============================

y_pred = model.predict(X_test)

print("\nAccuracy:", round(accuracy_score(y_test, y_pred), 4))
print("\nClassification Report:")
print(classification_report(
    y_test, y_pred,
    target_names=['Legitimate', 'Phishing']
))

print("\nFeature Importances:")
for name, score in sorted(
    zip(FEATURE_COLUMNS, model.feature_importances_),
    key=lambda x: x[1],
    reverse=True
):
    print(f"  {name:<30}: {score:.4f}")

# ============================
# SAVE MODEL AND FEATURE LIST
# ============================

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/url_model.pkl")
joblib.dump(FEATURE_COLUMNS, "model/feature_columns.pkl")

print("\nModel saved to       model/url_model.pkl")
print("Feature columns saved to model/feature_columns.pkl")