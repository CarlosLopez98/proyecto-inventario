from wtforms import Form
from wtforms import validators
from wtforms import StringField, PasswordField, BooleanField, HiddenField, TextAreaField, DecimalField, SelectField, FloatField, IntegerField
from wtforms.fields.html5 import EmailField
from flask_wtf.csrf import CSRFProtect

from .models import Usuario, Categoria, Estado


def lenght_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError(
            'Solo los humanos pueden completar este registro!')


class MyBaseForm(Form):
    class Meta:
        csrf = True  # Enable CSRF
        csrf_class = CSRFProtect  # Set the CSRF implementation
        csrf_secret = 'Llavesecretaparaelcsrf'  # Some implementations need a secret key.
        # Any other CSRF settings here.


# Formularios de usuarios

class LoginForm(MyBaseForm):
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
    
    nombre = StringField('Nombre', [
        validators.length(min=4, max=50, message='Nombre fuera de rango.'),
        validators.DataRequired(message='El nombre es requerido.')
    ])
    descripcion = TextAreaField('Descripción', render_kw={'rows': 4})
    precio = FloatField('Precio',[
        validators.number_range(min=1000, max=99000000, message='Precio fuera de rango'),
        validators.DataRequired(message='El precio es requerido.')
    ])
    iva = BooleanField('¿Tiene iva?')

    proveedores = []
    proveedor = SelectField('Proveedor', choices=proveedores, validate_choice=False)
    
    categorias = []
    categoria = SelectField('Categoría', choices=categorias, validate_choice=False)

    estados = []
    estado = SelectField('Estado', choices=estados, validate_choice=False)

    @property
    def providers(self):
        pass

    @providers.setter
    def providers(self, providers):
        self.proveedor.choices = providers

    @property
    def categories(self):
        pass

    @categories.setter
    def categories(self, categories):
        #self.categorias = categories
        self.categoria.choices = categories

    @property
    def status(self):
        pass

    @status.setter
    def status(self, status):
        #self.estados = status
        self.estado.choices = status


class ProviderForm(Form):

    nombre = StringField('Nombre', [
        validators.length(min=4, max=50, message='Nombre fuera de rango.'),
        validators.DataRequired(message='El nombre es requerido.')
    ])
    direccion = StringField('Dirección', [
        validators.length(min=6, max=50, message='Direccion fuera de rango de caracteres.')
    ])
    telefono = StringField('Teléfono', [
        validators.length(min=4, max=15, message='Teléfono fuera de rango.'),
        validators.DataRequired(message='El teléfono es requerido.')
    ])


class MovementsForm(Form):

    cantidad = IntegerField('Cantidad', [
        validators.NumberRange(min=1, message='Ingresa un número válido'),
        validators.DataRequired(message='La cantidad es requerida')
    ])
    tipos = []
    tipo = SelectField('Tipo', choices=tipos, validate_choice=False)
    concepto = TextAreaField('Descripción', render_kw={'rows': 3})

    @property
    def types(self):
        pass

    @types.setter
    def types(self, types):
        self.tipo.choices = types
