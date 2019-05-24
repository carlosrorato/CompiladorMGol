import csv

csvTerminais = "Tabela Sintática - Terminais.csv"
csvNaoTerminais = "Tabela Sintática - Não-Terminais.csv"

tabelaAcoes = []
tabelaDesvios = []

#Abre arquivo csv da Tabela de Ações(Terminais) e preenche a lista de dicionários tabelaAcoes
with open(csvTerminais) as fT:
    rd = csv.DictReader(fT, delimiter=',') 
    for linha in rd:
        print(linha)
        print()
        tabelaAcoes.append(linha)

#Abre arquivo csv da Tabela de Desvios(Não-Terminais) e preenche a lista de dicionários tabelaDesvios
with open(csvNaoTerminais) as fNT:
    rd = csv.DictReader(fNT, delimiter=',') 
    for linha in rd:
        print(linha)
        print()
        tabelaDesvios.append(linha)
