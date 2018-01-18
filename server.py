from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)
block = {'BlockHasg': 1234, 'PrevHash':0000, 'BlockHeight':1, 'TXs':[{'Hash':1100, 'From':1234, 'To':2345, 'Value':5000}, {'Hash':9887, 'From':1424, 'To':5566, 'Value':87}]}

@app.route("/")
def mainPage():
    return render_template('index.html', block = block)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
