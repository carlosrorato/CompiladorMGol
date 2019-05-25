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

    #Seja "a" o primeiro símbolo da entrada
    while True:
        a = analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos)["token"]
        if a != "Comentário":
            break

    #Repetir indefinidamente
    while(1):
        #Seja "s" o estado do topo da pilha
        s = pilha[len(pilha) - 1]

        #Verificando os dados nas tabelas

        if tabelaAcoes[int(s)].get(a):
            celula = tabelaAcoes[int(s)].get(a)

            #separacao do aux em letra e numero
            operacao = celula[0]
            t = celula.translate({ord('S'): None, ord('R'): None})
        else:
            t = 0

        #IF ACTION(s,a) = shift t
        if t and operacao == "S":
            #empilha t na pilha
            pilha.append(t)

            #seja "a" o prox simbolo da entrada: loop para evitar comentarios
            while True:
                a = analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos)["token"]
                if a != "Comentário":
                    break

        #ELSE IF ACTION(s,a) = reduce A->B
        elif t and operacao == "R":
            #Aqui, o t vai ser o numero da regra
            #desempilha |B| símbolos da pilha
            x = tabelaQtdSimbolos[int(t) - 1].get("TamanhoBeta")
            A = tabelaQtdSimbolos[int(t) - 1].get("A")
            B = tabelaQtdSimbolos[int(t) - 1].get("Beta")

            if x:
                for i in range(0, int(x)):
                    pilha.pop()

            #faça t ser o topo da pilha

            t = pilha[len(pilha) - 1]

            #empilha GOTO[t,A]

            if tabelaDesvios[int(t)].get(A):
                # Na tabela dos desvios a celula contem apenas o numero do estado
                valor = tabelaDesvios[int(t)].get(A)

                pilha.append(valor)
            #imprima a producao A->B

            print("Regra aplicada: " + A + " -> " + B)


        elif celula == "aceita":
            print("Analise sintatica finalizada: aceitou!")
            return

        else:
            print("Ocorreu um erro. Aqui, localizar e tratar o erro")
            return




