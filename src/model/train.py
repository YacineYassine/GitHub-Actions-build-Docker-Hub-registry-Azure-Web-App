from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import joblib
import os

# Charger données Iris
iris = load_iris()
X, y = iris.data, iris.target

# Entraîner modèle
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Sauvegarder
os.makedirs('../model', exist_ok=True)
joblib.dump(model, 'iris_model.pkl')
print("Modèle entraîné et sauvegardé!")