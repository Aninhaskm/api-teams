"""
Define o modelo de requisição para envio de mensagens via API Teams.
Utiliza Pydantic para validação automática dos dados recebidos.
"""
from pydantic import BaseModel # Validação automática dos dados recebidos

class MessageRequest(BaseModel): # Define o modelo de requisição para enviar mensagens
    user_email: str
    message: str