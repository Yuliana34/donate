import hashlib
import json
from time import time, localtime, strftime
from urllib.parse import urlparse
import requests 
from uuid import uuid4
from flask import Flask, jsonify, request

class Blockchain:
    def __init__(self):
        self.cadena = []
        self.current_transactions = []
        self.nodos = set()
        self.new_block(previous_hash = '1', proof = 100) 
        

    def registrar_nodo(self, direccion):
        parsed_url = urlparse(direccion)
        self.nodos.add(parsed_url.netloc)

    def sincronizar_cadena(self):
        max_longitud = len(self.cadena)
        nueva_cadena = None

        for nodo in self.nodos:
            response = request.get(f'http://{nodo}/cadena')

            if response.status_code == 200:
                longitud = response.json()['longitud']
                cadena = response.json()['cadena']

                if longitud > max_longitud and self.validar_cadena(cadena):
                    max_longitud = longitud
                    nueva_cadena = cadena
        if nueva_cadena: 
            self.cadena = nueva_cadena
            return True
        
    def validar_cadena(self, cadena):
        last_block = cadena[0]
        current_index = 1

        while current_index < len(cadena):
            block = cadena[current_index]
            if block['previous_hash']!= self.hash_block(last_block):
                return False
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True

    def new_block(self, proof, previous_hash = None):
        
        timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
        milliseconds = int(time() * 1000) % 1000
       
        block = {
            'index': len(self.cadena) + 1,
            'timestamp': f"{timestamp}.{milliseconds}",
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash_block(self.cadena[-1]),
        }

        block['hash_actual'] = self.hash_block(block)
        self.current_transactions = []
       
        self.cadena.append(block)
        return block
       
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,                   #Quien envía la Tx - Remitente
            'recipient': recipient,             #Destinatario
            'amount': amount,                   #Cantidad de la transferencia
        })
        return self.last_block['index'] +1
    
    @property
    def last_block(self):
        return self.cadena[-1]

    @staticmethod
    def hash_block(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()    
   
    def proof_of_work(self, last_proof,last_block_hash):
        proof = 0
        while self.valid_proof(last_proof, proof, last_block_hash) is False:
            proof +=1

        return proof
 
    @staticmethod
    def valid_proof(last_proof, proof,last_block_hash):
        guess = f'{last_proof} {proof} {last_block_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4]=="0000"

app = Flask(__name__)

id_nodo = str(uuid4()).replace('-','')

blockchain = Blockchain()

@app.route('/cadena', methods = ['GET'])

def cadena():
    response = {
        "cadena" : blockchain.cadena,
        "longitud" : len(blockchain.cadena),
    }
    return jsonify(response), 200


@app.route('/registrar_nodo', methods=['POST'])

def registrar_nodo():
    values  = request.get_json()
    nodos   = values.get('nodos')
    if nodos is None: 
        return "ERROR, la lista de nodos valida no existe", 400
    for nodo in nodos: 
        blockchain.registrar_nodo(nodo)

    response = {
        "message": 'Los nodos fueron añadidos de manera exitosa',
        "Lista_nodos": list(blockchain.nodos),
    }
    return jsonify(response), 201

#Dsde aquí jueves 9 mayo

@app.route('/sincronizar_cadena', methods=['GET']) 

def sincronizar_cadena():
    replaced = blockchain.sincronizar_cadena()
    if replaced:
        response = {
            "message": 'La cadena ha sido sincronizada',
            "cadena": blockchain.cadena
        }
    else:
        response = {
            "message": 'La cadena es correcta!',
            "cadena": blockchain.cadena
        }
    return jsonify(response), 200

@app.route("/minado", methods = ['GET'])
def minado():

    last_block = blockchain.last_block
    last_proof = last_block['proof']
    last_block_hash = blockchain.hash_block(last_block)
    proof = blockchain.proof_of_work(last_proof, last_block_hash)
    blockchain.new_transaction(
        sender="0",
        recipient=id_nodo,
        amount=2,
    )
    previous_hash = blockchain.hash_block(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        "message": 'Minado exitoso',
        "index" : block['index'],
        "transactions" : block['transactions'],
        "proof"    : block['proof'],
        "previous_hash" : block['previous_hash'],
        "hash_actual" : blockchain.hash_block(block),
        
    }
    return jsonify(response), 200



if __name__ == '__main__':
    from argparse import ArgumentParser 

    parser = ArgumentParser()
    parser.add_argument('-p', '--puerto', default=5000, type=int)
    args = parser.parse_args()
    puerto = args.puerto
    app.run(host='0.0.0.0', port=puerto)


