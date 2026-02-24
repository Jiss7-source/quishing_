import os
from modules.qr_extractor import extract_url_from_qr
from modules.url_analyzer import classify_url
from modules.ml_model import predict_url
from urllib.parse import urlparse

# Folder containing QR images
UPLOAD_FOLDER = "uploads"

# Trusted domains whitelist
trusted_domains = [
    "google.com", "www.google.com",
    "microsoft.com", "www.microsoft.com",
    "amazon.com", "www.amazon.com",
    "amazon.in", "www.amazon.in",
    "apple.com", "www.apple.com",
    "facebook.com", "www.facebook.com",
    "instagram.com", "www.instagram.com",
    "youtube.com", "www.youtube.com"
]

# Loop through all files in uploads folder
for filename in os.listdir(UPLOAD_FOLDER):

    if filename.lower().endswith((".png", ".jpg", ".jpeg")):

        print("\n==============================")
        print("Processing:", filename)

        image_path = os.path.join(UPLOAD_FOLDER, filename)

        url = extract_url_from_qr(image_path)

        if url:
            print("Extracted URL:", url)

            rule_result = classify_url(url)
            print("Rule-Based Result:", rule_result)

            ml_result = predict_url(url)
            print("ML Prediction:", ml_result)

            normalized_url = url if url.startswith("http") else "https://" + url
            parsed = urlparse(normalized_url)
            domain = parsed.netloc.lower()

            # Final Decision
            if rule_result == "Suspicious":
                print("FINAL VERDICT: Suspicious QR Code")

            elif domain in trusted_domains:
                print("FINAL VERDICT: Safe QR Code")

            elif ml_result == "phishing" and not normalized_url.startswith("https"):
                print("FINAL VERDICT: Suspicious QR Code")

            else:
                print("FINAL VERDICT: Safe QR Code")

        else:
            print("No QR code found in", filename)

print("\nAll QR codes processed.")