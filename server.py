from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)
blockchain = []
genesisBlock = {'BlockHasg': 1234, 'PrevHash':0000, 'BlockHeight':1, 'TXs':[{'Hash':1100, 'From':1234, 'To':2345, 'Value':5000}, {'Hash':9887, 'From':1424, 'To':5566, 'Value':87}]}
blockchain.append(genesisBlock)

@app.route("/")
def mainPage():
    return render_template('index.html', blockchain = blockchain)

def newBlock():
    block = {}
    block['BlockHasg'] = 7878
    block['PrevHash'] = 8787
    block['BlockHeight'] = len(blockchain)+1
    blockchain.append(block)
    return

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
