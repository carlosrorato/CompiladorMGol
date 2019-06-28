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
from Semantico.analisadorSemantico import *

# Preenche as tabelas utilizadas pelo Analisador Sintático
tabelaAcoes = preencheTabelaAcoes()
tabelaDesvios = preencheTabelaDesvios()
tabelaQtdSimbolos = preencheTabelaQtdSimbolos()
tabelaErros = preencheTabelaErros()

# Abre o arquivo passado como argumento
argumentos = sys.argv
# arqFonte = open(argumentos[1], encoding="utf-8")
arqFonte = open("fonte.alg", encoding="utf-8")

# Chama o Analisador Sintático
analisadorSintatico(tabelaAcoes,tabelaDesvios,tabelaQtdSimbolos, tabelaErros, arqFonte, arqDestino)

arqDestino.close()
arqFonte.close()