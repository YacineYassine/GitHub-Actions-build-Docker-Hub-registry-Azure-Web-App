import os
import sqlite3 
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Initialiser la base de données
def init_db():
    """Initialiser la base de données SQLite"""
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'feedbacks.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sepal_length REAL,
            sepal_width REAL,
            petal_length REAL,
            petal_width REAL,
            prediction TEXT,
            approved BOOLEAN,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_feedback(features, prediction, approved):
    """Sauvegarder un feedback utilisateur"""
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'feedbacks.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO feedbacks 
        (sepal_length, sepal_width, petal_length, petal_width, prediction, approved)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (*features, prediction, approved))
    
    conn.commit()
    conn.close()

# Initialiser la base de données
init_db()

# CHARGER LE MODÈLE (AJOUTEZ CETTE PARTIE)
model_path = os.path.join(os.path.dirname(__file__), 'model', 'iris_model.pkl')
model = joblib.load(model_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        features = [data['sepal_length'], data['sepal_width'], 
                   data['petal_length'], data['petal_width']]
        
        prediction = model.predict([features])[0]
        confidence = np.max(model.predict_proba([features]))
        
        return jsonify({
            'prediction': str(prediction),  # ← CONVERTIR en string
            'confidence': float(confidence)  # ← CONVERTIR en float Python
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/feedback', methods=['POST'])
def feedback():
    try:
        data = request.json
        features = [data['sepal_length'], data['sepal_width'], 
                   data['petal_length'], data['petal_width']]
        
        save_feedback(features, data['prediction'], data['approved'])
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask app on port: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)