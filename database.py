from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import os

load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")
app_name = os.getenv("MONGO_APP_NAME")

if not username or not password or not cluster or not app_name:
    raise EnvironmentError("One or more MongoDB environment variables are missing.")

encoded_password = quote_plus(password)
uri = f"mongodb+srv://{username}:{encoded_password}@{cluster}/?retryWrites=true&w=majority&appName={app_name}"

client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    db = client["student_management_system"]   
    students_collection = db["students"]  
except Exception as e:
    print(e)

