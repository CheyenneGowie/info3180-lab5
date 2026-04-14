from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)

import os
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'app/uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Info3180@localhost/lab5"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

from app import views