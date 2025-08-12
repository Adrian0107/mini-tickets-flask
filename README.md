# Mini Tickets (Flask + SQLite)

Sistema sencillo de **gestión de tickets** para practicar un flujo full-stack con **Flask**, **SQLAlchemy**, **Flask-Login**, **Bootstrap** y **SQLite**. Incluye autenticación básica, CRUD y filtros por estado.

---

## ✨ Características
- Crear, listar, cerrar y eliminar tickets.
- Filtro por estado: *todos*, *abiertos*, *cerrados*.
- Autenticación con **Flask-Login** (login/logout).
- Persistencia con **SQLite** (por defecto). Compatible con MySQL.
- Plantillas **Jinja2** + **Bootstrap 5**.
- Integración opcional con **DBeaver** para inspección de la BD.

---

## 📦 Requisitos
- Python **3.11+**
- pip
- (Opcional) DBeaver para ver la BD

---

## 🚀 Instalación rápida

```bash
# 1) Clonar el repo
git clone https://github.com/tu_usuario/mini-tickets-flask.git
cd mini-tickets-flask

# 2) Crear y activar entorno (Windows)
python -m venv .venv
.\.venv\Scripts\Activate

# (macOS / Linux)
# python3 -m venv .venv
# source .venv/bin/activate

# 3) Instalar dependencias
pip install -r requirements.txt

# 4) Inicializar BD y crear usuario admin
# Windows (PowerShell)
set FLASK_APP=app.py
flask shell -c "from app import db; db.create_all()"
flask create-admin

# macOS / Linux
# export FLASK_APP=app.py
# flask shell -c "from app import db; db.create_all()"
# flask create-admin

# 5) Ejecutar
python app.py
# Abre http://127.0.0.1:5000
