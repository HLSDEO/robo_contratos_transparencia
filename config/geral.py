from datetime import datetime
import re
from dateutil.relativedelta import relativedelta
import glob
import pandas as pd
from .log import *
import os

def consolidar_por_uasg(prefixo, log):
    """
    Consolida arquivos CSV por Unidade Gestora (UASG)

    Ex:
    contratos_*.csv → contratos_200352.csv
    """

    arquivos = glob.glob(f'files/{prefixo}_*.csv')

    if not arquivos:
        log.warning(f'Nenhum arquivo encontrado para {prefixo}')
        return

    dfs = []

    for arq in arquivos:
        try:
            df = pd.read_csv(arq, sep=';', dtype=str)
            dfs.append(df)
        except Exception as e:
            log.error(f'Erro ao ler {arq}: {e}')

    if not dfs:
        return

    df_total = pd.concat(dfs, ignore_index=True)

    if 'Unidade Gestora' not in df_total.columns:
        log.error(f'Coluna "Unidade Gestora" não encontrada em {prefixo}')
        return

    # normaliza UASG (somente números)
    df_total['Unidade Gestora'] = df_total['Unidade Gestora'].str.replace(r'\D', '', regex=True)

    # agrupa por UASG
    for uasg, grupo in df_total.groupby('Unidade Gestora'):
        if not uasg or uasg == 'nan':
            continue

        arquivo_saida = f'files/{prefixo}_{uasg}_final.csv'

        grupo.to_csv(
            arquivo_saida,
            sep=';',
            index=False,
            encoding='utf-8-sig'
        )

        log.success(f'Gerado: {arquivo_saida}')

def remover_fragmentados(log):
    """
    Remove arquivos fragmentados do tipo:
    contratos_*.csv, itens_*.csv, etc

    Mantém apenas o arquivo consolidado.
    """
    arquivos = glob.glob(f'files/*.csv')
    for arquivo in arquivos:
        # NÃO apaga o consolidado
        if 'final' in arquivo:
            continue
        try:
            os.remove(arquivo)
            log.info(f'Arquivo removido: {arquivo}')
        except Exception as e:
            log.error(f'Erro ao remover {arquivo}: {e}')

def consolidar_todos():
    tipos = [
        'contratos',
        'historicos',
        'empenhos',
        'faturas',
        'itens',
        'fiscais'
    ]

    identificacao = randint(10,100000000)
    log = base_logger.bind(id=identificacao, unidade='GERAL')

    for tipo in tipos:
        consolidar_por_uasg(tipo, log)

    remover_fragmentados(log)
        

def gerar_intervalos_trimestrais(data_inicio, data_limite):
    """
    Retorna uma lista de intervalos de datas de 3 em 3 meses.
    """
    intervalos = []
    atual = data_inicio

    while atual < data_limite:
        fim = atual + relativedelta(months=3) - relativedelta(days=1)

        if fim > data_limite:
            fim = data_limite

        intervalos.append((
            atual.strftime('%Y-%m-%d'),
            fim.strftime('%Y-%m-%d')
        ))

        atual += relativedelta(months=3)

    return intervalos

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

