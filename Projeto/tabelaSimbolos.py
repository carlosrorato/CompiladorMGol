# -*- coding: utf-8 -*-

# Universidade Federal de Goias
# Instituto de Informática - INF
# Compiladores - Compilador para MGol
#
# Módulo: Tabela de Simbolos
# Este módulo preenche a tabela de símbolos do analisador léxico,
# implementado através de um dicionário de dicionários.
#
# Alunos: Carlos Henrique Rorato Souza
# e Larissa Santos de Azevedo

import string

## Preenche a tabela com as palavras reservadas da linguagem
def preenchePalavrasReservadas():
    tabelaSimbolos = {}
    listaPalavrasReservadas = ['inicio', 'varinicio', 'varfim', 'escreva',
    'leia', 'se', 'entao', 'fimse', 'fim', 'inicio', 'lit', 'real']
    
    for palavra in listaPalavrasReservadas:
        tabelaSimbolos[palavra] = {'lexema': palavra, 'token': palavra, 'tipo': 'null'}
    return tabelaSimbolos

## Dado um lexema reconhecido pelo analisador léxico, procura se ele já está na tabela.
# Se não estiver, adiciona a tupla na tabela. 
# Retorna o dicionário cuja chave na tabela de símbolos é o lexema
def procuraToken(tupla, tabelaSimbolos):
    if not (tupla['lexema'] in tabelaSimbolos):
        tabelaSimbolos[tupla['lexema']] = tupla
        print("add: " + tupla['lexema'])
    return tabelaSimbolos[tupla['lexema']]
    

## Teste do funcionamento da tabela de símbolos
# tabelaSimbolosTeste = preenchePalavrasReservadas()

# for item in tabelaSimbolosTeste:
#     print(tabelaSimbolosTeste[item])
# print()
# print("########################################")
# print()
# t = procuraToken({'lexema': 'palavra', 'token': 'id', 'tipo': 'null'}, tabelaSimbolosTeste)
# t = procuraToken({'lexema': 'inicio', 'token': 'id', 'tipo': 'null'}, tabelaSimbolosTeste)
# print()
# print("########################################")
# print()
# for item in tabelaSimbolosTeste:
#     print(tabelaSimbolosTeste[item])