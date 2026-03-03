import sys
sys.path.append(r"C:\Users\jizzm\OneDrive\quishing_project\modules")

import pandas as pd
from sklearn.utils import resample

print("Loading dataset...")
df = pd.read_csv(r"C:\Users\jizzm\OneDrive\quishing_project\dataset\phishing_dataset.csv")

df = df[df['type'].isin(['benign', 'phishing'])]
df['Label'] = df['type'].apply(lambda x: 0 if x == 'benign' else 1)
df = df[['url', 'Label']].rename(columns={'url': 'URL'})
df = df.drop_duplicates().dropna()

print("\n--- RAW URLs BEFORE fix_url (first 5 benign) ---")
print(df[df['Label'] == 0]['URL'].head().tolist())

print("\n--- RAW URLs BEFORE fix_url (first 5 phishing) ---")
print(df[df['Label'] == 1]['URL'].head().tolist())

def fix_url(url):
    url = str(url).strip()
    if not url.startswith('http'):
        url = 'http://' + url
    return url

df['URL'] = df['URL'].apply(fix_url)

print("\n--- URLs AFTER fix_url (first 5 benign) ---")
print(df[df['Label'] == 0]['URL'].head().tolist())

print("\n--- URLs AFTER fix_url (first 5 phishing) ---")
print(df[df['Label'] == 1]['URL'].head().tolist())

print("\n--- Average URL length per class AFTER fix_url ---")
df['url_len'] = df['URL'].apply(len)
print(df.groupby('Label')['url_len'].mean().round(2))

print("\n--- URLs starting with https per class ---")
df['has_https'] = df['URL'].apply(lambda x: x.startswith('https'))
print(df.groupby('Label')['has_https'].mean().round(3))
