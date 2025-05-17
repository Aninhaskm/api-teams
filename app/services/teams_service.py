import requests
from app.config import Settings

class TeamsService:
    def __init__(self):
        self.token = self.get_acess_token()

    def get_acess_token(self):
        url = f"{Settings.AUTHORITY}/v2.0/token"
        data = {
            'client_id': Settings.CLIENT_ID,
            'client_secret': Settings.CLIENT_SECRET,
            'scope': Settings.SCOPE,
            'grant_type': 'client_credentials'        
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json().get('access_token')
    
    def send_message(self, user_id: str, message: str):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        # Cria um chat 1:1 entre o app e o usuário
        create_chat_url = f"{Settings.GRAPH_API_ENDPOINT}/chats"
        chat_data = {
            "chatType": "oneOnOne",
            "members": [
                {
                    "@odata.type": "#microsoft.graph.aadUserConversationMember",
                    "roles": ["owner"],
                    "user@odata.bind": f"{Settings.GRAPH_API_ENDPOINT}/users('{user_id}')"
                }
            ]
        }
        create_chat_response = requests.post(create_chat_url, headers=headers, json=chat_data)
        create_chat_response.raise_for_status()
        chat_id = create_chat_response.json().get('id')

        message_url = f"{Settings.GRAPH_API_ENDPOINT}/chats/{chat_id}/messages"
        message_data = {
            "body": {
                "content": message
            }
        }
        message_response = requests.post(message_url, headers=headers, json=message_data)
        message_response.raise_for_status()
        return message_response.json()