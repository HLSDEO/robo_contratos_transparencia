SITE = "https://contratos.comprasnet.gov.br/transparencia/contratos?orgao=%5B%2230108%22%5D&unidade={UNIDADE}&vigencia_fim=%7B%22from%22%3A%22{FIM_INICIO}%22%2C%22to%22%3A%22{FIM_FINAL}%22%7D&vigencia_inicio=%7B%22from%22%3A%222020-01-01%22%2C%22to%22%3A%222060-01-01%22%7D"
TEMPO_ESPERA = 5 # em segundos
AMBIENTE = "prod" # dev #prod
QUANTIDADE_MULTITASK_POR_UG = 3  # ajuste conforme CPU/RAM
MAX_UASG_THREADS = 10

unidades_uasg = {
    "CAOP/CGAP/DIREX/PF": 200432,
    "CGAD/DLOG/PF": 200334,
    "CGOF/DLOG/PF": 200336,
    "DCI/PF": 200434,
    "DIP/PF": 200430,
    "DIREN-ANP/PF": 200340,
    "DITEC/PF": 200406,
    "DPF/CAS/SP": 200416,
    "DPF/FIG/PR": 200366,
    "DPF/LDA/PR": 200368,
    "DPF/STS/SP": 200362,
    "DTI/PF": 200342,
    "SR/PF/AC": 200380,
    "SR/PF/AL": 200358,
    "SR/PF/AM": 200382,
    "SR/PF/AP": 200402,
    "SR/PF/BA": 200346,
    "SR/PF/CE": 200392,
    "SR/PF/DF": 200338,
    "SR/PF/ES": 200352,
    "SR/PF/GO": 200376,
    "SR/PF/MA": 200388,
    "SR/PF/MG": 200350,
    "SR/PF/MS": 200354,
    "SR/PF/MT": 200374,
    "SR/PF/PA": 200386,
    "SR/PF/PB": 200396,
    "SR/PF/PE": 200398,
    "SR/PF/PI": 200390,
    "SR/PF/PR": 200364,
    "SR/PF/RJ": 200356,
    "SR/PF/RN": 200394,
    "SR/PF/RO": 200378,
    "SR/PF/RR": 200384,
    "SR/PF/RS": 200372,
    "SR/PF/SC": 200370,
    "SR/PF/SE": 200344,
    "SR/PF/SP": 200360,
    "SR/PF/TO": 200404
}