# app.py
from flask import Flask, render_template, request, jsonify
from train_model import genetic_algorithm, GRAPH

app = Flask(__name__)

@app.route('/')
def index():
    nodes = list(GRAPH.keys())
    return render_template('index.html', nodes=nodes)

@app.route('/find_path', methods=['POST'])
def find_path():
    data = request.get_json()
    start = data['start']
    end = data['end']
    blocked = data.get('blocked', [])

    path, details = genetic_algorithm(start, end, blocked)

    return jsonify({
        'path': path,
        'start': start,
        'end': end,
        'blocked': blocked,
        'metrics': details
    })


if __name__ == '__main__':
    app.run(debug=True)