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

# SEMANTICO  ****** Função para imprimir no arquivo .c
def imprimir(texto, arquivo):
    return

# Cria uma string com o nome do token retornado pelo Léxico mais seu significado
# para imprimir mensagem do tipo de erro ocorrido 
def traduzToken(token):
    tokenTraduzido = token + "("
    if token == "Num":
        return tokenTraduzido + "Número)" 
    if token == "Literal":
        return tokenTraduzido + "Literal)"
    if token == "id":
        return tokenTraduzido + "Identificador)"
    if token == "Comentário":
        return tokenTraduzido + "Comentário)"
    if token == "OPM":
        return tokenTraduzido + "Operador Matemático)"
    if token == "OPR":
        return tokenTraduzido + "Operador Relacional)"
    if token == "RCB":
        return tokenTraduzido + "Atribuição)"
    if token == "AB_P":
        return tokenTraduzido + "Abre Parêntesis - '(')"
    if token == "FC_P":
        return tokenTraduzido + "Fecha Parêntesis - ')')"
    if token == "PT_V":
        return tokenTraduzido + "Ponto e Vírgula - ;)"

    # Caso o token seja palavra reservada
    else:
        return token

#Função principal do Analisador Sintático
def analisadorSintatico(tabelaAcoes, tabelaDesvios, tabelaQtdSimbolos, tabelaErros, arquivo):

    # Criação e preenchimento da tabela de transições do DFA
    TabelaTransicao = []
    preenche_tabela_dfa(TabelaTransicao)

    # Criação e preenchimento da tabela de símbolos
    TabelaSimbolos = preenchePalavrasReservadas()

    # Lista para simular pilha
    pilha = []

    # SEMANTICO  ****** Lista para a pilha auxiliar
    pilha_semantica = []

    # Empilha estado inicial
    pilha.append(0)

    # SEMANTICO  ****** Empilha uma "tupla inicial"
    pilha_semantica.append({"lexema": "null", "token": "", "tipo": "null", "linha": "","coluna": ""})

    # Implementacao do algoritmo - conforme descrito no livro
    # Seja "a" o primeiro símbolo da entrada
    while True:

        # Recebe token completo do Léxico (token, lexema, tipo, linha, coluna) 
        b = analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos)

        # Recebe apenas o valor da chave 'token' do dicionário recebido por b
        a = b["token"]

        # Aqui, ele deve prosseguir a analise, independente dos erros (que mesmo assim sao mostrados na tela)
        # e dos comentarios
        if a != "Comentário" and a != "ERRO":
            break

    # Flag para indicar o erro onde falta um símbolo
    flagSimbolo = False  

    # Guarda o último valor de a para tratamento de erro, se necessário
    aAntigo = a

    # Flag para indicar a ocorrencia de erros
    flagErro = False 

    # Inicializa célula para caso de erro sintático no primeiro token
    celula = ""

    # Repetir indefinidamente
    while(1):

        # Seja "s" o estado do topo da pilha
        s = pilha[len(pilha) - 1]

        # Verificando os dados nas tabelas
        if tabelaAcoes[int(s)].get(a):
            celula = tabelaAcoes[int(s)].get(a)

            # Separação do aux em letra e numero, para descobrir a ação a ser feita e o estado 
            # usado na ação 
            operacao = celula[0]
            t = celula.translate({ord('S'): None, ord('R'): None})

        # Indica que não há transição para o token recebido no estado atual
        else:
            t = 0

        # IF ACTION(s,a) = shift t
        if t and operacao == "S":

            # empilha t na pilha
            pilha.append(t)

            # SEMANTICO  ****** Empilha o token
            pilha_semantica.append(b)

            # seja "a" o prox simbolo da entrada: loop para evitar comentarios
            while True:

                # Caso tenha no passo anterior dado um erro de um unico simbolo
                if flagSimbolo: 
                    a = aAntigo
                    flagSimbolo = False

                # Lê um novo token do Léxico
                else:
                    b = analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos)
                    a = b["token"]

                # Aqui, ele deve prosseguir a analise, independente dos erros (que mesmo assim sao mostrados na tela)
                # e dos comentarios
                if a != "Comentário" and a != "ERRO":
                    break

        #ELSE IF ACTION(s,a) = reduce A->B
        elif t and operacao == "R":

            # Aqui, o t vai ser o numero da regra
            x = tabelaQtdSimbolos[int(t) - 1].get("TamanhoBeta")
            A = tabelaQtdSimbolos[int(t) - 1].get("A")
            B = tabelaQtdSimbolos[int(t) - 1].get("Beta")

            # SEMANTICO  ****** Estrutura para guardar os tokens desempilhados para a validação semântica
            tokensParaValidacao = []

            # desempilha |B| símbolos da pilha
            if x:
                for i in range(0, int(x)):
                    pilha.pop()
                    # SEMANTICO  ****** Desempilhar os tokens também.
                    # Esses N tokens são os que formam a regra e os que você vai usar na validação semântica.
                    tokensParaValidacao.append(pilha_semantica.pop())

            # faça t ser o topo da pilha
            t = pilha[len(pilha) - 1]

            # empilha GOTO[t,A]
            if tabelaDesvios[int(t)].get(A):

                # Na tabela dos desvios a celula contem apenas o numero do estado
                valor = tabelaDesvios[int(t)].get(A)
                pilha.append(valor)

                # SEMANTICO  ****** Acho que aqui temos que aplicar a regra e empilhar o não terminal!


            # imprima a producao A->B
            print("Regra aplicada: " + A +" -> " + B + RESET)

        # Chegou no estado de aceitação da análise, seja de forma correta ou por causa da recuperação
        # de erros
        elif celula == "aceita":

            # Questões estéticas
            print()
            print(BOLD + "----------------------------------------------------------------")

            # Houve recuperação de erros
            if flagErro:
                print("Análise Sintática finalizada: " + RESET + "foram encontrados erros. " + RED + "Falha!")
            
            # Análise finalizada sem erros
            else:
                print("Análise Sintática finalizada: " + GREEN + "aceitou!")

            # Questões estéticas
            print(RESET + BOLD + "----------------------------------------------------------------")    
            
            # Finaliza a execução do Sintático
            return

        # Se não houver transição na tabela de ações - t = 0
        else:
            flagErro = True
            
            # Inicializa dicionário para símbolos que faltam e lista para imprimi-los
            simbolosFaltando = {}
            listaParaImprimir = ""

            # Verifica na tabela de ações quais símbolos possuem transições dado o estado atual s,
            # adiciona no dicionário e cria a lista para impressão
            for k,v in tabelaAcoes[int(s)].items():
                if v != '' and k!='Estado':
                    simbolosFaltando.update({k : v})
                    nomeToken = traduzToken(k)
                    listaParaImprimir = listaParaImprimir + " " + str(nomeToken)

            # Imprime os símbolos que faltam para prosseguir a análise sintática
            # com o acréscimo de constantes por questões estéticas
            print(RED + BOLD + "\nErro Sintático. " + RESET + "Linha: " + b.get("linha") +" Coluna: " + b.get("coluna") +" Faltando algum do(s) símbolo(s):" + BOLD + CYANDARK + listaParaImprimir + RESET)

            # Verificando a quantidade de simbolos no dicionario
            if len(simbolosFaltando) == 1:
                # Se for apenas um símbolo, o insere na análise para continuá-la
                print(BOLD + "\tTratamento de erro." + RESET + " Inserindo símbolo ausente...")
                chave = [key for key in simbolosFaltando.keys()]

                # para armazenar o último token lido
                aAntigo = a

                # o token atual passa a ser o simbolo que faltava para continuar a análise
                a = chave[0]

                # Flag para indicar o erro onde falta um símbolo
                flagSimbolo = True 

                # Questões estéticas
                print("\t" + CYANDARK + BOLD + a + RESET + " inserido para prosseguir a análise.")
                print(BOLD + "\tFim de tratamento de erro\n" + RESET)

            # Mais de uma possibilidade de símbolos que poderiam ser inseridos para prosseguir a 
            # análise
            else:
                # Questões estéticas
                print(BOLD + "\t\tIniciando tratamento de erro." + RESET + " À procura de um token sincronizante...")
                
                # Obtem a lista de símbolos do conjunto Follow do não terminal à esquerda da primeira
                # regra do estado atual(topo da pilha) para resincronizar a análise
                listaFollow = tabelaErros[int(s)].get('Follow')
                aux = 1

                # Procura um token que está na lista de símbolos do conjunto Follow, descartando
                # os tokens recebidos do Léxico até encontrar ou finalizar o arquivo 
                while (aux):
                    while True:

                        # Recebe um token do Léxico
                        a = analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos)["token"]
                        
                        # Se for $(EOF), não foi encontrado um token para sincronizar a análise
                        # antes do fim do arquivo
                        if a == "$":

                            # Questões estéticas
                            print("\t\tArquivo finalizado. Não foi possível concluir a recuperação...")
                            print(BOLD + "\t\tFim de tratamento de erro\n")
                            print(BOLD + "\n----------------------------------------------------------------")
                            print("Análise Sintática finalizada: " + RESET + "foram encontrados erros. " + RED + "Falha!")
                            print(RESET + BOLD + "----------------------------------------------------------------")
                            return

                        # Aqui, ele deve prosseguir a analise, independente dos erros (que mesmo assim sao mostrados na tela)
                        # e dos comentarios, alem de tratar o fim de arquivo
                        elif a != "Comentário" and a != "ERRO":
                            break

                    # Verifica se o último token lido está na lista do conjunto Follow
                    # saindo do loop da linha 243 caso encontre
                    for token in listaFollow:
                        if token == a:
                            aux = 0
                            break

                # Questões estéticas
                print("\t\tEncontrado token sincronizante: " + CYANDARK + BOLD + a + RESET)

                # Obtém a quantidade de símbolos empilhados relacionados à primeira regra do estado
                # atual e desempilha-os para continuar a análise de forma correta
                x = tabelaErros[int(s)].get('QtdSimbolos')
                if x:
                    for i in range(0, int(x)):
                        pilha.pop()
                        # SEMANTICO  ****** Desempilhar os tokens também.
                        pilha_semantica.pop()

                # Questões estéticas
                print(BOLD + "\t\tRetomando análise sintática\n" + RESET)