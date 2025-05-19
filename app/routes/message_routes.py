"""
Define as rotas relacionadas ao envio de mensagens na API Teams.
Utiliza FastAPI para expor endpoint de envio de mensagens.
"""
from fastapi import APIRouter, HTTPException
from app.models.message import MessageRequest
from app.services.teams_service import TeamsService

router = APIRouter()
teams_service = TeamsService()

@router.post("/send_message") # Define uma rota post para enviar mensagens, recebe os dados da requisição, chama o serviço TeamsService e retorna a resposta
async def send_message(message: MessageRequest):
    try:
        response = teams_service.send_message(
            user_email=message.user_email,
            content=message.message
        )
        return {"status": "sent", "data": response}
    except Exception:
        # Não expõe detalhes internos para o cliente
        raise HTTPException(status_code=500, detail="Erro ao enviar mensagem.")
