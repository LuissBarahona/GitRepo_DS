from flask import Flask, flash, render_template, redirect, url_for, request, session
from dao.DAOEstudiante import DAOEstudiante
#lucho chupando GAAAAAAAAAAAAAAAAAAAAAAAAA
app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
db = DAOEstudiante()
##################Inicio######################
@app.route('/')
def inicio():
    return render_template('index.html')
##################Estudiante #################

@app.route('/estudiante/')
def iniciarSesion():
    return render_template('estudiante/iniciar_sesion.html')

@app.route('/estudiante/registrarse/')
def registro():
    return render_template('estudiante/registrarse.html')

@app.route('/estudiante/guardar/',methods = ['POST', 'GET'])
def guardarRegistro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        username = request.form.get('nombre_usuario')
        contrasena = request.form.get('contrasena')
        if db.insert({'nombre': nombre, 'apellido': apellido, 'username': username, 'contrasena': contrasena}):
            #flash('Registro exitoso')
            return redirect(url_for('facturacion'))
        else:
            flash("Error al registrar")
            return redirect(url_for('registro'))
@app.route('/estudiante/cursos/')
def cursos():
    return render_template('estudiante/cursos.html')


@app.route('/estudiante/facturacion/')
def facturacion():
    return render_template('estudiante/facturacion.html')

@app.route('/estudiante/inicio/')
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
