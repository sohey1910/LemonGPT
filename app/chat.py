import traceback
from transformers import AutoTokenizer, AutoModel


class Chatbot():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b-int4", trust_remote_code=True)
        self.model = AutoModel.from_pretrained("THUDM/chatglm-6b-int4", trust_remote_code=True).half().quantize(4).cuda()
        self.model = self.model.eval()

    def predict(self,question,history):
        
        count = 0
        for response, history in self.model.stream_chat(self.tokenizer, question, history=history):
            count += 1
            if count % 8 == 0:
                return self.__build_prompt(history)
        return self.__build_prompt(history)


    def __build_prompt(self,history):
        prompt=""
        for query, response in history:
            prompt += f"\n提问：{query}"
            prompt += f"\n回答：{response}"
        return prompt


if __name__ == "__main__":
    c=Chatbot()
    while True:
        try:
            history=[]
            query=input("\n请输入问题：")
            if query == "stop":
                break
            a1=c.predict(query,history)
            print(f"answer:{a1} history:{history}")
        except Exception as e:
            print(traceback.format_exc())

    