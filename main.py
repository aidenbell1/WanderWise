from fastapi import FastAPI
from transformers import pipeline
import requests

app = FastAPI()

# Load pre-trained sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis")

@app.get("/")
def home():
    return {"message": "Sentiment Analysis API is running!"}

@app.get("/sentiment/")
def get_sentiment(destination: str):
    # Fetch reviews
    reviews = [
        f"The beaches in {destination} are amazing!",
        f"The food in {destination} was overpriced.",
        f"{destination} has a great cultural atmosphere."
    ]

    # Analyze sentiment for each review
    results = [{"review": review, "sentiment": sentiment_pipeline(review)[0]} for review in reviews]
    
    return {"destination": destination, "reviews": results}
