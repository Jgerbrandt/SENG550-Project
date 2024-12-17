import os
from dotenv import load_dotenv
from pocketbase import Client
import pandas as pd

def authenticate_admin(client):
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    client.collection("_superusers").auth_with_password(admin_email, admin_password)

def export_collections_to_csv(client, output_dir, excluded_collections, excluded_fields):
    collections = client.collections.get_full_list()
    for collection in collections:
        collection_name = collection.name
        if collection_name in excluded_collections:
            continue
        records = client.collection(collection_name).get_full_list()
        data = [record.__dict__ for record in records]
        df = pd.DataFrame(data)
        df.drop(columns=excluded_fields, inplace=True, errors='ignore')
        csv_path = os.path.join(output_dir, f"{collection_name}.csv")
        df.to_csv(csv_path, index=False)
        print(f"Exported {collection_name} to {csv_path}")

if __name__ == "__main__":
    load_dotenv()
    output_dir = os.getcwd() + "/data"
    os.makedirs(output_dir, exist_ok=True)

    client = Client("http://127.0.0.1:8090") 
    authenticate_admin(client)

    excluded_collections = ["_superusers", "_authOrigins", "_externalAuths", "_mfas", "_otps"]
    excluded_fields = ["id", "created", "updated", "expand", "collection_id", "collection_name"]
    export_collections_to_csv(client, output_dir, excluded_collections, excluded_fields)