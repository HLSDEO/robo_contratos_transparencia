from loguru import logger
from random import randint
from .parametros import *

ARQUIVO_LOG = "files/log.txt"
IDENTIFICACAO = randint(10,100000000)

logger.add(ARQUIVO_LOG, format="{time:DD/MM/YYYY HH:mm:ss} | {level} | {extra[ambiente]} | {extra[id]} | {message}")
logger = logger.bind(id=IDENTIFICACAO)
logger = logger.bind(ambiente=AMBIENTE)