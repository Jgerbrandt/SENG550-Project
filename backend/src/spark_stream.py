from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType, LongType, StructField
import random
import numpy as np
import pandas as pd

spark = SparkSession.builder \
    .appName("StockDataStream") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0") \
    .getOrCreate()

schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("timestamp", LongType(), True),
    StructField("volume", DoubleType(), True),
    StructField("exchange", StringType(), True),
    StructField("conditions", StringType(), True)
])

raw_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "stock_topic") \
    .load()

stock_df = raw_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

stock_data = {
    "AAPL": [],
    "AMZN": [],
    "TSLA": [],
    "GOOGL": [],
    "MSFT": []
}

predicted_data = {
    "AAPL": [] * 60,
    "AMZN": [] * 60,
    "TSLA": [] * 60,
    "GOOGL": [] * 60,
    "MSFT": [] * 60
}

def process_batch(batch_df, batch_id):
    for symbol in stock_data.keys():
        # filter for current stock
        symbol_df = batch_df.filter(col("symbol") == symbol).orderBy("timestamp")
        
        data_points = symbol_df.collect()
        
        for row in data_points:
            # append the price to the stock data
            stock_data[symbol].append(row["price"], row['volume'])
            
            # keep len60
            if len(stock_data[symbol]) > 60:
                stock_data[symbol].pop(0)
            
            # random prediction for now
            # TODO: implement actual prediction
            if len(stock_data[symbol]) == 60:
                # data to df for aaron(grrrr)
                df = pd.DataFrame(stock_data[symbol], columns=["price", "volume"])
                
                # rando prediction
                predicted_price = random.uniform(df["price"].min(), df["price"].max())
                
                # slide array and add new prediction
                predicted_data[symbol].append(predicted_price)
                if len(predicted_data[symbol]) > 61:
                    predicted_data[symbol].pop(0)
                
                raw_data = stock_data[symbol]
                prediction_array = predicted_data[symbol]
               
                #TODO: replace with DB write
                print(f"Symbol: {symbol}, Raw Array: {raw_data}, Prediction Array: {prediction_array}")


query = stock_df.writeStream \
    .foreachBatch(process_batch) \
    .outputMode("append") \
    .start()

query.awaitTermination()