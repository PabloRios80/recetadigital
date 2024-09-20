from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from auth import role_required
from models import db, Receta, Vademecum

home_bp = Blueprint('home', __name__, template_folder='templates')

# Inicializa la aplicación Flask
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
    db.init_app(app)
    return app

# Ruta para el dashboard del médico
@home_bp.route('/medico/dashboard')
@role_required('medico')
def medico_dashboard():
    return render_template('medico_dashboard.html')

# Ruta para generar receta
@home_bp.route('/medico/receta', methods=['POST', 'GET'])
@role_required('medico')
def generar_receta():
    if request.method == 'POST':
        dni = request.form.get('dni')
        nombre_apellido = request.form.get('nombre_apellido')
        justificacion = request.form.get('justificacion')
        nombre_generico = request.form.get('nombre_generico')
        nombre_comercial = request.form.get('nombre_comercial')
        indicaciones = request.form.get('indicaciones')

        # Verifica si todos los campos requeridos están completos
        if not all([dni, nombre_apellido, justificacion, nombre_generico]):
            flash('Por favor, complete todos los campos requeridos.', 'error')
            return render_template('medico_dashboard.html')

        # Crea una nueva receta
        nueva_receta = Receta(
            dni_paciente=dni,
            nombre_apellido=nombre_apellido,
            justificacion=justificacion,
            nombre_generico=nombre_generico,
            nombre_comercial=nombre_comercial,
            indicaciones=indicaciones
        )
        db.session.add(nueva_receta)
        db.session.commit()

        flash(f'Receta generada para el paciente {nombre_apellido} con DNI {dni}', 'success')
        return redirect(url_for("home.ver_receta", receta_id=nueva_receta.id))

    return render_template('medico_dashboard.html')

@home_bp.route('/')
def index():
    return render_template('index.html')  # Crea una plantilla index.html si no existe

# Ruta para ver receta
@home_bp.route('/medico/ver_receta/<int:receta_id>')
@role_required('medico')
def ver_receta(receta_id):
    receta = Receta.query.get_or_404(receta_id)
    return render_template('ver_receta.html', receta=receta)

# Ruta para gestionar receta por el farmacéutico
@home_bp.route('/farmaceutico/gestionar_receta', methods=['POST', 'GET'])
@role_required('farmaceutico')
def gestionar_receta():
    if request.method == 'POST':
        dni = request.form.get('dni')
        receta = Receta.query.filter_by(dni_paciente=dni).first()

        if receta:
            return render_template('farmaceutico_dashboard.html', receta=receta)
        else:
            flash('No se encontró ninguna receta para el DNI ingresado.', 'error')

    return render_template('farmaceutico_dashboard.html')

# Ruta para consultar receta por el paciente
@home_bp.route('/paciente/consultar_receta', methods=['POST', 'GET'])
@role_required('paciente')
def consultar_receta():
    if request.method == 'POST':
        dni = request.form.get('dni')
        receta = Receta.query.filter_by(dni_paciente=dni).first()

        if receta:
            return render_template('paciente_dashboard.html', receta=receta)
        else:
            flash('No se encontró ninguna receta para el DNI ingresado.', 'error')

    return render_template('paciente_dashboard.html')

# NUEVO: Ruta para confirmar la entrega por el farmacéutico
@home_bp.route('/farmaceutico/confirmar_entrega', methods=['POST'])
@role_required('farmaceutico')
def confirmar_entrega():
    receta_id = request.form.get('receta_id')
    receta = Receta.query.get_or_404(receta_id)

    # Actualiza la receta con los datos de entrega
    receta.pvp = request.form.get('pvp')
    receta.cargo_afiliado = request.form.get('cargo_afiliado')
    receta.cargo_obra_social = request.form.get('cargo_obra_social')
    receta.observaciones = request.form.get('observaciones')
    receta.presentacion = request.form.get('presentacion')
    receta.cantidad_envases = request.form.get('cantidad_envases')
    
    db.session.commit()

    flash('Entrega confirmada. Revisa los datos antes de registrarla formalmente.', 'success')

    return render_template('confirmar_receta.html', receta=receta)

# NUEVO: Ruta para registrar formalmente la entrega del medicamento
@home_bp.route('/farmaceutico/registrar_entrega', methods=['POST'])
@role_required('farmaceutico')
def registrar_entrega():
    receta_id = request.form.get('receta_id')
    receta = Receta.query.get_or_404(receta_id)

    # Registra formalmente la entrega
    flash(f'Entrega registrada con éxito para la receta del paciente {receta.nombre_apellido}.', 'success')

    return redirect(url_for('home.gestionar_receta'))

# NUEVO: Ruta para agregar medicamentos al Vademecum
@home_bp.route('/agregar_medicamento', methods=['POST'])
@role_required('farmaceutico')
def agregar_medicamento():
    nombre_generico = request.form.get('nombre_generico')
    nombre_comercial = request.form.get('nombre_comercial')
    presentacion = request.form.get('presentacion')

    # Crear una nueva instancia del modelo Vademecum
    nuevo_medicamento = Vademecum(
        nombre_generico=nombre_generico,
        nombre_comercial=nombre_comercial,
        presentacion=presentacion
    )
    
    db.session.add(nuevo_medicamento)
    db.session.commit()

    flash('Medicamento agregado al Vademecum con éxito.', 'success')

    return redirect(url_for('home.farmaceutico_dashboard'))

# Ruta para el dashboard del farmacéutico
@home_bp.route('/farmaceutico_dashboard')
@role_required('farmaceutico')
def farmaceutico_dashboard():
    return render_template('farmaceutico_dashboard.html')
