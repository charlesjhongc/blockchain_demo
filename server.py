from flask import Flask, render_template, request, redirect
import hashlib
import time
import threading

class Block:
    """A Single Block"""
    def __init__(self):
        self.BlockHash = 0
        self.PrevHash = 0
        self.BlockHeight = 0
        self.TXs = []
    def caculateHash(self):
        hstr = ''
        #mt = MerkleTools(hash_type="sha256")
        for tx in self.TXs:
            #mt.add_leaf(tx['Hash'])
            hstr += tx.Hash
        #mt.make_tree()
        #mtRoot = mt.get_merkle_root()
        sha_gen = hashlib.sha256()
        sha_gen.update(str.encode(self.PrevHash + hstr))
        self.BlockHash = sha_gen.hexdigest()
        #self.BlockHash = mtRoot

class Tx:
    """A Transaction Record"""
    def __init__(self):
        self.From = ''
        self.To = ''
        self.Value = 0
        self.Hash = ''
    def caculateHash(self):
        sha_gen = hashlib.sha256()
        sha_gen.update(str.encode(self.From+self.To+str(self.Value)))
        self.Hash = sha_gen.hexdigest()

app = Flask(__name__)
blockchain = []
currentBlock = Block()
balance_table = dict()

@app.route('/')
def mainPage():
    return render_template('index.html', blockchain = blockchain)


@app.route('/addtx', methods=['POST'])
def addTX():
    global currentBlock
    sender = request.form['from_addr']
    receiver = request.form['to_addr']
    amount = int(request.form['value'])
    tx = Tx()
    if sender not in balance_table:
        balance_table[sender] = 100
    if receiver not in balance_table:
        balance_table[receiver] = 100
    if balance_table[sender] >= amount:
        balance_table[sender] -= amount;
        balance_table[receiver] += amount;
        tx.From = sender
        tx.To = receiver
        tx.Value = amount
        tx.caculateHash()
        currentBlock.TXs.append(tx)
        return redirect('/')
    else:
        return render_template('error.html')


def newBlock():
    print('#### Create new block')
    global currentBlock
    chain_length = len(blockchain)
    currentBlock.PrevHash = blockchain[chain_length-1].BlockHash
    currentBlock.BlockHeight = chain_length+1
    currentBlock.caculateHash()
    blockchain.append(currentBlock)
    currentBlock = Block()
    threading.Timer(10, newBlock).start()
    return


if __name__ == '__main__':
    genesisBlock = Block()
    genesisBlock.PrevHash = '0'
    genesisBlock.BlockHeight = 1
    genesisBlock.caculateHash()
    blockchain.append(genesisBlock)
    threading.Timer(10, newBlock).start()
    #app.debug = True
    app.run(host='0.0.0.0', port=8000)
