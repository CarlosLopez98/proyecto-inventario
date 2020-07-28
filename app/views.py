from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm, RecoveryForm
from .models import Usuario
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
    flash('Cerraste sesión exitosamente.', 'success')
    return redirect(url_for('.index'))


@page.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('page.perfil'))

    login_form = LoginForm(request.form)
    register_form = RegisterForm(request.form)
    recovery_form = RecoveryForm(request.form)

    if request.method == 'POST':
        if register_form.validate():
            nombre = register_form.nombre.data
            apellido = register_form.apellido.data
            correo = register_form.correo.data
            contrasena = register_form.password.data

            usuario = Usuario.get_by_email(correo)

            if not usuario:
                usuario = Usuario.create_element(nombre, apellido, correo, contrasena)
                # Posible mail de bienvenida
                flash('Usuario registrado exitosamente.', 'success')

            else:
                flash('Ya existe un registro con este correo electrónico.', 'danger')

        elif login_form.validate():
            if login_form.validate():
                correo = login_form.correo.data
                contrasena = login_form.password.data

                usuario = Usuario.get_by_email(correo)
                if usuario and usuario.verify_password(contrasena):
                    login_user(usuario)
                    flash('Usuario autenticado.', 'success')
                    
                    return redirect(url_for('page.perfil'))
            else:
                flash('correo o contraseña invalidos.', 'danger')
        elif recovery_form.validate():
            pass

    return render_template('index.html', title='Inicio', login_form=login_form, register_form=register_form, recovery_form=recovery_form)


@page.route('/perfil')
@login_required
def perfil():
    return render_template('usuario/perfil.html')
