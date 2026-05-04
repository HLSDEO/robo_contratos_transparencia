from loguru import logger
from .parametros import *
from random import randint

ARQUIVO_LOG = "files/log.txt"

logger.remove()

logger.add(
    ARQUIVO_LOG,
    format="{time:DD/MM/YYYY HH:mm:ss} | {level} | {extra[ambiente]} | {extra[unidade]} | {extra[id]} | {message}",
)

base_logger = logger.bind(
    ambiente=AMBIENTE,
    unidade="-",
    id="-"
)