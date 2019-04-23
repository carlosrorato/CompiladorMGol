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

## Cores
GREEN = '\033[92m'
RESET = '\033[0m'

def preenchePalavrasReservadas():
    tabelaSimbolos = {}
    listaPalavrasReservadas = ['inicio', 'varinicio', 'varfim', 'escreva',
    'leia', 'se', 'entao', 'fimse', 'fim', 'inicio', 'lit', 'real']
    
    for palavra in listaPalavrasReservadas:
        tabelaSimbolos[palavra] = {'lexema': palavra, 'token': palavra, 'tipo': 'null'}
    return tabelaSimbolos

def procuraToken(tupla, tabelaSimbolos):
    if not (tupla['lexema'] in tabelaSimbolos):
        tabelaSimbolos[tupla['lexema']] = tupla
        print(GREEN + "Adicionado na tabela de símbolos: " + RESET + tupla['lexema'])
    return tabelaSimbolos[tupla['lexema']]

