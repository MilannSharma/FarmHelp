from flask import Flask, render_template, request, jsonify
import os
import joblib
import numpy as np
import warnings
from config import Config
from datetime import datetime

warnings.filterwarnings("ignore")

app = Flask(__name__)
app.config.from_object(Config)
model = joblib.load("model.pkl")

# Initialize knowledge processor (lazy loading)
knowledge_processor = None

def get_knowledge_processor():
    """Lazy load the knowledge processor"""
    global knowledge_processor
    if knowledge_processor is None:
        try:
            from knowledge_processor import AgricultureKnowledgeProcessor
            knowledge_processor = AgricultureKnowledgeProcessor()
            print("🧠 Knowledge processor initialized")
        except Exception as e:
            print(f"⚠️  Could not initialize knowledge processor: {str(e)}")
            knowledge_processor = None
    return knowledge_processor

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('predict.html')
    try:
        if request.form.get('temperature'):
            temp = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            ph = float(request.form['ph'])
            rainfall = float(request.form['rainfall'])
        else:
            temp = float(request.form.get('temperatureManual', 0))
            humidity = float(request.form.get('humidityManual', 0))
            ph = float(request.form.get('ph', 0))
            rainfall = float(request.form.get('rainfall', 0))

        input_data = np.array([[temp, humidity, ph, rainfall]])
        prediction = model.predict(input_data)[0]

        blog_suggestions = [
            {"title": "Top 10 Tips for Successful Farming", "url": "https://exampleblog.com/farming-tips"},
            {"title": "How to Improve Soil Quality", "url": "https://exampleblog.com/soil-quality"},
            {"title": "Pest Control Methods for Crops", "url": "https://exampleblog.com/pest-control"}
        ]
        video_suggestions = [
            {"title": "Farming Basics for Beginners", "url": "https://www.youtube.com/watch?v=example1"},
            {"title": "Advanced Crop Management", "url": "https://www.youtube.com/watch?v=example2"},
            {"title": "Sustainable Agriculture Practices", "url": "https://www.youtube.com/watch?v=example3"}
        ]

        return render_template('result.html', prediction=prediction, blogs=blog_suggestions, videos=video_suggestions)
    except Exception as e:
        return f"Error: {e}"

@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()
    input_data = np.array([[data['temperature'], data['humidity'], data['ph'], data['rainfall']]])
    prediction = model.predict(input_data)[0]
    return jsonify({"crop": prediction})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Starting Farmer Guider AI Flask application on port {port}...")
    app.run(host='0.0.0.0', port=port)
