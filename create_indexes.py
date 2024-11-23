import os
import urllib

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

USERNAME = os.getenv("USERNAME", "")
PWD = os.getenv("PWD", "")

uri = (
    "mongodb+srv://"
    + urllib.parse.quote_plus(USERNAME)
    + ":"
    + urllib.parse.quote_plus(PWD)
    + "@cluster0.k3qwm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
client = MongoClient(uri)
collection = client["llm_task"]["purchase_order"]

indexes = [
    {"keys": [("Creation Date", 1)], "options": {}},
    {"keys": [("Creation Date", 1), ("Total Price", -1)], "options": {}},
    {"keys": [("Item Name", 1), ("Quantity", -1)], "options": {}},
    {"keys": [("Supplier Name", 1), ("Supplier Code", 1)], "options": {}},
    {"keys": [("Acquisition Type", 1), ("Sub-Acquisition Type", 1)], "options": {}},
    {"keys": [("Classification Codes", 1), ("Total Price", -1)], "options": {}},
    {"keys": [("Location", 1), ("Department Name", 1)], "options": {}},
    {"keys": [("Fiscal Year", 1)], "options": {}},
    {"keys": [("Purchase Order Number", 1)], "options": {}},
]

for index in indexes:
    collection.create_index(index["keys"], **index["options"])

print("Indexes created successfully!")
