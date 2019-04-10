# Universidade Federal de Goiás
# Instituto de Informática - INF
# Compiladores - Compilador para MGol
#
# Alunos: Carlos Henrique Rorato Souza
# e Larissa Santos de Azevedo
import string

#Estrutura de dados para a tabela de transição do DFA: matriz de dicionários (hash)
Tabela_Transicao = []

def preenche_tabela_dfa():

    #preenchimento para o estado 0:
    linha = {}
    for c in string.ascii_lowercase:
        linha.update({c:9})
    for c in string.ascii_uppercase:
        linha.update({c: 9})
    for c in range(0,10):
        linha.update({str(c):1})
    linha.update({"\n":0 , "\_":0 , "\t": 0})
    linha.update({"EOF":13})
    linha.update({"\"": 7})
    linha.update({"{":10 , "<":14 , ">":17 , "=":19})
    linha.update({"+": 12, "-": 12, "*": 12, "/": 12})
    linha.update({"(": 20, ")": 21, ";": 22})
    Tabela_Transicao.append(linha)

    # preenchimento para o estado 1:
    linha = {}
    for c in range(0, 10):
        linha.update({str(c): 1})
    linha.update({".": 2, "E": 4, "e": 4})
    Tabela_Transicao.append(linha)

    # preenchimento para o estado 2:
    linha = {}
    for c in range(0, 10):
        linha.update({str(c): 3})
    Tabela_Transicao.append(linha)

    # preenchimento para o estado 3:
    linha = {}
    for c in range(0, 10):
        linha.update({str(c): 3})
    linha.update({"E": 4, "e": 4})
    Tabela_Transicao.append(linha)

    # preenchimento para o estado 4:
    linha = {}
    for c in range(0, 10):
        linha.update({str(c): 6})
    linha.update({"+": 5, "-": 5})
    Tabela_Transicao.append(linha)

    # preenchimento para o estado 5:
    linha = {}
    for c in range(0, 10):
        linha.update({str(c): 6})
    Tabela_Transicao.append(linha)

    # preenchimento para o estado 6:
    linha = {}
    for c in range(0, 10):
        linha.update({str(c): 6})
    Tabela_Transicao.append(linha)


preenche_tabela_dfa()

#Imprime toda a tabela de transições
i = 0
for k in Tabela_Transicao:
    print(Tabela_Transicao[i])
    i+=1