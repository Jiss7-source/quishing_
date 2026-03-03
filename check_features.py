# check_features.py — save in project root
import pandas as pd
import sys
sys.path.append('modules')
from feature_extractor import extract_features

df = pd.read_csv('dataset/PhiUSIIL_Phishing_URL_Dataset.csv')
sample = df.head(3)

FEATURE_COLUMNS = [
    'URLLength', 'DomainLength', 'IsDomainIP', 'TLDLength',
    'NoOfSubDomain', 'HasObfuscation', 'NoOfObfuscatedChar',
    'ObfuscationRatio', 'NoOfLettersInURL', 'LetterRatioInURL',
    'NoOfDegitsInURL', 'DegitRatioInURL', 'NoOfEqualsInURL',
    'NoOfQMarkInURL', 'NoOfAmpersandInURL',
    'NoOfOtherSpecialCharsInURL', 'SpacialCharRatioInURL', 'IsHTTPS'
]

for _, row in sample.iterrows():
    url = row['URL']
    print(f"\nURL: {url}")
    print(f"{'Feature':<30} {'Dataset':>10} {'Extractor':>10} {'Match':>8}")
    print("-" * 62)
    extracted = extract_features(url)
    for i, col in enumerate(FEATURE_COLUMNS):
        dataset_val   = round(float(row[col]), 4)
        extractor_val = round(float(extracted[i]), 4)
        match = "✓" if dataset_val == extractor_val else "✗ DIFF"
        print(f"  {col:<28} {dataset_val:>10} {extractor_val:>10} {match:>8}")