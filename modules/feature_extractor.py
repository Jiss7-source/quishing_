import re
from urllib.parse import urlparse, urlunparse


def get_domain_info(url):
    try:
        parsed = urlparse(url)
        full_domain = parsed.netloc.lower()
        domain_clean = full_domain.split(':')[0]
        domain_no_www = re.sub(r'^www\.', '', domain_clean)
        parts = domain_clean.split('.')
        tld = parts[-1] if parts else ''
        subdomain_count = max(0, len(parts) - 2)
        return domain_clean, domain_no_www, tld, subdomain_count
    except Exception:
        return '', '', '', 0


def normalize_url(url):
    """
    Normalizes URL to match dataset format.
    Adds www. to plain domains so features are consistent.
    """
    url = str(url).strip()

    # Add scheme if missing
    if not url.startswith('http'):
        url = 'http://' + url

    try:
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()
        clean_netloc = netloc.split(':')[0]

        # Check if it's an IP address — don't add www. to IPs
        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        is_ip = bool(re.match(ip_pattern, clean_netloc))

        # Check if subdomain already exists (has 2+ dots)
        has_subdomain = clean_netloc.count('.') >= 2

        # Add www. only to plain domains like google.com
        if not has_subdomain and not is_ip:
            netloc = 'www.' + clean_netloc
            url = urlunparse((
                parsed.scheme,
                netloc,
                parsed.path,
                parsed.params,
                parsed.query,
                parsed.fragment
            ))
    except Exception:
        pass

    return url


def extract_features(url):
    """
    Extracts exactly 18 URL-based features matching
    the PhiUSIIL dataset calculation method precisely.
    """
    try:
        # Normalize URL before feature extraction
        url = normalize_url(url)

        domain_clean, domain_no_www, tld, subdomain_count = get_domain_info(url)

        # 1. URLLength
        url_length = len(url) - 1

        # 2. DomainLength
        domain_length = len(domain_clean)

        # 3. IsDomainIP
        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        is_domain_ip = 1 if re.match(ip_pattern, domain_clean) else 0

        # 4. TLDLength
        tld_length = len(tld)

        # 5. NoOfSubDomain
        no_of_subdomain = subdomain_count

        # 6. HasObfuscation
        obfuscated_chars = re.findall(r'%[0-9a-fA-F]{2}', url)
        has_obfuscation = 1 if obfuscated_chars else 0

        # 7. NoOfObfuscatedChar
        no_of_obfuscated = len(obfuscated_chars)

        # 8. ObfuscationRatio
        obfuscation_ratio = round(
            no_of_obfuscated / url_length, 4
        ) if url_length > 0 else 0

        # 9. NoOfLettersInURL
        no_of_letters = sum(c.isalpha() for c in domain_no_www) - 1

        # 10. LetterRatioInURL
        letter_ratio = round(
            no_of_letters / url_length, 4
        ) if url_length > 0 else 0

        # 11. NoOfDegitsInURL
        no_of_digits = sum(c.isdigit() for c in domain_no_www)

        # 12. DegitRatioInURL
        digit_ratio = round(
            no_of_digits / url_length, 4
        ) if url_length > 0 else 0

        # 13. NoOfEqualsInURL
        no_of_equals = url.count('=')

        # 14. NoOfQMarkInURL
        no_of_qmark = url.count('?')

        # 15. NoOfAmpersandInURL
        no_of_ampersand = url.count('&')

        # 16. NoOfOtherSpecialCharsInURL
        no_of_special = sum(
            1 for c in domain_no_www
            if not c.isalnum()
        )

        # 17. SpacialCharRatioInURL
        special_ratio = round(
            no_of_special / url_length, 4
        ) if url_length > 0 else 0

        # 18. IsHTTPS
        is_https = 1 if url.lower().startswith('https') else 0

        return [
            url_length,         # 1.  URLLength
            domain_length,      # 2.  DomainLength
            is_domain_ip,       # 3.  IsDomainIP
            tld_length,         # 4.  TLDLength
            no_of_subdomain,    # 5.  NoOfSubDomain
            has_obfuscation,    # 6.  HasObfuscation
            no_of_obfuscated,   # 7.  NoOfObfuscatedChar
            obfuscation_ratio,  # 8.  ObfuscationRatio
            no_of_letters,      # 9.  NoOfLettersInURL
            letter_ratio,       # 10. LetterRatioInURL
            no_of_digits,       # 11. NoOfDegitsInURL
            digit_ratio,        # 12. DegitRatioInURL
            no_of_equals,       # 13. NoOfEqualsInURL
            no_of_qmark,        # 14. NoOfQMarkInURL
            no_of_ampersand,    # 15. NoOfAmpersandInURL
            no_of_special,      # 16. NoOfOtherSpecialCharsInURL
            special_ratio,      # 17. SpacialCharRatioInURL
            is_https,           # 18. IsHTTPS
        ]

    except Exception:
        return [0] * 18