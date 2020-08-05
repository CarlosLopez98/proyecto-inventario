from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm, RecoveryForm, UpdateUserForm
from .forms import ProductForm
from .models import Usuario, Producto, Categoria, Estado
from . import login_manager

page = Blueprint('page', __name__)

@login_manager.user_loader
def load_user(id):
    return Usuario.get_by_id(id)


@page.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


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

    productos = Producto.get_all()
    categorias = Categoria.get_all()
    categories = []
    estados = Estado.get_all()
    status = []

    for categoria in categorias:
        categories.append((categoria.id, categoria.nombre))

    for estado in estados:
        status.append((estado.id, estado.nombre))

    form = ProductForm()
    form.categories = categories
    form.status = status

    return render_template('producto/index.html', title='Productos', 
        productos_active='item-active', productos=productos, form=form)

@page.route('/producto/nuevo')
@login_required
def añadir_producto():
    return render_template('producto/añadirproducto.html', title='Añadir producto')


@page.route('/producto/consultar')
@login_required
def consultar_producto():
    return render_template('producto/consultarproducto.html', title='Consultar producto')


@page.route('/proveedores')
@login_required
def proveedores():
    return render_template('proveedor/index.html', title='Proveedores', proveedores_active='item-active')


@page.route('/proveedor/consultar')
@login_required
def consultar_proveedor():
    return render_template('proveedor/consultarproveedor.html', title='Consultar proveedor')
