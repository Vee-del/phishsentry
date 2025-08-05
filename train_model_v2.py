import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

# Sample training dataset (expand later with real-world examples)
data = {
    "text": [
        "Click here to verify your account",
        "Urgent: your password has been stolen",
        "Hello, can we schedule a meeting?",
        "Free rewards! Claim now!",
        "Let’s catch up for coffee",
        "Update your payment information now",
        "Account suspended due to suspicious activity",
        "Here is the report you requested"
    ],
    "label": [1, 1, 0, 1, 0, 1, 1, 0]  # 1 = phishing, 0 = not phishing
}

# Create DataFrame
df = pd.DataFrame(data)

# Create ML pipeline with Random Forest
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# Train model
pipeline.fit(X_train, y_train)

# Evaluate performance
y_pred = pipeline.predict(X_test)
print("📊 Classification Report:\n", classification_report(y_test, y_pred))

# Save model
joblib.dump(pipeline, 'phish_detector_v2.joblib')
print("✅ Model saved as phish_detector_v2.joblib")
