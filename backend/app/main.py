from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import db
from sentiment.sentiment import analyze_sentiment_vader, analyze_sentiment_transformers

app = FastAPI()

@app.post("/analyze-sentiment")
async def analyze_sentiment(review: str):
    sentiment, sentiment_score = analyze_sentiment_vader(review)
    return {"sentiment": sentiment, "score": sentiment_score}

@app.post("/save-review")
async def save_review(review: str):
    # Analyze sentiment using Vader
    sentiment, sentiment_score = analyze_sentiment_vader(review)
    
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

    # Analyze sentiment for each review using the transformer model
    results = [{"review": review, "sentiment": analyze_sentiment_transformers(review)} for review in reviews]
    
    return {"destination": destination, "reviews": results}
