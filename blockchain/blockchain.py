from flask import Flask, render_template, jsonify, request
from time import time
from flask_cors import CORS # Flask extension to handle Cross-Origin-Resource-Sharing(CORS), to allow cross-origin AJAX
from collections import OrderedDict
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5  #
from Crypto.Hash import SHA
import binascii

MINING_SENDER = "The Blockchain"


class Blockchain:

    def __init__(self):
        self.pending_transactions = []
        self.chain = []
        # Create the Genesis Block
        self.create_block(0, '00')

    def create_block(self, nonce, previous_hash):
        # Function to create a new block
        block = {
            'block_number': len(self.chain) + 1,
            'timestamp': time(),
            'pending_transactions': self.pending_transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        }

        # Reset the list of pending_transactions after adding the pending transaction to the latest created block
        self.pending_transactions = []
        self.chain.append(block)

    def verify_signature(self, sender_public_key, signature, transaction):
        # import the hexadecimal public key and encode it into a string under UTF-8 encoding
        public_key = RSA.importKey(binascii.unhexlify(sender_public_key))
        verifier = PKCS1_v1_5.new(public_key)  # Created to verify the signature
        # Get the transaction => convert it into string => encode it to UTF-8 => Hash is using SHA
        h = SHA.new(str(transaction).encode('utf8'))
        # Now verify that the signature has already been done by/with the public_key
        # verify does not return True or False, rather raise a value error
        try:
            verifier.verify(h, binascii.unhexlify(signature))
            return True  # Return True if everything is good
        except ValueError:
            return False  # Return False if verify raises a ValueError
        # This will return true, if the Hash corresponds to the signature, which was signed by/using this public key

        # When an information is signed, it will be signed using the private key, but for verification, it done using-
        # -the public key of the signer

    def submit_transaction(self, sender_public_key, recipient_public_key, signature, amount):
        # Fn() to add the new transaction to pending transactions

        transaction = OrderedDict({
            'sender_public_key': sender_public_key,
            'recipient_public_key': recipient_public_key,
            # signature is not required here, as the data that the client has signed and sent does not have this info-
            # The transaction should be verified only with Sender&Recipient public key + amount
            'amount': amount
        })

        # => Reward the miner
        # To reward the miner, the sender_public_key should be specific or else, the block was mined from another-
        # -transaction
        if sender_public_key == MINING_SENDER: # Reward for Mining a Block
            self.pending_transactions.append(transaction)  # Append the transaction into the current transaction list without-
            # -any checking, as the transaction is from the Blockchain
            return len(self.chain) + 1
        else:  # Transaction from one wallet to another
            # => Signature Validation
            signature_verification = self.verify_signature(sender_public_key, signature, transaction) # Temp var
            if signature_verification:  # If the signature is verified to be true
                self.pending_transactions.append(transaction)  # Append the transaction into the current transaction
                return len(self.chain) + 1 # The "+ 1" intimates the client that this transaction will be added to-
                # -the next block
            else:
                return False  # Return False if the signature is not Authentic

# Instantiate the Blockchain
blockchain = Blockchain()

# Instantiate the Node
app = Flask(__name__)  # Instance of the Flask class, the i/p args is like a placeholder for current module
CORS(app)


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    pending_transactions = blockchain.pending_transactions
    response = {'pending_transactions': pending_transactions}
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.form

    # Check the required fields for values
    required = [
                'confirmation_sender_public_key',
                'confirmation_recipient_public_key',
                'transaction_signature',
                'confirmation_amount'
               ]
    if not all( k in values for k in required):
        return 'Missing Values', 400

    # This is entirely from the backend, so the form may not be relied upon completely, for the transaction details
    # This logic just checks to see if everything is in place correctly, also prevents any vulnerability like when-
    # -an attacker tries to send a form => This is just a prototype

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
