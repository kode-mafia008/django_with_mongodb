import os
from pymongo import MongoClient

def get_mongo_client():
    """
    Returns a MongoDB client instance.
    Can be called from Django settings.
    """
    try:
        # Get connection details from environment variables
        mongo_host = os.getenv('MONGO_HOST', 'mongo')
        mongo_port = int(os.getenv('MONGO_PORT', 27017))
        mongo_user = os.getenv('MONGO_INITDB_ROOT_USERNAME', 'root')
        mongo_password = os.getenv('MONGO_INITDB_ROOT_PASSWORD', 'example')
        
        # Build connection string
        connection_string = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/?authSource=admin"
        
        # Create and return client
        client = MongoClient(connection_string)
        
        # Test the connection
        client.admin.command('ping')
        print(f"MongoDB connected successfully to {mongo_host}:{mongo_port}")
        
        return client
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        raise Exception("Failed to connect to MongoDB: ", e)

def get_mongo_database(db_name='nitapp'):
    """
    Returns a specific MongoDB database instance.
    """
    if db_name is None:
        db_name = os.getenv('MONGO_DB_NAME', 'nitman_db')
    
    client = get_mongo_client()
    return client[db_name]


# Initialize client (optional - for direct usage)
mongo_client = None
mongo_db = None

try:
    mongo_client = get_mongo_client()
    mongo_db = get_mongo_database()
except Exception as e:
    print(f"Warning: MongoDB not initialized - {e}")

