# -*- coding: utf-8 -*-

# # Universidade Federal de Goiás
# Instituto de Informática - INF
# Compiladores - Compilador para MGol
#
# Módulo: Analisador Sintatico
# Recebe os tokens vindos do Analisador Léxico
# e faz uma análise em relação as produções
# da gramática
#
# Alunos: Carlos Henrique Rorato Souza
# e Larissa Santos de Azevedo


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


    #Implementacao do algoritmo - conforme descrito no livro

    #Seja "a" o primeiro símbolo da entrada
    while True:
        a = analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos)["token"]

        # Aqui, ele deve prosseguir a analise, independente dos erros (que mesmo assim sao mostrados na tela)
        # e dos comentarios
        if a != "Comentário" and a != "Erro":
            break

    flagSimbolo = False  # Flag para indicar o erro onde falta um símbolo
    a_antigo = a
    flagErro = False # Flag para indicar a ocorrencia de erros

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

        # IF ACTION(s,a) = shift t
        if t and operacao == "S":
            # empilha t na pilha
            pilha.append(t)

            # seja "a" o prox simbolo da entrada: loop para evitar comentarios
            while True:
                if flagSimbolo: # Caso tenha no passo anterior dado um erro de um unico simbolo
                    a = a_antigo
                    flagSimbolo = False
                else:
                    b = analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos)
                    a = b["token"]

                # Aqui, ele deve prosseguir a analise, independente dos erros (que mesmo assim sao mostrados na tela)
                # e dos comentarios
                if a != "Comentário" and a != "Erro":
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

            if flagErro:
                print("Analise sintatica finalizada: foram encontrados erros. Falhou!")
            else:
                print("Analise sintatica finalizada: aceitou!")
                
            return

        else:
            flagErro = True

            simbolosFaltando = {}

            listaParaImprimir = ""

            for k,v in tabelaAcoes[int(s)].items():
                if v != '' and k!='Estado':
                    simbolosFaltando.update({k : v})
                    listaParaImprimir = listaParaImprimir + " " + str(k)

            print("Erro Sintático. Faltando algum do(s) símbolo(s): " + listaParaImprimir)

            #Verificando a quantidade de simbolos no dicionario
            if len(simbolosFaltando) == 1:

                chave = [key for key in simbolosFaltando.keys()]

                # para armazenar o último token lido
                a_antigo = a

                a = chave[0]

                flagSimbolo = True #Flag para indicar o erro onde falta um símbolo

            else:

                print("Iniciando o modo pânico...entrando em pânico....")
                return