import random
import time
from pocketbase import PocketBase

client = PocketBase('http://127.0.0.1:8090')

# Initialize data for each stock
stocks = ["AMZN", "AAPL", "GOOGL", "MSFT", "TSLA"]
data = {
    stock: {
        "actual": [random.randint(1, 100) for _ in range(60)],
        "predicted": [random.randint(1, 100) for _ in range(60)]
    }
    for stock in stocks
}

# Define the collections
collections = {
    "AMZNRaw": "AMZN",
    "AMZNPredicted": "AMZN",
    "AAPLRaw": "AAPL",
    "AAPLPredicted": "AAPL",
    "GOOGLRaw": "GOOGL",
    "GOOGLPredicted": "GOOGL",
    "MSFTRaw": "MSFT",
    "MSFTPredicted": "MSFT",
    "TSLARaw": "TSLA",
    "TSLAPredicted": "TSLA"
}

while True:
    try:
        for collection, stock in collections.items():
            entry = {}
            if "Raw" in collection:
                entry['data'] = data[stock]["actual"]
            else:
                entry['data'] = data[stock]["predicted"]
            client.collection(collection).create(entry)
            print(f"Created entry in {collection}")
    except Exception as e:
        print(e)
        time.sleep(1)

    # Update data with random increases and decreases
    for stock in stocks:
        actual_change = random.randint(-5, 5)
        predicted_change = random.randint(-5, 5)

        new_actual_value = max(0, data[stock]["actual"][-1] + actual_change)
        new_predicted_value = max(0, data[stock]["predicted"][-1] + predicted_change)

        data[stock]["actual"].append(new_actual_value)
        data[stock]["actual"].pop(0)

        data[stock]["predicted"].append(new_predicted_value)
        data[stock]["predicted"].pop(0)

    time.sleep(1)