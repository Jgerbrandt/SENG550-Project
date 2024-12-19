import random
import time

POCKETBASE_URL = 'http://127.0.0.1:8090'

# General imports =================================================================================
import os
from pocketbase import Client
from dotenv import load_dotenv



if __name__ == "__main__":
    load_dotenv()

    client = Client(POCKETBASE_URL)
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    client.admins.auth_with_password(admin_email, admin_password)
    authData = client.collection("_superusers").auth_with_password(admin_email, admin_password)

    actual_data = []
    predicted_data = [0] * 61

    for i in range(60):
        random_number = random.randint(1, 100)
        actual_data.append(random_number)

    while True:
        try:
            entry = {}
            entry['ml'] = predicted_data
            entry['actual'] = actual_data
            client.collection("AMZN").create(entry)
            print("created entry")
        except Exception as e:
            print(e)
            time.sleep(1)

        random_number = random.randint(1, 100)
        actual_data.append(random_number)
        actual_data.pop(0)

        predicted_data.append(random_number + 20)
        predicted_data.pop(0)

        time.sleep(1)

