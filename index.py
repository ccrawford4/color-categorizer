import pandas as pd
from fastapi import FastAPI
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from fastapi.responses import PlainTextResponse
import mangum
import os

# Load dataset and preprocess
# For simplicity, we will assume it's bundled with the Lambda deployment package.
data = pd.read_csv("colors.csv")  # Ensure your CSV file is available
X = data[["red", "green", "blue"]]
y = data["label"]

# Encode labels as numbers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train/Test Split (though this is a Lambda function, this part is done once during deployment)
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train a model (this might be done at deploy time and saved as a pickle or joblib file in Lambda Layer or S3)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Creating the FastAPI app
app = FastAPI()

color_map = {
    "Pink": "pink",
    "Red": "red",
    "Orange": "orange",
    "Yellow": "yellow",
    "Green": "green",
    "Blue": "blue",
    "Purple": "violet",
    "Black": "black",
    "Brown": "brown",
    "Grey": "grey",
    "White": "white",
}

@app.get("/{hex_color:path}", response_class=PlainTextResponse)
def predict_color(hex_color: str):
    try:
        # Remove the # if present
        if hex_color.startswith("#"):
            hex_color = hex_color[1:]

        # Validate HEX format
        if len(hex_color) != 6 or not all(c in "0123456789ABCDEFabcdef" for c in hex_color):
            return PlainTextResponse("Invalid HEX color", status_code=400)

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        # Predict the color
        prediction = model.predict([[r, g, b]])[0]
        predicted_label = label_encoder.inverse_transform([prediction])[0]
        return color_map[predicted_label]
    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)

# Wrap the FastAPI app with Mangum to handle Lambda requests
handler = mangum.Mangum(app)