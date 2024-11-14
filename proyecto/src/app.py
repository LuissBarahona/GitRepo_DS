#Yulinio
from flask import Flask, flash, render_template, redirect, url_for, request, session
from dao.DAOEstudiante import DAOEstudiante
from dao.DAOAdmin import DAOAdmin
from noticias import obtener_noticias  # Importa la función obtener_noticias
import bcrypt
import requests

from datetime import datetime

app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
db = DAOEstudiante()
dbA = DAOAdmin()
####La función login_requerido, realiza la proteccion de las rutas###
def login_requerido(f):
    def wrapper(*args, **kwargs):
        # Verificar si el usuario está autenticado
        if 'username' not in session:
            return redirect(url_for('iniciarSesion'))  # Redirige a la página de login si no está autenticado
        return f(*args, **kwargs)  # Si está autenticado, continua con la ejecución de la ruta
    wrapper.__name__ = f.__name__ 
    return wrapper
##################Inicio(ESTUDIANTE ADMINISTRADOR)######################
@app.route('/')
def inicio():
    return render_template('index.html')


#FUNCIONES adicionales DE LUCHO PARA EL ADMIN

NEWS_API_KEY = '99fde377df2f4d1082857bb8042dedfe'  # Inserta aquí tu API Key de News API u otra API de noticias


def obtener_noticias():
    url = ('https://newsapi.org/v2/everything?q=embedded%20systems%20OR%20electronics&'
           'sortBy=publishedAt&apiKey=' + NEWS_API_KEY)
    response = requests.get(url)
    noticias = response.json().get('articles', [])
    
    # Formatear la fecha en cada artículo
    for noticia in noticias:
        if 'publishedAt' in noticia:
            noticia['publishedAt'] = datetime.strptime(noticia['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d/%m/%Y')

    return noticias[:8]


##################Estudiante #################

@app.route('/estudiante/')
def iniciarSesion():
    return render_template('estudiante/iniciar_sesion.html')

@app.route('/estudiante/entrar/', methods = ['POST', 'GET'])
def entrar():
    if request.method == 'POST':
        username = request.form.get('correoNombreUsuario')
        contrasena = request.form.get('contrasena')
        # Recupera los datos del usuario de la base de datos
        usuario = db.read(username)  # Ahora usando la nueva función

        if usuario and bcrypt.checkpw(contrasena.encode('utf-8'), usuario['contrasena'].encode('utf-8')):
            # flash('Inicio de sesión exitoso')
            session['username'] = usuario['nombreUsuario']
            return redirect(url_for('estudianteInicio'))
        else:
            flash("Usuario o contraseña incorrecta")
            return redirect(url_for('iniciarSesion'))
        
@app.route('/estudiante/cerrar_sesion/')
def cerrar_sesion():
    session.pop('username', None)  # Elimina 'username' de la sesión
    #flash("Has cerrado sesión exitosamente.")
    return redirect(url_for('iniciarSesion'))

@app.route('/estudiante/registrarse/')
def registro():
    return render_template('estudiante/registrarse.html')

@app.route('/estudiante/guardar/',methods = ['POST', 'GET'])
def guardarRegistro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        username = request.form.get('nombreUsuario')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        if db.insert({'nombre': nombre, 'apellido': apellido, 'nombreUsuario': username, 'correo': correo, 'contrasena': hashed_password}):

            #flash('Registro exitoso')
            return redirect(url_for('iniciarSesion'))
        else:
            flash("Nombre de usuario o correco existente")
            return redirect(url_for('registro'))

@app.route('/estudiante/cursos/')
def cursos():
    return render_template('estudiante/cursos.html')


@app.route('/estudiante/facturacion/')
def facturacion():
    return render_template('estudiante/facturacion.html')

# Ruta de inicio de estudiante
@app.route('/estudiante/inicio/')
@login_requerido
def estudianteInicio():
    noticias = obtener_noticias()  # Llama a la función y guarda las noticias en la variable
    return render_template('estudiante/inicio.html', noticias=noticias)


@app.route('/estudiante/cursosRuta/')
def estudianteCursosRuta():
    return render_template('estudiante/cursosRuta.html')

@app.route('/estudiante/cursosWebinar/')
def estudianteCursosWebinar():
    return render_template('estudiante/cursosWebinar.html')

@app.route('/estudiante/inicioPadre/')
def estudianteInicioPadre():
    return render_template('estudiante/inicioPadre.html')

@app.route('/estudiante/desarrollo/')
def estudianteDesarrollo():
    return render_template('estudiante/desarrollo.html')

@app.route('/estudiante/desarrolloManufactura/')
def estudianteDesarrolloManufactura():
    return render_template('estudiante/desarrolloManufactura.html')

@app.route('/estudiante/trabajo/')
def estudianteTrabajo():
    return render_template('estudiante/trabajo.html')

@app.route('/estudiante/soporte/')
def estudianteSoporte():
    return render_template('estudiante/soporte.html')

@app.route('/estudiante/cursosVenta/')
def estudianteCursoVenta():
    return render_template('estudiante/cursosVenta.html')

@app.route('/estudiante/cursosUso/')
def estudianteCursoUso():
    return render_template('estudiante/cursosUso.html')
###############ADMINISTRADOR##############
#################DESDE ACÁ EMPIEZA LUCHO CON ADMINISTRADOR TEMPLATES #########
@app.route('/administrador/')
def iniciarSesionAdmin():
    return render_template('administrador/iniciar_sesion.html')

@app.route('/administrador/entrar/', methods = ['POST', 'GET'])
def entrarAdmin():
    if request.method == 'POST':
        username = request.form.get('correoNombreUsuario')
        contrasena = request.form.get('contrasena')
        # Recupera los datos del usuario de la base de datos
        usuario = dbA.read(username)  # Ahora usando la nueva función

        if usuario and bcrypt.checkpw(contrasena.encode('utf-8'), usuario['contrasena'].encode('utf-8')):
            # flash('Inicio de sesión exitoso')
            session['username'] = usuario['nombreUsuario']
            return redirect(url_for('administradorInicio'))
        else:
            flash("Usuario o contraseña incorrecta")
            return redirect(url_for('iniciarSesionAdmin'))
        
@app.route('/administrador/cerrar_sesion/')
def cerrar_sesionAdmin():
    session.pop('username', None)  # Elimina 'username' de la sesión
    #flash("Has cerrado sesión exitosamente.")
    return redirect(url_for('iniciarSesionAdmin'))

@app.route('/administrador/registrarse/')
def registroAdmin():
    return render_template('administrador/registrarse.html')

@app.route('/administrador/guardar/',methods = ['POST', 'GET'])
def guardarRegistroAdmin():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        username = request.form.get('nombreUsuario')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        if dbA.insert({'nombre': nombre, 'apellido': apellido, 'nombreUsuario': username, 'correo': correo, 'contrasena': hashed_password}):

            #flash('Registro exitoso')
            return redirect(url_for('iniciarSesionAdmin'))
        else:
            flash("Nombre de usuario o correco existente")
            return redirect(url_for('registroAdmin'))

@app.route('/administrador/cursos/')
def cursosAdmin():
    return render_template('administrador/cursos.html')


@app.route('/administrador/facturacion/')
def facturacionAdmin():
    return render_template('administrador/facturacion.html')

@app.route('/administrador/inicio/')
@login_requerido
def administradorInicio():
    noticias = obtener_noticias() 
    return render_template('administrador/inicio.html',noticias=noticias)


@app.route('/administrador/cursosRuta/')
def administradorCursosRuta():
    return render_template('administrador/cursosRuta.html')

@app.route('/administrador/cursosWebinar/')
def administradorCursosWebinar():
    return render_template('administrador/cursosWebinar.html')

@app.route('/administrador/inicioPadre/')
def administradorInicioPadre():
    return render_template('administrador/inicioPadre.html')

@app.route('/administrador/desarrollo/')
def administradorDesarrollo():
    return render_template('administrador/desarrollo.html')

@app.route('/administrador/desarrolloManufactura/')
def administradorDesarrolloManufactura():
    return render_template('administrador/desarrolloManufactura.html')

@app.route('/administrador/trabajo/')
def administradorTrabajo():
    return render_template('administrador/trabajo.html')

@app.route('/administrador/soporte/')
def administradorSoporte():
    return render_template('administrador/soporte.html')

@app.route('/administrador/cursosVenta/')
def administradorCursoVenta():
    return render_template('administrador/cursosVenta.html')

@app.route('/administrador/cursosUso/')
def administradorCursoUso():
    return render_template('administrador/cursosUso.html')

@app.route('/administrador/cursos/cursoForm')
def adminCursoForm():
    return render_template('administrador/cursoForm.html')

@app.route('/administrador/cursos/desarrolloForm')
def adminDesarrolloForm():
    return render_template('administrador/desarrolloForm.html')

@app.route('/administrador/cursos/jobForm')
def adminJobForm():
    return render_template('administrador/jobForm.html')



@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0",debug=True)
