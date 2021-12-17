from time import time
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from Crypto.PublicKey import RSA
from collections import OrderedDict
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import binascii

class BlockChain:
    def __init__(self):
        self.transactions = []
        self.chain = []
        # Create a genesis block
        self.create_block(0, '00')

    def create_block(self, nonce, previous_hash):
        # Add a block of trasaction to the blockchain
        block = {
            'block_number': len(self.chain) + 1,
            'timestamp': time(),
            'transaction': self.transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        }
        # Reset the current list of transactions
        self.transactions = []
        self.chain.append(block)

    def verify_transaction_signature(self, sender_public_key, signature, transaction):
        public_key = RSA.importKey(binascii.unhexlify(sender_public_key))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA.new(str(transaction).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(signature))

    def submit_transaction(self, sender_public_key, recipient_public_key, signature, amount):
        # TODO: Reward the miner
        # TODO: Signature validation

        transaction = OrderedDict({
            'sender_public_key': sender_public_key,
            'recipient_public_key': recipient_public_key,
            'amount': amount
        })
        signature_verification = self.verify_transaction_signature(sender_public_key, signature, transaction)
        if signature_verification:
            self.transactions.append(transaction)
            return len(self.chain) + 1
        else:
            return False


# Instaniate the Blockchain
blockchain = BlockChain()

# Instaniate the Node
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.form
    # TODO: check the required fields
    transaction_results = blockchain.submit_transaction(values['confirmation_sender_public_key'],
                                                        values['confirmation_recipient_public_key'],
                                                        values['transaction_signature'], values['confirmation_amount'])


    if transaction_results == False:
        response = {'message': 'Invalid transaction/signature'}
        return jsonify(response), 406
    else:
        response = {'message': 'Transaction will be added to the Block ' + str(transaction_results)}
        return jsonify(response), 201


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
