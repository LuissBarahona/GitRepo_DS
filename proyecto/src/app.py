from flask import Flask, flash, render_template, redirect, url_for, request, session
from dao.DAOEstudiante import DAOEstudiante
import bcrypt
app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
db = DAOEstudiante()
####La función login_requerido, realiza la proteccion de las rutas###
def login_requerido(f):
    def wrapper(*args, **kwargs):
        # Verificar si el usuario está autenticado
        if 'username' not in session:
            return redirect(url_for('iniciarSesion'))  # Redirige a la página de login si no está autenticado
        return f(*args, **kwargs)  # Si está autenticado, continua con la ejecución de la ruta
    wrapper.__name__ = f.__name__ 
    return wrapper
##################Inicio######################
@app.route('/')
def inicio():
    return render_template('index.html')
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

@app.route('/estudiante/inicio/')
@login_requerido
def estudianteInicio():
    return render_template('estudiante/inicio.html')


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
################ADMINISTRADOR##############
@app.route('/administrador/')
def administrador():
    return render_template('administrador/index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0",debug=True)
