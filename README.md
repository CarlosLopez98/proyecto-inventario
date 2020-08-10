# Proyecto de inventarios
Proyecto web con Python y Flask

## Requerimientos
- Python3.8
- Pip
- Virtualenv
- Sqlite3

## Ejecutar el proyecto
- Clonar el repositorio `git clone https://github.com/CarlosLopez98/proyecto-inventario`
- Con virtualenv crear un entorno virtual, por ejemplo: `virtualenv -p python3 venv`
- Luego ingresar al entorno virtual `source venv/bin/activate`
- Con `pip` instalar los requerimientos que se encuentran en el archivo `requirements.txt`, de la siguiente manera: `pip install -r requirements.txt`
- Si todas la dependencias se instalaron corretamente, ejecutamos el proyecto con el archivo `manage.py`, dela siguiente manera: `python3 manage.py runserver`
- Si todo salió correctamente, el proyecto debería funcionar perfectamente
- En caso de que la base de datos no tenga registros haremos lo siguiente:
    - Con `sqlite3` ejecutamos el archivo de la base de datos que se encuentra en `app/data/proyecto_inventarios.sqlite3`
    - Y copiamos todas las instrucciones sql que se encuntran en `initial_data.sql` y las ejecutamos en sqlite3
- Por último vamos a la ruta [localhost:5000](http://localhost:5000)
