from wtforms import Form
from wtforms import validators
from wtforms import StringField, PasswordField, BooleanField, HiddenField, TextAreaField, DecimalField, SelectField, FloatField
from wtforms.fields.html5 import EmailField

from .models import Usuario, Categoria, Estado


def lenght_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError(
            'Solo los humanos pueden completar este registro!')


# Formularios de usuarios

class LoginForm(Form):
    correo = EmailField('Correo', [
        validators.length(
            min=6, max=100, message='El campo debe tener entre 4 y 50 caracteres.'),
        validators.Required(message='El email es requerido.'),
        validators.Email(message='Ingrese un email válido.')
    ])
    password = PasswordField('Contraseña', [
        validators.Required(message='La contraseña es requerida.'),
    ])


class RegisterForm(Form):
    nombre = StringField('Nombre', [
        validators.length(min=4, max=50)
    ])
    apellido = StringField('Apellido', [
        validators.length(min=4, max=50)
    ])
    correo = EmailField('Correo', [
        validators.length(
            min=6, max=100, message='El campo debe tener entre 4 y 50 caracteres.'),
        validators.Required(message='El email es requerido.'),
        validators.Email(message='Ingrese un email válido.')
    ])
    password = PasswordField('Contraseña', [
        validators.Required(message='La contraseña es requerida.'),
    ])
    confirm_password = PasswordField('Confirmar contraseña')
    honeypot = HiddenField('', [lenght_honeypot])

    def validate_email(self, email):
        if Usuario.get_by_email(email.data):
            raise validators.ValidationError(
                'El correo ya se encuentra registrado.')

    # Sobreescritura del metodo validate
    def validate(self):
        if not Form.validate(self):
            return False

        # Validaciones propias
        if len(self.password.data) < 4:
            self.password.errors.append('La contraseña es demasiado corta.')
            return False

        return True


class RecoveryForm(Form):
    correo = EmailField('Ingresa tu correo', [
        validators.length(
            min=6, max=100, message='El campo debe tener entre 4 y 50 caracteres.'),
        validators.Required(message='El email es requerido.'),
        validators.Email(message='Ingrese un email válido.')
    ])


class UpdateUserForm(Form):
    nombre = StringField('Nombre', [
        validators.length(min=4, max=50)
    ])
    apellido = StringField('Apellido', [
        validators.length(min=4, max=50)
    ])
    correo = EmailField('Correo', [
        validators.length(
            min=6, max=100, message='El campo debe tener entre 4 y 50 caracteres.'),
        validators.Email(message='Ingrese un email válido.')
    ])
    old_password = PasswordField('Antigua contraseña *', [
        validators.Required(message='La contraseña antigua es requerida para validar el cambio.'),
    ])
    password = PasswordField('Contraseña', [
    ])
    confirm_password = PasswordField('Confirmar contraseña')
    honeypot = HiddenField('', [lenght_honeypot])

    def validate_email(self, email):
        if Usuario.get_by_email(email.data):
            raise validators.ValidationError(
                'El correo ya se encuentra registrado.')

    # Sobreescritura del metodo validate
    def validate(self):
        if not Form.validate(self):
            return False

        # Validaciones propias
        if len(self.password.data) < 4:
            self.password.errors.append('La contraseña es demasiado corta.')
            return False

        return True


# Formularios para productos
class ProductForm(Form):
    
    nombre = StringField('Titulo', [
        validators.length(min=4, max=50, message='Título fuera de rango.'),
        validators.DataRequired(message='El título es requerido.')
    ])
    descripcion = TextAreaField('Descripción', render_kw={'rows': 4})
    precio = FloatField('Precio', [

    ])
    iva = BooleanField('¿Tiene iva?', [
        validators.DataRequired()
    ])
    
    categorias = []
    categoria = SelectField('Categoría', choices=categorias)

    estados = []
    estado = SelectField('Estado', choices=estados)

    honeypot = HiddenField('', [lenght_honeypot])

    @property
    def categories(self):
        pass

    @categories.setter
    def categories(self, categories):
        self.categorias = categories
        self.categoria.choices = categories

    @property
    def status(self):
        pass

    @status.setter
    def status(self, status):
        self.estados = status
        self.estado.choices = status
