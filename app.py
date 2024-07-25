from flask import Flask, request, render_template, redirect, url_for
from flask_restful import Api
from flask_login import LoginManager, login_required, login_user, current_user
from dotenv import load_dotenv
import os
from db import db
from controllers.guarderia_controller import GuarderiaController
from controllers.perros_controller import PerroController
from controllers.cuidadores_controller import CuidadorController
from models.user import User


# Cargar variables de entorno desde el archivo .env
load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_database = os.getenv('DB_DATABASE')
secret_key = os.urandom(24)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_database}"
app.config["SECRET_KEY"] = secret_key
db.init_app(app)
api = Api(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(id):
    user = User.query.get(id)
    if user:
        return user
    return None

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            if user.is_admin:
                return redirect(url_for("perrocontroller"))
            else:
                return redirect(url_for("main"))
        
    return render_template("login.html", error="Credenciales inválidas")

api.add_resource(GuarderiaController, '/guarderias')
api.add_resource(PerroController, '/perros')
api.add_resource(CuidadorController, '/cuidadores')