from Lexico.analisadorLexico import *
from Lexico.tabelaSimbolos import *
from Lexico.tabelaTransicao import *
import string

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

    #Implementacao do algoritmo - conforme descrito no livro

    #Seja "a" o primeiro símbolo da gramática
    a = analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos)

    #Repetir indefinidamente
    while(1):
        #Seja "s" o estado do topo da pilha
        s = pilha[len(pilha) - 1]

        #Verificando os dados nas tabelas

        if tabelaAcoes[s][a]:
            aux = tabelaAcoes[s][a]

            #separacao do aux em letra e numero
            operacao = aux[0]
            t = aux.translate({ord('S'): None, ord('R'): None})

        #IF ACTION(s,a) = sift t
        if t and operacao == "S":
            #empilha t na pilha
            pilha.append(t)

            #seja "a" o prox simbolo da pilha
            a = analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos)

        #ELSE IF ACTION(s,a) = reduce A->B
        elif t and operacao == "R":
            #Aqui, o t vai ser o numero da regra
            #desempilha |B| símbolos da pilha
            x = tabelaQtdSimbolos[t - 1]["TamanhoBeta"]
            A = tabelaQtdSimbolos[t - 1]["A"]
            B = tabelaQtdSimbolos[t - 1]["Beta"]

            if x:
                pilha.pop(x)

            #faça t ser o topo da pilha

            t = pilha[len(pilha) - 1]

            #empilha GOTO[t,A]

            if tabelaDesvios[t][A]:
                # Na tabela dos desvios a celula contem apenas o numero do estado
                valor = tabelaDesvios[t][A]

            pilha.append(valor)
            #imprima a producao A->B

            print("Regra aplicada: " + A + " -> " + B)

            





