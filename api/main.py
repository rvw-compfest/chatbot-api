from flask import Flask, request, jsonify
from retrieve import get_response

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hi!"

@app.route('/ask', methods=["POST"])
def get_answer():
    data = request.json

    print(data)

    query = data.get('question')

    if not query:
        return jsonify({'error': 'Please provide a question.'}), 400
    
    answer = get_response(query)

    return answer

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
