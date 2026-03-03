# save as diagnose_length.py in project root
import pandas as pd

df = pd.read_csv('dataset/PhiUSIIL_Phishing_URL_Dataset.csv')
sample = df.head(5)

for _, row in sample.iterrows():
    url = row['URL']
    stored_len = int(row['URLLength'])
    stored_letters = int(row['NoOfLettersInURL'])
    stored_special = int(row['NoOfOtherSpecialCharsInURL'])
    
    print(f"\nURL: {url}")
    print(f"Stored URLLength       : {stored_len}")
    print(f"len(full url)          : {len(url)}")
    print(f"len(url) - https://    : {len(url) - 8}")
    print(f"len(url) - http://     : {len(url) - 7}")
    print(f"len(url) - https://www.: {len(url) - 12}")
    print(f"---")
    print(f"Stored NoOfLetters     : {stored_letters}")
    print(f"letters in full url    : {sum(c.isalpha() for c in url)}")
    print(f"letters in url[8:]     : {sum(c.isalpha() for c in url[8:])}")
    print(f"letters in url[12:]    : {sum(c.isalpha() for c in url[12:])}")
    print(f"---")
    print(f"Stored NoOfSpecial     : {stored_special}")
    normal = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/:@')
    normal2 = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    print(f"special (excl /:@)     : {sum(1 for c in url if c not in normal)}")
    print(f"special (alpha/digit)  : {sum(1 for c in url if c not in normal2)}")
    print(f"special in url[8:]     : {sum(1 for c in url[8:] if c not in normal)}")
    print(f"dots in domain         : {url[8:].split('/')[0].count('.')}")