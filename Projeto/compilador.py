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
    for c in range(0,9):
        linha.update({c:1})
    linha.update({"\n":0 , "\_":0 , "\t": 0})
    linha.update({"EOF":13})
    linha.update({"\"": 7})
    linha.update({"{":10 , "<":14 , ">":17 , "=":19})
    linha.update({"+": 12, "-": 12, "*": 12, "/": 12})
    linha.update({"(": 20, ")": 21, ";": 22})
    Tabela_Transicao.append(linha)


preenche_tabela_dfa()
print(Tabela_Transicao)