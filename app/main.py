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



