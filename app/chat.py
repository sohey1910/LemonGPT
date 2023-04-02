import traceback
from transformers import AutoTokenizer, AutoModel
from data import record
import json

class Chatbot():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b-int4", trust_remote_code=True)
        self.model = AutoModel.from_pretrained("THUDM/chatglm-6b-int4", trust_remote_code=True).half().quantize(4).cuda()
        self.model = self.model.eval()

    def predict(self,token,id):
        question=record.record[token]['prompt'][id]
        history=[]
        for _id,value in record.record[token]['prompt'].items():
            if _id!=id:
                question=value['question']
                answer=value['answer']
                history.append((question,answer))
        print(f"predict question:{question} history:{history}")
        count = 0
        stop_stream=False
        for response, history in self.model.stream_chat(self.tokenizer, question, history=history):
            if stop_stream:
                stop_stream = False
                break
            else:
                count += 1
                if count % 8 == 0:
                    yield self.__build_prompt(history,False)
        yield self.__build_prompt(history,True,token,id)
        #             stop_stream=True
        #             return self.__build_prompt(history)
        # return self.__build_prompt(history)


    def __build_prompt(self,history,is_finished=False,token=None,id=None):
        prompt=""
        for query, response in history:
            # prompt += f"\n提问：{query}"
            prompt += f"\n回答：{response}"
        if is_finished:
            record.record[token][id]["answer"]=response
        json_data=json.dumps({"question":query,"answer":prompt})
        return f"data:{json_data}\n\n"
        # json_data = json.dumps({'time': time.time(), 'value': random.random() * 100})
		# 	yield f"data:{json_data}\n\n"



if __name__ == "__main__":
    c=Chatbot()
    while True:
        try:
            history=[]
            query=input("\n请输入问题：")
            if query == "stop":
                break
            a1=c.predict(query,history)
            # print(f"answer:{a1} history:{history}")
            for vv in a1:
                print(f"vv:{vv}")
        except Exception as e:
            print(traceback.format_exc())

    