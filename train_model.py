import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

# Sample dataset
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
    "label": [1, 1, 0, 1, 0, 1, 1, 0]  # 1 = phishing, 0 = not
}

df = pd.DataFrame(data)

# Create pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression())
])

# Split and train
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2)
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(pipeline, 'phish_detector.joblib')
print("✅ Model saved as phish_detector.joblib")
