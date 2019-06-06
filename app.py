from flask import Flask, request, render_template
from blockchain import *
from Crypto.PublicKey import RSA
import Crypto
import binascii
app = Flask(__name__)


#initial values
bc = blockchain()
bc.mine_pending_transactions('miner1')                    #miner1: 100
bc.create_transaction(transaction('miner1', 'addr1', 50)) #miner1: 50  addr1:50
bc.create_transaction(transaction('addr1', 'addr2', 20))  #miner1: 50  addr1:30  addr2: 20      
bc.mine_pending_transactions('miner1')


@app.route('/')
def hello():
    is_valid = bc.is_chain_valid()
    return render_template('home.html', chain=bc.chain, is_valid=is_valid)


@app.route('/create-transaction', methods=['GET', 'POST'])
def create_transaction():
    if request.method == 'GET':
        return render_template('create-transaction.html')

    if request.method == 'POST':
        from_addr = request.form['from']
        to_addr = request.form['to']
        amount = request.form['amount']
        bc.create_transaction(transaction(from_addr, to_addr, float(amount)))
        return render_template('success.html')


@app.route('/check-balance', methods=['GET', 'POST'])
def get_balance():
    if request.method == 'GET':
        return render_template('balance-form.html')

    if request.method == 'POST':
        
        addr = request.form['addr']
        balance = bc.get_balance(addr)
        return render_template('balance.html', balance=balance, addr=addr)

@app.route('/wallet-gen', methods=['GET', 'POST'])
def wallet_gen():
    if request.method == 'GET':
        return render_template('wallet-gen.html')

    if request.method == 'POST':
        rg = Crypto.Random.new().read
        prv_k = RSA.generate(1024, rg)
        pub_k = prv_k.publickey()
        prv_k= binascii.hexlify(prv_k.exportKey(format='DER')).decode('ascii')
        pub_k= binascii.hexlify(pub_k.exportKey(format='DER')).decode('ascii')

        print(prv_k)
        return render_template('wallet-generated.html', pub_k=pub_k, prv_k=prv_k)

@app.route('/mine', methods=['GET'])
def mine():
    bc.mine_pending_transactions('miner1')
    h = bc.get_latest_block().hash
    return render_template('mined.html',h=h)
    


if __name__ == '__main__':
    app.run()
