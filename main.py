from config.csv import *
from config.log import *
from config.parametros import *
from config.selenium import *
from config.geral import *
from xpath import *
from concurrent.futures import ThreadPoolExecutor, as_completed

def executar_consulta(unidade, data_inicio, data_fim, log):
    """
    Faz a consulta no site do contratos e faz a raspagem dos dados.
    """
    log.info(f'Iniciando: {unidade} | {data_inicio} até {data_fim}')

    driver = criar_driver(log)

    try:

        # nomes únicos por task
        sufixo = f"{unidade}_{data_inicio}_{data_fim}".replace("/", "-")
        arquivo_contratos = f'files/contratos_{sufixo}.csv'
        arquivo_historico = f'files/historicos_{sufixo}.csv'
        arquivo_empenho   = f'files/empenhos_{sufixo}.csv'
        arquivo_faturas   = f'files/faturas_{sufixo}.csv'
        arquivo_itens     = f'files/itens_{sufixo}.csv'
        arquivo_fiscais   = f'files/fiscais_{sufixo}.csv'

        # PRIMEIRA TASK
        abrir_site(driver, log, SITE.format(UNIDADE=unidade, FIM_INICIO=data_inicio, FIM_FINAL=data_fim))

        # AGUARDAR CARREGAMENTO DA TABELA
        sleep(5)

        pagina_atual = 1
        while True:
            log.info(f'Processando página {pagina_atual}')

            quantidade_linhas = contar_elementos(driver, log, xpath_tabela_contratos)

            for i in range(1, quantidade_linhas + 1):

                clicar_no_elemento(driver, log, xpath_detalhar_contrato.format(numero=i), nova_janela=True)

                xpath_texto_unidade_gestora = '/html/body/div[2]/div/section[2]/div/div/div/div/table/tbody/tr[2]/td[2]'
                texto = esperar_texto(driver, log,xpath_texto_unidade_gestora)

                if str(texto) == 'False':
                    break

                # GERA OS XPATHS CONFORME A EXISTENCIA DO LINK OU NÃO
                tem_link_pncp = (buscar_elemento(driver, log, xpath_link_pncp, 1) != False)
                offset = 0 if tem_link_pncp else -1
                unidade_gestora      = buscar_elemento(driver, log, xpath_texto_unidade_gestora).text
                unidade_gestora      = re.sub(r'\D', '', unidade_gestora)
                numero_contrato      = buscar_elemento(driver, log, xpath_tr(XPATH_BASE_DETALHES, 6, offset=0)).text 
                numero_edital        = buscar_elemento(driver, log, xpath_tr(XPATH_BASE_DETALHES, 9, offset=offset)).text
                modalidade_edital    = buscar_elemento(driver, log, xpath_tr(XPATH_BASE_DETALHES, 10, offset=offset)).text
                texto_fornecedor     = buscar_elemento(driver, log, xpath_tr(XPATH_BASE_DETALHES, 16, offset=offset)).text
                documento_fornecedor = texto_fornecedor.split(" - ", 1)[0]
                try:
                    fornecedor = texto_fornecedor.split(" - ", 1)[1]
                except:
                    fornecedor = texto_fornecedor
                num_sei              = buscar_elemento(driver, log, xpath_tr(XPATH_BASE_DETALHES, 17, offset=offset)).text
                objeto               = buscar_elemento(driver, log, xpath_tr(XPATH_BASE_DETALHES, 18, offset=offset)).text
                objeto_complementar  = buscar_elemento(driver, log, xpath_tr(XPATH_BASE_DETALHES, 19, offset=offset)).text
                vigencia_inicio      = buscar_elemento(driver, log, xpath_tr(XPATH_BASE_DETALHES, 20, offset=offset)).text
                vigencia_fim         = buscar_elemento(driver, log, xpath_tr(XPATH_BASE_DETALHES, 21, offset=offset)).text
                valor_global         = buscar_elemento(driver, log, xpath_tr(XPATH_BASE_DETALHES, 22, offset=offset)).text

                tabela_historico = capturar_tabela(driver, log, xpath_tr(XPATH_BASE_DETALHES, 27, offset=offset, sufixo="/td[2]/span/table"))
                tabela_empenho   = capturar_tabela(driver, log, xpath_tr(XPATH_BASE_DETALHES, 29, offset=offset, sufixo="/td[2]/span/table"))
                tabela_faturas   = capturar_tabela(driver, log, xpath_tr(XPATH_BASE_DETALHES, 30, offset=offset, sufixo="/td[2]/span/table"))
                tabela_itens     = capturar_tabela(driver, log, xpath_tr(XPATH_BASE_DETALHES, 32, offset=offset, sufixo="/td[2]/span/table"))
                tabela_fiscais   = capturar_tabela(driver, log, xpath_tr(XPATH_BASE_DETALHES, 34, offset=offset, sufixo="/td[2]/span/table"))
            
                if tem_link_pncp:
                    link_pncp           = buscar_elemento(driver, log, xpath_link_pncp).get_property('href')
                    resultado           = clicar_no_elemento(driver, log, xpath_link_pncp, nova_janela=True)

                    ## NA PÁGINA DO PNCP
                    id_contratacao_pncp     = buscar_elemento(driver, log, xpath_id_contratacao_pncp).text
                    id_contrato_pncp        = buscar_elemento(driver, log, xpath_id_contrato_pncp).text
                    texto_tipo_pessoa_fornecedor  = buscar_elemento(driver, log, xpath_tipo_pessoa_fornecedor).text
                    if texto_tipo_pessoa_fornecedor == 'Pessoa jurídica':
                        tipo_pessoa_fornecedor = 'PJ'
                    elif texto_tipo_pessoa_fornecedor == 'Pessoa física':
                        tipo_pessoa_fornecedor = 'PF'
                    else:
                        tipo_pessoa_fornecedor = 'PE'
                    fechar_nova_aba(driver, log, indice=1)
                else:
                    id_contratacao_pncp = f"{unidade_gestora}-1-{numero_edital}"
                    id_contrato_pncp = f"{unidade_gestora}-{numero_edital}-{numero_contrato}"
                    link_pncp = "#"
                    if re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', documento_fornecedor):
                        tipo_pessoa_fornecedor = 'PJ'
                    elif re.search(r'\d{3}\.\d{3}\.\d{3}-\d{2}', documento_fornecedor):
                        tipo_pessoa_fornecedor = 'PF'
                    else:
                        tipo_pessoa_fornecedor = 'PE'
                
                cabecalho_contratos = [
                    'Unidade Gestora',
                    'Número do Contrato',
                    'Número do Edital',
                    'Modalidade do Edital',
                    'Fornecedor',
                    'Doc. Fornecedor',
                    'Tipo Fornecedor',
                    'Número SEI',
                    'Objeto',
                    'Objeto Complementar',
                    'Vigência Início',
                    'Vigência Fim',
                    'Valor Global',
                    'Link PNCP',
                    'ID Contratacao PNCP',
                    'ID Contrato_PNCP'
                ]

                lista_contratos = [
                    unidade_gestora,
                    numero_contrato,
                    numero_edital,
                    modalidade_edital,
                    fornecedor,
                    documento_fornecedor,
                    tipo_pessoa_fornecedor,
                    num_sei,
                    objeto,
                    objeto_complementar,
                    vigencia_inicio,
                    vigencia_fim,
                    valor_global,
                    link_pncp,
                    id_contratacao_pncp,
                    id_contrato_pncp
                ]

                escrever_linha_csv(
                    arquivo=arquivo_contratos,
                    conteudo=lista_contratos,
                    cabecalho=cabecalho_contratos,
                    log=log
                )

                escrever_tabela_csv(
                    arquivo=arquivo_historico,
                    linhas_tabela=tabela_historico,
                    identificadores={"ID Contrato_PNCP":id_contrato_pncp, "CNPJ_fornecedor": documento_fornecedor},
                    log=log
                )

                escrever_tabela_csv(
                    arquivo=arquivo_empenho,
                    linhas_tabela=tabela_empenho,
                    identificadores={"ID Contrato_PNCP":id_contrato_pncp, "CNPJ_fornecedor": documento_fornecedor},
                    log=log
                )

                escrever_tabela_csv(
                    arquivo=arquivo_faturas,
                    linhas_tabela=tabela_faturas,
                    identificadores={"ID Contrato_PNCP":id_contrato_pncp, "CNPJ_fornecedor": documento_fornecedor},
                    log=log
                )

                escrever_tabela_csv(
                    arquivo=arquivo_itens,
                    linhas_tabela=tabela_itens,
                    identificadores={"ID Contrato_PNCP":id_contrato_pncp, "CNPJ_fornecedor": documento_fornecedor},
                    log=log
                )

                escrever_tabela_csv(
                    arquivo=arquivo_fiscais,
                    linhas_tabela=tabela_fiscais,
                    identificadores={"ID Contrato_PNCP":id_contrato_pncp, "CNPJ_fornecedor": documento_fornecedor},
                    log=log
                )

                log.info(f'contrato {numero_contrato}/{unidade_gestora} - fornecedor: {documento_fornecedor}')

                fechar_nova_aba(driver, log)

            ## PRÓXIMA PAGÍNA?
            if buscar_elemento(driver, log, "//li[@id='crudTable_next' and not(contains(@class,'disabled'))]/a") != False:
                clicar_no_elemento(driver, log, "//li[@id='crudTable_next']/a")
                pagina_atual += 1
            else:
                log.success('Última página processada.')
                break
    except Exception as e:
        log.error(f'Erro na execução: {e}')
    finally:
        driver.quit()

## GERA OS INTERVALOS DE CONSULTA
data_inicio_consulta = datetime.today().replace(day=1)
data_limite_consulta = datetime(2040, 12, 31)
intervalos = gerar_intervalos_trimestrais(data_inicio_consulta, data_limite_consulta)

## CRIA AS CONSULTAS EM MULTITASK POR UNIDADE GESTORA
def executar_multitask(unidade):
    futures = []
    identificacao = randint(10,100000000)
    log = base_logger.bind(id=identificacao, unidade=unidade)

    with ThreadPoolExecutor(max_workers=QUANTIDADE_MULTITASK_POR_UG) as executor:

        for data_inicio, data_fim in intervalos:
            futures.append(
                executor.submit(
                    executar_consulta,
                    unidade,
                    data_inicio,
                    data_fim,
                    log.bind(task=f"{data_inicio}_{data_fim}")
                )
            )

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                log.error(f'Erro na execução: {e}')

## EXECUTA AS CONSULTAS EM MULTITASK POR UNIDADE GESTORA
executar_multitask('200352')

# CONSOLIDAÇÃO FINAL
consolidar_todos()