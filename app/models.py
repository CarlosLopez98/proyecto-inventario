from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime, string, random
from sqlalchemy import asc, desc


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(94), nullable=False)
    rol = db.Column(db.String(5), default='user')
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
    def update_element(cls, id, nombre=None, apellido=None, correo=None, password=None, rol=None):
        usuario = Usuario.get_by_id(id)

        if usuario is None:
            return False

        if not nombre is None : usuario.nombre = nombre
        if not apellido is None : usuario.apellido = apellido
        if not correo is None : usuario.correo = correo
        if not rol is None : usuario.rol = rol
        if not password is None : usuario.password = password

        db.session.add(usuario)
        db.session.commit()

        return usuario

    @classmethod
    def delete_element(cls, id):
        usuario = Usuario.get_by_id(id)

        if usuario is None:
            return False

        db.session.delete(usuario)
        db.session.commit()

        return True

    @classmethod
    def update_rol(cls, id):
        usuario = Usuario.get_by_id(id)

        if usuario is None:
            return False

        if usuario.rol == 'admin':
            usuario.rol = 'user'
        elif usuario.rol == 'user':
            usuario.rol = 'admin'

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

    @classmethod
    def get_all(cls):
        return Usuario.query.all()


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


class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(50), nullable=True)
    telefono = db.Column(db.String(15), nullable=False)
    estado = db.Column(db.String(10), default='activo')
    productos = db.relationship('Producto', lazy='dynamic')

    def __str__(self):
        return self.nombre

    @ classmethod
    def create_element(cls, nombre, direccion, telefono):
        proveedor = Proveedor(nombre=nombre, direccion=direccion, telefono=telefono)

        db.session.add(proveedor)
        db.session.commit()

        return proveedor

    @ classmethod
    def update_element(cls, id, nombre, direccion, telefono):
        proveedor = Proveedor.get_by_id(id)

        if proveedor is None:
            return False

        proveedor.nombre = nombre
        proveedor.direccion = direccion
        proveedor.telefono = telefono

        db.session.add(proveedor)
        db.session.commit()

        return proveedor

    @classmethod
    def update_estado(cls, id):
        proveedor = Proveedor.get_by_id(id)

        if proveedor is None:
            return False

        if proveedor.estado == 'activo':
            proveedor.estado = 'inactivo'
        elif proveedor.estado == 'inactivo':
            proveedor.estado = 'activo'

        db.session.add(proveedor)
        db.session.commit()

        return proveedor

    @classmethod
    def get_by_id(cls, id):
        return Proveedor.query.filter_by(id=id).first()

    @classmethod
    def get_by_name(cls, nombre=''):
        if nombre:
            query = f"SELECT * FROM proveedores WHERE nombre LIKE '%{nombre}%'"
            results = db.session.execute(query)
            proveedores = []

            for result in results:
                proveedor = Proveedor(
                    id=result[0],
                    nombre=result[1],
                    direccion=result[2],
                    telefono=result[3]
                )
                proveedores.append(proveedor)

            return proveedores

    @classmethod
    def get_all(cls):
        return Proveedor.query.all()


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text())
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=True, default=0)
    iva = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now())
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    estado_id = db.Column(db.Integer, db.ForeignKey('estados.id'))
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    movimientos = db.relationship('Movimiento', lazy='dynamic')

    valor_iva = 0.19

    def __str__(self):
        return f"{self.nombre} -> {self.precio}"

    @property
    def little_description(self):
        if len(self.descripcion) > 50:
            return self.descripcion[:49] + "..."
        return self.descripcion

    @classmethod
    def create_element(cls, nombre, descripcion, precio, iva, proveedor_id, categoria_id, estado_id):
        producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio,
            iva=iva, proveedor_id=proveedor_id, categoria_id=categoria_id, estado_id=estado_id)

        db.session.add(producto)
        db.session.commit()

        return producto

    @classmethod
    def update_element(cls, id, nombre, descripcion, precio, iva, proveedor_id, categoria_id, estado_id, cantidad=0):
        producto = Producto.get_by_id(id)

        if producto is None:
            return False

        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.cantidad = cantidad
        producto.iva = iva
        producto.proveedor_id = proveedor_id
        producto.categoria_id = categoria_id
        producto.estado_id = estado_id

        db.session.add(producto)
        db.session.commit()

        return producto

    @classmethod
    def update_estado(cls, id):
        producto = Producto.get_by_id(id)

        if producto is None:
            return False

        if producto.estado_id == 1:
            producto.estado_id = 2
        elif producto.estado_id == 2:
            producto.estado_id = 1

        db.session.add(producto)
        db.session.commit()

        return producto

    @classmethod
    def get_by_id(cls, id):
        return Producto.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        return Producto.query.all()

    @classmethod
    def get_by_name(cls, nombre=''):
        if nombre:
            query = f"SELECT * FROM productos WHERE nombre LIKE '%{nombre}%'"
            results = db.session.execute(query)
            productos = []

            for result in results:
                producto = Producto(
                    id=result[0],
                    nombre=result[1],
                    descripcion=result[2],
                    precio=result[3],
                    cantidad=result[4],
                    iva=result[5],
                    created_at=result[6],
                    categoria_id=result[7],
                    estado_id=result[8],
                    proveedor_id=result[9]
                )
                productos.append(producto)

            return productos

    @classmethod
    def get_by_order(cls, campo='nombre', orden='desc'):
        if orden == 'desc':
            return Producto.query.order_by(campo)
        else:
            return Producto.query.order_by(asc(campo))


class Tipo(db.Model):
    __tablename__ = "tipos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    movimientos = db.relationship('Movimiento', lazy='dynamic')

    def __str__(self):
        return self.nombre

    @classmethod
    def create_element(cls, nombre):
        tipo = Tipo(nombre=nombre)

        db.session.add(tipo)
        db.session.commit()

        return tipo

    @classmethod
    def get_by_id(cls, id):
        return Tipo.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        return Tipo.query.all()


class Movimiento(db.Model):
    __tablename__ = 'movimientos'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime(), default=datetime.datetime.now())
    concepto = db.Column(db.Text())
    cantidad = db.Column(db.Integer, nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos.id'))
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
