import re
from urllib.parse import urlparse

def analyze_url(url):
    score = 0

    parsed = urlparse(url)
    domain = parsed.netloc

    # 1️⃣ Check if HTTPS is used
    if not url.startswith("https"):
        score += 1

    # 2️⃣ Check if domain is IP address
    if re.match(r'\d+\.\d+\.\d+\.\d+', domain):
        score += 2

    # 3️⃣ Check for suspicious keywords
    suspicious_words = ["login", "verify", "update", "secure", "bank", "password"]
    for word in suspicious_words:
        if word in url.lower():
            score += 1

    # 4️⃣ Check if URL is very long
    if len(url) > 75:
        score += 1

    return score


def classify_url(url):
    score = analyze_url(url)

    if score >= 3:
        return "Suspicious"
    else:
        return "Safe"
