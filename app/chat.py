import traceback
from transformers import AutoTokenizer, AutoModel
from data import record
import json,re

class Chatbot():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b-int4", trust_remote_code=True)
        self.model = AutoModel.from_pretrained("THUDM/chatglm-6b-int4", trust_remote_code=True).half().quantize(4).cuda()
        self.model = self.model.eval()

    def _sub_new_generate(self,pre,cur):
        if not pre:
            return cur
        else:
            pattern=f"^{pre}"
            diff=re.sub(pattern, "" ,cur)
            return diff

    def predict(self,token,id):
        question=record.record[token]['prompt'][id]['question']
        history=[]
        for _id,value in record.record[token]['prompt'].items():
            if _id!=id:
                question=value.get("question","")
                answer=value.get("answer","")
                history.append((question,answer))
        print(f"predict question:{question} history:{history}")
        count = 0
        stop_stream=False
        pre=""
        full_str=""
        for response, history in self.model.stream_chat(self.tokenizer, question, history=history):
            if stop_stream:
                stop_stream = False
                break
            else:
                count += 1
                if count % 8 == 0:
                    cur=history[-1][1]
                    diff=self._sub_new_generate(pre,cur)
                    pre=cur
                    full_str+=diff
                    yield self.__format_response(question,diff)
        cur=history[-1][1]
        diff=self._sub_new_generate(pre,cur)
        pre=cur
        full_str+=diff
        # finished
        record.record[token]['prompt'][id]['answer']=full_str
        yield self.__format_response(question,diff)

    def __format_response(self,question,response):
        json_data=json.dumps({'question':question,'answer':response},ensure_ascii=False)
        return f"data:{json_data}\n\n"


    def __build_prompt(self,history,is_finished=False,token=None,id=None):
        prompt=""
        for query, response in history:
            # prompt += f"\n提问：{query}"
            prompt += f"\n回答：{response}"
        if is_finished:
            record.record[token]['prompt'][id]["answer"]=response
        json_data=json.dumps({"question":query,"answer":prompt})
        return f"data:{json_data}\n\n"
        # json_data = json.dumps({'time': time.time(), 'value': random.random() * 100})
		# 	yield f"data:{json_data}\n\n"



if __name__ == "__main__":
    from collections import OrderedDict
    import time

    def test_init(query):
      token="1111111111111"
      id=f"{time.time()}"
      if token not in record.record:
        record.record[token]={
            'prompt':OrderedDict()
        }
      record.record[token]['prompt'][id]={}
      record.record[token]['prompt'][id]['question']=query
      return token,id

    c=Chatbot()
    while True:
        try:
            # history=[]
            query=input("\n请输入问题：")
            token,id=test_init(query)
            if query == "stop":
                break
            a1=c.predict(token,id)
            # print(f"answer:{a1} history:{history}")
            print(f"type a1:{type(a1)}")
            for vv in a1:
                print(f"vv:{vv}")
        except Exception as e:
            print(traceback.format_exc())

    