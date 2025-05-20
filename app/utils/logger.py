"""
Configura o logger da aplicação Teams API.
Formato limpo e em linha única com extras legíveis.
"""
import logging
import sys

# Configura o logger principal
logger = logging.getLogger("API Teams")
logger.setLevel(logging.DEBUG)

# Handler padrão (console)
handler = logging.StreamHandler(sys.stdout)

# Formato customizado (linha única)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s %(name)s | %(message)s '
    '[%(filename)s:%(lineno)d]'
)

handler.setFormatter(formatter)
logger.addHandler(handler)
