# Universidade Federal de Goiás
# Instituto de Informática - INF
# Compiladores - Compilador para MGol
#
# Módulo: Analisador Léxico
# Este módulo implementa o analisador léxico
# para a linguagem. Ele lê o arquivo fonte caractere
# a caractere e faz sua análise e classificação em
# lexemas e tokens. Ele utliza a tabela de transições
# para fazer o processamento das cadeias e preenche
# a tabela de símbolos.
#
# Alunos: Carlos Henrique Rorato Souza
# e Larissa Santos de Azevedo

from tabelaTransicao import *

#Criação e preenchimento da tabela de transições do DFA
TabelaTransicao = []
preenche_tabela_dfa(TabelaTransicao)

def verifica_tabela_dfa(caractere, estado_atual):
    prox_estado = TabelaTransicao[estado_atual].get(caractere)
    if prox_estado:
        return prox_estado
    else:
        return -1

def verifica_token_dfa(estado):
    if estado == 1 or estado == 3 or estado == 6:
        token = "Num"
    if estado == 8:
        token = "Literal"
    if estado == 9:
        token = "id"
    if estado == 11:
        token = "Comentário"
    if estado == 12:
        token = "OPM"
    if estado == 13 or estado == 15 or estado == 16 or estado == 17 or estado == 18:
        token = "OPR"
    if estado == 14:
        token = "RCB"
    if estado == 19:
        token = "AB_P"
    if estado == 20:
        token = "FC_P"
    if estado == 21:
        token = "PT_V"
    return token




def analisadorLexico(arquivo):
    tupla = {"lexema": "", "token": "", "tipo": "null"}

    char = arquivo.read(1)

    estado = 0

    while True:
        estado_aux = verifica_tabela_dfa(char, estado)
        estado = estado_aux

        if estado == -1: #Ou seja, não existem mais transições
            if not char:  # chegou ao final do arquivo
                return {"lexema": "EOF", "token": "EOF", "tipo": "null"}

            elif char != " " and char != "\n" and char != "\t":
                arquivo.seek(arquivo.tell()-1) #volta o carro de leitura
                return tupla

        elif TabelaTransicao[estado].get("final"):# se é estado final
            lexema = tupla.get("lexema") + char
            token = verifica_token_dfa(estado)
            tupla ={"lexema": lexema, "token": token, "tipo": "null"}

        else:
            lexema = tupla.get("lexema") + char
            tupla["lexema"] = lexema

        char = arquivo.read(1)


## Testando


####### PARA TESTES: Imprime toda a tabela de transições
#i = 0
#for k in TabelaTransicao:
#    print("Estado:" + str(i) + " " + str(TabelaTransicao[i]) + "\n")
#    i+=1

arq = open("./teste.mgol", encoding="utf8")
while(1):
    resultado = analisadorLexico(arq)
    if resultado.get("token") == "EOF":
        print(resultado)
        break
    else:
        print(resultado)

arq.close()