# strawberry-chatbot
This is a chatbot which I named of strawberry who will be the first page that I made using react.js


# Rodar o projecto

## Inicializar o servidor backend
### Criar um ambiente virtual
python3 -m  venv .venv

### Ativar ambiente virtual windows
.venv/Activate/Scripts

### Ativar ambiente virtual Linux
source .venv/Scripts/bash

### Instalar os requisitos

pip install -r requirements.txt

### Ligar o servidor

cd backend
uvicorn main:app --reload --port 8000


## Inicializar o servidor frontend
### Instalar as dependencias do projecto
cd frontend
npm install

### Ligar o servidor
npm run dev