from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <h1>ABBAOU Yacine</h1>
    <h1>Hello World from Flask in Docker!</h1>
    <p>Application déployée sur Azure App Service</p>
    <p>Port utilisé: {}</p>
    '''.format(os.environ.get('PORT', '5000'))

@app.route('/health')
def health():
    return {'status': 'healthy', 'port': os.environ.get('PORT', '5000')}

if __name__ == '__main__':
    # Essayer plusieurs variables d'environnement
    port = int(os.environ.get('PORT', 
               os.environ.get('WEBSITES_PORT', 
               os.environ.get('HTTP_PLATFORM_PORT', 5000))))
    
    print(f"Starting Flask app on port: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)