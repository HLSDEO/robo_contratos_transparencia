from datetime import datetime
import re

def data_atual():
    return datetime.today().strftime('%d/%m/%Y')

def limpar_texto(s: str) -> str:
    if s is None:
        return ""
    # normaliza espaços e quebras
    return re.sub(r"\s+", " ", s).strip()

def xpath_tr(base: str, n: int, offset: int = 0, sufixo: str = "/td[2]") -> str:
    """
    Retorna um xpath do tipo: {base}/tr[{n+offset}]{sufixo}
    offset pode ser 0 (normal) ou -1 (quando não existe a linha do link PNCP).
    """
    return f"{base}/tr[{n + offset}]{sufixo}"