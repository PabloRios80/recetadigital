from flask import Blueprint, render_template, request, redirect, url_for, flash
from auth import role_required  # Asegúrate de importar el decorador role_required

recipes_bp = Blueprint('recipes', __name__, template_folder='templates')

# Dummy database for recipes
recipes_db = []

@recipes_bp.route('/medical_form', methods=['GET', 'POST'])
@role_required('medico')  # Solo médicos pueden acceder
def medical_form():
    if request.method == 'POST':
        recipe = {
            'nombre_apellido': request.form['nombre_apellido'],
            'dni': request.form['dni'],
            'justificacion_clinica': request.form['justificacion_clinica'],
            'nombre_generico': request.form['nombre_generico'],
            'nombre_comercial': request.form['nombre_comercial'],
            'presentacion': request.form['presentacion']
        }
        recipes_db.append(recipe)
        flash('Receta registrada correctamente', 'success')
        return redirect(url_for('recipes.recipe_list'))
    
    return render_template('medical_form.html')

@recipes_bp.route('/recipe_list', methods=['GET'])
@role_required('medico')  # Solo médicos pueden acceder
def recipe_list():
    return render_template('recipe_list.html', recipes=recipes_db)

@recipes_bp.route('/pharmacist_form/<int:recipe_id>', methods=['GET', 'POST'])
@role_required('farmaceutico')  # Solo farmacéuticos pueden acceder
def pharmacist_form(recipe_id):
    recipe = next((r for r in recipes_db if recipes_db.index(r) == recipe_id), None)
    if not recipe:
        flash('Receta no encontrada', 'error')
        return redirect(url_for('recipes.recipe_list_pharmacist'))
    
    if request.method == 'POST':
        recipe.update({
            'pvp': request.form['pvp'],
            'a_cargo_afiliado': request.form['a_cargo_afiliado'],
            'a_cargo_obrasocial': request.form['a_cargo_obrasocial'],
            'observaciones': request.form['observaciones']
        })
        flash('Receta actualizada correctamente', 'success')
        return redirect(url_for('recipes.recipe_list_pharmacist'))
    
    return render_template('pharmacist_form.html', recipe=recipe)

@recipes_bp.route('/recipe_list_pharmacist', methods=['GET'])
@role_required('farmaceutico')  # Solo farmacéuticos pueden acceder
def recipe_list_pharmacist():
    return render_template('recipe_list_pharmacist.html', recipes=recipes_db)
