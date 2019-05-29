# -*- coding: utf-8 -*-

# # Universidade Federal de Goiás
# Instituto de Informática - INF
# Compiladores - Compilador para MGol
#
# Módulo: Main
# Função principal do programa, que
# integra todos os outros módulos do
# compilador(Léxico e Sintático)
#
# Alunos: Carlos Henrique Rorato Souza
# e Larissa Santos de Azevedo

import sys
from Lexico.tabelaTransicao import *
from Lexico.tabelaSimbolos import *
from Lexico.analisadorLexico import *
from Sintatico.analisadorSintatico import *
from Sintatico.preencheTabelas import *

# Função para formatar a impressão dos tokens
def imprime(resultado):

    # Códigos de formatacao para saida do print
    BOLD = '\033[1m'
    RESET = '\033[0m'
    CYAN  = "\033[94m"

    print(BOLD + "Lexema: " + CYAN + resultado["lexema"] + RESET + ", " + BOLD + 
    "Token: " + RESET + CYAN + resultado['token'] + RESET +  ", " + BOLD + "Tipo: " + RESET + resultado['tipo'])
    print("-------------------------------------------------------------------------------------------------")
    
# Criação e preenchimento da tabela de transições do DFA
#TabelaTransicao = []
#preenche_tabela_dfa(TabelaTransicao)

# Criação e preenchimento da tabela de símbolos
#TabelaSimbolos = preenchePalavrasReservadas()

tabelaAcoes = preencheTabelaAcoes()
tabelaDesvios = preencheTabelaDesvios()
tabelaQtdSimbolos = preencheTabelaQtdSimbolos()
tabelaPanico = preencheTabelaPanico()

# Abre o arquivo passado como argumento
argumentos = sys.argv
arq = open(argumentos[1], encoding="utf-8")

# Chama o léxico e immprime o resultado
#while(1):
#    resultado = analisadorLexico(arq, TabelaTransicao, TabelaSimbolos)
#    if resultado:
#        imprime(resultado)
#       if resultado.get("token") == "$":
#            break

#chama o léxico

analisadorSintatico(tabelaAcoes,tabelaDesvios,tabelaQtdSimbolos, tabelaPanico, arq)

arq.close()