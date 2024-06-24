from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb://localhost:27017"
MONGO_DATABASE = "py-group-chat"  # database name

client = AsyncIOMotorClient(MONGO_DETAILS)

# database
database = client.get_database(MONGO_DATABASE)

# collection
user_collection = database.get_collection("users")
chat_collection = database.get_collection("chats")
chat_user_collection = database.get_collection("chat_users")
participant_collection = database.get_collection("participants")
message_collection = database.get_collection("messages")
