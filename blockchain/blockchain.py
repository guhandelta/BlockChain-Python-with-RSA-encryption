from flask import Flask, render_template
from time import time


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


# Instantiate the Blockchain
blockchain = Blockchain()

# Instantiate the Node
app = Flask(__name__)  # Instance of the Flask class, the i/p args is like a placeholder for current module


@app.route('/')
def index():
    return render_template('./index.html')


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help="This is the port to be listened")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
