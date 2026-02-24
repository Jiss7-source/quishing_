import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
MODEL_PATH = "model/trained_model.pkl"
import joblib

MODEL_PATH = "model/trained_model.pkl"


def normalize_url(url):
    url = str(url)
    if not url.startswith("http"):
        return "https://" + url
    return url


def train_model():
    # Load dataset (already cleaned)
    data = pd.read_csv("dataset/phishing_dataset.csv")

    # Remove duplicates
    data = data.drop_duplicates()

    # Normalize URLs
    def normalize(url):
        url = str(url).strip()
        if not url.startswith("http"):
            return "https://" + url
        return url

    data['url'] = data['url'].apply(normalize)

    # Balance dataset
    phishing = data[data['type'] == 'phishing']
    benign = data[data['type'] == 'benign']

    min_size = min(len(phishing), len(benign))

    phishing_sample = phishing.sample(min_size, random_state=42)
    benign_sample = benign.sample(min_size, random_state=42)

    data = pd.concat([phishing_sample, benign_sample])
    data = data.sample(frac=1, random_state=42)

    X = data['url']
    y = data['type']

    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(
        analyzer='char',
        ngram_range=(3, 5)
    )

    X_vectorized = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized,
        y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded
    )

    model = LogisticRegression(max_iter=1000, class_weight='balanced')
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print("Model Accuracy:", accuracy)

    joblib.dump((model, vectorizer, label_encoder), MODEL_PATH)
    print("Model saved successfully!")

def predict_url(url):
    model, vectorizer, label_encoder = joblib.load(MODEL_PATH)

    # Normalize input
    url = str(url).strip()
    if not url.startswith("http"):
        url = "https://" + url

    url_vectorized = vectorizer.transform([url])
    prediction = model.predict(url_vectorized)

    label = label_encoder.inverse_transform(prediction)

    return label[0]