
## XPATHS DE NAVEGAÇÃO
xpath_detalhar_contrato = '//*[@id="crudTable"]/tbody/tr[{numero}]/td[10]/a'
xpath_tabela_contratos = '//*[@id="crudTable"]/tbody/tr'
xpath_btn_paginacao = "//li[@id='crudTable_next' and not(contains(@class,'disabled'))]/a"

# TEXTOS – DETALHES DO CONTRATO
XPATH_BASE_DETALHES = '/html/body/div[2]/div/section[2]/div/div/div/div/table/tbody'
xpath_link_pncp                  = f'{XPATH_BASE_DETALHES}/tr[7]/td[2]/span/a'

# PÁGINA DO PNCP
xpath_id_contratacao_pncp        = '//*[@id="main-content"]/pncp-item-detail/div/div[7]/div[3]/p/a'
xpath_id_contrato_pncp           = '//*[@id="main-content"]/pncp-item-detail/div/div[7]/div[1]/p/span'
xpath_tipo_pessoa_fornecedor     = '//*[@id="main-content"]/pncp-item-detail/div/div[9]/div[2]/div/div/div[1]/p[2]/span'