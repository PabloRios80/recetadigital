from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Dummy database (use a real database in production)
users_db = {}
roles = {'medico': 'medico', 'farmaceutico': 'farmaceutico', 'paciente': 'paciente'}

# Decorador para verificar el rol del usuario
def role_required(role):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if 'role' not in session:
                flash("Por favor, inicia sesión para acceder a esta página.", 'error')
                return redirect(url_for('auth.login'))
            
            if session['role'] != role:
                flash("No tienes permisos para acceder a esta página.", 'error')
                return redirect(url_for('home.index'))  # O donde prefieras redirigir
            
            return func(*args, **kwargs)
        return decorated_view
    return wrapper

# Ruta para el inicio de sesión
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verificar si el usuario existe y la contraseña es correcta
        user = users_db.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['role'] = user['role']
            flash('Inicio de sesión exitoso', 'success')

            # Redirigir según el rol del usuario
            if user['role'] == 'medico':
                return redirect(url_for('auth.medico_dashboard'))
            elif user['role'] == 'farmaceutico':
                return redirect(url_for('auth.farmaceutico_dashboard'))
            elif user['role'] == 'paciente':
                return redirect(url_for('auth.paciente_dashboard'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'error')
    
    return render_template('auth_login.html')

# Ruta para el registro de usuarios
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        if username in users_db:
            flash('El nombre de usuario ya existe', 'error')
        else:
            users_db[username] = {'password': generate_password_hash(password), 'role': role}
            flash('Registro exitoso', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('auth_register.html', roles=roles)

# Ruta protegida para médicos
@auth_bp.route('/medico_dashboard')
@role_required('medico')
def medico_dashboard():
    return render_template('medico_dashboard.html')

# Ruta protegida para farmacéuticos
@auth_bp.route('/farmaceutico_dashboard')
@role_required('farmaceutico')
def farmaceutico_dashboard():
    return render_template('farmaceutico_dashboard.html')

# Ruta protegida para pacientes
@auth_bp.route('/paciente_dashboard')
@role_required('paciente')
def paciente_dashboard():
    return render_template('paciente_dashboard.html')

# Ruta para cerrar sesión
@auth_bp.route('/logout')
def logout():
    session.clear()  # Limpiar la sesión
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('auth.login'))
