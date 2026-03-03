import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from url_extractor import extract_url_from_qr
from predict_url import predict_url


def analyze_qr(image_path):
    """
    Full pipeline:
    1. Extract URL from QR code image
    2. Pass URL directly to predict_url
    3. Return combined result
    """

    # Step 1: Extract URL from QR image
    # extract_url_from_qr returns a single string or None
    url = extract_url_from_qr(image_path)

    # If extraction failed
    if url is None:
        return {
            "image_path": image_path,
            "url":        None,
            "verdict":    "Error",
            "risk_level": "UNKNOWN",
            "confidence": "0%",
            "reason":     "Could not extract URL from QR code (no QR found or unreadable image)."
        }

    print(f"URL extracted: {url}")

    # Step 2: Pass extracted URL to predict_url
    result = predict_url(url)

    # Step 3: Add image path to result
    result["image_path"] = image_path

    return result


def resolve_image_path(image_path):
    """
    Resolve the image path by checking common fallback locations:
    1. As given
    2. uploads/ relative to cwd
    3. uploads/ relative to project root (parent of modules/)
    """
    resolved = Path(image_path)
    if resolved.exists():
        return resolved

    fallbacks = [
        Path("uploads") / resolved.name,
        Path(__file__).parent.parent / "uploads" / resolved.name,
    ]

    for fallback in fallbacks:
        if fallback.exists():
            print(f"ℹ️  Found file at '{fallback}'")
            return fallback

    return resolved  # Return original path so error message is meaningful


def main():
    print("\n--- QR Code Phishing Detector ---")

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("Enter path to QR code image: ").strip()

    # Resolve path with fallback search
    image_path = str(resolve_image_path(image_path))

    if not Path(image_path).exists():
        print(f"Error: File not found at {image_path}")
        sys.exit(1)

    print(f"\n🔍 Scanning: {image_path}")

    result = analyze_qr(image_path)

    print("\n" + "=" * 60)
    print("  QR CODE PHISHING ANALYSIS REPORT")
    print("=" * 60)
    print(f"  Image     : {result.get('image_path')}")
    print(f"  URL       : {result.get('url', 'N/A')}")
    print(f"  Verdict   : {result.get('verdict')}")
    print(f"  Risk Level: {result.get('risk_level')}")
    print(f"  Confidence: {result.get('confidence')}")
    print(f"  Reason    : {result.get('reason')}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
