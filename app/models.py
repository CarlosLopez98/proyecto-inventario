from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime, string, random


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(94), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now())
    movimientos = db.relationship('Movimiento', lazy='dynamic')

    def generate_password(self):
        caracteres = string.ascii_letters + '123456789$%&/'
        password = ''

        for i in range(10):
            password += random.choice(caracteres)

        return password

    def verify_password(self, contrasena_clean):
        # contrasena_clean es la contraseña sin encriptar
        return check_password_hash(self.contrasena, contrasena_clean)

    @property
    def password(self):
        pass

    @password.setter
    def password(self, value):
        self.contrasena = generate_password_hash(value)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    @classmethod
    def create_element(cls, nombre, apellido, correo, password):
        usuario = Usuario(nombre=nombre, apellido=apellido,
                          correo=correo, password=password)

        db.session.add(usuario)
        db.session.commit()

        return usuario

    @ classmethod
    def update_element(cls, id, nombre, apellido, correo, password):
        usuario = Usuario.get_by_id(id)

        if usuario is None:
            return False

        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.correo = correo

        db.session.add(usuario)
        db.session.commit()

        return usuario

    @classmethod
    def update_password(cls, id, password=None):
        usuario = Usuario.get_by_id(id)

        if usuario is None:
            return False

        # Password generada automaticamente
        if password is None:
            password = usuario.generate_password()

        usuario.password = password

        db.session.add(usuario)
        db.session.commit()

        return usuario

    @classmethod
    def get_by_id(cls, id):
        return Usuario.query.filter_by(id=id).first()

    @classmethod
    def get_by_email(cls, correo):
        return Usuario.query.filter_by(correo=correo).first()


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    productos = db.relationship('Producto', lazy='dynamic')

    def __str__(self):
        return self.nombre

    @classmethod
    def create_element(cls, nombre):
        categoria = Categoria(nombre=nombre)

        db.session.add(categoria)
        db.session.commit()

        return categoria

    @classmethod
    def get_by_id(cls, id):
        return Categoria.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        return Categoria.query.all()


class Estado(db.Model):
    __tablename__ = "estados"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    productos = db.relationship('Producto', lazy='dynamic')

    def __str__(self):
        return self.nombre

    @classmethod
    def create_element(cls, nombre):
        estado = Estado(nombre=nombre)

        db.session.add(estado)
        db.session.commit()

        return estado

    @classmethod
    def get_by_id(cls, id):
        return Estado.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        return Estado.query.all()


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text())
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    iva = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now())
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    estado_id = db.Column(db.Integer, db.ForeignKey('estados.id'))
    movimientos = db.relationship('Movimiento', lazy='dynamic')
    pedidos = db.relationship('Pedido', lazy='dynamic')

    def __str__(self):
        return f"{self.nombre} -> {self.precio}"

    @property
    def little_description(self):
        if len(self.descripcion) > 50:
            return self.descripcion[:49] + "..."
        return self.descripcion

    @classmethod
    def create_element(cls, nombre, descripcion, precio, cantidad, iva, categoria_id, estado_id):
        producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, cantidad=cantidad,
            iva=iva, categoria_id=categoria_id, estado_id=estado_id)

        db.session.add(producto)
        db.session.commit()

        return producto

    @classmethod
    def update_element(cls, id, nombre, descripcion, precio, cantidad, iva, categoria_id, estado_id):
        producto = Producto.get_by_id(id)

        if producto is None:
            return False

        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.cantidad = cantidad
        producto.iva = iva
        producto.categoria_id = categoria_id
        producto.estado_id = estado_id

        db.session.add(producto)
        db.session.commit()

        return producto

    @classmethod
    def get_by_id(cls, id):
        return Producto.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        return Producto.query.all()

    # FIXIT
    @classmethod
    def get_by_precio(cls, valor=None, orden='desc'):
        return Producto.query.order_by(Producto.precio)


class Movimiento(db.Model):
    __tablename__ = 'movimientos'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime(), default=datetime.datetime.now())
    tipo = db.Column(db.Integer, nullable=False)
    concepto = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))

    @classmethod
    def create_element(cls, tipo, concepto, cantidad, usuario_id, producto_id):
        movimiento = Movimiento(tipo=tipo, concepto=concepto, cantidad=cantidad,
            usuario_id=usuario_id, producto_id=producto_id)

        db.session.add(movimiento)
        db.session.commit()

        return movimiento

    @classmethod
    def update_element(cls, id, tipo, concepto, cantidad, usuario_id, producto_id):
        movimiento = Movimiento.get_by_id(id)

        if movimiento is None:
            return False

        movimiento.tipo = tipo
        movimiento.concepto = concepto
        movimiento.cantidad = cantidad
        movimiento.usuario_id = usuario_id
        movimiento.producto_id = producto_id

        db.session.add(movimiento)
        db.session.commit()

        return movimiento

    @ classmethod
    def get_by_id(cls, id):
        return Movimiento.query.filter_by(id = id).first()

    @ classmethod
    def get_by_usuario(cls, usuario_id):
        return Movimiento.query.filter_by(usuario_id = usuario_id)

    @ classmethod
    def get_by_producto(cls, producto_id):
        return Movimiento.query.filter_by(producto_id = producto_id)


class Proveedor(db.Model):
    __tablename__='proveedores'

    id=db.Column(db.Integer, primary_key = True)
    nombre=db.Column(db.String(50), nullable = False)
    telefono=db.Column(db.String(15), nullable = False)
    pedidos=db.relationship('Pedido', lazy = 'dynamic')

    def __str__(self):
        return self.nombre

    @ classmethod
    def create_element(cls, nombre, telefono):
        proveedor = Proveedor(nombre = nombre, telefono = telefono)

        db.session.add(proveedor)
        db.session.commit()

        return proveedor

    @ classmethod
    def update_element(cls, id, nombre, telefono):
        proveedor = Proveedor.get_by_id(id)

        if proveedor is None:
            return False

        proveedor.nombre = nombre
        proveedor.telefono = telefono

        db.session.add(proveedor)
        db.session.commit()

        return proveedor

    @ classmethod
    def get_by_id(cls, id):
        return Proveedor.query.filter_by(id=id).first()


class Pedido(db.Model):
    __tablename__='pedidos'

    id=db.Column(db.Integer, primary_key = True)
    cantidad=db.Column(db.Integer, nullable = False)
    valor=db.Column(db.Float, nullable = False)
    producto_id=db.Column(db.Integer, db.ForeignKey('productos.id'))
    proveedor_id=db.Column(db.Integer, db.ForeignKey('proveedores.id'))
