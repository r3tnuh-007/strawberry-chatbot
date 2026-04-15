from langchain_core.messages import HumanMessage
from utils.agent_init import agent_init

class ValidatorAgent:
	def __init__(self):
		"""
		Inicializa o cliente Azure OpenAI via LangChain
		"""
		self.llm = agent_init()

	def validate_data_basic(self, text, rules="None"):
		"""
			Valida os dados fornecidos em texto
		"""
		if rules == "BI":
			template_prompt = f"""Você é um agente de validação de dados.
			Seu trabalho é revisar o seguinte texto(documento) extraído. A data de hoje é 17/02/2026.
			Retorne Nome do proprietario|Numero de identificação|Residência|Data de nascimento(dd/mm/aaaa) (nesse mesmo formato)
			se não conseguir retirar essas informações podes preencher com Nenhum|Nenhum|Nenhum|Nenhum,
			se as informações forem parciais podes fazer uma mistura com as que tiver disponivel
			por exemplo:
			Nome do proprietario|Nenhum|Residência|Data de nascimento(dd/mm/aaaa)
			Nenhum|Numero de identificação|Residência|Data de nascimento(dd/mm/aaaa)
			Retorne apenas o resultado seguindo o formato indicado, sem explicações ou texto adicional.
			O texto a validar é:
			{text}
			"""
		elif rules == "Morada":
			template_prompt = f"""Você é um agente de validação de dados.
			Seu trabalho é revisar o seguinte texto(documento) extraído. A data de hoje é 17/02/2026.
			Retorne Nome do proprietario|Numero de identificação|Data de nascimento(dd/mm/aaaa) (nesse mesmo formato)
			se não conseguir retirar essas informações
			podes preencher com Nenhum|Nenhum|Nenhum,
			se as informações forem parciais podes fazer uma mistura com as que tiver disponivel
			por exemplo:
			Nome do proprietario|Nenhum|Data de Nascimento(dd/mm/aaaa)
			Nenhum|Numero de identificação|Data de nascimento(dd/mm/aaaa)
			Retorne apenas o resultado seguindo o formato indicado, sem explicações ou texto adicional.
			O texto a validar é:
			{text}
			"""
		# Criar mensagem com texto
		message = HumanMessage(
			content=template_prompt
			)

		# Chamar o modelo
		response = self.llm.invoke([message])
		return response.content