"""
Arquivo principal da aplicação FastAPI.
Responsável por inicializar o app, configurar middlewares e incluir rotas.
"""
# Middlewares: usado para registrar logs de todas as requisições recebidas e respostas enviadas, além de capturar e registrar exceções.
# Permite adicionar funcionalidades como autenticação, logging, tratamento de erros e manipulação de cabeçalhos de forma centralizada, sem precisar repetir código em cada rota. 
from fastapi import FastAPI, Request
from app.routes import message_routes
from app.utils.logger import logger 

# Inicializa o FastAPI
app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("Requisição recebida", extra={
        "method": request.method,
        "url": str(request.url)
    })
    try:
        response = await call_next(request)

        logger.info("Resposta enviada", extra={
            "status_code": response.status_code,
            "method": request.method, 
            "url": str(request.url)
        })

        return response
    except Exception as e: 
        logger.exception("Erro durante processamento da requisição")
        raise e

# Inclui as rotas definidas no arquivo message_routes.py
app.include_router(message_routes.router)



