from langchain_openai import AzureChatOpenAI
from configparser import ConfigParser
from langchain_openai import ChatOpenAI

configs = ConfigParser()
configs.read('configs.ini')

def agent_init():
	client = ChatOpenAI(
            model=configs['CLAUDE'][ 'HAIKU_MODEL' ],
            temperature=0,
            openai_api_key=configs['CLAUDE'][ 'API_KEY' ],
            openai_api_base=configs['CLAUDE'][ 'ENDPOINT' ]
        )

	return client