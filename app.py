from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    current_user,
    login_required,
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"  # cámbiala en prod
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tickets.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ---------- MODELOS ----------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)  # simple: primer usuario admin

    def set_password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="abierto")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------- LOGIN MANAGER ----------
login_manager = LoginManager(app)
login_manager.login_view = "login"  # si no está logueado, redirige aquí


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------- RUTAS ----------
@app.route("/")
def home():
    status = request.args.get("status", "todos")
    q = Ticket.query
    if status == "abiertos":
        q = q.filter_by(status="abierto")
    elif status == "cerrados":
        q = q.filter_by(status="cerrado")
    tickets = q.order_by(Ticket.created_at.desc()).all()
    return render_template("index.html", tickets=tickets, status=status)


@app.route("/tickets/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        if not title or not description:
            flash("Título y descripción son requeridos.")
            return redirect(url_for("nuevo"))
        db.session.add(Ticket(title=title, description=description))
        db.session.commit()
        flash("✅ Ticket creado.")
        return redirect(url_for("home"))
    return render_template("new_ticket.html")


@app.route("/tickets/<int:ticket_id>/cerrar", methods=["POST"])
@login_required
def cerrar(ticket_id):
    t = Ticket.query.get_or_404(ticket_id)
    t.status = "cerrado"
    db.session.commit()
    flash("🟢 Ticket cerrado.")
    return redirect(url_for("home"))


@app.route("/tickets/<int:ticket_id>/eliminar", methods=["POST"])
@login_required
def eliminar(ticket_id):
    t = Ticket.query.get_or_404(ticket_id)
    db.session.delete(t)
    db.session.commit()
    flash("🗑️ Ticket eliminado.")
    return redirect(url_for("home"))


# ---------- AUTH ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Bienvenido 👋")
            next_url = request.args.get("next") or url_for("home")
            return redirect(next_url)
        flash("Usuario o contraseña incorrectos.")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.")
    return redirect(url_for("login"))


# ---------- INIT DB ----------
@app.cli.command("create-admin")
def create_admin():
    """Crea un usuario admin interactivo: flask create-admin"""
    username = input("Usuario admin: ").strip()
    password = input("Contraseña: ").strip()
    if User.query.filter_by(username=username).first():
        print("Ya existe ese usuario.")
        return
    u = User(username=username, is_admin=True)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    print("Admin creado ✅")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
