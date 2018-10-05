from flask import Flask, request
from document import Document

app = Flask(__name__)

@app.route('/draw', methods=['POST'])
def draw():
    Document.add_content(request.get_json()['message'])
    return Document.get_content()
