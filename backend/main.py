from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir o frontend React aceder ao backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # porta típica do Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    user_message = request.message

    # Aqui colocas a tua lógica de chatbot
    # Por agora, uma resposta simples
    if "olá" in user_message.lower():
        reply = "Olá! Como posso ajudar?"
    else:
        reply = f"Recebi a tua mensagem: '{user_message}'. Ainda estou a aprender 🙂"

    return ChatResponse(reply=reply)
