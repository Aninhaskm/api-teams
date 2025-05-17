import requests
from app.config import get_settings
from app.utils.logger import logger


class TeamsService:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.GRAPH_API_ENDPOINT
        self.token_url = f"{self.settings.AUTHORITY}/v2.0/token"

    def get_access_token(self):
        data = {
            'client_id': self.settings.CLIENT_ID,
            'client_secret': self.settings.CLIENT_SECRET,
            'scope': self.settings.SCOPE,
            'grant_type': 'client_credentials'
        }
        logger.info("Solicitando token de acesso ao Azure AD", extra={"url": self.token_url})

        try:
            response = requests.post(self.token_url, data=data)
            response.raise_for_status()
            token = response.json().get('access_token')

            if not token:
                logger.error("Token não encontrado na resposta!", extra={"resposta": response.text})
                raise ValueError("Token de acesso ausente na resposta.")
            
            logger.info("Token de acesso obtido com sucesso")
            return token 
        
        except requests.exceptions.HTTPError as http_err:
            logger.error("Erro HTTP ao solicitar token", extra={
                "erro": str(http_err),
                "status_code": response.status_code,
                "resposta": response.text
            })
            raise

        except Exception as e:
            logger.exception("Erro inesperado ao obter token de acesso")
            raise

    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Content-Type': 'application/json'
        }
    
    def get_user_id_by_email(self, email: str) -> str:
        headers = self.get_headers()
        url = f"{self.base_url}/users/{email}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("id")
    
    def create_chat_with_user(self, user_id: str) -> str:
        headers = self.get_headers()
        url = f"{self.base_url}/chats"
        payload = {
            "chatType": "oneOnOne",
            "members": [{
                "@data.type": "#microsoft.graph.aadUserConversationMember",
                "roles": ["owner"],
                "user@odata.bind": f"{self.base_url}/users('{user_id}')"
            }]
        }
        response = requests.posts(url, headears=headers, json=payload)
        response.raise_for_status()
        return response.json()["id"]
    
    def send_message(self, user_email: str, content: str):
        logger.info("Iniciando envio de mensagem", extra={"email": user_email})

        user_id = self.get_user_id_by_email(user_email)
        logger.info("ID do usuário obtido", extra={"user_id": user_id})

        chat_id = self.create_chat_with_user(user_id)
        logger.info("Chat criado com sucesso", extra={"chat_id": chat_id})

        headers = self.get_headers()
        url = f"{self.base_url}/chats/{chat_id}/messages"
        payload = {
            "body": {
                "content": content
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        logger.info("Mensagem enviada com sucesso", extra={"status": response.status_code})
        return response.json()
