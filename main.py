from flask_cors import CORS
from flask import Flask
from config.app_config import AppConfig
from routes.auth import auth_bp
from routes.player import player_bp
from routes.quest import quest_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = AppConfig.SECRET_KEY
    CORS(app, supports_credentials=True)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(player_bp, url_prefix='/player')
    app.register_blueprint(quest_bp, url_prefix='/quest')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)