from flask_ngrok import run_with_ngrok
from flask import Flask, request, jsonify, render_template, Response,stream_with_context
# from chatbot import ChatGPT
from chat import Chatbot
import time

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
    print(f"ip_addr:{ip_addr}  history:{history[ip_addr]}  answer:{answer}")
    return jsonify({'answer': answer})

@app.route('/streaming')
def streaming():
	def generate_dummy_data():
		for i in range(10):
			time.sleep(0.5)
			yield str(time.time())
	
	response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
	response.headers["Cache-Control"] = "no-cache"
	response.headers["X-Accel-Buffering"] = "no"
	return response

if __name__ == '__main__':
    app.run()
