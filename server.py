from flask import Flask, render_template, request, redirect
import json
import time
import threading

import random

class Block:
    """A Single Block"""
    def __init__(self):
        self.BlockHasg = 0
        self.PrevHash = 0
        self.BlockHeight = 0
        self.TXs = []
    #del caculateHash():
        #self..BlockHasg = 9999

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
    tx['Hash'] = random.randint(1, 9999)
    currentBlock.TXs.append(tx)
    return redirect("/")


def newBlock():
    print('#### Create new block')
    global currentBlock
    chain_length = len(blockchain)
    currentBlock.BlockHasg = random.randint(1, 9999)
    currentBlock.PrevHash = blockchain[chain_length-1].BlockHasg
    currentBlock.BlockHeight = chain_length+1
    blockchain.append(currentBlock)
    currentBlock = Block()
    threading.Timer(10, newBlock).start()
    return


if __name__ == '__main__':
    #genesisBlock = {'BlockHasg': 1234, 'PrevHash':0000, 'BlockHeight':1, 'TXs':[{'Hash':1100, 'From':1234, 'To':2345, 'Value':5000}, {'Hash':9887, 'From':1424, 'To':5566, 'Value':87}]}
    genesisBlock = Block()
    genesisBlock.BlockHasg = random.randint(1, 9999)
    genesisBlock.PrevHash = 0000
    genesisBlock.BlockHeight = 1
    blockchain.append(genesisBlock)
    threading.Timer(10, newBlock).start()
    #app.debug = True
    app.run(host='0.0.0.0', port=8000)
