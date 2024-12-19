import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

def predict_from_df(model, df, stock_id=0, window_size=60):
    """
    Given a model and a DataFrame of the correct size (window_size rows),
    this function returns the predicted next value for the 'close' price.

    Parameters:
    - model: A loaded TensorFlow Keras model that expects inputs [X, stock_id].
    - df: DataFrame containing columns ['timestamp', 'close', 'high', 'low', 'trade_count', 'open', 'volume', 'vwap']
          and exactly `window_size` rows.
    - stock_id: Integer representing the stock ID. Defaults to 0 if only one stock or no embedding needed.
    - window_size: Number of time steps used by the model input.

    Returns:
    - prediction: A single float representing the predicted scaled close value.
      If the model was trained on scaled values, this will be in scaled terms. 
      If you want it in original scale, you need the original scaler to inverse_transform.
    """
    required_cols = ['price', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"DataFrame must contain column '{col}'.")

    if len(df) != window_size:
        raise ValueError(f"DataFrame must have exactly {window_size} rows for one prediction.")

    # Extract features
    features = df[required_cols].values

    # Scale features
    # NOTE: If you want consistent predictions with training, load the training scaler instead of fitting a new one.
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(features)

    # The model expects: X input of shape (1, window_size, num_features)
    # and stock_id input of shape (1, )
    X_input = np.expand_dims(scaled_features, axis=0)      # shape: (1, window_size, 7)
    stock_id_input = np.array([stock_id])                  # shape: (1, )

    # Predict
    prediction = model.predict([X_input, stock_id_input])
    # prediction is a numpy array of shape (1,1), extract the value
    prediction_value = prediction[0, 0]

    return prediction_value


# Example usage (not part of the function, just a demonstration):
# Assume you have a model saved at 'saved_model.keras' and a df prepared for prediction:
# model = tf.keras.models.load_model("saved_model.keras")
# prediction = predict_from_df(model, df=my_df_of_length_60)
# print("Predicted Value:", prediction)
