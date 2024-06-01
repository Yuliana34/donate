from flask import Flask, request, jsonify
#from blockchain import Blockchain
import json 
import hashlib
import requests 

app = Flask(__name__)
#blockchain = Blockchain()

nodos = set()
@app.route('/registrar_nodo', methods=['POST'])

def registrar_nodo():
    valores = request.get_json()
    nodos_nuevos = valores.get('nodos')
    if nodos_nuevos is None: 
        return "ERROR, la lista de nodos valida no existe", 400
    for nodo in nodos_nuevos: 
        nodos.add(nodo)

    response = {
        "message": 'Los nodos fueron añadidos de manera exitosa',
        "Lista_nodos": list(nodos),
    }
    return jsonify(response), 201

@app.route('/sincronizar_cadena', methods = ['GET'])

def sincronizar_cadena():
    nueva_cadena = None
    max_longitud = len(nueva_cadena)
    for nodo in nodos:
        response = requests.get(f'http://{nodo}/cadena')

        if response.status_code == 200:
            longitud = response.json()['length']
            cadena = response.json()['cadena']

            if longitud > max_longitud and validar_cadena(cadena):
                max_longitud = longitud
                nueva_cadena = cadena

    if nueva_cadena:
        cadena = nueva_cadena
        response = {
            "message": 'Se reemplazó la cadena',
            "new_cadena": cadena,
        }
    else:
        response = {
            "message": 'La cadena es correcta'
        }   
    return jsonify(response), 200

def validar_cadena(cadena):
    last_block = cadena[0]
    current_index = 1

    while current_index < len(cadena):
        block = cadena[current_index]
        if block['previous_hash']!= hash(last_block):
            return False
        
        if not validar_prueba(last_block['proof'], block['proof']):
            return False
        last_block = block
        current_index += 1
    return True

def hash(block):
    return hashlib.sha512(json.dumps(block, sort_keys=True).encode()).hexdigest()

def validar_prueba(last_proof, proof):

    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha512(guess).hexdigest()
    return guess_hash[:4] == '0000'

if __name__ == '__main__':
    from argparse import ArgumentParser 

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int)
    args = parser.parse_args()
    puerto = args.port
    app.run(host='0.0.0.0', port=puerto)

#python node.py -p 5500 -->Aquí define el puerto dinamicamente