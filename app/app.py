from flask_ngrok import run_with_ngrok
from flask import Flask, request, jsonify, render_template

from chatbot import ChatGPT

app = Flask(__name__)
run_with_ngrok(app)
chatbot = ChatGPT()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
	question = request.form['question']
	answer = chatbot.chat(question)
	return jsonify({'answer': answer})

if __name__ == '__main__':
	app.run()
