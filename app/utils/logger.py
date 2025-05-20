"""
Configura o logger para a aplicação Teams API.
Utiliza python-json-logger para formatação estruturada dos logs.
"""
import logging
from pythonjsonlogger import jsonlogger
 
logger = logging.getLogger("teams_api")
logger.setLevel(logging.INFO)
 
log_handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(message)s %(name)s %(pathname)s %(lineno)d'
)
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)