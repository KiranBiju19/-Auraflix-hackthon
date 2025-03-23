import string
from collections import Counter
import nltk
import sklearn_crfsuite
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn_crfsuite import metrics
from nltk.tokenize import word_tokenize, WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer

# Ensure NLTK downloads
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
tk = WhitespaceTokenizer()

# Step 1: Preprocess Text
def preprocess_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:

        text = file.read().lower()
        cleaned_text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(cleaned_text, "english")
    return tokens

# Step 2: Extract Features
def extract_features(tokens):
    features = []
    for i, word in enumerate(tokens):
        feature = {
            'word': word,
            'is_upper': word.isupper(),
            'is_title': word.istitle(),
            'is_digit': word.isdigit(),
            'suffix': word[-3:],  # last 3 characters
            'prefix': word[:3],   # first 3 characters
            'length': len(word),
        }
        features.append(feature)
    return features

# Step 3: Prepare Data for CRF
def prepare_data(tokens, emotions_file):
    with open(emotions_file, "r") as file:
        emotion_dict = {}
        for line in file:
            tokenized_line = tk.tokenize(line.strip())
            if len(tokenized_line) >= 2:
                emotion_dict[tokenized_line[0].lower()] = tokenized_line[1]

    features = extract_features(tokens)
    labels = [emotion_dict.get(word,emotion_dict.get(lemmatizer.lemmatize(word),"NEU")) for word in tokens]
    return features, labels

# Step 4: Train CRF Model 
def train_crf(features, labels):
    X = [features]
    y = [labels]
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1, 
        max_iterations=100,
        all_possible_transitions=True
    )
    crf.fit(X, y)
    return crf

# Step 5: Sentiment Analysis with CRF
def predict_crf(crf_model, tokens):
    features = extract_features(tokens)
    predictions = crf_model.predict([features])[0]
    return predictions

# Main Script
if __name__ == "__main__":
    # Paths
    text_path = r"C:\Users\krish\Downloads\read.txt"
    emotions_path = r"C:\Users\krish\Downloads\emotions.txt"

    # Preprocess Text
    tokens = preprocess_text(text_path)

    # Prepare Data
    features, labels = prepare_data(tokens, emotions_path)

    # Train CRF Model
    crf = train_crf(features, labels)

    # Predict on New Data
    predictions = predict_crf(crf, tokens)
    counts = len(tokens)
    print("\n")
    for i in range(0,counts):
        print(tokens[i]+" : ",end="")
        print(predictions[i])
    

    # Emotion Distribution
    emotion_counts = Counter(predictions)
    print("Emotion Counts:", emotion_counts)

    #python package
    def sentiment_analyse(sentiment_text):
        score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
        print(score)
        if score['neg'] > score['pos']:
            print("Negative Reviews Prevail")
        elif score['neg'] < score['pos']:
            print("Positive Reviews Prevail")
        else:
            print("Neutral Sentiment")

f1 = open(r"C:\Users\krish\Downloads\read.txt", "r")
text = f1.read()
lower_case = text.lower()
cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
sentiment_analyse(cleaned_text)

# Plot Emotion Counts
import matplotlib.pyplot as plt
fig, ax1 = plt.subplots()
ax1.bar(emotion_counts.keys(), emotion_counts.values())
plt.title("Emotion Distribution")
plt.xlabel("Emotions")
plt.ylabel("Frequency")
plt.savefig('crf_emotion_graph.png')
plt.show()