# Universidade Federal de Goiás
# Instituto de Informática - INF
# Compiladores - Compilador para MGol
#
# Alunos: Carlos Henrique Rorato Souza
# e Larissa Santos de Azevedo
import string

#Estrutura de dados para a tabela de transição do DFA: matriz de dicionários (hash)
#Tabela_Transicao = []

#Constantes para estados
estadoInicial = 0
estadoNum = 1
estadoNumPonto = 2
estadoNumPontoFinal = 3
estadoNumExpoente1 = 4
estadoNumExpoente2 = 5
estadoNumExpoenteFinal = 6
estadoLiteral = 7
estadoLiteralFinal = 8
estadoId = 9
estadoComentario = 10
estadoComentarioFinal = 11
estadoOPM = 12
#estadoEOF = 13
estadoOPRMenor = 13
estadoRCB = 14
estadoOPRMenorIgualDiferente = 15
estadoOPRMaior = 16
estadoOPRMaiorIgual = 17
estadoOPRIgual = 18
estadoABP = 19
estadoFCP = 20
estadoPTV = 21

#função que preenche a tabela de transição do autômato
def preenche_tabela_dfa(Tabela_Transicao):

    #preenchimento para o estado 0:
    linha = {}
    for c in string.ascii_lowercase:
        linha.update({c:estadoId})
    for c in string.ascii_uppercase:
        linha.update({c: estadoId})
    for c in range(0,10):
        linha.update({str(c):estadoNum})
    linha.update({"\n":estadoInicial , "\_":estadoInicial , "\t": estadoInicial})

    ####python retorna string vazia - read
    #### while 1:
    ####    char = file.read(1)          # read by character
    ####    if not char: break

    linha.update({"final": False})
    linha.update({"\"": estadoLiteral})
    linha.update({"{":estadoComentario})
    linha.update({"<":estadoOPRMenor , ">":estadoOPRMaior , "=":estadoOPRIgual})
    linha.update({"+": estadoOPM, "-": estadoOPM, "*": estadoOPM, "/": estadoOPM})
    linha.update({"(": estadoABP, ")": estadoFCP, ";": estadoPTV})
    Tabela_Transicao.append(linha)

    # preenchimento para o estado 1 - estadoNum:
    linha = {}
    linha.update({"final": True})
    for c in range(0, 10):
        linha.update({str(c): estadoNum})
    linha.update({".": estadoNumPonto, "E": estadoNumExpoente1, "e": estadoNumExpoente1})
    Tabela_Transicao.append(linha)

    # preenchimento para o estado 2 - estadoNumPonto:
    linha = {}
    linha.update({"final": False})
    for c in range(0, 10):
        linha.update({str(c): estadoNumPontoFinal})
    Tabela_Transicao.append(linha)

    # preenchimento para o estado 3 - estadoNumPontoFinal:
    linha = {}
    linha.update({"final": True})
    for c in range(0, 10):
        linha.update({str(c): estadoNumPontoFinal})
    linha.update({"E": estadoNumExpoente1, "e": estadoNumExpoente1})
    Tabela_Transicao.append(linha)

    # preenchimento para o estado 4 - estadoNumExpoente1:
    linha = {}
    linha.update({"final": False})
    for c in range(0, 10):
        linha.update({str(c): estadoNumExpoenteFinal})
    linha.update({"+": estadoNumExpoente2, "-": estadoNumExpoente2})
    Tabela_Transicao.append(linha)

    # preenchimento para o estado 5 - estadoNumExpoente2:
    linha = {}
    linha.update({"final": False})
    for c in range(0, 10):
        linha.update({str(c): estadoNumExpoenteFinal})
    Tabela_Transicao.append(linha)

    # preenchimento para o estado 6 - estadoNumExpoenteFinal:
    linha = {}
    linha.update({"final": True})
    for c in range(0, 10):
        linha.update({str(c): estadoNumExpoenteFinal})
    Tabela_Transicao.append(linha)

    #preenchimento para o estado 7 - estadoLiteral
    linha = {}
    linha.update({"final": False})
    #####Como indicar qqr coisa?#####
    linha.update({"\"": estadoLiteralFinal})
    Tabela_Transicao.append(linha)

    #estado 8 - estadoLiteralFinal
    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    #preenchimento estado 9 - estadoId
    linha = {}
    linha.update({"final": True})
    for c in range(0, 10):
        linha.update({str(c): estadoId})
    for c in string.ascii_lowercase:
        linha.update({c:estadoId})
    for c in string.ascii_uppercase:
        linha.update({c: estadoId})
    #####ver se underscore está funcionando
    linha.update({"_": estadoId})
    Tabela_Transicao.append(linha)

    #preenchimento estado 10 - estadoComentario
    linha = {}
    linha.update({"final": False})
    #####Como indicar qqr coisa?#####
    linha.update({"}": estadoComentarioFinal})
    Tabela_Transicao.append(linha)

    #estado 11 - estadoComentarioFinal
    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    #estado 12 - estadoOPM
    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    #preenchimento estado 13 - estadoOPRMenor
    linha = {}
    linha.update({"final": True})
    linha.update({"-": estadoRCB})
    linha.update({">": estadoOPRMenorIgualDiferente, "=": estadoOPRMenorIgualDiferente})
    Tabela_Transicao.append(linha)

    #estado 14 - estadoRCB
    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    #estado 15 - estadoOPRMenorIgualDiferente
    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    #preenchimento estado 16 - estadoOPRMaior
    linha = {}
    linha.update({"final": True})
    linha.update({"=": estadoOPRMaiorIgual})
    Tabela_Transicao.append(linha)

    #estado 17 - estadoOPRMaiorIgual
    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    #estado 18 - estadoOPRIgual
    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    #estado 19 - estadoABP
    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    #estado 20 - estadoFCP
    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    #estado 21 - estadoPTV
    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)
    
Teste = []
preenche_tabela_dfa(Teste)

#Imprime toda a tabela de transições
i = 0
for k in Teste:
    print("Estado: " + str(i) + " " + str(Teste[i]) + "\n")
    i+=1