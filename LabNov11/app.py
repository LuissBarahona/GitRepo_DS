from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ENUM

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave secreta segura
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/db_poo'  # Cambiar a PostgreSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define el tipo ENUM con nombre
tipo_enum = ENUM('profesor', 'alumno', name='tipo_enum', create_type=True)


# Modelo para la tabla usuarios
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    codigo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    clave = db.Column(db.String(255), nullable=False)
    tipo = db.Column(tipo_enum, nullable=False)

# Ruta para la página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombres = request.form['nombres']
        login = request.form['login']
        clave = generate_password_hash(request.form['clave'], method='sha256')
        tipo = request.form['tipo']

        nuevo_usuario = Usuario(nombres=nombres, login=login, clave=clave, tipo=tipo)
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash("Error al registrarse: " + str(e), "danger")

    return render_template('register.html')

# Ruta para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        clave = request.form['clave']
        usuario = Usuario.query.filter_by(login=login).first()

        if usuario and check_password_hash(usuario.clave, clave):
            session['usuario_id'] = usuario.codigo
            session['usuario_tipo'] = usuario.tipo
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Credenciales incorrectas", "danger")

    return render_template('login.html')

# Ruta de la página de dashboard (simplemente como ejemplo)
@app.route('/dashboard')
def dashboard():
    if 'usuario_id' in session:
        return f"Bienvenido al dashboard, usuario tipo {session['usuario_tipo']}!"
    else:
        return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=7000)

