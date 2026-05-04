from datetime import datetime
import re
from dateutil.relativedelta import relativedelta
import glob
import pandas as pd
from .log import *
import os

def consolidar_por_uasg(prefixo, uasg, log):
    """
    Consolida arquivos CSV por tipo + UASG específica

    Ex:
    contratos_*_200352_*.csv → contratos_200352_final.csv
    """

    uasg = re.sub(r'\D', '', str(uasg))

    # pega apenas arquivos daquela UG
    arquivos = glob.glob(f'files/{prefixo}_*{uasg}*.csv')

    # remove possíveis arquivos já consolidados
    arquivos = [a for a in arquivos if '_final' not in a]

    if not arquivos:
        log.warning(f'Nenhum arquivo encontrado para {prefixo} - UASG {uasg}')
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

    arquivo_saida = f'files/{prefixo}_{uasg}_final.csv'

    df_total.to_csv(
        arquivo_saida,
        sep=';',
        index=False,
        encoding='utf-8-sig'
    )

    log.success(f'Gerado: {arquivo_saida}')

def remover_fragmentados(log):
    """
    Remove arquivos fragmentados (mantém apenas *_final.csv)
    """
    arquivos = glob.glob('files/*.csv')

    for arquivo in arquivos:
        if '_final' in arquivo:
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

    # DESCOBRIR TODAS AS UASGs EXISTENTES
    arquivos = glob.glob('files/contratos_*.csv')

    uasgs = set()

    for arq in arquivos:
        # ignora já consolidados
        if '_final' in arq:
            continue

        try:
            df = pd.read_csv(arq, sep=';', dtype=str)

            if 'Unidade Gestora' not in df.columns:
                continue

            df['Unidade Gestora'] = df['Unidade Gestora'].str.replace(r'\D', '', regex=True)

            uasgs.update(
                df['Unidade Gestora']
                .dropna()
                .unique()
            )

        except Exception as e:
            log.error(f'Erro ao identificar UASG em {arq}: {e}')

    if not uasgs:
        log.warning('Nenhuma UASG encontrada para consolidação')
        return

    # CONSOLIDA POR (TIPO + UASG)
    for uasg in uasgs:
        for tipo in tipos:
            consolidar_por_uasg(tipo, uasg, log)

    # 🧹 REMOVE FRAGMENTADOS
    remover_fragmentados(log)

    log.success('Consolidação final concluída')     

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

