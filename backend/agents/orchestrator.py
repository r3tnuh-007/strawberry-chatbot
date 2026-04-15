from langchain_core.messages import HumanMessage
from utils.agent_init import agent_init
from agents.extractor_agent import LangChainVisionExtractor
from agents.validator_agente import ValidatorAgent

class OrchestratorAgent:
	def __init__(self):
		"""
		Inicializa o cliente Azure OpenAI via LangChain
		"""
		self.llm = agent_init()

	def extract(self, image_path, prompt):
		"""
			Chama o agente para extracao de dados básicos de uma imagem
		"""
		extractor = LangChainVisionExtractor()
		return extractor.extract_data_basic(image_path, prompt)

	def validate(self, text, rules="None"):
		"""
			Chama o agente para validação de dados fornecidos em texto
		"""
		validator = ValidatorAgent()
		return validator.validate_data_basic(text, rules)

	def decide_agent(self, text, rules="None"):
		"""
			Decide qual agente usar baseado no texto fornecido
		"""
		template_prompt = f"""Você é um agente orquestrador.
		Tens a tua disposição dois agentes: Extractor e Validator.
		Seu trabalho é revisar o seguinte texto(documento) extraído.
		Responda com "Extractor" se o texto for o caminho para uma imagem
		e o documento precisar de extração de dados,
		responda com "Validator" se o documento for um bilhete de identidade ou um Documento que
		contenha a morada e precisar de validação desses dados com base nas regras: {rules}.
		Se o texto não se enquadrar em nenhum dos dois casos, responda com "Nenhum".
		{text}
		"""
		# Criar mensagem com texto
		message = HumanMessage(
			content=template_prompt
			)

		# Chamar o modelo
		response = self.llm.invoke([message])
		if response.content == "Extractor":
			prompt = "Extraia todo o texto desta imagem, mantendo ao maximo o seu formato original."
			return self.validate(self.extract(text, prompt), rules)  # chaining extract and validate
		elif response.content == "Validator":
			return self.validate(text, rules)
		else:
			return "Inválido: Esse documento não contém informações relevantes para extração ou validação."

