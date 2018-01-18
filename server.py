from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

@app.route("/")
def mainPage():
    return render_template('index.html')

if __name__ == '__main__':
    updateSearchResult()
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
