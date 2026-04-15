from langchain_core.messages import HumanMessage
import base64
from PIL import Image
import io
from utils.agent_init import agent_init

class LangChainVisionExtractor:
	def __init__(self):
		"""
		Inicializa o cliente Azure OpenAI via LangChain
		"""
		self.llm = agent_init()

	def image_to_base64(self, image_path):
		"""Converte imagem para base64"""
		with open(image_path, "rb") as image_file:
			return base64.b64encode(image_file.read()).decode('utf-8')

	def extract_data_basic(self, image_path, prompt):
		"""
		Extrai dados básicos de uma imagem
		"""
		# Codificar imagem
		base64_image = self.image_to_base64(image_path)

		# Criar mensagem com imagem
		message = HumanMessage(
			content=[
				{"type": "text", "text": prompt},
				{
					"type": "image_url",
					"image_url": {
					"url": f"data:image/jpeg;base64,{base64_image}"
					}
				}
			]
		)

		# Chamar o modelo
		response = self.llm.invoke([message])
		return response.content
