from Lexico.analisadorLexico import *
from Lexico.tabelaSimbolos import *
from Lexico.tabelaTransicao import *

def analisadorSintatico(tabelaAcoes, tabelaDesvios, tabelaQtdSimbolos, arquivo):

    # Criação e preenchimento da tabela de transições do DFA
    TabelaTransicao = []
    preenche_tabela_dfa(TabelaTransicao)

    # Criação e preenchimento da tabela de símbolos
    TabelaSimbolos = preenchePalavrasReservadas()
    
    #lista para simular pilha
    pilha = []
    #empilha estado inicial
    pilha.append(0)