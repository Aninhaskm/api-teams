from fastapi import FastAPI
from app.routes import message_routes

# Inicializa o FastAPI
app = FastAPI()

# Inclui as rotas definidas no arquivo message_routes.py
app.include_router(message_routes.router)



