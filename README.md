# Robô de Contratos - Transparência

## 1 - Sobre
Robô de coleta de dados de contratos do portal [Comprasnet Transparência](https://contratos.comprasnet.gov.br/transparencia/contratos). Navega pelas páginas de contratos de uma unidade gestora, acessa o detalhe de cada contrato e extrai informações como dados gerais, histórico, empenhos, faturas, itens e fiscais, salvando tudo em arquivos CSV.

## 2 - Tecnologias Utilizadas
- Python 3.9+
- Selenium
- ChromeDriverManager
- Loguru

## 3 - Instalação
Requer Python 3.9 ou superior e Google Chrome instalados.

```bash
pip install -r requirements.txt
```

## 4 - Configurações
As configurações estão no arquivo `config/parametros.py`.

| Variável | Descrição |
|---|---|
| `SITE` | URL do portal com parâmetros de filtro (unidade gestora, vigência) |
| `TEMPO_ESPERA` | Tempo de espera padrão (em segundos) para o ChromeDriver |
| `AMBIENTE` | `dev` para testes locais ou `prod` para execução em produção |

## 5 - Organização das pastas
```
├── config/
│   ├── csv.py         # Funções para escrita de arquivos CSV
│   ├── geral.py       # Funções gerais auxiliares
│   ├── log.py         # Configuração do logger (Loguru)
│   ├── parametros.py  # Parâmetros de execução
│   └── selenium.py    # Funções de automação com Selenium
├── files/
│   ├── contratos.csv  # Dados principais dos contratos
│   ├── empenhos.csv   # Tabela de empenhos por contrato
│   ├── faturas.csv    # Tabela de faturas por contrato
│   ├── fiscais.csv    # Tabela de fiscais por contrato
│   ├── historicos.csv # Tabela de histórico por contrato
│   ├── itens.csv      # Tabela de itens por contrato
│   └── log.txt        # Log gerado na execução
├── main.py            # Fluxo principal de execução
├── xpath.py           # XPaths utilizados na navegação
└── requirements.txt   # Dependências do projeto
```

## 6 - Execução

```bash
python main.py
```