from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nulleable=False)
    apellido = db.Column(db.String(50), nulleable=False)
    correo = db.Column(db.String(100), unique=True, nulleable=False)
    contrasena = db.Column(db.String(94), nulleable=False)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now())
