import pandas as pd
from pymongo import MongoClient
import secrets


def send_data():
    mongo_url = secrets.mongo_host_connection("admin", "admin")
    database_name = "inventory"
    collection_name = "inventory"
    csv_file_path = "inventory.csv"

    client = MongoClient(mongo_url)
    db = client[database_name]
    collection = db[collection_name]  # Getting access to database and collection
    df = pd.read_csv(csv_file_path)

    data = df.to_dict(orient='records')  # Convert to dictionary

    collection.insert_many(data)  # Insert dictionary into MongoDB
    print("Data sent successfully!")


def ping():
    client = MongoClient(secrets.mongo_host_connection("admin", "admin"))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    send_data()
