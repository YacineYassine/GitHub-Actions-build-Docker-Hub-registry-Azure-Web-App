import os
import psycopg2  # ← CHANGER: psycopg2 au lieu de sqlite3
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DB_CONFIG = {
    'host': 'iris-db.cj2wyc8csa0m.ca-central-1.rds.amazonaws.com',
    'database': 'iris_prod', 
    'user': 'postgres',
    'password': os.getenv('DB_PASSWORD'),
    'port': 5432,
    'sslmode': 'require'  # ← AJOUTER CETTE LIGNE
}

app = Flask(__name__)

def init_db():
    """Vérifier la connexion RDS - la table existe déjà"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.close()
        print("✅ Connexion RDS réussie")
    except Exception as e:
        print(f"❌ Erreur connexion RDS: {e}")

def save_prediction(features, prediction, confidence):
    """Sauvegarder une prédiction dans RDS"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions 
            (sepal_length, sepal_width, petal_length, petal_width, prediction, confidence)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (*features, str(prediction), float(confidence)))
        
        conn.commit()
        conn.close()
        print("✅ Prédiction sauvegardée dans RDS")
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde RDS: {e}")
        return False

def save_feedback(features, prediction, approved):
    """Sauvegarder un feedback dans RDS"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions 
            (sepal_length, sepal_width, petal_length, petal_width, prediction, feedback)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (*features, prediction, approved))
        
        conn.commit()
        conn.close()
        print("✅ Feedback sauvegardé dans RDS")
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde feedback RDS: {e}")
        return False

# Initialiser la connexion RDS
init_db()

# Charger le modèle
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
        
        # SAUVEGARDER DANS RDS
        save_prediction(features, prediction, confidence)
        
        return jsonify({
            'prediction': str(prediction),
            'confidence': float(confidence)
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