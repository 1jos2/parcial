from flask import Flask
from modelo.modeloCliente import ClienteModel

app = Flask(__name__)	

@app.route('/')
def hello_world():
        return 'hola INF530'

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    emp= ClienteModel.listar_cliente()
    return emp

@app.route('/clientes', methods=['POST'])
def crear_clientes():
    emp= ClienteModel.registrar_cliente()
    return emp

@app.route('/clientes/:<codigo>', methods=['DELETE'])
def eliminar_clientes(codigo):
    emp= ClienteModel.eliminar_cliente(codigo)
    return emp

@app.route('/clientes/:<codigo>', methods=['PUT'])
def modificar_clientes(codigo):
    emp= ClienteModel.modificar_cliente(codigo)
    return emp

if __name__ == '__main__':
   		app.run(debug=True,host='0.0.0.0') 
                
