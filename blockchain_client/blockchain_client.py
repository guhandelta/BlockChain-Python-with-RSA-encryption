from flask import Flask, render_template


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
    return 'Wallet Created'


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8081, type=int, help="This is the port to be listened")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
