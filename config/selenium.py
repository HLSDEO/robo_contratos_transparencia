# LIB
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# LOCAL
from .parametros import *
from .log import *
from .geral import *

def criar_driver(log):
    log.info("Inicializando Selenium")
    chrome_options = Options()

    if AMBIENTE.strip().lower() == "prod":
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

def buscar_elemento(driver, log, xpath: str, tempo:int=TEMPO_ESPERA):
    """
    Localiza um elemento via XPath, tentando repetidamente até o tempo limite.

    :param xpath: XPath do elemento a ser localizado
    :param tempo: Tempo máximo de espera (em segundos)
    :return: WebElement se encontrado, False caso contrário
    """
    driver.implicitly_wait(tempo)
    for n in range(tempo):
        try:
            return driver.find_element(By.XPATH, xpath)
        except:
            log.debug(f"Não achou o elemento: {xpath}. Tentativa {n+1}/{tempo}")
            sleep(1)
            continue
    return False

def esperar_texto(driver, log, xpath: str, tempo:int = TEMPO_ESPERA):
    """
    Aguarda até que qualquer texto (não vazio) apareça no elemento informado.

    Útil para conteúdos carregados via AJAX/JS (APEX, DataTables, etc).

    :param xpath: XPath do elemento
    :param tempo: Tempo máximo de espera (em segundos)
    :return: Texto encontrado (innerText) ou False em caso de timeout
    """
    driver.implicitly_wait(tempo)
    for n in range(tempo):
        try:
            elemento = driver.find_element(By.XPATH, xpath)
            texto_atual = elemento.get_attribute("innerText")

            if texto_atual and texto_atual.strip():
                return texto_atual  # retorna o texto encontrado
        except:
            log.debug(f"Aguardando qualquer texto em {xpath}. Tentativa {n+1}/{tempo}")
            sleep(1)
            continue
    return False

def contar_elementos(driver, log, xpath: str, tempo:int=TEMPO_ESPERA):
    """
    Conta quantos elementos existem para um determinado XPath.

    :param xpath: XPath a ser contado
    :param tempo: Tempo máximo de espera (em segundos)
    :return: Quantidade de elementos encontrados ou False
    """
    driver.implicitly_wait(tempo)
    for n in range(tempo):
        try:
            return len(driver.find_elements(By.XPATH, xpath))
        except:
            log.debug(f"Não achou o elemento: {xpath}. Iniciando nova tentativa.")
            sleep(1)
            continue
    return False

def abrir_site(driver, log, site: str, tempo:int=TEMPO_ESPERA) -> bool:
    """
    Abre um site no navegador e ajusta a janela.

    :param site: URL do site
    :param tempo: Tempo de espera implícito após abertura
    :return: True se o site abrir corretamente, False caso contrário
    """
    try:
        driver.get(site)
        driver.implicitly_wait(tempo)
        driver.minimize_window()
        driver.maximize_window()
        sleep(1)
        return True
    except:
        log.critical("Falha ao abrir o site")
        return False

def selecionar_iframe(driver, log, xpath:str) -> bool:
    """
    Retorna ao contexto principal e seleciona um iframe pelo XPath.

    :param xpath: XPath do iframe
    :return: True se o iframe for selecionado, False em caso de erro
    """
    try:
        driver.switch_to.default_content()
        iframe = buscar_elemento(driver, log, xpath)
        driver.switch_to.frame(iframe)
        return True
    except:
        log.critical("Falha ao selecionar o elemento")
        return False
    
def escrever_no_elemento(driver, log, xpath: str, texto: str) -> bool:
    """
    Escreve texto em um campo identificado pelo XPath.

    :param xpath: XPath do campo
    :param texto: Texto a ser digitado
    :return: True se a escrita ocorrer com sucesso, False caso contrário
    """
    try:    
        elemento = buscar_elemento(driver, log, xpath)
        if(elemento != False):
            elemento.send_keys(texto)
            return True
    except:
        log.error(f"Falha ao selecionar o elemento: {xpath}")
        return False

def clicar_no_elemento(driver, log, xpath: str, nova_janela: bool = False) -> bool:
    """
    Clica no elemento identificado pelo XPath, com a possibilidade de abrir uma nova janela ou não.

    :param xpath: XPath do campo
    :param nova_janela: BOOL
    :return: True se a escrita ocorrer com sucesso, False caso contrário
    """
    try:
        elemento = buscar_elemento(driver, log,xpath)
        if elemento is False:
            raise

        janelas_antes = driver.window_handles

        if nova_janela:
            href = elemento.get_attribute("href")
            if href:
                driver.execute_script(
                    "window.open(arguments[0], '_blank');", href
                )
            else:
                # fallback JS click
                driver.execute_script("arguments[0].click();", elemento)
        else:
            driver.execute_script("arguments[0].click();", elemento)

        if nova_janela:
            for _ in range(10):
                if len(driver.window_handles) > len(janelas_antes):
                    driver.switch_to.window(driver.window_handles[-1])
                    return True
                sleep(0.5)

            log.warning("Nova aba não foi aberta.")

        return True

    except Exception as e:
        log.error(f"Falha ao clicar no elemento {xpath}: {e}")
        return False
    
def fechar_nova_aba(driver, log, indice=0) -> None:
    """
    Fecha a aba/janela atual e retorna para a janela principal.
    Pressupõe que a janela principal seja a primeira da lista.

    :param indice: number do indice da janela que ficará ativa
    """
    try:
        janelas = driver.window_handles
        driver.close()
        driver.switch_to.window(janelas[indice])
        driver.switch_to.default_content()
    except Exception as e:
        log.error(f"Erro ao fechar a nova aba e voltar para a principal: {e}")


def obter_valor_campo_selecao(driver, log, xpath: str):
    """
    Obtém o texto da opção atualmente selecionada em um <select>.

    :param xpath: XPath do campo de seleção
    :return: Texto da opção selecionada ou False
    """
    try:    
        elemento = Select(buscar_elemento(driver, log, xpath))
        return elemento.first_selected_option.text
    except:
        log.error(f"Falha ao obter o valor do elemento: {xpath}")
        return False

def selecionar_campo_selecao_por_valor(driver, log, xpath: str, texto: str) -> bool:
    """
    Seleciona uma opção de um <select> pelo atributo value.

    :param xpath: XPath do campo de seleção
    :param texto: Valor (value) da opção
    :return: True se selecionado com sucesso, False caso contrário
    """
    try:    
        elemento = Select(buscar_elemento(driver, log, xpath))
        elemento.select_by_value(texto)
        return True
    except:
        log.error(f"Falha ao selecionar o campo de seleção - elemento: {xpath}")
        return False

def selecionar_campo_selecao_por_indice(driver, log, xpath: str, indice: int) -> bool:
    """
    Seleciona uma opção de um <select> pelo índice.

    :param xpath: XPath do campo de seleção
    :param indice: Índice da opção
    :return: True se selecionado com sucesso, False caso contrário
    """
    try:    
        elemento = Select(buscar_elemento(driver, log, xpath))
        elemento.select_by_index(indice)
        return True
    except:
        log.error(f"Falha ao selecionar o campo de seleção - elemento: {xpath}")
        return False

def selecionar_campo_selecao_por_texto_visivel(driver, log, xpath: str, texto: str) -> bool:
    """
    Seleciona uma opção de um <select> pelo texto visível.

    :param xpath: XPath do campo de seleção
    :param texto: Texto visível da opção
    :return: True se selecionado com sucesso, False caso contrário
    """
    try:    
        elemento = Select(buscar_elemento(driver, log, xpath))
        elemento.select_by_visible_text(texto)
        return True
    except:
        log.error(f"Falha ao selecionar o campo de seleção - elemento: {xpath}")
        return False

def capturar_tabela(driver, log, xpath_tabela: str, tempo: int = TEMPO_ESPERA, usar_header_como_chave: bool = True):
    """
    Captura uma tabela HTML e devolve uma lista de dicts (um dict por linha).

    Exemplo de retorno:
    [
      {"Data Assinatura": "14/05/2025", "Número": "00017/2025", ...},
      {"Data Assinatura": "...", ...},
    ]

    Se usar_header_como_chave=False, retorna:
    [
      {"col1": "...", "col2": "..."},
      ...
    ]
    """
    try:
        tabela = buscar_elemento(driver, log, xpath_tabela, tempo)
        if tabela is False:
            return False

        # headers
        ths = tabela.find_elements(By.XPATH, ".//thead//th")
        headers = [limpar_texto(th.get_attribute("innerText")) for th in ths]
        headers = [h if h else f"col{idx+1}" for idx, h in enumerate(headers)]

        # linhas do body
        trs = tabela.find_elements(By.XPATH, ".//tbody/tr")
        resultado = []

        for tr in trs:
            tds = tr.find_elements(By.XPATH, "./td")
            valores = [limpar_texto(td.get_attribute("innerText")) for td in tds]

            # ajusta tamanhos (caso HTML venha inconsistente)
            if len(valores) < len(headers):
                valores += [""] * (len(headers) - len(valores))
            elif len(valores) > len(headers):
                # se tiver td a mais, cria nomes extras
                for i in range(len(headers), len(valores)):
                    headers.append(f"col{i+1}")

            if usar_header_como_chave:
                linha = {headers[i]: valores[i] for i in range(len(headers))}
            else:
                linha = {f"col{i+1}": valores[i] for i in range(len(valores))}

            # ignora linha totalmente vazia
            if any(v.strip() for v in linha.values()):
                resultado.append(linha)

        return resultado

    except Exception as e:
        log.error(f"Erro ao capturar tabela {xpath_tabela}: {e}")
        return False