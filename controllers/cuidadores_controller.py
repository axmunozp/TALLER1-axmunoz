from flask import render_template, make_response
from flask_restful import Resource
from models.cuidadores import Cuidadores
from db import db
from flask_login import login_required



class CuidadorController(Resource):
    @login_required
    def get(self):
        cuidadores = Cuidadores.query.all()
        return make_response(render_template("cuidadores.html", cuidadores=cuidadores))