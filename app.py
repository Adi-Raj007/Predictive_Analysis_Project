from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

MODEL_PATH = 'model.pkl'

@app.route('/')
def home():
    return "Welcome to the Predictive Analysis API"

@app.route('/favicon.ico')
def favicon():
    return '', 204
@app.route('/upload', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    data = pd.read_csv(file)
    data.to_csv('uploaded_data.csv', index=False)
    return jsonify({"message": "File uploaded successfully", "data_preview": data.head().to_dict()}), 200

@app.route('/train', methods=['POST'])
def train_model():
    if not os.path.exists('uploaded_data.csv'):
        return jsonify({"error": "No dataset uploaded. Please upload a dataset first."}), 400

    data = pd.read_csv('uploaded_data.csv')
    X = data[['Temperature', 'Run_Time']]
    y = data['Downtime_Flag']

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    return jsonify({"message": "Model trained successfully"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    if not os.path.exists(MODEL_PATH):
        return jsonify({"error": "Model not trained. Please train the model first."}), 400

    model = joblib.load(MODEL_PATH)

    input_data = request.get_json()
    df = pd.DataFrame([input_data])
    prediction = model.predict(df)
    confidence = model.predict_proba(df).max()

    return jsonify({"Downtime": "Yes" if prediction[0] == 1 else "No", "Confidence": round(confidence, 2)})

if __name__ == '__main__':
    app.run(debug=True)
