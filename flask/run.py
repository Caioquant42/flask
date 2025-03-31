from flask import Flask
from app.api import bp as api_bp
from flask_cors import CORS
from app import create_app

app, celery = create_app()
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://46.202.149.154:5173", "https://zommaquant.com.br"]}}, supports_credentials=True)

if __name__ == '__main__':
    app.run(debug=True)