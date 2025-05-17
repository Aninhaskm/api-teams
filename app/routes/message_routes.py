from fastapi import APIRouter, HTTPException
from app.models.message import MessageRequest
from app.services.teams_service import TeamsService

router = APIRouter()

@router.post("/send_message") # Define uma rota post para enviar mensagens, recebe os dados da requisição, chama o serviço TeamsService e retorna a resposta
async def send_message(message: MessageRequest):
    teams_service = TeamsService()
    try:
        response = teams_service.send_message(
            user_email=message.user_email,
            content=message.message
        )
        return {"status": "sent", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar mensagem: {str(e)}")
