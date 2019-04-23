# -*- coding: utf-8 -*-

# # Universidade Federal de Goiás
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
from tabelaSimbolos import *

#Marcadores para a linha e coluna onde ocorre um erro:
linha = 1
col = 1

#Cores no terminal
RED = "\033[1;31m" 
RESET = "\033[0;0m"

def verifica_tabela_dfa(caractere, estado_atual, TabelaTransicao):
    prox_estado = TabelaTransicao[estado_atual].get(caractere)
    if prox_estado != None:
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


def analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos):
    global linha
    global col

    tupla = {"lexema": "", "token": "", "tipo": "null"}

    char = arquivo.read(1)

    estado = 0

    if not char:  # chegou ao final do arquivo
        return {"lexema": "EOF", "token": "EOF", "tipo": "null"}

    while True:

        # fazendo o incremento da linha e zerando a coluna para caso de erro
        if char == "\n":
            linha += 1
            col = 0

        estado_aux = verifica_tabela_dfa(char, estado, TabelaTransicao)
        estado = estado_aux

        if estado == -1:  # Ou seja, não existem mais transições

            if not char:  # ultimo token
                return tupla

            elif char != " " and char != "\n" and char != "\t":
                if tupla['lexema'] == '':
                    # imprimindo a linha e coluna do erro
                    print(RED + "Erro léxico: " + RESET + "Linha " + str(linha) + ", Coluna " + str(col))

                    col = col + 1

                    return {"lexema": char, "token": "ERRO", "tipo": "null"}
                arquivo.seek(arquivo.tell() - 1)  # volta o carro de leitura

                if tupla["token"] == "id":
                    tupla = procuraToken(tupla, TabelaSimbolos)
                #Se não é identificador, não precisa ser salvo na Tabela de Símbolos.
                return tupla

        elif TabelaTransicao[estado].get("final"):  # se é estado final
            lexema = tupla.get("lexema") + char
            token = verifica_token_dfa(estado)
            tupla = {"lexema": lexema, "token": token, "tipo": "null"}

        else:
            if estado == 0 and char != " " and char != "\n" and char != "\t":
                lexema = tupla.get("lexema") + char
                tupla["lexema"] = lexema
            elif estado != 0:
                lexema = tupla.get("lexema") + char
                tupla["lexema"] = lexema

        char = arquivo.read(1)

        # incrementando contador de coluna
        col += 1