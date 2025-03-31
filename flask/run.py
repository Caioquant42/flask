from flask import Flask
from app.api import bp as api_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://46.202.149.154:5173", "https://zommaquant.com.br"]}}, supports_credentials=True)
    app.register_blueprint(api_bp, url_prefix='/api')
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)