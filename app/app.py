from flask_ngrok import run_with_ngrok
from flask import Flask, request, jsonify, render_template, Response,stream_with_context
# from chatbot import ChatGPT
from chat import Chatbot
import time,random,json
import os,copy
from base64 import b64encode


app = Flask(__name__)
run_with_ngrok(app)
# chatbot = ChatGPT()
chatbot = Chatbot()
history = {}

def generate_token():
    byte_str=os.urandom(16)
    ret=b64encode(byte_str).decode('utf-8')
    return ret

@app.route("/get_token")
def get_token():
    if not request.cookies.get("token",None):
        resp = make_response('存储cookie')
        token=generate_token()
        record[token]=[]
        resp.set_cookie(key='token',value=token,max_age=60*10)
    else:
        resp = make_response('存在cookie')
    return resp


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    token = request.cookie.get("token")
    if token not in history:
        history[token] = []
    question = request.form['question']
    # answer = chatbot.chat(question)
    answer = chatbot.predict(question, copy.deepcopy(history[token]))
    print(f"token:{token}  history:{history[token]}  answer:{answer}")
    return jsonify({'answer': answer})

@app.route('/streaming')
def streaming():
	def generate_dummy_data():
		for i in range(10):
			json_data = json.dumps({'time': time.time(), 'value': random.random() * 100})
			yield f"data:{json_data}\n\n"
			time.sleep(1)
	
	response = Response(stream_with_context(generate_dummy_data()), mimetype="text/event-stream")
	response.headers["Cache-Control"] = "no-cache"
	response.headers["X-Accel-Buffering"] = "no"
	return response

if __name__ == '__main__':
    app.run()
