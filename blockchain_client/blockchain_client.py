from flask import Flask,render_template

class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.value = value

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/make/transactions')
def make_transaction():
    return render_template('/make_transaction.html')

@app.route('/view/transactions')
def view_transaction():
    return render_template('/view_transaction.html')

@app.route('/wallet/new')
def new_wallet():
    return ''

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8081, type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1',port=port, debug=True)