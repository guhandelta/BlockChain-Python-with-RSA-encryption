from flask import Flask, render_template, jsonify, request
import Crypto
from Crypto import Random
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
            'sender_public_key': self.sender_public_key,
            'sender_private_key': self.sender_private_key,
            'recipient_public_key': self.recipient_public_key,
            'amount': self.amount,
        })


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('./index.html')

# API to generate a new transaction
@app.route('/transaction/generate', methods=['POST'])
def generate_transactions():
    # Step 1: Get the Transaction Info
    sender_public_key = request.form['sender_public_key']
    sender_private_key = request.form['sender_private_key']
    recipient_public_key = request.form['recipient_public_key']
    amount = request.form['amount']

    # Step 2: Create a transaction object from the instance/constructor of the Transaction Class
    transaction = Transaction(sender_public_key, sender_private_key, recipient_public_key, amount)

    # Step 3: Return the response, which is a Dictionary
    response = {
        'transaction': transaction.to_dict(), # Converting the transantion details into a transaction
        'signature': 'blah'
    }

    return jsonify(response), 200 # Converting the Dict to JSON


# Page to create transaction
@app.route('/transaction/make')
def make_transactions():
    return render_template('./make_transactions.html')


# Page to view transactions
@app.route('/transaction/view')
def view_transactions():
    return render_template('./view_transactions.html')


# Page to create new wallet
@app.route('/wallet/new')
def new_wallet():
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen) # Generating a Private key using RSA Algo
    # 1st param => Key Length or Key size in bits _must be atleast 1024_ || 2nd param => Function that returns random-
    # -bytes _Crypto.Random()is used here_
    public_key = private_key.publickey() # Generating a Public key from the Private key

    response = {    # Dictionary
        'private_key' : binascii.hexlify(private_key.export_key(format('DER'))).decode('ascii'),
        # exporting the key in DER encoded format and converting it to hexadecimal
        'public_key' : binascii.hexlify(public_key.export_key(format('DER'))).decode('ascii')
    }

    return jsonify(response), 200 # The response will be a Dictionary, so converting it into JSON, so the browser can understand


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8081, type=int, help="This is the port to be listened")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
