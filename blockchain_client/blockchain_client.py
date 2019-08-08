from flask import Flask, render_template, jsonify
import Crypto
from Crypto import Random
from Crypto.PublicKey import RSA
import binascii


class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, amount):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.amount = amount


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('./index.html')

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
