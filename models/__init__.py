# models/__init__.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from cryptography.fernet import Fernet
import os

db = SQLAlchemy()

key = os.environ.get('ENCRYPTION_KEY', Fernet.generate_key())
cipher_suite = Fernet(key)

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(15))
    profile_picture = db.Column(db.String(200))
    
    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = generate_password_hash(plaintext)
    
    def check_password(self, plaintext):
        return check_password_hash(self._password, plaintext)
    
    def encrypt_sensitive_data(self):
        self.phone_number = cipher_suite.encrypt(self.phone_number.encode()).decode()
        self.address = cipher_suite.encrypt(self.address.encode()).decode()
    
    def save(self):
        self.encrypt_sensitive_data()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.username}>"
