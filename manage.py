from app import create_app
from app import db, User#, Task #Importar Modelos de app
from flask_script import Manager, Shell
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from config import config


config_class = config['development']
app = create_app(config_class)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


if __name__ == '__main__':
    manager = Manager(app)

    # python manage.py shell
    manager.add_command('shell', Shell(make_context=make_shell_context))
    manager.add_command('db', MigrateCommand)

    #Pruebas unitarias
    @manager.command
    def test():
        import unittest
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner().run(tests)

    manager.run()  # python manage.py runserver
