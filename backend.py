from flask import Flask, jsonify, request
from flask_cors import CORS
from flaskext.mysql import MySQL #pip install flask-mysql
import pymysql
from flasgger import Swagger

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'tp'
app.config['MYSQL_DATABASE_PASSWORD'] = 'trabajop@'
app.config['MYSQL_DATABASE_DB'] = 'hospital'
app.config['MYSQL_DATABASE_HOST'] = '13.58.169.125' #no olvidar cambiar la ip
mysql.init_app(app)

swagger = Swagger(app)

#enable CORS
CORS(app, resources={r'/*': {'origins': ''}})

# sanity check route
@app.route('/')
def home():
    tabla = request.args.get('tabla', 'paciente')
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM {}".format(tabla))
        data = cursor.fetchall()
        return jsonify({
            'status': 'success',
            'data': data,
            'tabla': tabla
        })
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# GET'S ALL

@app.route('/pacientes', methods=['GET'])
def pacientes():
    """
    Obtiene una lista de todos los pacientes.
    ---
    responses:
      200:
        description: Lista de pacientes.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM paciente order by idPaciente")
    data = cursor.fetchall()
    return jsonify({
        'status': 'success',
        'Pacientes': data
    })

@app.route('/medicos', methods=['GET'])
def medicos():
    """
    Obtiene una lista de todos los médicos
    ---
    responses:
      200:
        description: Lista de médicos.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM medico order by idMedico")
    data = cursor.fetchall()
    return jsonify({
        'status': 'success',
        'Medicos': data
    })

@app.route('/citas', methods=['GET'])
def citas():
    """
    Obtiene una lista de todos los citas
    ---
    responses:
      200:
        description: Lista de citas.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM Cita order by idCita")
    data = cursor.fetchall()
    return jsonify({
        'status': 'success',
        'Citas': data
    })

@app.route('/tratamientos', methods=['GET'])
def tratamientos():
    """
    Obtiene una lista de todos los tratamientps
    ---
    responses:
      200:
        description: Lista de tratamientos.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM tratamiento order by idTratamiento")
    data = cursor.fetchall()
    return jsonify({
        'status': 'success',
        'Tratamientos': data
    })

@app.route('/especialidades', methods=['GET'])
def especialidades():
    """
    Obtiene una lista de todos los especialidades
    ---
    responses:
      200:
        description: Lista de especialidades.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM especialidad order by idEspecialidad")
    data = cursor.fetchall()
    return jsonify({
        'status': 'success',
        'Especialidad': data
    })

@app.route('/especialidadmedicos', methods=['GET'])
def especialidadmedicos():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM especialidadMedico")
    data = cursor.fetchall()
    return jsonify({
        'status': 'success',
        'EspecialidadMedico': data
    })

@app.route('/schedules', methods=['GET']) 
def schedules():
    """
    Obtiene una lista de todos los schedules
    ---
    responses:
      200:
        description: Lista de schedules.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM schedule")
    data = cursor.fetchall()
    for row in data: 
        row['Hora'] = str(row['Hora'])
    return jsonify({
        'status': 'success',
        'Schedule': data
    })

@app.route('/compras', methods=['GET'])
def compras():
    """
    Obtiene una lista de todos los compras
    ---
    responses:
      200:
        description: Lista de compras.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM compra")
    data = cursor.fetchall()
    return jsonify({
        'status': 'success',
        'Compra': data
    })

@app.route('/medicamentos', methods=['GET'])
def medicamentos():
    """
    Obtiene una lista de todos los medicamentos
    ---
    responses:
        200:
            description: Lista de medicamentos.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM medicamento")
    data = cursor.fetchall()
    return jsonify({
        'status': 'success',
        'Medicamento': data
    })

#GET'S BY ID

@app.route('/paciente/<string:id>', methods=['GET'])
def paciente_id(id):
    """
    Obtiene información de un paciente por su ID.
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID del paciente a consultar.
    responses:
      200:
        description: Información del paciente.
      404:
        description: Paciente no encontrado.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(id)
    cursor.execute("SELECT * FROM paciente WHERE idPaciente = %s", [id])
    row = cursor.fetchone()

    return jsonify({
        'status': 'success',
        'paciente' + id : row
    })

@app.route('/especialidad/<string:id>', methods=['GET'])
def especialidad_id(id):
    """
    Obtiene información de una especialidad por su ID.
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID de la especialidad a consultar.
    responses:
      200:
        description: Información de la especialidad.
      404:
        description: Especialidad no encontrado.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(id)
    cursor.execute("SELECT * FROM especialidad WHERE IdEspecialidad = %s", [id])
    row = cursor.fetchone()

    return jsonify({
        'status': 'success',
        'especialidad' + id: row
    })

@app.route('/medico/<string:id>', methods=['GET'])
def medico_id(id):
    """
    Obtiene información de un medico por su ID.
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID del medico a consultar.
    responses:
      200:
        description: Información del medico.
      404:
        description: Medico no encontrado.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(id)
    cursor.execute("SELECT * FROM medico WHERE idMedico = %s", [id])
    row = cursor.fetchone()

    return jsonify({
        'status': 'success',
        'medico' + id: row
    })        

@app.route('/cita/<string:id>', methods=['GET'])    
def cita_id(id):
    """
    Obtiene información de una cita por su ID.
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID de la cita a consultar.
    responses:
      200:
        description: Información de la cita.
      404:
        description: Cita no encontrado.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(id)
    cursor.execute("SELECT * FROM Cita WHERE idCita = %s", [id])
    row = cursor.fetchone()
    return jsonify({
        'status': 'success',
        'cita' + id: row
    })

@app.route('/tratamiento/<string:id>', methods=['GET'])
def tratamiento_id(id):
    """
    Obtiene información de un tratamiento por su ID.
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID del tratamiento a consultar.
    responses:
      200:
        description: Información del tratamiento.
      404:
        description: Tratamiento no encontrado.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(id)
    cursor.execute("SELECT * FROM tratamiento WHERE idTratamiento = %s", [id])
    row = cursor.fetchone()

    return jsonify({
        'status': 'success',
        'tratamiento' + id: row
    })

@app.route('/compra/<string:id>', methods=['GET'])
def compra_id(id):
    """
    Obtiene información de una compra por su ID.
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID de la compra a consultar.
    responses:
      200:
        description: Información de la compra.
      404:
        description: Compra no encontrado.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(id)
    cursor.execute("SELECT * FROM compra WHERE idCompra = %s", [id])
    row = cursor.fetchone()

    return jsonify({
        'status': 'success',
        'compra' + id: row
    })

@app.route('/schedule/<string:id>', methods=['GET'])
def schedule_id(id):
    """
    Obtiene información de un schedule por su ID.
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID del schedule a consultar.
    responses:
      200:
        description: Información del schedule.
      404:
        description: Schedule no encontrado.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(id)
    cursor.execute("SELECT * FROM schedule WHERE idSchedule = %s", [id])
    row = cursor.fetchone() 
    row['Hora'] = str(row['Hora'])
    return jsonify({
        'status': 'success',
        'schedule' + id: row
    })

@app.route('/medicamento/<string:id>', methods=['GET'])
def medicamento_id(id):
    """
    Obtiene información de un medicamento por su ID.
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID del medicamento a consultar.
    responses:
      200:
        description: Información del medicamento.
      404:
        description: Medicamento no encontrado.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(id)
    cursor.execute("SELECT * FROM medicamento WHERE idMedicamento = %s", [id])
    row = cursor.fetchone()

    return jsonify({
        'status': 'success',
        'medicamento' + id: row
    })

# POST'S 

@app.route('/paciente', methods=['POST'])
def paciente():
    """
    Agrega un nuevo paciente.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombreP:
              type: string
            apellidoPP:
              type: string
            apellidoMP:
              type: string
            dniP:
              type: string
            generoP:
              type: string
            fnacimientoP:
              type: string
            emailP:
              type: string
            telefonoP:
              type: string
    responses:
      200:
        description: Paciente agregado exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        nombre = post_data.get('nombreP')
        apellidop = post_data.get('apellidoPP')
        apellidom = post_data.get('apellidoMP')
        dni = post_data.get('dniP')
        genero = post_data.get('generoP')
        fnac = post_data.get('fnacimientoP')
        email = post_data.get('emailP')
        telef = post_data.get('telefonoP')

        print(nombre)
        print(apellidop)
        print(apellidom)
        print(dni)
        print(genero)
        print(fnac)
        print(email)
        print(telef)

        sql = "INSERT INTO paciente (nombreP, apellidoPP, apellidoMP, dniP, generoP, fnacimientoP, emailP, telefonoP) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (nombre, apellidop, apellidom, dni, genero, fnac, email, telef)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        response_object['message'] = 'Paciente agregado!'
    return jsonify(response_object)

@app.route('/medico', methods=['POST'])
def medico():
    """
    Agrega un nuevo médico.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombreM:
              type: string
            apellidoPM:
              type: string
            apellidoMM:
              type: string
            dniM:
              type: string
            generoM:
              type: string
            emailM:
              type: string
            telefonoM:
              type: string
            numColegialM:
              type: string
    responses:
      200:
        description: Médico agregado exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        nombreM = post_data.get('nombreM')
        apellidoPM = post_data.get('apellidoPM')
        apellidoMM = post_data.get('apellidoMM')
        dniM = post_data.get('dniM')
        generoM = post_data.get('generoM')
        emailM = post_data.get('emailM')
        telefonoM = post_data.get('telefonoM')
        numColegialM = post_data.get('numColegialM')

        print(nombreM)
        print(apellidoPM)
        print(apellidoMM)
        print(dniM)
        print(generoM)
        print(emailM)
        print(telefonoM)
        print(numColegialM)

        sql = "INSERT INTO medico (nombreM, apellidoPM, apellidoMM, dniM, generoM, emailM, telefonoM, numColegialM) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (nombreM, apellidoPM, apellidoMM, dniM, generoM, emailM, telefonoM, numColegialM)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        response_object['message'] = 'Medico agregado!'
    return jsonify(response_object)

@app.route('/cita', methods=['POST'])
def cita():
    """
    Agrega una nueva cita.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            IdPaciente:
              type: integer
            IdSchedule:
              type: integer
    responses:
      200:
        description: Cita agregada exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        IdPaciente = post_data.get('IdPaciente')
        IdSchedule = post_data.get('IdSchedule')

        print(IdPaciente)
        print(IdSchedule)

        sql = "INSERT INTO Cita (IdPaciente, IdSchedule) VALUES (%s, %s)"
        data = (IdPaciente, IdSchedule)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        response_object['message'] = 'Cita agregada!'
    return jsonify(response_object)

@app.route('/tratamiento', methods=['POST'])  
def tratamiento():
    """
    Agrega un nuevo tratamiento.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            descripcion:
              type: string
            duracion:
              type: string
            tratamiento:
              type: string
            idCita:
              type: integer
    responses:
      200:
        description: Tratamiento agregado exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        descripcion = post_data.get('descripcion')
        duracion = post_data.get('duracion')
        tratamiento = post_data.get('tratamiento')
        idCita = post_data.get('idCita')

        print(descripcion)
        print(duracion)
        print(tratamiento)
        print(idCita)

        sql = "INSERT INTO tratamiento (descripcion, duracion, tratamiento, idCita) VALUES (%s, %s, %s, %s)"
        data = (descripcion, duracion, tratamiento, idCita)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        response_object['message'] = 'Tratamiento agregado!'
    return jsonify(response_object)

@app.route('/especialidad', methods=['POST'])
def especialidad():
    """
    Agrega una nueva especialidad.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            descripcion:
              type: string
    responses:
      200:
        description: Especialidad agregada exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        descripcion = post_data.get('descripcion')

        print(descripcion)

        sql = "INSERT INTO especialidad (descripcion) VALUES (%s)"
        data = (descripcion)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        response_object['message'] = 'Especialidad agregada!'
    return jsonify(response_object)

@app.route('/especialidadmedico', methods=['POST'])
def especialidadmedico():
    """
    Agrega una nueva especialidad médica para un médico.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idMedico:
              type: integer
            idEspecialidad:
              type: integer
            aniosExp:
              type: integer
    responses:
      200:
        description: Especialidad médica agregada exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        idMedico = post_data.get('idMedico')
        idEspecialidad = post_data.get('idEspecialidad')
        aniosExp = post_data.get('aniosExp')

        print(idMedico)
        print(idEspecialidad)
        print(aniosExp)

        sql = "INSERT INTO especialidadMedico (idMedico, idEspecialidad, aniosExp) VALUES (%s, %s, %s)"
        data = (idMedico, idEspecialidad, aniosExp)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        response_object['message'] = 'EspecialidadMedico agregada!'
    return jsonify(response_object)

@app.route('/schedule', methods=['POST'])
def schedule():
    """
    Agrega un nuevo horario de consulta.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            Fecha:
              type: string
            Hora:
              type: string
            IdMedico:
              type: integer
            IdEspecialidad:
              type: integer
    responses:
      200:
        description: Horario de consulta agregado exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        Fecha = post_data.get('Fecha')
        Hora = post_data.get('Hora')
        IdMedico = post_data.get('IdMedico')
        IdEspecialidad = post_data.get('IdEspecialidad')

        print(Fecha)
        print(Hora)
        print(IdMedico)
        print(IdEspecialidad)

        sql = "INSERT INTO schedule (Fecha, Hora, IdMedico, IdEspecialidad) VALUES (%s, %s, %s, %s)"
        data = (Fecha, Hora, IdMedico, IdEspecialidad)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        response_object['message'] = 'Schedule agregado!'
    return jsonify(response_object)

@app.route('/compra', methods=['POST'])
def compra():
    """
    Agrega una nueva compra de medicamento.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            Fecha:
              type: string
            Cantidad:
              type: integer
            Precio:
              type: float
            total:
              type: float
            IdTratamiento:
              type: integer
            IdPaciente:
              type: integer
            IdMedicamento:
              type: integer
    responses:
      200:
        description: Compra de medicamento agregada exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        Fecha = post_data.get('Fecha')
        Cantidad = post_data.get('Cantidad')
        Precio = post_data.get('Precio')
        total = post_data.get('total')
        IdTratamiento = post_data.get('IdTratamiento')
        IdPaciente = post_data.get('IdPaciente')
        IdMedicamento = post_data.get('IdMedicamento')

        print(Fecha)
        print(Cantidad)
        print(Precio)
        print(total)
        print(IdTratamiento)
        print(IdPaciente)
        print(IdMedicamento)

        sql = "INSERT INTO compra (Fecha, Cantidad, Precio, total, IdTratamiento, IdPaciente, IdMedicamento) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = (Fecha, Cantidad, Precio, total, IdTratamiento, IdPaciente, IdMedicamento)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        response_object['message'] = 'Compra agregada!'
    return jsonify(response_object)

@app.route('/medicamento', methods=['POST'])
def medicamento():
    """
    Agrega un nuevo medicamento.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            Nombre:
              type: string
    responses:
      200:
        description: Medicamento agregado exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        Nombre = post_data.get('Nombre')

        print(Nombre)
        sql = "INSERT INTO medicamento (Nombre) VALUES (%s)"
        data = (Nombre,)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        response_object['message'] = 'Medicamento agregado!'
    return jsonify(response_object)


# PUT'S

@app.route('/paciente/<string:id>', methods=['PUT'])
def update_paciente(id):
    """
    Actualiza un paciente existente.
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: string
        description: ID del paciente que se va a actualizar.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombreP:
              type: string
            apellidoPP:
              type: string
            apellidoMP:
              type: string
            dniP:
              type: string
            generoP:
              type: string
            fnacimientoP:
              type: string
            emailP:
              type: string
            telefonoP:
              type: string
    responses:
      200:
        description: Paciente actualizado exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json(silent=True)
        nombre = post_data.get('nombreP')
        apellidop = post_data.get('apellidoPP')
        apellidom = post_data.get('apellidoMP')
        dni = post_data.get('dniP')
        genero = post_data.get('generoP')
        fnac = post_data.get('fnacimientoP')
        email = post_data.get('emailP')
        telef = post_data.get('telefonoP')

        print(nombre)
        print(apellidop)
        print(apellidom)
        print(dni)
        print(genero)
        print(fnac)
        print(email)
        print(telef)

        cursor.execute ("UPDATE paciente SET nombreP = %s, apellidoPP = %s, apellidoMP = %s, dniP = %s, generoP = %s, fnacimientoP = %s, emailP = %s, telefonoP = %s WHERE idPaciente = %s", 
        (nombre, apellidop, apellidom, dni, genero, fnac, email, telef, id))
        conn.commit()   
        cursor.close()
        response_object['message'] = 'Paciente actualizado!'
    return jsonify(response_object)

@app.route('/medico/<string:id>', methods=['PUT'])
def update_medico(id):
    """
    Actualiza un médico existente.
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: string
        description: ID del médico que se va a actualizar.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombreM:
              type: string
            apellidoPM:
              type: string
            apellidoMM:
              type: string
            dniM:
              type: string
            generoM:
              type: string
            emailM:
              type: string
            telefonoM:
              type: string
            numColegialM:
              type: string
    responses:
      200:
        description: Médico actualizado exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json(silent=True)
        nombreM = post_data.get('nombreM')
        apellidoPM = post_data.get('apellidoPM')
        apellidoMM = post_data.get('apellidoMM')
        dniM = post_data.get('dniM')
        generoM = post_data.get('generoM')
        emailM = post_data.get('emailM')
        telefonoM = post_data.get('telefonoM')
        numColegialM = post_data.get('numColegialM')

        print(nombreM)
        print(apellidoPM)
        print(apellidoMM)
        print(dniM)
        print(generoM)
        print(emailM)
        print(telefonoM)
        print(numColegialM)

        cursor.execute ("UPDATE medico SET nombreM = %s, apellidoPM = %s, apellidoMM = %s, dniM = %s, generoM = %s, emailM = %s, telefonoM = %s , numColegialM = %s WHERE idMedico = %s",
        (nombreM, apellidoPM, apellidoMM, dniM, generoM, emailM, telefonoM, numColegialM, id))
        conn.commit()
        cursor.close()
        response_object['message'] = 'Medico actualizado!'
    return jsonify(response_object)

@app.route('/cita/<string:id>', methods=['PUT'])
def update_cita(id):
    """
    Actualiza una cita existente.
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: string
        description: ID de la cita que se va a actualizar.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            IdPaciente:
              type: string
            IdSchedule:
              type: string
    responses:
      200:
        description: Cita actualizada exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json(silent=True)
        IdPaciente = post_data.get('IdPaciente')
        IdSchedule = post_data.get('IdSchedule')

        print(IdPaciente)
        print(IdSchedule)

        cursor.execute ("UPDATE Cita SET IdPaciente = %s, IdSchedule = %s WHERE idCita = %s",
        (IdPaciente, IdSchedule, id))
        conn.commit()
        cursor.close()
        response_object['message'] = 'Cita actualizada!'
    return jsonify(response_object)

@app.route('/tratamiento/<string:id>', methods=['PUT'])
def update_tratamiento(id):
    """
    Actualiza un tratamiento existente.
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: string
        description: ID del tratamiento que se va a actualizar.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            descripcion:
              type: string
            duracion:
              type: string
            tratamiento:
              type: string
            idCita:
              type: string
    responses:
      200:
        description: Tratamiento actualizado exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json(silent=True)
        descripcion = post_data.get('descripcion')
        duracion = post_data.get('duracion')
        tratamiento = post_data.get('tratamiento')
        idCita = post_data.get('idCita')

        print(descripcion)
        print(duracion)
        print(tratamiento)
        print(idCita)

        cursor.execute ("UPDATE tratamiento SET descripcion = %s, duracion = %s, tratamiento = %s, idCita = %s WHERE idTratamiento = %s",
        (descripcion, duracion, tratamiento, idCita, id))
        conn.commit()
        cursor.close()
        response_object['message'] = 'Tratamiento actualizado!'
    return jsonify(response_object)

@app.route('/especialidadmedico/<string:id>', methods=['PUT'])
def update_especialidadmedico(id):
    """
    Actualiza una especialidad del médico existente.
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: string
        description: ID de la especialidad del médico que se va a actualizar.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idMedico:
              type: string
            idEspecialidad:
              type: string
            aniosExp:
              type: string
    responses:
      200:
        description: Especialidad del médico actualizada exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json(silent=True)
        idMedico = post_data.get('idMedico')
        idEspecialidad = post_data.get('idEspecialidad')
        aniosExp = post_data.get('aniosExp')

        print(idMedico)
        print(idEspecialidad)
        print(aniosExp)

        cursor.execute ("UPDATE especialidadMedico SET idMedico = %s, idEspecialidad = %s, aniosExp = %s WHERE idEspecialidadMedico = %s",
        (idMedico, idEspecialidad, aniosExp, id))
        conn.commit()
        cursor.close()
        response_object['message'] = 'EspecialidadMedico actualizado!'
    return jsonify(response_object)

@app.route('/schedule/<string:id>', methods=['PUT'])
def update_schedule(id):
    """
    Actualiza un horario (schedule) existente.
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: string
        description: ID del horario que se va a actualizar.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            Fecha:
              type: string
            Hora:
              type: string
            IdMedico:
              type: string
            IdEspecialidad:
              type: string
    responses:
      200:
        description: Horario actualizado exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}    
    if request.method == 'PUT':
        post_data = request.get_json(silent=True)
        Fecha = post_data.get('Fecha')
        Hora = post_data.get('Hora')
        IdMedico = post_data.get('IdMedico')
        IdEspecialidad = post_data.get('IdEspecialidad')

        print(Fecha)
        print(Hora)
        print(IdMedico)
        print(IdEspecialidad)

        cursor.execute ("UPDATE schedule SET Fecha = %s, Hora = %s, IdMedico = %s, IdEspecialidad = %s WHERE IdSchedule = %s",
        (Fecha, Hora, IdMedico, IdEspecialidad, id))
        conn.commit()
        cursor.close()
        response_object['message'] = 'Schedule actualizado!'
    return jsonify(response_object)

@app.route('/compra/<string:id>', methods=['PUT'])
def update_compra(id):
    """
    Actualiza una compra existente.
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: string
        description: ID de la compra que se va a actualizar.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            Fecha:
              type: string
            Cantidad:
              type: integer
            Precio:
              type: float
            total:
              type: float
            IdTratamiento:
              type: integer
            IdPaciente:
              type: integer
            IdMedicamento:
              type: integer
    responses:
      200:
        description: Compra actualizada exitosamente.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}    
    if request.method == 'PUT':
        post_data = request.get_json(silent=True)
        Fecha = post_data.get('Fecha')
        Cantidad = post_data.get('Cantidad')
        Precio = post_data.get('Precio')
        total = post_data.get('total')
        IdTratamiento = post_data.get('IdTratamiento')
        IdPaciente = post_data.get('IdPaciente')
        IdMedicamento = post_data.get('IdMedicamento')

        print(Fecha)
        print(Cantidad)
        print(Precio)
        print(total)
        print(IdTratamiento)
        print(IdPaciente)
        print(IdMedicamento)

        cursor.execute ("UPDATE compra SET Fecha = %s,  Cantidad = %s, Precio = %s, total = %s, IdTratamiento = %s, IdPaciente = %s, IdMedicamento = %s WHERE idCompra = %s",
        (Fecha, Cantidad, Precio, total, IdTratamiento, IdPaciente, IdMedicamento, id))
        conn.commit()
        cursor.close()
        response_object['message'] = 'Compra actualizada!'
    return jsonify(response_object)

if __name__ == '__main__':
    app.run(port = 5000, debug = True)