from flask import flash,render_template, make_response, url_for, redirect
from flask_restful import Resource
from models.guarderias import Guarderias
from db import db
from flask_login import login_required, current_user

class GuarderiaController(Resource):
    @login_required
    def get(self):
        if not current_user.is_admin:
            flash("No tienes permiso para acceder a esta página (Guarderias)", "danger")
            return redirect(url_for('main'))  # Redirige a la página principal
        guarderias = Guarderias.query.all()
        return make_response(render_template("guarderias.html", guarderias=guarderias))

