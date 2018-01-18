from flask import Flask, render_template, request, redirect
import json

class Block:
    """A Single Block"""
    BlockHasg = 0
    PrevHash = 0
    BlockHeight = 0
    TXs = []


app = Flask(__name__)
blockchain = []
currentBlock = Block()


@app.route("/")
def mainPage():
    return render_template('index.html', blockchain = blockchain)


def receiveTX():
    tx = {}
    tx['From'] = 666
    tx['To'] = 777
    tx['Value'] = 888
    tx['Hash'] = 9797
    currentBlock.TXs.append(tx)
    return 1


def newBlock():
    currentBlock.BlockHasg = 7878
    block = Block()
    block.PrevHash = blockchain[len(blockchain)-1].BlockHasg
    block.BlockHeight = len(blockchain)+1
    blockchain.append(block)
    currentBlock.TXs.clear()
    #set alarm
    return


if __name__ == '__main__':
    #genesisBlock = {'BlockHasg': 1234, 'PrevHash':0000, 'BlockHeight':1, 'TXs':[{'Hash':1100, 'From':1234, 'To':2345, 'Value':5000}, {'Hash':9887, 'From':1424, 'To':5566, 'Value':87}]}
    genesisBlock = Block()
    genesisBlock.BlockHasg = 1234
    genesisBlock.PrevHash = 0000
    genesisBlock.BlockHeight = 1
    blockchain.append(genesisBlock)
    receiveTX()
    receiveTX()
    receiveTX()
    newBlock()
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
