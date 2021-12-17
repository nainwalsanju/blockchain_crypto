from Tools.scripts.make_ctype import method
from flask import Flask,render_template,jsonify,request
import Crypto
import Crypto.Random
from Crypto.PublicKey import RSA
import binascii
from collections import OrderedDict

class Transaction:

    def __init__(self, sender_public_key, sender_private_key, recipient_public_key, amount):
        self.sender_public_key = sender_public_key
        self.sender_private_key = sender_private_key
        self.recipient_public_key = recipient_public_key
        self.amount = amount

    def to_dict(self):
        return OrderedDict({
            "sender_public_key": self.sender_public_key,
            "sender_private_key": self.sender_private_key,
            "recipient_public_key": self.recipient_public_key,
            "amount": self.amount,
        })

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/make/transaction')
def make_transaction():
    return render_template('/make_transaction.html')

@app.route('/generate/transaction', methods=['POST'])
def generate_transaction():
    sender_public_key = request.form['sender_public_key']
    sender_private_key = request.form['sender_private_key']
    recipient_public_key = request.form['recipient_public_key']
    amount = request.form['amount']

    transaction = Transaction(sender_public_key, sender_private_key, recipient_public_key, amount)
    response = {
        'transaction': transaction.to_dict(),
        'signature': 'blah'
    }

    return jsonify(response),200

@app.route('/view/transactions')
def view_transactions():
    return render_template('/view_transactions.html')

@app.route('/wallet/new')
def new_wallet():
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.public_key()
    response = {
        "private_key":binascii.hexlify( private_key.export_key(format("DER"))).decode('ascii'),
        "public_key": binascii.hexlify( public_key.export_key(format("DER"))).decode('ascii'),
    }
    return jsonify(response),200

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8081, type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1',port=port, debug=True)