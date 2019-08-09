from flask import Flask, render_template, jsonify, request
from time import time
from flask_cors import CORS # Flask extension to handle Cross-Origin-Resource-Sharing(CORS), to allow cross-origin AJAX
from collections import OrderedDict


class Blockchain:

    def __init__(self):
        self.transactions = []
        self.chain = []
        # Create the Genesis Block
        self.create_block(0, '00')

    def create_block(self, nonce, previous_hash):
        # Function to create a new block
        block = {
            'block_number': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        }

        # Reset the list of transactions after adding the pending transaction to the latest created block
        self.transactions = []
        self.chain.append(block)

    def submit_transaction(self, sender_public_key, recipient_public_key, signature, amount):
        # Fn() to add the new transaction to pending transactions

        # => Reward the miner
        # => Signature Validation

        transaction = OrderedDict({
            'sender_public_key': sender_public_key,
            'recipient_public_key': recipient_public_key,
            'signature': signature,
            'amount': amount
        })
        signature_verification = True # Temp var
        if signature_verification:  # If the signature is verified to be true
            self.transactions.append(transaction)  # Append the transaction into the current transaction
            return len(self.chain) + 1  # The "+ 1" is to intimate the user that this transaction will be added to the-
            # -next block
        else:
            return False  # Return False if the signature is not Authentic

        return True

# Instantiate the Blockchain
blockchain = Blockchain()

# Instantiate the Node
app = Flask(__name__)  # Instance of the Flask class, the i/p args is like a placeholder for current module
CORS(app)


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    values = request.form

    # Check the required fields for values
    transaction_results = blockchain.submit_transaction(
                                                        values['confirmation_sender_public_key'],
                                                        values['confirmation_recipient_public_key'],
                                                        values['transaction_signature'],
                                                        values['confirmation_amount']
                                                       )
    # Will provide the transaction details as input
    if transaction_results == False:
        response = {'message': 'Invalid Transaction'}
        return jsonify(response), 406  # HTTP code 406 => Invalid Response
    else:
        # If the transaction_results has the transaction values, return this msg, along with the block number to which-
        # -the transaction will be added on to
        response = {'message': 'Transaction Successful and will be added in the Block: ' + str(transaction_results)}
        # The submit_transaction() will return the next block number
        return jsonify(response), 201  # 201 => to say that we are getting a new resource


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help="This is the port to be listened")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
