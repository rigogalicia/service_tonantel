from flask_restful import Resource
from bson.objectid import ObjectId
from db.mongo import Conexion

class Evaluacion(Resource):

    def __init__(self):
        ''' Metodo constructor de la clase '''
        self.__db = Conexion().get_db()


    def datos_evaluacion(self, id_evaluacion):
        ''' Este metodo consulta los datos de la evaluacion por el id '''
        collection = self.__db.ed_evaluacion

        condicion = {
            '_id': ObjectId(id_evaluacion)
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
    

    def datos_colaborador(self, usr_conect, clave_conect):
        ''' Metodo para consultar los datos del colaborador '''
        collection = self.__db.colaboradores
        
        condicion = {
            '_id': usr_conect,
            'clave': clave_conect
            }

        campos = {
            'nombre': 1,
            'subordinados': 1
            }
        
        data_result = {'datosJefe': self.datos_jefe_inmediato(usr_conect)}
        
        result = collection.find(condicion, campos)
        for data in result:
            data_result.update(data)
        
        return data_result
    

    def datos_jefe_inmediato(self, usr_conect):
        ''' Metodo para obtener los datos del Jefe inmediato '''
        collection = self.__db.colaboradores

        condicion = {
            'subordinados.idColaborador': usr_conect
            }
        campos = {
            'nombre': 1
            }

        result = collection.find(condicion, campos)
        for data in result:
            return {
                'nombre': data['nombre'],
                'id': data['_id']
                }
    

    def post(self, usr_conect, clave_conect, id_evaluacion):
        ''' Este metodo realiza la peticion por medio de POST '''
        data = self.datos_evaluacion(id_evaluacion)
        data.update(self.datos_colaborador(usr_conect, clave_conect))
        return data
