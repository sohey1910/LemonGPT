import openai
import os

# openai.api_key = os.environ.get("OPENAI_API_KEY")  # 设置 API 密钥
openai.api_key=""

class ChatGPT:
	def __init__(self):
		self.prompt = "请问你有什么问题？"
		# self.model = "text-davinci-002"  # GPT-3 模型
		self.model="gpt-3.5-turbo"

	def chat(self, question):
		# input_text = f"{self.prompt}\nQ: {question}\nA:"
		# response = openai.Completion.create(
		# 	#engine=self.model,
		# 	model=self.model,
		# 	prompt=input_text,
		# 	max_tokens=1024,
		# 	n=1,
		# 	stop=None,
		# 	temperature=0.7,
		# )
		# answer = response.choices[0].text.strip()
		response = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=[
		    	{"role": "user", "content": question}
			]
		)
		answer=response.choices[0].message.content.strip()
		print(f"answer:{answer}  type:{type(answer)}")
        # import os
        # import openai
        # openai.api_key = os.getenv("OPENAI_API_KEY")
		return answer
