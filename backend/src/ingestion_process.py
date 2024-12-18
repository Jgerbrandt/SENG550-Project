import websocket
import os
from dotenv import load_dotenv
from pocketbase import Client
from pocketbase.models.collection import Collection
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType
import pandas as pd
from datetime import datetime
from kafka import KafkaProducer

def data_transform(ws, message):
    data = json.loads(message)
    if isinstance(data, list):
        for trade in data:
            if trade['T'] == 't':
                try:
                    timestamp_unix = int(datetime.fromisoformat(trade['t'].replace('Z', '+00:00')).timestamp() * 1000)
                    clean_data = {
                        'symbol': trade['S'],
                        'price': trade['p'],
                        'timestamp': timestamp_unix,
                        'volume': trade['s'],
                        'exchange': trade['x'],
                        'conditions': json.dumps(trade['c']),
                    }
                    if '@' in trade['c']:
                        insert_data(clean_data)
                        producer.send('stock_topic', clean_data)
                except Exception as e:
                    print(f"Error processing trade data: {e}")

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    auth_data = {
        "action": "auth",
        "key": os.getenv("API_KEY"),
        "secret": os.getenv("SECRET_KEY")
    }
    ws.send(json.dumps(auth_data))
    listen_message = {
        "action": "subscribe",
        "trades": ["AAPL", "AMZN", "TSLA", "GOOGL", "MSFT"]
    }
    ws.send(json.dumps(listen_message))

def insert_data(data):
    collection_name = data['symbol']
    
    # Check if the collection exists, if not, create it
    try:
        client.collections.get_one(collection_name)
    except:
        client.collections.create({
            "name": collection_name,
            "type": "base",
            "fields": [
                {
                    "name": "symbol",
                    "type": "text",
                    "required": True,
                },
                {
                    "name": "price",
                    "type": "number",
                    "required": True,
                },
                {
                    "name": "timestamp",
                    "type": "number",
                    "required": True,
                },
                {
                    "name": "volume",
                    "type": "number",
                    "required": True,
                },
                {
                    "name": "exchange",
                    "type": "text",
                    "required": True,
                },
                {
                    "name": "conditions",
                    "type": "json",
                    "required": True,
                },
            ],
        })

    # Insert data into the collection
    client.collection(collection_name).create({
        "symbol": data['symbol'],
        "price": data['price'],
        "timestamp": data['timestamp'],
        "volume": data['volume'],
        "exchange": data['exchange'],
        "conditions": data['conditions']
    })

if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    client = Client("http://127.0.0.1:8090")
    authData = client.collection("_superusers").auth_with_password(admin_email, admin_password);

    producer = KafkaProducer(bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))


    ws = websocket.WebSocketApp(
        "wss://stream.data.alpaca.markets/v2/iex",
        header=[
            f"APCA-API-KEY-ID: {API_KEY}",
            f"APCA-API-SECRET-KEY: {SECRET_KEY}"
        ],
        on_message=data_transform,
        on_error=on_error,
        on_close=on_close
    )

    ws.on_open = on_open
    ws.run_forever()

