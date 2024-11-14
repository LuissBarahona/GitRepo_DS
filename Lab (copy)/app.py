from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave segura

# Configuración de la conexión a la base de datos
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="mi_base_de_datos",
        user="usuario",
        password="contraseña",
        cursor_factory=RealDictCursor
    )

# Ruta de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombres = request.form['nombres']
        login = request.form['login']
        clave = generate_password_hash(request.form['clave'])
        tipo = request.form['tipo']

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO usuarios (nombres, login, clave, tipo) VALUES (%s, %s, %s, %s)",
                        (nombres, login, clave, tipo))
            conn.commit()
            flash("Usuario registrado exitosamente", "success")
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", "danger")
        finally:
            cur.close()
            conn.close()
    return render_template('register.html')

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        clave = request.form['clave']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE login = %s", (login,))
        usuario = cur.fetchone()
        cur.close()
        conn.close()

        if usuario and check_password_hash(usuario['clave'], clave):
            session['user_id'] = usuario['codigo']
            session['nombres'] = usuario['nombres']
            session['tipo'] = usuario['tipo']

            # Redirigir según el tipo de usuario
            if usuario['tipo'] == 'alumno':
                return redirect(url_for('alumno_home'))
            elif usuario['tipo'] == 'profesor':
                return redirect(url_for('profesor_home'))
        else:
            flash("Credenciales incorrectas", "danger")
    return render_template('login.html')

# Ruta para alumnos
@app.route('/alumno/home')
def alumno_home():
    if 'user_id' not in session or session['tipo'] != 'alumno':
        flash("Acceso denegado", "danger")
        return redirect(url_for('login'))
    return render_template('alumnoHome.html')

# Ruta para profesores
@app.route('/profesor/home')
def profesor_home():
    if 'user_id' not in session or session['tipo'] != 'profesor':
        flash("Acceso denegado", "danger")
        return redirect(url_for('login'))
    return render_template('profesorHome.html')

# Rutas para manejar los botones
@app.route('/alumno/<action>')
def alumno_action(action):
    return f"Alumno - Acción seleccionada: {action}"

@app.route('/profesor/<action>')
def profesor_action(action):
    return f"Profesor - Acción seleccionada: {action}"

# Ruta de logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
