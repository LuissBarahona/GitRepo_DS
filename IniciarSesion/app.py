import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_secret_key")


def get_db_connection():
    retries = 10  # Aumenta el número de reintentos
    delay = 5  # Espera de 5 segundos entre cada intento

    db_host = os.getenv("DATABASE_HOST")
    db_name = os.getenv("DATABASE_NAME")
    db_user = os.getenv("DATABASE_USER")
    db_password = os.getenv("DATABASE_PASSWORD")

    # Verifica si todas las variables de entorno están configuradas
    if not all([db_host, db_name, db_user, db_password]):
        raise Exception("Faltan variables de entorno para la conexión a la base de datos.")

    while retries > 0:
        try:
            print("Intentando conectar a la base de datos...")
            conn = psycopg2.connect(
                host=db_host,
                database=db_name,
                user=db_user,
                password=db_password,
                cursor_factory=RealDictCursor
            )
            print("Conexión a la base de datos establecida exitosamente.")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Error de conexión: {e}")
            retries -= 1
            print(f"Reintentando en {delay} segundos... Intentos restantes: {retries}")
            time.sleep(delay)
    raise Exception("No se pudo conectar a la base de datos después de varios intentos.")


@app.route('/')
def home():
    return render_template('home.html')

# Ruta de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombres = request.form['nombres']
        login = request.form['login']
        clave = generate_password_hash(request.form['clave'])
        tipo = request.form['tipo']

        try:
           
            conn = get_db_connection()

            cur = conn.cursor()
            cur.execute("INSERT INTO usuarios (nombres, login, clave, tipo) VALUES (%s, %s, %s, %s)",
                        (nombres, login, clave, tipo))
            conn.commit()
            flash("Usuario registrado exitosamente", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error al registrar usuario: {str(e)}", "danger")
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
    return render_template('register.html')

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        clave = request.form['clave']

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuarios WHERE login = %s", (login,))
            usuario = cur.fetchone()
        finally:
            if 'cur' in locals() and cur:
                cur.close()
            if 'conn' in locals() and conn:
                conn.close()


        if usuario and check_password_hash(usuario['clave'], clave):
            session['user_id'] = usuario['codigo']
            session['nombres'] = usuario['nombres']
            session['tipo'] = usuario['tipo']

            if usuario['tipo'] == 'alumno':
                return redirect(url_for('alumno_home'))
            elif usuario['tipo'] == 'profesor':
                return redirect(url_for('profesor_home'))
        else:
            flash("Credenciales incorrectas", "danger")
    return render_template('login.html')

# Rutas adicionales
@app.route('/alumno/home')
def alumno_home():
    if 'user_id' not in session or session['tipo'] != 'alumno':
        flash("Acceso denegado", "danger")
        return redirect(url_for('login'))
    return render_template('alumnoHome.html')

@app.route('/profesor/home')
def profesor_home():
    if 'user_id' not in session or session['tipo'] != 'profesor':
        flash("Acceso denegado", "danger")
        return redirect(url_for('login'))
    return render_template('profesorHome.html')

@app.route('/alumno/<action>')
def alumno_action(action):
    return f"Alumno - Acción seleccionada: {action}"

@app.route('/profesor/<action>')
def profesor_action(action):
    return f"Profesor - Acción seleccionada: {action}"

@app.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
