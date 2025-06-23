# train_model.py
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MultiLabelBinarizer

# Dummy training data — add more real resume data for better performance
texts = [
    "John Doe is a Software Engineer skilled in Python, Java, and SQL. Holds a B.Tech in Computer Science.",
    "Completed AWS Certified Solutions Architect and Microsoft Certified: Azure Fundamentals.",
    "Worked as a data analyst at XYZ Corp. B.Sc in Information Technology."
]

labels = [
    ["Skills", "Education"],
    ["Certifications"],
    ["Skills", "Education"]
]

# Convert labels into multi-label format
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(labels)

# TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(texts)

# Train model
model = OneVsRestClassifier(KNeighborsClassifier(n_neighbors=3))
model.fit(X, y)

# Save vectorizer, label binarizer, and model
with open('model.pkl', 'wb') as f:
    pickle.dump((vectorizer, mlb, model), f)

print("✅ Training complete. Model saved to model.pkl")
# This script trains a simple KNN model for resume parsing and saves the model, vectorizer, and label binarizer.