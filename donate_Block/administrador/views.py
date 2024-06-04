from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .blockchain import Blockchain
import json as JSON
from uuid import uuid4
from urllib.parse import urlparse

# VISTAS PARA BLOCKCHAIN
node_address = str(uuid4()).replace('-',' ')

blockchain = Blockchain()

def __init__(self):
        self.cadena = []
        self.current_transactions = []
        self.nodos = set()
        self.new_block(previous_hash = '1', proof = 100) 
        
def home(request):
    context = {}
    return render(request, 'administrador/index.html', context=context)
def formulario(request):
    return render(request, 'administrador/index1.html')

def mine_block(request):
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    # blockchain.add_transactions(sender = node_address, reciever = 'Prakhar',amount = 10)

    blockchain.sync_transactions()

    block = blockchain.create_block(proof, previous_hash)

    # Added by Kshitiz
    blockchain.empty_transactions()
    response = {
        'message': "Congratulations, You just mined a block!!",
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'transactions': block['transactions'],
    }
    return JsonResponse(response)

def get_chain(request):
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return JsonResponse(response)

def is_valid(request):
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {
            'message': "Todo está bien !!! Nada de que preocuparse. La cadena de bloques es válida."}
    else:
        response = {
            'message': "No... Entonces, tenemos problemas... ¡¡¡Blockchain no es válido!!!"}
    return JsonResponse(response)

def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender ,                  #Quien envía la Tx - Remitente
            'recipient':recipient,             #Destinatario
            'amount': amount,                   #Cantidad de la transferencia
        })
        return self.last_block['index'] +10


def add_donate_transaction(request):
    if request.method == 'POST':
        record_data = request.POST
        # transaction_keys = ['recordType', 'recordData']
        # if not all(key in json for key in transaction_keys):
        # 	return "Some elements of transaction are misssing" , 400
        # record_data = json['recordData']
        index = blockchain.add_donate_transactions(
            record_data['name'],
            record_data['correo'],
            record_data['monto'],
            
        )
        response = {
            'message': f'La transacción de donación se agregará al bloqueo. {index}'}
        return JsonResponse(response)
    

      
def connect_node(request):
    current_node = urlparse(request.build_absolute_uri())
    current_node = "http://" + str(current_node.netloc)
    content_string = None
    nodes = None
    with open('static/nodes.json', 'r') as file:
        content_string = file.read()
    content = JSON.loads(content_string)
    if content is not None:
        nodes = content['nodes']
    else:
        return HttpResponse("Something went wrong!")
    if nodes is None:
        return HttpResponse("No hay nodos en la red!")
    for node in nodes:
        if current_node != str(node):
            blockchain.add_node(node)
    response = {
        "message": "Todos los nodos están conectados. La cadena de bloques Blockchain contiene los siguientes nodos:",
        "total_nodes": list(blockchain.nodes)
    }
    return JsonResponse(response)

def replace_chain(request):
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {
            'message': "Los nodos tenían cadenas diferentes, por lo que la cadena fue reemplazada por la más larga..",
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': "Todo está bien. La cadena era la más grande.",
            'actual_chain': blockchain.chain
        }
    return JsonResponse(response)
   
def get_transactions(request):
    response = {
        'number_of_transactions': len(blockchain.transactions),
        'transactions': blockchain.transactions,
    }
    return JsonResponse(response)

def empty_transactions(request):
    blockchain.transactions = []
    response = {'message': 'Las transacciones se vaciaron exitosamente'}
    return JsonResponse(response)

def all_transactions(request):
    blockchain.sync_transactions()
    transactions = blockchain.transactions
    total_transactions = []
    if len(transactions) != 0:
        for transaction in transactions:
            print(transaction)
            total_transactions.append(
                {'status': 'pending', 'transaction': transaction})

    if len(blockchain.chain) != 0:
        for block in blockchain.chain:
            for transaction in block["transactions"]:
                total_transactions.append(
                    {'status': 'completed', 'transaction': transaction, 'timestamp': block["timestamp"]})

    response = {
        'number_of_pending_transactions': len(blockchain.transactions),
        'number_of_completed_transactions': len(total_transactions)-len(blockchain.transactions),
        'total_transactions': total_transactions,
    }
    return JsonResponse(response)

def fetch_record(request, record_type, public_key):
    # chain = blockchain.chain
    # required_transaction = []
    # for block in chain:
    #     transactions = block['transactions']
    #     if transactions:
    #         for transaction in transactions:
    #             record_type = transaction['recordType']
    #             if str(record_type) == str(record_type):
    #                 record_data = transaction['recordData']
    #                 name =
    return HttpResponse("fgg")


# VISTAS PARA front
def conectar_frontend(request):
    data = {'mensaje': '¡conexión exitosa con el backend!'}
    return JsonResponse(data)

#def index(request):
    #return render(request, 'administrador/index.html')

def donado(request):
    return render(request, 'administrador/donado.html')

    
def donar(request):
    return render(request, 'administrador/donar.html')

def causas(request):
    return render(request, 'administrador/causes.html')

