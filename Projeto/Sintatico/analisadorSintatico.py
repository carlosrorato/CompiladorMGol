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

# Cores para formatar saída 
BOLD = '\033[1m'
CYANDARK  = "\033[94m"
CYAN = "\033[96m"
GREEN = '\033[92m'
RED = "\033[1;31m"
RESET = '\033[0m'

def traduzToken(token):
    if token == "Num":
        return "Número"
    if token == "Literal":
        return "Literal"
    if token == "id":
        return "Identificador"
    if token == "Comentário":
        return "Comentário"
    if token == "OPM":
        return "Operador Matemático"
    if token == "OPR":
        return "Operador Relacional"
    if token == "RCB":
        return "Atribuição"
    if token == "AB_P":
        return "Abre Parêntesis"
    if token == "FC_P":
        return "Fecha Parêntesis"
    if token == "PT_V":
        return "Ponto e Vírgula"


def analisadorSintatico(tabelaAcoes, tabelaDesvios, tabelaQtdSimbolos, tabelaPanico, arquivo):

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
        if a != "Comentário" and a != "ERRO":
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
                if a != "Comentário" and a != "ERRO":
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

            print("Regra aplicada: " + A +" -> " + B + RESET)


        elif celula == "aceita":
            print()
            print(BOLD + "----------------------------------------------------------------")
            if flagErro:
                print("Análise Sintática finalizada: " + RESET + "foram encontrados erros. " + RED + "Falha!")
            else:
                print("Análise Sintática finalizada: " + GREEN + "aceitou!")
            print(RESET + BOLD + "----------------------------------------------------------------")    
            return

        else:
            flagErro = True

            simbolosFaltando = {}

            listaParaImprimir = ""

            for k,v in tabelaAcoes[int(s)].items():
                if v != '' and k!='Estado':
                    simbolosFaltando.update({k : v})
                    listaParaImprimir = listaParaImprimir + " " + traduzToken(k)

            print(RED + BOLD + "Erro Sintático. " + RESET + "Linha:" + b.get("linha") +" Coluna:" + b.get("coluna") +" Faltando algum do(s) símbolo(s): " + BOLD + CYANDARK + listaParaImprimir + RESET)

            #Verificando a quantidade de simbolos no dicionario
            if len(simbolosFaltando) == 1:
                print(BOLD + "\tTratamento de erro." + RESET + " Inserindo símbolo ausente...")

                chave = [key for key in simbolosFaltando.keys()]

                # para armazenar o último token lido
                a_antigo = a

                a = chave[0]

                flagSimbolo = True #Flag para indicar o erro onde falta um símbolo

                print("\t" + CYANDARK + BOLD + a + RESET + " inserido para prosseguir a análise.")
                print(BOLD + "\tFim de tratamento de erro\n")

            else:
                print(BOLD + "\t\tIniciando tratamento de erro." + RESET + " À procura de um token sincronizante...")
                listaFollow = tabelaPanico[int(s)].get('Follow')
                teste = 1
                while (teste):
                    while True:
                        a = analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos)["token"]
                        # Aqui, ele deve prosseguir a analise, independente dos erros (que mesmo assim sao mostrados na tela)
                        # e dos comentarios, alem de tratar o fim de arquivo
                        if a == "$":
                            print("\t\tArquivo finalizado. Não foi possível concluir a recuperação...")
                            print(BOLD + "\t\tFim de tratamento de erro\n")
                            print(BOLD + "\n----------------------------------------------------------------")
                            print("Análise Sintática finalizada: " + RESET + "foram encontrados erros. " + RED + "Falha!")
                            print(RESET + BOLD + "----------------------------------------------------------------")
                            return
                        elif a != "Comentário" and a != "ERRO":
                            break
                    for token in listaFollow:
                        if token == a:
                            teste = 0
                            break
                print("\t\tEncontrado token sincronizante: " + CYANDARK + BOLD + a + RESET)

                x = tabelaPanico[int(s)].get('QtdSimbolos')
                if x:
                    for i in range(0, int(x)):
                        pilha.pop()
                print(BOLD + "\t\tRetomando análise sintática" + RESET)
                
## Faltando
# arrumar linha e coluna do erro sintático para exibir na tela
# arrumar erro léxico quando finaliza arquivo com \n e e está no meio do modo pânico
# 