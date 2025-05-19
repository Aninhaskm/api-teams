import requests
import re
from app.config import get_settings
from app.utils.logger import logger


class TeamsService:
    """
    Serviço responsável por interagir com a API do Microsoft Teams via Microsoft Graph.
    Gerencia autenticação, busca de usuários, criação de chats e envio de mensagens.
    """
    def __init__(self):
        """
        Inicializa o serviço, carregando configurações e URLs base.
        """
        self.settings = get_settings()
        self.base_url = self.settings.GRAPH_API_ENDPOINT
        self.token_url = f"{self.settings.AUTHORITY}/v2.0/token"

    def get_access_token(self):
        """
        Solicita e retorna um token de acesso do Azure AD para autenticação nas requisições.
        Lança exceções em caso de erro na requisição ou resposta inválida.
        """
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
        """
        Retorna os headers necessários para requisições autenticadas na API Graph.
        """
        return {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Content-Type': 'application/json'
        }
    
    def get_user_id_by_email(self, email: str) -> str:
        """
        Busca o ID do usuário no Microsoft Teams a partir do e-mail fornecido.
        Args:
            email (str): E-mail do usuário.
        Returns:
            str: ID do usuário encontrado.
        """
        # Validação de e-mail para evitar entradas maliciosas
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            logger.warning("E-mail inválido fornecido para busca de usuário.")
            raise ValueError("Formato de e-mail inválido.")
        headers = self.get_headers()
        url = f"{self.base_url}/users/{email}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            user_id = response.json().get("id")
            if not user_id:
                logger.warning("ID de usuário não encontrado para o e-mail informado.")
                raise ValueError("Usuário não encontrado.")
            return user_id
        except requests.exceptions.RequestException as e:
            logger.error("Erro ao buscar usuário no Graph API.")
            raise ValueError("Erro ao buscar usuário.") from e
    
    def create_chat_with_user(self, user_id: str) -> str:
        """
        Cria um chat 1:1 com o usuário especificado pelo ID.
        Args:
            user_id (str): ID do usuário para criar o chat.
        Returns:
            str: ID do chat criado.
        """
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
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            chat_id = response.json().get("id")
            if not chat_id:
                logger.warning("ID do chat não retornado pela API.")
                raise ValueError("Falha ao criar chat.")
            return chat_id
        except requests.exceptions.RequestException as e:
            logger.error("Erro ao criar chat no Graph API.")
            raise ValueError("Erro ao criar chat.") from e
    
    def send_message(self, user_email: str, content: str):
        """
        Envia uma mensagem para o usuário especificado por e-mail.
        Cria o chat se necessário e registra logs do processo.
        Args:
            user_email (str): E-mail do destinatário.
            content (str): Conteúdo da mensagem a ser enviada.
        Returns:
            dict: Resposta da API Graph após envio da mensagem.
        """
        logger.info("Iniciando envio de mensagem")
        try:
            user_id = self.get_user_id_by_email(user_email)
            logger.info("ID do usuário obtido com sucesso")
            chat_id = self.create_chat_with_user(user_id)
            logger.info("Chat criado com sucesso")
            headers = self.get_headers()
            url = f"{self.base_url}/chats/{chat_id}/messages"
            payload = {
                "body": {
                    "content": content
                }
            }
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logger.info("Mensagem enviada com sucesso")
            return response.json()
        except Exception:
            logger.error("Falha ao enviar mensagem.")
            raise ValueError("Erro ao enviar mensagem.")
