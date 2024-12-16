import websocket
import os
from dotenv import load_dotenv
from pocketbase import Client
from pocketbase.models.utils.schema_field import SchemaField
from pocketbase.models.collection import Collection
import json

def data_transform(ws, message):
    data = json.loads(message)
    if data['type'] == 'trade':
        for trade in data['data']:
            clean_data = {
                'symbol': trade['s'],
                'price': trade['p'],
                'timestamp': trade['t'],
                'volume': trade['v'],
                'conditions': trade['c'],
            }
            insert_data(clean_data)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    # ws.send('{"type":"subscribe","symbol":"AMZN"}')
    # ws.send('{"type":"subscribe","symbol":"TSLA"}')
    # ws.send('{"type":"subscribe","symbol":"GOOGL"}')
    # ws.send('{"type":"subscribe","symbol":"MSFT"}')

def insert_data(data):
    collection_name = data['symbol']
    
    # Check if the collection exists, if not, create it
    try:
        client.collections.get_one(collection_name)
    except:
        schema = [
            SchemaField(name="symbol", type="text", required=True),
            SchemaField(name="price", type="number", required=True),
            SchemaField(name="timestamp", type="number", required=True),
            SchemaField(name="volume", type="number", required=True),
            SchemaField(name="conditions", type="json", required=True)
        ]
        collection ={
            "name": collection_name,
            "schema": schema,
        }
        client.collections.create(collection)

    # Insert data into the collection
    client.collection(collection_name).create({
        "symbol": data['symbol'],
        "price": data['price'],
        "timestamp": data['timestamp'],
        "volume": data['volume'],
        "conditions": data['conditions']
    })

def authenticate_admin(client):
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    auth_data = client.admins.auth_with_password(admin_email, admin_password)
    return auth_data.token

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("API_KEY")

    client = Client("http://127.0.0.1:8090")
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    authData = client.collection("_superusers").auth_with_password(admin_email, admin_password);
    
    #websocket.enableTrace(True)

    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=" + TOKEN,
                              on_message = data_transform,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
