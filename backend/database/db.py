import motor.motor_asyncio

# MongoDB connection
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client["wanderwise_db"]
