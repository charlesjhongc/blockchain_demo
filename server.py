from flask import Flask, render_template, request, redirect
import hashlib
import time
import threading

class Block:
    """A Single Block"""
    def __init__(self):
        self.BlockHasg = 0
        self.PrevHash = 0
        self.BlockHeight = 0
        self.TXs = []
    def caculateHash(self):
        sha_gen = hashlib.sha256()
        sha_gen.update(b'fwqwe')
        self.BlockHasg = sha_gen.hexdigest()

app = Flask(__name__)
blockchain = []
currentBlock = Block()

@app.route("/")
def mainPage():
    return render_template('index.html', blockchain = blockchain)

@app.route("/addtx", methods=["POST"])
def addTX():
    global currentBlock
    tx = {}
    tx['From'] = request.form["from_addr"]
    tx['To'] = request.form["to_addr"]
    tx['Value'] = request.form["value"]
    sha_gen = hashlib.sha256()
    sha_gen.update(str.encode(tx['From']+tx['To']+tx['Value']))
    tx['Hash'] = sha_gen.hexdigest()
    currentBlock.TXs.append(tx)
    return redirect("/")


def newBlock():
    print('#### Create new block')
    global currentBlock
    chain_length = len(blockchain)
    currentBlock.PrevHash = blockchain[chain_length-1].BlockHasg
    currentBlock.BlockHeight = chain_length+1
    currentBlock.caculateHash()
    blockchain.append(currentBlock)
    currentBlock = Block()
    threading.Timer(10, newBlock).start()
    return


if __name__ == '__main__':
    genesisBlock = Block()
    genesisBlock.PrevHash = 0
    genesisBlock.BlockHeight = 1
    genesisBlock.caculateHash()
    blockchain.append(genesisBlock)
    threading.Timer(10, newBlock).start()
    #app.debug = True
    app.run(host='0.0.0.0', port=8000)
