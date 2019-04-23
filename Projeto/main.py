# -*- coding: utf-8 -*-

# # Universidade Federal de Goiás
# Instituto de Informática - INF
# Compiladores - Compilador para MGol
#
# Módulo: Main
# Função principal do programa, que
# integra todos os outros módulos do
# compilador
#
# Alunos: Carlos Henrique Rorato Souza
# e Larissa Santos de Azevedo

import sys
from tabelaTransicao import *
from tabelaSimbolos import *
from analisadorLexico import *

##Função para formatar a impressão dos tokens
def imprime(resultado):
    BOLD = '\033[1m'
    RESET = '\033[0m'
    CYAN  = "\033[94m"

    print(BOLD + "Lexema: " + CYAN + resultado["lexema"] + RESET + ", " + BOLD + 
    "Token: " + RESET + CYAN + resultado['token'] + RESET +  ", " + BOLD + "Tipo: " + RESET + resultado['tipo'])
    print("-------------------------------------------------------------------------------------------------")


#Criação e preenchimento da tabela de transições do DFA
TabelaTransicao = []
preenche_tabela_dfa(TabelaTransicao)

#Criação e preenchimento da tabela de símbolos
TabelaSimbolos = preenchePalavrasReservadas()

argumentos = sys.argv

arq = open(argumentos[1], encoding="utf-8")

#Chama o léxico e immprime o resultado
while(1):
    resultado = analisadorLexico(arq, TabelaTransicao, TabelaSimbolos)
    if resultado:
        imprime(resultado)
        if resultado.get("token") == "EOF":
            break

arq.close()