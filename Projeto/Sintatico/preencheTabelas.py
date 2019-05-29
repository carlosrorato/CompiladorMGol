import csv

#Nome dos arquivos
csvTerminais = "Sintatico/Tabela Sintática - Terminais.csv"
csvNaoTerminais = "Sintatico/Tabela Sintática - Não-Terminais.csv"
csvQtdSimbolos = "Sintatico/Tabela Sintática - qtd_SimbolosB.csv"
csvErros = "Sintatico/Tabela Sintática - Pânico.csv"

#Abre arquivo csvFile, o csv recebido como parametro, e preenche a lista de dicionários
def preencheTabela(csvFile):
    tabela = []
    with open(csvFile) as fT:
        dados = csv.DictReader(fT, delimiter=',') 
        for linha in dados:
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
def preencheTabelaErros():
    tabela = preencheTabela(csvErros)

    # Cria uma lista de símbolos do conjunto seguinte como valor da chave 'Follow' no dicionário que 
    # representa a tabela
    for entrada in tabela:
        if not (entrada['Follow'] == ''):
            lista = entrada['Follow'].split()
            entrada['Follow'] = lista
    return tabela
