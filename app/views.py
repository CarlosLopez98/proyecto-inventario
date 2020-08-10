from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFError
from .forms import LoginForm, RegisterForm, RecoveryForm, UpdateUserForm
from .forms import ProductForm, ProviderForm, MovementsForm
from .models import Usuario, Producto, Categoria, Estado, Proveedor, Movimiento, Tipo
from . import login_manager
from datetime import datetime

page = Blueprint('page', __name__)

@login_manager.user_loader
def load_user(id):
    return Usuario.get_by_id(id)


@page.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@page.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('errors/csrf_error.html', reason=e.description), 400


@page.route('/logout')
def logout():
    logout_user()
    flash('Cerraste sesión exitosamente.', 'exito')
    return redirect(url_for('.index'))


@page.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html', title='Inicio', inicio_active='item-active')

@page.route('/usuarios', methods=['GET', 'POST'])
@login_required
def usuarios():

    if not current_user.rol == 'admin':
        return redirect(url_for('page.perfil'))

    modals = [
        {
            'id': 'modalAdmin',
            'id_label': 'modalAdminLabel',
            'title': '¿Está seguro de esta operación?',
            'text': 'Este usuario ahora tendrá permisos de Administrador.',
            'no': 'Cancelar',
            'yes': 'Aceptar'
        },
        {
            'id': 'modalUser',
            'id_label': 'modalUserLabel',
            'title': '¿Está seguro de esta operación?',
            'text': 'Este usuario ahora dejará de tener permisos de Administrador.',
            'no': 'Cancelar',
            'yes': 'Aceptar'
        },
        {
            'id': 'modalDelete',
            'id_label': 'modalDeleteLabel',
            'title': '¿Está seguro de esta operación?',
            'text': 'Este usuario será removido de la base de datos.',
            'no': 'Cancelar',
            'yes': 'Aceptar'
        },
    ]

    if request.method == 'POST':
        buscar = request.form['buscar']

        usuarios = Usuario.get_all()
    else:
        usuarios = Usuario.get_all()

    return render_template('usuario/todos.html', title='Administrar',
                           usuario_active='item-active', usuarios=usuarios, modals=modals)


@page.route('/usuarios/change_rol', methods=['GET'])
@login_required
def change_rol():
    # Si el usuario logueado no tiene permisos de administrador no podrá
    # acceder datos mediante la ruta, si lo intenta sera redireccionado al index
    if not current_user.rol == 'admin':
        return redirect(url_for('page.index'))

    # Se obtiene el parametro get user_id se verifica que este parametro exista,
    # sino se redirecciona y se notifica un error
    user_id = request.args.get('user_id')
    if user_id is None:
        flash('Ocurrió un error al actualizar el usuario.', 'danger')
        return redirect(url_for('page.usuarios'))

    user = Usuario.update_rol(user_id)
    if user:
        flash(f'Los permisos del usuario {user} han cambiado.', 'exito')
    else:
        flash('El usuario al que intenta darle permisos no existe', 'danger')

    return redirect(url_for('page.usuarios'))


@page.route('/usuarios/delete', methods=['GET'])
@login_required
def delete_user():
    if not current_user.rol == 'admin':
        return redirect(url_for('page.index'))

    user_id = request.args.get('user_id')
    if user_id is None:
        flash('Ocurrió un error al eliminar el usuario', 'danger')
        return redirect(url_for('page.usuarios'))

    user = Usuario.delete_element(user_id)
    if user:
        flash(f'El usuario se ha eliminado de la base de datos.', 'exito')
    else:
        flash('El usuario al que intenta eliminar no existe', 'danger')

    return redirect(url_for('page.usuarios'))

@page.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('page.index'))

    login_form = LoginForm(request.form)

    if request.method == 'POST':
        if login_form.validate():
            correo = login_form.correo.data
            contrasena = login_form.password.data

            usuario = Usuario.get_by_email(correo)
            if usuario:
                if usuario.verify_password(contrasena):
                    login_user(usuario)
                    flash('Usuario autenticado.', 'exito')

                    return redirect(url_for('page.index'))
                else:
                    flash('Contraseña incorrecta.', 'warning')
            else:
                flash('Correo electrónico incorrecto.', 'warning')
        else:
            flash('Correo invalido.', 'danger')

    return render_template('usuario/login.html', title='Iniciar sesión', usuario_active='item-active', login_form=login_form)


@page.route('/signup', methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('page.index'))

    register_form = RegisterForm(request.form)

    if request.method == 'POST':
        if register_form.validate():
            nombre = register_form.nombre.data
            apellido = register_form.apellido.data
            correo = register_form.correo.data
            contrasena = register_form.password.data

            usuario = Usuario.get_by_email(correo)

            if not usuario:
                usuario = Usuario.create_element(
                    nombre, apellido, correo, contrasena)
                # Posible mail de bienvenida
                flash('Usuario registrado exitosamente.', 'exito')
                return redirect(url_for('page.index'))

            else:
                flash('Ya existe un registro con este correo electrónico.', 'warning')

    return render_template('usuario/signup.html', title='Registro', usuario_active='item-active', register_form=register_form)


@page.route('/recovery', methods=['GET', 'POST'])
def recovery():

    if current_user.is_authenticated:
        return redirect(url_for('page.index'))

    recovery_form = RecoveryForm(request.form)

    if request.method == 'POST':
        if recovery_form.validate():
            pass

    return render_template('usuario/recovery.html', title='Recuperar contraseña', usuario_active='item-active', recovery_form=recovery_form)


@page.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():

    update_form = UpdateUserForm(request.form)

    if request.method == 'POST':
        id = current_user.id
        nombre = None if update_form.nombre.data == '' else update_form.nombre.data
        apellido = None if update_form.apellido.data == '' else update_form.apellido.data
        correo = None if update_form.correo.data == '' else update_form.correo.data
        old_contrasena = None if update_form.old_password.data == '' else update_form.old_password.data
        contrasena = None if update_form.password.data == '' else update_form.password.data

        if current_user.verify_password(old_contrasena):
            current_user.update_element(id=id, nombre=nombre, apellido=apellido, correo=correo, password=contrasena)
            flash('Perfil actualizado.', 'exito')

            return redirect(url_for('page.perfil'))
        else:
            flash('Contraseña incorrecta.', 'warning')

    modals = [
        {
            'id': 'modalActualizar',
            'id_label': 'modalActualizarLabel',
            'title': '¿Esta seguro de actualizar?',
            'text': 'Esta accíón realizará cambios en su cuenta.',
            'no': 'Cancelar',
            'yes': 'Aceptar'
        },
    ]

    return render_template('usuario/perfil.html', title='Perfil', usuario_active='item-active',
        update_form=update_form, modals=modals)


@page.route('/productos', methods=['GET', 'POST'])
@login_required
def productos():

    if request.args.get('panel'):
        if request.args.get('panel') == 'añadir':
            panel = 'añadir'
    else:
        panel = 'todos'

    productos = Producto.get_all()
    proveedores = Proveedor.get_all()
    providers = []
    categorias = Categoria.get_all()
    categories = []
    estados = Estado.get_all()
    status = []

    if request.args.get('estado'):
        for estado in estados:
            if estado.id == int(request.args.get('estado')):
                print(estado.id)
                productos = estado.productos

    if request.args.get('categoria'):
        for categoria in categorias:
            if categoria.id == int(request.args.get('categoria')):
                productos = categoria.productos

    for proveedor in proveedores:
        providers.append((proveedor.id, proveedor.nombre))

    for categoria in categorias:
        categories.append((categoria.id, categoria.nombre))

    for estado in estados:
        status.append((estado.id, estado.nombre))

    form = ProductForm(request.form)
    form.providers = providers
    form.categories = categories
    form.status = status

    if request.method == 'POST':
        if request.form['accion'] == 'buscar':
            buscar = request.form['buscar']
            if buscar != '':
                productos = Producto.get_by_name(buscar)


        elif request.form['accion'] == 'añadir':
            if form.validate():
                nombre = form.nombre.data
                descripcion = form.descripcion.data
                precio = form.precio.data
                iva = form.iva.data
                categoria_id = form.categoria.data
                estado_id = form.estado.data
                proveedor_id = form.proveedor.data

                producto = Producto.create_element(nombre, descripcion, precio, iva, proveedor_id, categoria_id, estado_id)
                flash('Producto guardado con éxito.', 'exito')

                return render_template('producto/index.html', title='Productos',
            productos_active='item-active', productos=productos, form=form, panel='todos')
            else:
                return render_template('producto/index.html', title='Productos',
                                    productos_active='item-active', productos=productos, form=form, panel='añadir')

    return render_template('producto/index.html', title='Productos', productos_active='item-active',
                            productos=productos, form=form, panel=panel, categorias=categorias, estados=estados)

@page.route('/producto/eliminar', methods=['GET'])
@login_required
def eliminar_producto():
    if request.args.get('producto_id'):
        producto_id = request.args.get('producto_id')
        producto = Producto.update_estado(producto_id)
        if producto:
            if producto.estado_id == 1:
                flash('El producto pasó a estado "Activo"', 'exito')
            elif producto.estado_id == 2:
                flash('El producto pasó a estado "Inactivo"', 'exito')
        else:
            flash('Hubo problemas para cambiar el estado del producto', 'warning')


    return redirect(url_for('page.productos'))


@page.route('/producto/editar', methods=['GET', 'POST'])
@login_required
def editar_producto():

    if request.args.get('producto_id'):
        producto_id = request.args.get('producto_id')

        producto = Producto.get_by_id(producto_id)

        if producto is None:
            flash('El producto al que intenta acceder no existe', 'warning')
            return redirect(url_for('page.productos'))

        if producto.estado_id == 2:
            flash('Este producto se encuentra inactivo y no se puede editar', 'warning')
            return redirect(url_for('page.productos'))

        proveedores = Proveedor.get_all()
        categorias = Categoria.get_all()
        estados = Estado.get_all()

        form = ProductForm(request.form)

        # METODO POST
        if request.method == 'POST':
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            precio = request.form['precio']
            proveedor = request.form['proveedor']
            categoria = request.form['categoria']
            estado = request.form['estado']
            iva = request.form['iva']

            # Posibles validaciones

            producto.update_element(
                id=producto.id,
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                iva=True if iva == 'on' else False,
                proveedor_id=proveedor,
                categoria_id=categoria,
                estado_id=estado
            )

            flash('El producto se actualizó con éxito', 'exito')
            return redirect(url_for('page.productos'))
    else:
        return redirect(url_for('page.productos'))

    return render_template('producto/editar.html', title='Editar productos',
                            productos_active='item-active', form=form, producto=producto,
                            proveedores=proveedores, categorias=categorias, estados=estados)


@page.route('/proveedores', methods=['GET', 'POST'])
@login_required
def proveedores():

    if request.args.get('panel'):
        panel = request.args.get('panel')
    else:
        panel = 'todos'

    proveedores = Proveedor.get_all()

    form = ProviderForm(request.form)

    if request.method == 'POST':
        if request.form['accion'] == 'añadir':
            if form.validate():
                nombre = form.nombre.data
                direccion = form.direccion.data
                telefono = form.telefono.data

                proveedor = Proveedor.create_element(nombre=nombre, direccion=direccion, telefono=telefono)
                flash('El proveedor se ha creado con éxito.', 'exito')
                return redirect(url_for('page.proveedores'))
            else:
                flash('El formulario debe estar correctamente diligenciado.', 'danger')
                return redirect(url_for('page.proveedores', panel='añadir'))
        elif request.form['accion'] == 'buscar':
            buscar = request.form['buscar']
            if buscar != '':
                proveedores = Proveedor.get_by_name(buscar)

    return render_template('proveedor/index.html', title='Proveedores', proveedores_active='item-active',
                            proveedores=proveedores, panel=panel, form=form)


@page.route('/proveedor/editar', methods=['GET', 'POST'])
@login_required
def editar_proveedor():

    if request.args.get('proveedor_id'):
        proveedor_id = request.args.get('proveedor_id')

        proveedor = Proveedor.get_by_id(proveedor_id)

        if proveedor is None:
            flash('El proveedor al que intenta acceder no existe', 'warning')
            return redirect(url_for('page.proveedores'))

        if proveedor.estado == 'inactivo':
            flash('No puede editar el proveedor debido a que está inactivo', 'warning')
            return redirect(url_for('page.proveedores'))

        # Opcional para menejo de estados en los proveedores
        #if producto.estado_id == 2:
        #    flash('Este producto se encuentra inactivo y no se puede editar', 'warning')
        #    return redirect(url_for('page.productos'))

        form = ProviderForm(request.form)

        if proveedor:
            # METODO POST
            if request.method == 'POST':
                if form.validate():
                    nombre = form.nombre.data
                    direccion = form.direccion.data
                    telefono = form.telefono.data

                    proveedor.update_element(
                        id=proveedor.id,
                        nombre=nombre,
                        direccion=direccion,
                        telefono=telefono
                    )

                    flash('El proveedor se actualizó con éxito', 'exito')
                    return redirect(url_for('page.proveedores'))
        else:
            flash('El proveedor que está tratando de editar no existe.', 'warning')
            return redirect(url_for('page.proveedores'))
    else:
        return redirect(url_for('page.proveedores'))

    return render_template('proveedor/editar.html', title='Consultar proveedor', proveedores_active='item-active',
                            form=form, proveedor=proveedor)

@page.route('/proveedor/eliminar', methods=['GET'])
@login_required
def eliminar_proveedor():
    if request.args.get('proveedor_id'):
        proveedor_id = request.args.get('proveedor_id')

        proveedor = Proveedor.get_by_id(proveedor_id)

        if proveedor:
            proveedor = Proveedor.update_estado(proveedor_id)

            if proveedor.estado == 'activo':
                flash('El proveedor ha sido nuevamente agregado.', 'exito')
            elif proveedor.estado == 'inactivo':
                flash('El proveedor ha sido eliminado.', 'exito')
        else:
            flash('El proveedor que intenta eliminar no existe.', 'warning')

    return redirect(url_for('page.proveedores'))


# Vistas de movimientos
@page.route('/movimientos')
@login_required
def movimientos():

    movimientos = Movimiento.get_all()

    movements = []
    for movimiento in movimientos:
        movement = {
            'movimiento': movimiento,
            'producto': Producto.get_by_id(movimiento.producto_id),
            'usuario': Usuario.get_by_id(movimiento.usuario_id),
            'tipo': Tipo.get_by_id(movimiento.tipo_id)
        }
        movements.append(movement)

    return render_template('movimiento/index.html', title='Movimientos', prouctos_active='item-active',
                            movimientos=movements)


@page.route('/movimiento/agregar', methods=['GET', 'POST'])
@login_required
def add_movimiento():

    if not request.args.get('producto_id'):
        flash('Para realizar un movimiento necesitas seleccionar un producto', 'warning')
        return redirect(url_for('page.productos'))

    producto_id = request.args.get('producto_id')
    producto = Producto.get_by_id(producto_id)

    if producto is None:
        flash('El producto al que intentas realizarle un movimiento no existe', 'warning')
        return redirect(url_for('page.productos'))

    if producto.estado_id == 2:
        flash('El producto al que intentas realizarle un movimiento esta inactivo', 'warning')
        return redirect(url_for('page.productos'))

    form = MovementsForm(request.form)

    if request.method == 'POST':
        if form.validate():
            cantidad = form.cantidad.data
            tipo = form.tipo.data
            concepto = form.concepto.data

            producto = Producto.update_cantidad(id=producto_id, cantidad=cantidad, op=tipo)
            movimiento = Movimiento.create_element(concepto=concepto, cantidad=cantidad, tipo_id=tipo,
                                                    usuario_id=current_user.id, producto_id=producto_id)

            if producto and movimiento:
                flash('El movimiento se realizó con éxito', 'exito')
                return redirect(url_for('page.movimientos'))
            else:
                flash('Hubo problemas para realizar el movimiento', 'danger')
                return redirect(url_for('page.productos'))

    categoria = Categoria.get_by_id(producto.categoria_id)
    proveedor = Proveedor.get_by_id(producto.proveedor_id)

    tipos = Tipo.get_all()
    types = []
    for tipo in tipos:
        types.append((tipo.id, tipo.nombre))

    form.types = types

    return render_template('movimiento/agregar.html', title='Realizar movimiento', productos_active='item-active',
                            form=form, producto=producto, categoria=categoria, proveedor=proveedor)
