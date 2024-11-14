from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/flask_db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    clave = db.Column(db.String(60), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # 'alumno' o 'profesor'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        codigo = request.form.get("codigo")
        nombres = request.form.get("nombres")
        login = request.form.get("login")
        clave = bcrypt.generate_password_hash(request.form.get("clave")).decode('utf-8')
        tipo = request.form.get("tipo")
        user = User(codigo=codigo, nombres=nombres, login=login, clave=clave, tipo=tipo)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        clave = request.form.get("clave")
        user = User.query.filter_by(login=login).first()
        if user and bcrypt.check_password_hash(user.clave, clave):
            login_user(user)
            return redirect(url_for("home"))
        flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html")

@app.route("/home")
@login_required
def home():
    if current_user.tipo == "alumno":
        return render_template("alumno_home.html")
    elif current_user.tipo == "profesor":
        return render_template("profesor_home.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
