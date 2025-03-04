from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# Load pre-trained sentiment analysis model (Hugging Face)
sentiment_pipeline = pipeline("sentiment-analysis")

# Initialize Vader Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_vader(review: str):
    sentiment_score = analyzer.polarity_scores(review)
    sentiment = "positive" if sentiment_score["compound"] > 0 else "negative" if sentiment_score["compound"] < 0 else "neutral"
    return sentiment, sentiment_score

def analyze_sentiment_transformers(review: str):
    return sentiment_pipeline(review)[0]