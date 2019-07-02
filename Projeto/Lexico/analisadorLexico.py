# -*- coding: utf-8 -*-

# # Universidade Federal de Goiás
# Instituto de Informática - INF
# Compiladores - Compilador para MGol
#
# Módulo: Analisador Léxico
# Este módulo implementa o analisador léxico
# para a linguagem. Ele lê o arquivo fonte caractere
# a caractere e faz sua análise e classificação em
# lexemas e tokens. Ele utliza a tabela de transições
# para fazer o processamento das cadeias e preenche
# a tabela de símbolos.
#
# Alunos: Carlos Henrique Rorato Souza
# e Larissa Santos de Azevedo

from Lexico.tabelaTransicao import *
from Lexico.tabelaSimbolos import *

# Marcadores para a linha e coluna onde ocorre um erro
dadosErro = {"linha" : 1, "colAtual": 0, "colAntiga": 0 }

# Cores para formatar saida do print (em caso de erro)
RED = "\033[1;31m" 
RESET = "\033[0;0m"

# Procura se há transição no DFA do estado atual lendo o caracter passado como argumento 
def verifica_tabela_dfa(caractere, estado_atual, TabelaTransicao):
    prox_estado = TabelaTransicao[estado_atual].get(caractere)
    if prox_estado != None:
        return prox_estado
    else:
        return -1

# Retorna o nome do token dos estados finais
def verifica_token_dfa(estado):
    if estado == 1 or estado == 3 or estado == 6:
        token = "Num"
    if estado == 8:
        token = "Literal"
    if estado == 9:
        token = "id"
    if estado == 11:
        token = "Comentário"
    if estado == 12:
        token = "OPM"
    if estado == 13 or estado == 15 or estado == 16 or estado == 17 or estado == 18:
        token = "OPR"
    if estado == 14:
        token = "RCB"
    if estado == 19:
        token = "AB_P"
    if estado == 20:
        token = "FC_P"
    if estado == 21:
        token = "PT_V"
    return token


def analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos):
    # Variavel que controla o ultimo caracter aceito para reiniciar a analise após retornas um token
    distanciaUltimoAceito = 1

    # Variaveis para verificacao dos possiveis erros:
    # O que não for erro de parenteses ou chave, é de caractere invalido
    abreAspas = 0
    abreChaves = 0

    tupla = {"lexema": "", "token": "", "tipo": "null", "linha": "","coluna": ""}

    # Lê o caracter, incrementa o contador da coluna atual, vai para o estado 0 e reseta a palavra
    char = arquivo.read(1)
    dadosErro['colAtual'] += 1
    palavra = ""
    estado = 0

    #Verificacao do tipo de erro:
    if char == '\"':
        abreAspas = 1
    elif char == '{':
        abreChaves = 1
    elif char == '}':
        abreChaves = 0

    # Verifica se chegou ao final do arquivo
    if not char:  
        return {"lexema": "EOF", "token": "$", "tipo": "null", "linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])}

    while True:
        # Fazendo o incremento da linha, zerando a coluna para caso de erro e armazenando a coluna anterior
        if char == "\n":
            dadosErro["linha"] += 1
            dadosErro["colAntiga"] = dadosErro["colAtual"] 
            dadosErro["colAtual"] = 0

        # Recebe o estado do automato com o caracter lido 
        estado_aux = verifica_tabela_dfa(char, estado, TabelaTransicao)
        estado = estado_aux

        # Caso não exista transição / Escopo onde será retornada a tupla com o seu respectivo token e a
        # mensagem de erro, caso precise
        if estado == -1:  

            # Verifica se o char é o EOF e retorna o último token
            if not char:  
                # Se o token estiver vazio, imprime a mensagem de erro e muda o valor da tupla
                if tupla['token'] == '' and tupla['lexema'] != '':

                    # Verifica o tipo de erro
                    if abreAspas % 2 != 0:
                        tipoErro = "Não fechou as aspas"
                    elif abreChaves == 1:
                        tipoErro = "Não fechou as chaves"
                    else:
                        tipoErro = "Caractere invalido"

                    print(RED + "Erro léxico. " + RESET + tipoErro + ": "+ palavra + " - Linha " + str(dadosErro["linha"]) + ", Coluna " + str(dadosErro["colAtual"]))
                    tupla = {"lexema": palavra, "token": "ERRO", "tipo": "null", "linha": str(dadosErro["linha"]), "coluna": str(dadosErro["colAtual"])}
                elif tupla["token"] == "id":
                    tupla = procuraToken(tupla, TabelaSimbolos)
                    tupla.update({"linha": str(dadosErro["linha"]), "coluna": str(dadosErro["colAtual"])})
                else:
                    tupla = {"lexema": "EOF", "token": "$", "tipo": "null", "linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])}
                return tupla

            # Se o token estiver vazio, imprime a mensagem de erro e retorna tupla de erro
            if tupla['lexema'] == '':

                # Verifica o tipo de erro
                if abreAspas % 2 != 0:
                    tipoErro = "Não fechou as aspas"
                elif abreChaves == 1:
                    tipoErro = "Não fechou as chaves"
                else:
                    tipoErro = "Caractere invalido"

                # imprimindo a linha e coluna do erro
                    print(RED + "Erro léxico. " + RESET + tipoErro + ": " + char + " - Linha " + str(
                        dadosErro["linha"]) + ", Coluna " + str(dadosErro["colAtual"]))
                tupla = {"lexema": char, "token": "ERRO", "tipo": "null", "linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])}
                return tupla
            
            # Se a tupla não estiver vazia, volta o carro de leitura para o último caracter aceito para
            # recomeçar a leitura quando o próximo token for solicitado 
            arquivo.seek(arquivo.tell() - distanciaUltimoAceito)

            # Se o caracter lido por último for \n, ao voltar o carro de leitura o \n será lido novamente.
            # Para manter a contagem correta de linhas, diminui o valor da linha e como a coluna foi zerada
            # na linha 82, o valor da coluna atual passa a ser o da coluna antiga menos a distância do ultimo
            # caracter aceito, pois tais caracteres serão lidos novamente   
            if char == '\n':
                dadosErro["linha"] -= 1
                dadosErro["colAtual"] = dadosErro["colAntiga"] - distanciaUltimoAceito
            # Se não for \n, apenas diminui a distância do ultimo caracter aceito, de onde se vai recomeçar
            # a leitura
            else :
                dadosErro["colAtual"] = dadosErro["colAtual"] - distanciaUltimoAceito

            # Se é identificador, procura na Tabela de Símbolos pela entrada
            if tupla["token"] == "id":
                tupla = procuraToken(tupla, TabelaSimbolos)
                tupla.update({"linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])})

            # Retorna tupla com o token != de ERRO    
            return tupla

        # Se a transição existir, verifica se o novo estado é final. Se for atualiza o lexema na tupla
        # que será retornada e reestabelece a distância do ultimo caracter aceito para 1 
        elif TabelaTransicao[estado].get("final"):  
            palavra = palavra + char
            distanciaUltimoAceito = 1
            token = verifica_token_dfa(estado)
            if(estado == 1):
                tupla = {"lexema": palavra, "token": token, "tipo": "int", "linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])}
            elif(estado == 3 or estado == 6):
                tupla = {"lexema": palavra, "token": token, "tipo": "real", "linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])}
            else:
                tupla = {"lexema": palavra, "token": token, "tipo": "null", "linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])}

        # Caso exista transição e o novo estado não é atual, adiciona o caracter lido na palavra.
        # Caso o caracter seja espaço, \n ou \t, nada é feito para que sejam reconhecidos e ignorados 
        else:
            if (estado == 0 and char != " " and char != "\n" and char != "\t") or estado != 0:
                palavra = palavra + char
                # Aumenta a distância do último caracter aceito para controlar a posição que deve se iniciar
                # a leitura do próximo token
                distanciaUltimoAceito += 1

        # Lê um novo caracter e incrementa o contador de coluna
        char = arquivo.read(1)
        dadosErro['colAtual'] += 1

        # Verificacao do tipo de erro:
        if char == '\"':
            abreAspas = abreAspas + 1
        elif char == '{':
            abreChaves = 1
        elif char == '}':
            abreChaves = 0

