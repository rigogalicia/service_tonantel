from flask_restful import Resource
from db.mongo import Conexion

class Interrogante(Resource):

    def __init__(self):
        ''' Metodo constructor de la clase '''
        self.__db = Conexion().get_db()


    def datos_interrogante(self, id_evaluacion, id_colaborador):
        ''' Este metodo devuelve los datos de la interrogante '''
        collection = self.__db.ed_interrogantes

        condicion = {
            'evaluacion': id_evaluacion,
            'puesto': {'$in': [" ", "Auxiliar de Talento Humano"]},
            'lider': 'NO'
        }

        campos = {
            '_id': 1,
            'conducta': 1,
            'descripcion': 1
        }

        result = collection.find_one(condicion, campos)

        result_interrogante = {
            'idConducta': str(result['_id']),
            'tipoConducta': result['conducta'],
            'descripcion': result['descripcion']
        }

        return result_interrogante


    def post(self):
        ''' Metodo encargado de realizar la peticion, por medio de POST '''
        return self.datos_interrogante('5c069e547bb1b606d287b497', 'todesaragb')


