import os
import sys
import joblib
import pandas as pd
import traceback

# Ensure modules folder is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from feature_extractor import extract_features

# ============================
# LOAD MODEL AND FEATURE LIST
# Loaded once silently at module level
# so importing this file doesn't print anything
# ============================

BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH    = os.path.join(BASE_DIR, "model", "url_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "model", "feature_columns.pkl")

model           = joblib.load(MODEL_PATH)
FEATURE_COLUMNS = joblib.load(FEATURES_PATH)

# ============================
# PREDICTION FUNCTION
# ============================

def predict_url(url):
    """
    Takes a URL string.
    Returns a result dictionary with verdict,
    risk level, confidence and reason.
    Called directly OR by qr_pipeline.py
    """
    try:
        # Step 1: Extract 18 features from URL string
        features = extract_features(url)

        # Step 2: Verify feature count matches model
        if len(features) != len(FEATURE_COLUMNS):
            raise ValueError(
                f"Feature count mismatch: "
                f"expected {len(FEATURE_COLUMNS)}, "
                f"got {len(features)}"
            )

        # Step 3: Build DataFrame with correct column names
        features_df = pd.DataFrame([features], columns=FEATURE_COLUMNS)

        # Step 4: Get prediction and confidence
        prediction  = model.predict(features_df)[0]
        probability = model.predict_proba(features_df)[0]
        confidence  = round(max(probability) * 100, 2)

        # Step 5: Build result
        # 0 = Legitimate, 1 = Phishing
        if prediction == 1:
            verdict    = "Suspicious"
            risk_level = "HIGH" if confidence > 85 else "MEDIUM"
            reason     = "ML model detected phishing patterns"
        else:
            verdict    = "Safe"
            risk_level = "LOW"
            reason     = "URL appears legitimate"

        return {
            "url"        : url,
            "verdict"    : verdict,
            "risk_level" : risk_level,
            "confidence" : f"{confidence}%",
            "reason"     : reason,
            "prediction" : int(prediction)
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "url"        : url,
            "verdict"    : "Error",
            "risk_level" : "UNKNOWN",
            "confidence" : "0%",
            "reason"     : str(e),
            "prediction" : -1
        }

# ============================
# RUN FROM TERMINAL
# Only runs when you execute
# predict_url.py directly —
# NOT when imported by qr_pipeline.py
# ============================

if __name__ == "__main__":
    print("\n--- URL Phishing Detector ---")
    print("Type 'quit' to exit\n")

    while True:
        test_url = input("Enter URL: ").strip()

        if test_url.lower() == 'quit':
            break

        if not test_url:
            print("  Please enter a URL.\n")
            continue

        result = predict_url(test_url)

        print(f"\n  URL        : {result['url']}")
        print(f"  Verdict    : {result['verdict']}")
        print(f"  Risk Level : {result['risk_level']}")
        print(f"  Confidence : {result['confidence']}")
        print(f"  Reason     : {result['reason']}")
        print()