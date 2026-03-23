from config.csv import *
from config.log import *
from config.parametros import *
from config.selenium import *
from xpath import *

# PRIMEIRA TASK
abrir_site(SITE.format(UNIDADE='200334'))

# AGUARDAR CARREGAMENTO DA TABELA
sleep(5)

pagina_atual = 1
while True:
    logger.info(f'Processando página {pagina_atual}')

    quantidade_linhas = contar_elementos(xpath_tabela_contratos)

    for i in range(1, quantidade_linhas + 1):

        clicar_no_elemento(xpath_detalhar_contrato.format(numero=i), nova_janela=True)

        xpath_texto_unidade_gestora = '/html/body/div[2]/div/section[2]/div/div/div/div/table/tbody/tr[2]/td[2]'
        texto = esperar_texto(xpath_texto_unidade_gestora)

        if str(texto) == 'False':
            break

        # GERA OS XPATHS CONFORME A EXISTENCIA DO LINK OU NÃO
        tem_link_pncp = (buscar_elemento(xpath_link_pncp, 1) != False)
        offset = 0 if tem_link_pncp else -1
        unidade_gestora      = buscar_elemento(xpath_texto_unidade_gestora).text
        unidade_gestora      = re.sub(r'\D', '', unidade_gestora)
        numero_contrato      = buscar_elemento(xpath_tr(XPATH_BASE_DETALHES, 6, offset=0)).text 
        numero_edital        = buscar_elemento(xpath_tr(XPATH_BASE_DETALHES, 9, offset=offset)).text
        modalidade_edital    = buscar_elemento(xpath_tr(XPATH_BASE_DETALHES, 10, offset=offset)).text
        texto_fornecedor     = buscar_elemento(xpath_tr(XPATH_BASE_DETALHES, 16, offset=offset)).text
        documento_fornecedor = texto_fornecedor.split(" - ", 1)[0]
        try:
            fornecedor           = texto_fornecedor.split(" - ", 1)[1]
        except:
            fornecedor = texto_fornecedor
        num_sei              = buscar_elemento(xpath_tr(XPATH_BASE_DETALHES, 17, offset=offset)).text
        objeto               = buscar_elemento(xpath_tr(XPATH_BASE_DETALHES, 18, offset=offset)).text
        objeto_complementar  = buscar_elemento(xpath_tr(XPATH_BASE_DETALHES, 19, offset=offset)).text
        vigencia_inicio      = buscar_elemento(xpath_tr(XPATH_BASE_DETALHES, 20, offset=offset)).text
        vigencia_fim         = buscar_elemento(xpath_tr(XPATH_BASE_DETALHES, 21, offset=offset)).text
        valor_global         = buscar_elemento(xpath_tr(XPATH_BASE_DETALHES, 22, offset=offset)).text

        tabela_historico = capturar_tabela(xpath_tr(XPATH_BASE_DETALHES, 27, offset=offset, sufixo="/td[2]/span/table"))
        tabela_empenho   = capturar_tabela(xpath_tr(XPATH_BASE_DETALHES, 29, offset=offset, sufixo="/td[2]/span/table"))
        tabela_faturas   = capturar_tabela(xpath_tr(XPATH_BASE_DETALHES, 30, offset=offset, sufixo="/td[2]/span/table"))
        tabela_itens     = capturar_tabela(xpath_tr(XPATH_BASE_DETALHES, 32, offset=offset, sufixo="/td[2]/span/table"))
        tabela_fiscais   = capturar_tabela(xpath_tr(XPATH_BASE_DETALHES, 34, offset=offset, sufixo="/td[2]/span/table"))
    
        if tem_link_pncp:
            link_pncp           = buscar_elemento(xpath_link_pncp).get_property('href')
            resultado           = clicar_no_elemento(xpath_link_pncp, nova_janela=True)

            ## NA PÁGINA DO PNCP
            id_contratacao_pncp     = buscar_elemento(xpath_id_contratacao_pncp).text
            id_contrato_pncp        = buscar_elemento(xpath_id_contrato_pncp).text
            texto_tipo_pessoa_fornecedor  = buscar_elemento(xpath_tipo_pessoa_fornecedor).text
            if texto_tipo_pessoa_fornecedor == 'Pessoa jurídica':
                tipo_pessoa_fornecedor = 'PJ'
            elif texto_tipo_pessoa_fornecedor == 'Pessoa física':
                tipo_pessoa_fornecedor = 'PF'
            else:
                tipo_pessoa_fornecedor = 'PE'
            fechar_nova_aba(indice=1)
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
            'files/contratos.csv',
            lista_contratos,
            cabecalho=cabecalho_contratos
        )

        escrever_tabela_csv(
            arquivo="files/historicos.csv",
            linhas_tabela=tabela_historico,
            identificadores={"ID Contrato_PNCP":id_contrato_pncp, "CNPJ_fornecedor": documento_fornecedor}
        )

        escrever_tabela_csv(
            arquivo="files/empenhos.csv",
            linhas_tabela=tabela_empenho,
            identificadores={"ID Contrato_PNCP":id_contrato_pncp, "CNPJ_fornecedor": documento_fornecedor}
        )

        escrever_tabela_csv(
            arquivo="files/faturas.csv",
            linhas_tabela=tabela_faturas,
            identificadores={"ID Contrato_PNCP":id_contrato_pncp, "CNPJ_fornecedor": documento_fornecedor}
        )

        escrever_tabela_csv(
            arquivo="files/itens.csv",
            linhas_tabela=tabela_itens,
            identificadores={"ID Contrato_PNCP":id_contrato_pncp, "CNPJ_fornecedor": documento_fornecedor}
        )

        escrever_tabela_csv(
            arquivo="files/fiscais.csv",
            linhas_tabela=tabela_fiscais,
            identificadores={"ID Contrato_PNCP":id_contrato_pncp, "CNPJ_fornecedor": documento_fornecedor}
        )

        logger.info(f'contrato {numero_contrato}/{unidade_gestora} - fornecedor: {documento_fornecedor}')

        fechar_nova_aba()

    ## PRÓXIMA PAGÍNA?
    if buscar_elemento("//li[@id='crudTable_next' and not(contains(@class,'disabled'))]/a") != False:
        clicar_no_elemento("//li[@id='crudTable_next']/a")
        pagina_atual += 1
    else:
        logger.success('Última página processada.')
        break