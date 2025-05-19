"""
Script para inicializar o servidor Uvicorn para a aplicação FastAPI.
Execute este arquivo para rodar a API localmente.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)