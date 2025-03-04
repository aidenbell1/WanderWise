import motor.motor_asyncio
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import requests

app = FastAPI()

# Load pre-trained sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis")

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client["wanderwise_db"]

analyzer = SentimentIntensityAnalyzer()

@app.post("/analyze-sentiment")
async def analyze_sentiment(review: str):
    sentiment_score = analyzer.polarity_scores(review)
    sentiment = "positive" if sentiment_score["compound"] > 0 else "negative" if sentiment_score["compound"] < 0 else "neutral"
    return {"sentiment": sentiment, "score": sentiment_score}

@app.post("/save-review")
async def save_review(review: str):
    # Analyze sentiment
    sentiment_score = analyzer.polarity_scores(review)
    sentiment = "positive" if sentiment_score["compound"] > 0 else "negative" if sentiment_score["compound"] < 0 else "neutral"
    
    # Store the review and sentiment data
    review_data = {
        "review": review,
        "sentiment": sentiment,
        "score": sentiment_score
    }
    
    # Save to MongoDB
    await db.reviews.insert_one(review_data)
    
    return {"message": "Review saved successfully!", "data": review_data}

@app.get("/db-test")
async def db_test():
    test_collection = db["test_collection"]
    data = await test_collection.find_one({"name": "test"})
    return {"message": "Connected to MongoDB", "data": data}

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React frontend to connect
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

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
