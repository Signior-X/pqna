from flask import Flask, render_template, jsonify
import pandas as pd
import random

app = Flask(__name__)

last_question_number = 4
qdics = {
    0: 'Do ***** likes Shivani?',
    1: 'Kya ***** ka byah hogya?',
    2: 'Has ***** ever kissed in his life?',
    3: 'Is ***** laugh a lot?',
    4: 'Can ***** murder someone?'
}

players = {
    0: 'Babu',
    1: 'Sarthak',
    2: 'Khubi',
    3: 'Deepali',
    4: 'Devansh',
}

# Main pages here
@app.route('/')
def index():
    qr = random.randint(0,last_question_number)
    pr = random.randint(0,4)
    qname = qdics[qr].replace("*****", players[pr])
    return render_template('index.html', qno=qr, pno=pr, ques=qname )

# APIs here
@app.route('/api/generate')
def generate():
    return 'Hello'

if __name__ == "main":
    app.run()
