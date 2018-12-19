from flask_restful import Resource
from bson.objectid import ObjectId
from db.mongo import Conexion

class Evaluacion(Resource):

    def __init__(self):
        ''' Metodo constructor de la clase '''
        self.__db = Conexion().get_db()


    def save_calificacion(self, user, clave, id_evaluacion):
        ''' Este metodo inicia la tabla de calificacion en la base de datos '''
        collection = self.__db.ed_calificacion

        ed = self.datos_evaluacion(id_evaluacion)
        colaborador = self.datos_colaborador(user, clave)
        jefe_inmediato = self.datos_jefe_inmediato(user)
        

        info = {'_id': user + id_evaluacion}
        info.update(ed)
        info.update(colaborador)
        info.update({'datosJefe': jefe_inmediato})

        datos_calificacion = info

        try:
            collection.insert(datos_calificacion)
        except:
            print('! El usuario ya se encuentra registrado en calificacion')
        
        return info


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
            '_id': 0,
            'firma': 0,
            'clave': 0,
            'correo': 0
        }
        
        result = collection.find_one(condicion, campos)
        
        return result
    

    def datos_jefe_inmediato(self, usr_conect):
        ''' Metodo para obtener los datos del Jefe inmediato '''
        collection = self.__db.colaboradores

        condicion = {
            'subordinados.idColaborador': usr_conect
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
    

    def post(self, usr_conect, clave_conect, id_evaluacion):
        ''' Este metodo realiza la peticion por medio de POST '''
        data = self.save_calificacion(usr_conect, clave_conect, id_evaluacion)

        return data
