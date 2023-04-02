from flask_ngrok import run_with_ngrok
from flask import Flask, request, jsonify, render_template, Response,stream_with_context,make_response
# from chatbot import ChatGPT
from chat import Chatbot
from data import record

import time,random,json
import os,copy,traceback
from base64 import b64encode
from threading import Thread
from collections import OrderedDict

TOKEN_TIME_OUT=60*5

app = Flask(__name__)
run_with_ngrok(app)
chatbot = Chatbot()

# history = {}
# streaming={}

def generate_token():
    byte_str=os.urandom(16)
    ret=b64encode(byte_str).decode('utf-8')
    return ret

def del_timeout_token():
	while True:
		try:
			keys=list(record.record.keys())
			# for key,value in record.record.items():
			for key in keys:
				value=record.record[key]
				exists_time=time.time()-value['create_time']
				if exists_time > TOKEN_TIME_OUT:
					del record.record[key]
					continue
				if len(value['prompt']) > 5:
					del record.record[key]["prompt"][0]
		except Exception as e:
			print(traceback.format_exc())
		

@app.route("/get_token")
def get_token():
    if not request.cookies.get("token",None):
        resp = make_response('存储cookie')
        token=generate_token()
        record.record[token]={}
        record.record[token]['create_time']=time.time()
        record.record[token]['prompt']=OrderedDict()
        resp.set_cookie(key='token',value=token,max_age=TOKEN_TIME_OUT)
    else:
        resp = make_response('存在cookie')
    return resp


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    token = request.cookies.get("token")
    if token not in record.record:
        record.record[token]={}
        record.record[token] = {
			"create_time":time.time(),
			"prompt":OrderedDict()
		}
    question = request.form['question']
    id=request.values.get("id")
    print(f"id:{id}  question:{question} token:{token}")
    # answer = chatbot.chat(question)
    record.record[token]['prompt'][id]={
		"question":question,
		"answer":""
	}
    return jsonify({"ec":0,"em":"success","result":""})

@app.route('/streaming')
def streaming():
	token=request.cookies.get("token")
	id=request.values.get("id")
	print(f"streaming token:{token}  id:{id}")
	response = Response(stream_with_context(chatbot.predict(token,id)), mimetype="text/event-stream")
	response.headers["Cache-Control"] = "no-cache"
	response.headers["X-Accel-Buffering"] = "no"
	return response

if __name__ == '__main__':
    Thread(target=del_timeout_token).start()
    app.run()
