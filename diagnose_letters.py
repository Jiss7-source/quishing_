# save as diagnose_letters.py in project root
import pandas as pd
import re

df = pd.read_csv('dataset/PhiUSIIL_Phishing_URL_Dataset.csv')

for _, row in df.head(5).iterrows():
    url = row['URL']
    stored = int(row['NoOfLettersInURL'])
    url_len = int(row['URLLength'])
    
    from urllib.parse import urlparse
    parsed = urlparse(url)
    domain = parsed.netloc.lower().split(':')[0]
    domain_no_www = re.sub(r'^www\.', '', domain)
    
    letters_full     = sum(c.isalpha() for c in domain_no_www)
    letters_no_tld   = sum(c.isalpha() for c in domain_no_www.rsplit('.', 1)[0])
    letters_path     = sum(c.isalpha() for c in parsed.path)
    
    print(f"URL             : {url}")
    print(f"domain_no_www   : {domain_no_www}")
    print(f"Stored letters  : {stored}")
    print(f"full domain     : {letters_full}")
    print(f"excl TLD        : {letters_no_tld}")
    print(f"path letters    : {letters_path}")
    print(f"excl TLD + path : {letters_no_tld + letters_path}")
    print()