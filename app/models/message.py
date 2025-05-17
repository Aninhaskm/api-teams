from pydantic import BaseModel # Validação automática dos dados recebidos

class MessageRequest(BaseModel): # Define o modelo de requisição para enviar mensagens
    user_id: str
    message: str