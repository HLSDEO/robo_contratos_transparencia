import csv
import os
from .log import *
from typing import Any

def escrever_linha_csv(
    arquivo: str,
    conteudo: list,
    cabecalho: list | None = None,
    codificacao: str = "utf-8-sig",
    log=None
) -> bool:
    """
    Escreve uma linha em um arquivo CSV, com opção de escrever o cabeçalho
    automaticamente na primeira criação do arquivo.

    :param arquivo: Caminho do arquivo CSV
    :param conteudo: Lista com os valores da linha a ser escrita
    :param cabecalho: Lista opcional com os nomes das colunas
                      (escrito apenas se o arquivo não existir)
    :param codificacao: Codificação do arquivo (default: utf-8)
    :return: True se a escrita ocorrer com sucesso, False em caso de erro
    """
    try:
        arquivo_existe = os.path.isfile(arquivo)
        escrever_cabecalho = cabecalho is not None and not arquivo_existe

        with open(arquivo, 'a+', newline='', encoding=codificacao) as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL)

            if escrever_cabecalho:
                writer.writerow(cabecalho)

            writer.writerow(conteudo)

        return True

    except Exception as e:
        log.error(f"Erro ao escrever CSV ({arquivo}): {e}")
        return False

def escrever_tabela_csv(
    arquivo: str,
    linhas_tabela: list[dict[str, Any]],
    identificadores: dict[str, Any],
    codificacao: str = "utf-8-sig",
    delimiter: str = ";",
    log=None
) -> bool:
    """
    Escreve no CSV as linhas (dicts), adicionando múltiplas colunas identificadoras à ESQUERDA.

    - identificadores: dict com {nome_coluna: valor}
      Ex: {"ID_CONTRATO": "X", "ID_FORNECEDOR": "Y"}
    """
    try:
        if not linhas_tabela:
            return True

        arquivo_existe = os.path.isfile(arquivo)
        modo = "a+"

        # começa com as chaves da primeira linha
        headers: list[str] = list(linhas_tabela[0].keys())

        # adiciona chaves novas na ordem em que aparecem
        vistos = set(headers)
        for linha in linhas_tabela[1:]:
            for k in linha.keys():
                if k not in vistos:
                    headers.append(k)
                    vistos.add(k)

        # remove identificadores se existirem no payload
        for col_id in identificadores.keys():
            headers = [h for h in headers if h != col_id]

        # identificadores sempre à esquerda (na ordem do dict)
        headers = list(identificadores.keys()) + headers

        escrever_cabecalho = not arquivo_existe

        with open(arquivo, modo, newline="", encoding=codificacao) as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter, quoting=csv.QUOTE_ALL)

            if escrever_cabecalho:
                writer.writerow(headers)

            for linha in linhas_tabela:
                row = []

                # valores dos identificadores
                for col_id in identificadores.keys():
                    v = identificadores.get(col_id, "")
                    row.append("" if v is None else str(v))

                # valores da linha da tabela
                for h in headers[len(identificadores):]:
                    v = linha.get(h, "")
                    row.append("" if v is None else str(v))

                writer.writerow(row)

        return True

    except Exception as e:
        log.error(f"Erro ao escrever tabela CSV ({arquivo}): {e}")
        return False

def carregar_csv(arquivo: str, delimitador:str, log=None):
    """
    Carrega um arquivo CSV e retorna um reader para iteração linha a linha.

    :param arquivo: Caminho do arquivo CSV
    :param delimitador: Delimitador utilizado no CSV (ex: ',' ou ';')
    :return: Objeto csv.reader em caso de sucesso, False em caso de erro
    """
    try:
        with open(arquivo, newline='') as csvfile:
            conteudo = csv.reader(csvfile, delimiter=delimitador)
            return conteudo
    except Exception as e:
        if log:
            log.error(f"Erro ao carregar CSV ({arquivo}): {e}")
        return False