# app.py

from flask import Flask, jsonify
from config import config
from models import db
from flask_migrate import Migrate
from resources import api_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Register API routes
app.register_blueprint(api_bp, url_prefix='/api')

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'An internal error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
