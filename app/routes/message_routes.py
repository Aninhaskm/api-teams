from fastapi import APIRouter, HTTPException
from app.models.message import MessageRequest
from app.services.teams_service import TeamsService

router = APIRouter()
teams_service = TeamsService()

@router.post("/send_message") # Define uma rota post para enviar mensagens, recebe os dados da requisição, chama o serviço TeamsService e retorna a resposta
async def send_message(message_request: MessageRequest):
    """
    Envia uma mensagem para um usuário específico no Microsoft Teams.
    """
    try:
        response = teams_service.send_message(message_request.user_id, message_request.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))