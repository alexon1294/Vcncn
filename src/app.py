from flask import (Flask, render_template, request, 
                   redirect, url_for, flash, jsonify, 
                   send_file, session, make_response, current_app)
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from decouple import config
from config import config
from flask_jwt_extended import (JWTManager, jwt_required, 
                                get_jwt_identity,create_access_token, verify_jwt_in_request)
from functools import wraps
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
from urllib.parse import quote
import json

#utils:
from utils.Security import Security

# Model user:
from models.ModelUser import ModelUser

# Model table:
from models.ModelTable import ModelTable

#Model aplicante:
from models.ModelAplicante import ModelAplicante

#Model lote:
from models.ModelLote import ModelLote

#Model comprobante:
from models.ModelComprobante import ModelComprobante

# Entities:
from models.entities.User import User

from models.entities.Table import Table


app = Flask(__name__)

app.permanent_session_lifetime = timedelta(minutes=30)

app.config['UPLOAD_FOLDER'] = './excel/'
app.config['COMPROBANTES_FOLDER'] = '../comprobantes/'

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# # Inicialización del JWTManager
# jwt = JWTManager(app)

# Inicializacion de la Base de Datos
db = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user:
            if logged_user.password:    #verificamos si la contrasena ingresada 
                                        #es igual a la haseada en la db
                session["logged_in"]= True
                session["fullname"] = logged_user.fullname
                return redirect('/home')
            else:
                flash('Contrasena invalida.')
                return render_template('auth/login.html', success=False)
        else:
            flash("Usuario no encontrado.")
            return render_template('auth/login.html', succes=False)
    else:
        return render_template('auth/login.html')
    
@app.route('/logout')
def logout():
    session.pop('logged_in', False)
    return redirect(url_for('login'))

@app.route('/home', methods=['GET'])
@login_required
def home():
    fullname = session.get('fullname')
    return render_template('home.html', fullname=fullname)

@app.route('/table', methods=['GET', 'POST'])
@login_required
def table():
    try:
        excel_folder = app.config['UPLOAD_FOLDER']
        loaded_files = os.listdir(excel_folder)

        aplicantes = ModelAplicante.get_aplicante_rows(db)
        lotes = ModelLote.get_lote_rows(db)

        return render_template('table.html', loaded_files=loaded_files, aplicantes=aplicantes, lotes=lotes)

    except Exception as e:
        print(f"Error: {e}")
        loaded_files = []  # En caso de error, se muestra una lista vacía

    return render_template('table.html', loaded_files=loaded_files)

@app.route('/dataTable', methods=['GET', 'POST'])
@login_required
def get_data():
    try:
        search_value = request.args.get('search', default=None)
        columns_value = request.args.get('columns', default=None)

        columns = columns_value.split(',') if columns_value else None
        search = search_value if search_value else None

        table_entries = ModelTable.get_table_rows(db, search=search, columns=columns)

        if table_entries:
            return jsonify(table_entries)
        else:
            return jsonify(message='No se encontraron entradas en la tabla.')
    except Exception as e:
        return jsonify(message=f'Error: {e}')

@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    try:
        if 'archivo' in request.files:
            file = request.files['archivo']
            if not file.filename == '':
                if allowed_file(file.filename):
                    if not os.path.exists(app.config['UPLOAD_FOLDER']):
                        os.makedirs(app.config['UPLOAD_FOLDER'])
                    else:
                        file_path =os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                    if not os.path.exists(file_path):
                        file.save(file_path.replace('\\','/'))
                        flash('Archivo cargado correctamente.', 'success')
                    else:
                        flash('Archivo ya cargado.', 'warning')
                else:
                    flash('Archivo incompatible.', 'error')
            else:
                flash('No has cargado un archivo.', 'error')
    except Exception as ex:
        flash(f'Error al cargar el archivo: {ex}.', 'error')

    return redirect('/table')

@app.route('/generate_table', methods=['GET', 'POST'])
def generate_table():
    file_name = request.form['file_name']
    file_path = f'./excel/{quote(file_name)}'
    try:
        if os.path.exists(file_path):
            ModelTable.update_table_from_excel(db, file_path)
            
            flash('Tabla generada con éxito.', 'success-deleteGenerate')
        else:
            flash('No se pudo generar la tabla.', 'error-deleteGenerate')
    except Exception as e:
        flash(f'Error al generar el archivo: {str(e)}', 'error-deleteGenerate')
    
    return redirect('/table')

@app.route('/delete_excel', methods=['POST'])
def delete_excel():
    file_name = request.form['file_name']
    file_path = f'./excel/{quote(file_name)}'
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            flash(f'Archivo {file_name} eliminado correctamente.', 'success-deleteGenerate')
        else:
            flash('El archivo no existe.', 'error-deleteGenerate')
    except Exception as e:
        flash(f'Error al eliminar el archivo: {str(e)}', 'error-deleteGenerate')
    
    return redirect('/table')

@app.route('/update_cell', methods=['GET', 'POST'])
def update_cell():
    try:
        data = request.json
        new_cells = data.get('nuevosValores')

        if ModelTable.update_table_row(db, new_cells):
            flash('Datos actualizados correctamente.', 'update-cell-success')
            return jsonify({'message': 'Datos actualizados correctamente.', 'new_cells': new_cells[1:], 'success':True})
        else:
            flash('No se pudo actualizar la celda.', 'update-cell-error')
            return jsonify({'message': 'Datos invalidos.', 'success':False})
        
    except Exception as e:
        flash(f"'Error': {str(e)}")
        return jsonify({'message':f'error ,{str(e)}', 'success':False})

@app.route('/comprobante', methods=['POST'])
def comprobante():
    if request.method == 'POST':
        datos = request.get_json()

        id = datos['valores'][0]
        a_paterno = datos['valores'][1]
        a_materno = datos['valores'][2]
        nombre = datos['valores'][3]
        id_lote = datos['valores'][4]
        id_aplicante = datos['valores'][5]
        lote = datos['valores'][6]
        aplicante = datos['valores'][7]

        # Construimos la URL con los argumentos
        url = f'/generar_comprobante?id={id}&nombre={nombre}&a_paterno={a_paterno}&a_materno={a_materno}&id_lote={id_lote}&id_aplicante={id_aplicante}&lote={lote}&aplicante={aplicante}'

        return jsonify({'url': url})

@app.route('/guardar_opcion/<string:opcion>', methods=['POST'])
def guardar_opcion_lote(opcion):
    datos = request.get_json()
    if opcion == 'lote':
        lote = datos['opcionLote']
        existe = ModelLote.guardar_nuevo_lote(db, lote)
        if existe != None:
            flash('Lote creado.', 'creado-success')
        else:
            flash('Lote no pudo crearse.', 'creado-error')
        return jsonify({'existe': existe}) #existe devuelve None o el id del lote agregado

    elif opcion == 'aplicante':
        aplicante = datos['opcionAplicante'].title()
        existe = ModelAplicante.guardar_nuevo_aplicante(db, aplicante)
        if existe != None:
            flash('Nombre de aplicante creado.', 'creado-success')
        else:
            flash('Nombre de aplicante no pudo crearse', 'creado-error')
        return jsonify({'existe': existe})

@app.route('/borrar_opcion/<string:nombre_opcion>/<string:id_opcion>', methods=['DELETE'])
def borrar_opcion(nombre_opcion, id_opcion):
    existe = False
    
    if nombre_opcion == 'lote':
        existe = ModelLote.borrar_lote(db, id_opcion)
        print(existe)
    elif nombre_opcion == 'aplicante':
        existe = ModelAplicante.borrar_aplicante(db, id_opcion)

    return jsonify({'existe': existe})

@app.route('/generar_comprobante')
def generar_comprobante():
    nombre = request.args.get('nombre').title()
    a_paterno = request.args.get('a_paterno').title()
    a_materno = request.args.get('a_materno').title()
    id = request.args.get('id')
    id_aplicante = request.args.get('id_aplicante')
    id_lote = request.args.get('id_lote')
    lote = request.args.get('lote')
    nombre_completo_aplicante = request.args.get('aplicante')
    print(nombre_completo_aplicante)
    # Obtenemos la fecha y hora actual para mostrar en el comprobante
    fecha_generacion_comprobante = datetime.now().strftime("%Y-%m-%d %H:%M")

    comprobante = ModelComprobante.crear_comrpobante(db, id, id_lote, id_aplicante, fecha_generacion_comprobante)
        
    return render_template('comprobante.html', nombre=nombre, a_paterno=a_paterno, a_materno=a_materno, nombre_completo_aplicante=nombre_completo_aplicante,
                                                 lote=lote, fecha_generacion_comprobante=fecha_generacion_comprobante, comprobante=comprobante)

@app.route('/registro_publico', methods=['GET'])
def registro_publico():
    return render_template('registro_publico.html')

@app.route('/formularioRegistro', methods=['POST'])
def formulario_registro():
    datos = request.json
    nombre = datos.get('nombre')
    fecha_generacion_comprobante = datetime.now().strftime("%Y-%m-%d %H:%M")

    datos_registro = [
        fecha_generacion_comprobante,
        nombre,
        datos.get('a_paterno'),
        datos.get('a_materno'),
        datos.get('f_nacimiento'),
        datos.get('edad'),
        datos.get('sexo'),
        datos.get('alergias'),
        datos.get('detalleAlergia'),
        datos.get('fechaVacunaCovid'),
        datos.get('fechaVacunaInfluenza'),
        datos.get('telefono'),
        datos.get('email'),
        datos.get('calle'),
        datos.get('numext'),
        datos.get('colonia'),
        datos.get('municipio'),
        datos.get('cp'),
        datos.get('aplicaVacunaCovid'),
        datos.get('aplicaVacunaInfluenza'),
        
    ]
    print(datos_registro)
    registro = ModelTable.add_new_row(db, datos_registro)

    if not registro:
        print('Error de registro.')
    else:
        print('Registro exitoso.')
    return jsonify({'nombre': nombre})

@app.route('/gracias_registro/<name>', methods=['GET'])
def gracias_registro(name):
    return render_template('gracias_registro.html', name=name)

def status_401(error):
    return "<h1>Página no encontrada</h1>"

def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    # csrf.init_app(app)
    #mapeo de errores mediante register_error_handler
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
