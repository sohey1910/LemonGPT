from flask_ngrok import run_with_ngrok
from flask import Flask, request, jsonify, render_template
# from chatbot import ChatGPT
from chat import Chatbot
app = Flask(__name__)
run_with_ngrok(app)
# chatbot = ChatGPT()
chatbot = Chatbot()
history = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    ip_addr = request.remote_addr
    if ip_addr not in history:
        history[ip_addr] = []
    question = request.form['question']
    # answer = chatbot.chat(question)
    answer = chatbot.predict(question, history[ip_addr])
    print(f"ip_addr:{ip_addr}  history:{history[ip_addr]}")
    return jsonify({'answer': answer})


if __name__ == '__main__':
    app.run()
