import csv

#Nome dos arquivos
csvTerminais = "Sintatico/Tabela Sintática - Terminais.csv"
csvNaoTerminais = "Sintatico/Tabela Sintática - Não-Terminais.csv"
csvQtdSimbolos = "Sintatico/Tabela Sintática - qtd_SimbolosB.csv"
csvModoPanico = "Sintatico/Tabela Sintática - Pânico.csv"

#Abre arquivo csvFile, o csv recebido como parametro, e preenche a lista de dicionários
def preencheTabela(csvFile):
    tabela = []
    with open(csvFile) as fT:
        rd = csv.DictReader(fT, delimiter=',') 
        for linha in rd:
            tabela.append(linha)
    return tabela

#Passa o csv da Tabela de Ações(terminais) como argumento para preencheTabela
def preencheTabelaAcoes():
    tabela = preencheTabela(csvTerminais)
    return tabela

#Passa o csv da Tabela de Desvios(não terminais) como argumento para preencheTabela
def preencheTabelaDesvios():
    tabela = preencheTabela(csvNaoTerminais)
    return tabela

#Passa o csv da Tabela de Quantidade de simbolos para desempilhar como argumento para preencheTabela
def preencheTabelaQtdSimbolos():
    tabela = preencheTabela(csvQtdSimbolos)
    return tabela

#Passa o csv da Tabela do Modo Pânico como argumento para preencheTabela
def preencheTabelaPanico():
    tabela = preencheTabela(csvModoPanico)
    for entrada in tabela:
        if not (entrada['Follow'] == ''):
            lista = entrada['Follow'].split()
            entrada['Follow'] = lista
    return tabela

# #teste
# a = preencheTabelaPanico()
# for entrada in a:
#     if not (entrada['Follow'] == ''):
#         print(entrada)

# s = '4'
# listaFollow = a[int(s)].get('Follow')
# print(listaFollow)