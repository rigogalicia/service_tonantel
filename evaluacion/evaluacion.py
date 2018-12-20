from flask_restful import Resource, reqparse
from bson.objectid import ObjectId
from db.mongo import Conexion

parser = reqparse.RequestParser()
parser.add_argument('user')
parser.add_argument('clave')
parser.add_argument('id_evaluacion')

class Evaluacion(Resource):

    def __init__(self):
        ''' Metodo constructor de la clase '''
        self.__db = Conexion().get_db()
        self.__args = {}


    def datos_evaluacion(self):
        ''' Este metodo consulta los datos de la evaluacion por el id '''
        collection = self.__db.ed_evaluacion

        try:

            condicion = {
                '_id': ObjectId(self.__args['id_evaluacion'])
            }

            campos = {
                'nombreEvaluacion': 1,
                'fechaFin': 1,
                'instrucciones': 1,
                'estado': 1
            }

            result = collection.find(condicion, campos)
            for e in result:
                return {
                    'nombreEvaluacion': e['nombreEvaluacion'],
                    'fechaFin': str(e['fechaFin']),
                    'instrucciones': e['instrucciones'],
                    'estado': e['estado']
                }
        except:
            return {'nombreEvaluacion': 'Evaluacion no encontrada'}
    

    def datos_colaborador(self):
        ''' Metodo para consultar los datos del colaborador '''
        collection = self.__db.colaboradores
        
        try:
            condicion = {
                '_id': self.__args['user'],
                'clave': self.__args['clave']
            }

            campos = {
                '_id': 0,
                'firma': 0,
                'clave': 0,
                'correo': 0
            }
            
            result = collection.find_one(condicion, campos)
            
            return result
        except:
            return {'nombre': 'Datos del usuario no disponibles'}
    

    def datos_jefe_inmediato(self):
        ''' Metodo para obtener los datos del Jefe inmediato '''
        collection = self.__db.colaboradores
        
        try:
            condicion = {
                'subordinados.idColaborador': self.__args['user']
            }

            campos = {
                'nombre': 1,
                'puesto': 1
            }

            result = collection.find(condicion, campos)
            for data in result:
                return {
                    'id': data['_id'],
                    'nombre': data['nombre'],
                    'puesto': data['puesto']
                }
        except:
            return {}
    

    def save_calificacion(self):
        ''' Este metodo inicia la tabla de calificacion en la base de datos '''
        collection = self.__db.ed_calificacion

        ed = self.datos_evaluacion()
        colaborador = self.datos_colaborador()
        jefe_inmediato = self.datos_jefe_inmediato()

        try:
            info = {'_id': self.__args['user'] + self.__args['id_evaluacion']}
            info.update(ed)
            info.update({'id_colaborador': colaborador['_id']}, colaborador)
            info.update({'datosJefe': jefe_inmediato})

            datos_calificacion = info

            collection.insert(datos_calificacion)
        except:
            print('! El usuario ya se encuentra registrado en calificacion')

        return info
    

    def post(self):
        ''' Este metodo realiza la peticion por medio de POST '''
        args = parser.parse_args()
        self.__args = args

        data = self.save_calificacion()

        return data
