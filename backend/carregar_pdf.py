from PyPDF2 import PdfReader
import tempfile
from utils.convert_pdf_to_image import *
from agents.extractor_agent import LangChainVisionExtractor
from agents.validator_agente import ValidatorAgent
from agents.orchestrator import OrchestratorAgent
import asyncio


#arquivos = st.file_uploader("Escolha os arquivos PDF", type=["pdf"], accept_multiple_files=True)

def processar_pdf(arquivo, rule="BI"):
	extractor = LangChainVisionExtractor()
	pdf_path = "uploads/" + arquivo
	if arquivo:
		print()
		print("[Carregamento do PDF]")
		print(f"🟢 - Arquivo {arquivo} carregado com sucesso")
		caminhos = pdf_to_png_simples(pdf_path=pdf_path)
		print(f"🟢 - Arquivo **{arquivo}** convertido para imagens com sucesso.")
		# Extrair texto das imagens
		texto = ""
		for caminho in caminhos:
			texto1 = extractor.extract_data_basic(
				image_path=caminho,
				prompt="Extraia todo o texto desta imagem, mantendo ao maximo o seu formato original."
			)
			texto = texto + texto1
			#print(f"Texto extraído da imagem {caminho}:\n{texto}\n")
		# Mostrar resultados
		print("[Extração do PDF]")
		print("🟢 - Texto extraído do PDF com sucesso.")
		print()
		print("[Validação do PDF]")
		orquestrador = OrchestratorAgent()
		validacao = orquestrador.decide_agent(texto, rule)
		print("🟢 - Validação concluída com sucesso.")
		print()
		return validacao
	else:
		print("Nenhum arquivo selecionado.")
		return  "Nenhum|Nenhum|Nenhum"





