from flask import jsonify, request
from modelo.coneccion import db_connection

def buscar_cliente(codigo):
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("""select ci,nombre,direccion,fecha_nac,ciudad FROM cliente WHERE ci = %s""", (codigo,))
        datos = cur.fetchone()
        conn.close()
        if datos != None:
            cliente = {'ci': datos[0], 'nombre': datos[1],
                       'direccion': datos[2], 'fecha_nac': datos[3],
                       'ciudad': datos[4]}
            return cliente
        else:
            return None
    except Exception as ex:
            raise ex

class ClienteModel():
    @classmethod
    def listar_cliente(self):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""select ci,nombre,direccion,fecha_nac,ciudad from cliente""")
            datos = cur.fetchall()
            clientes = []
            for fila in datos:
                cliente = {'ci': fila[0],
                           'nombre': fila[1],
                           'direccion': fila[2],
                           'fecha_nac': fila[3],
                           'ciudad': fila[4]}
                clientes.append(cliente)
            conn.close()
            return jsonify({'clientes':clientes, 'mensaje': "clientes listados.",'exito':True})
        except Exception as ex: 
             return jsonify({'mensaje':"Error",'exito': False})   
                     
        

    @classmethod
    def registrar_cliente(self):
        try:
            cliente = buscar_cliente(request.json['ci'])
            if cliente != None:
                return jsonify({'mensaje': "Ci ya existe, no se puede duplicar.", 'exito': False})
            else:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute('INSERT INTO cliente values(%s,%s,%s,%s,%s)', (request.json['ci'], request.json['nombre'], request.json['direccion'],
                                                                            request.json['fecha_nac'], request.json['ciudad']))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "cliente registrado.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})  
        
    @classmethod
    def eliminar_cliente(self,codigo):
        try:
            cliente = buscar_cliente(codigo)
            if cliente != None:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute("""DELETE FROM cliente WHERE ci = %s""", (codigo,))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "cliente eliminado.", 'exito': True})
            else:
                return jsonify({'mensaje': "cliente no encontrado.", 'exito': False})
        except Exception as ex:
                return jsonify({'mensaje': "Error", 'exito': False})
        
    @classmethod
    def modificar_cliente(self,codigo):
        try:
            cliente = buscar_cliente(codigo)
            if cliente != None:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute("""UPDATE cliente SET nombre=%s, direccion=%s, fecha_nac=%s,
                ciudad=%s WHERE ci=%s""",
                        (request.json['nombre'], request.json['direccion'], request.json['fecha_nac'], request.json['ciudad'], codigo))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "cliente actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "cliente no encontrado.", 'exito': False})
        except Exception as ex:
                return jsonify({'mensaje': "Error", 'exito': False})   