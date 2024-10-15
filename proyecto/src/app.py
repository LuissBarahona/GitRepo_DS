from flask import Flask, flash, render_template, redirect, url_for, request, session
from dao.DAOEstudiante import DAOEstudiante
#lucho chupando
app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
db = DAOEstudiante()
##################Inicio######################
@app.route('/')
def inicio():
    return render_template('index.html')
##################Estudiante #################

@app.route('/estudiante/')
def iniciar_sesion():
    return render_template('estudiante/iniciar_sesion.html')

@app.route('/estudiante/registrarse/')
def registro():
    return render_template('estudiante/registrarse.html')

@app.route('/estudiante/guardar/',methods = ['POST', 'GET'])
def guardar_resgistro():
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

################ADMINISTRADOR##############
@app.route('/administrador/')
def administrador():
    return render_template('administrador/index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0",debug=True)
