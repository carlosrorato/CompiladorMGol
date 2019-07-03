# -*- coding: utf-8 -*-

# Universidade Federal de Goiás
# Instituto de Informática - INF
# Compiladores - Compilador para MGol
#
# Módulo: Analisador Semantico
# Realiza a análise semântica junto às reduções da análise sintática
# Gerando um arquivo .c com a tradução do código de mgol ou mensagens 
# de erro em caso de erro semântico
#
# Alunos: Carlos Henrique Rorato Souza
# e Larissa Santos de Azevedo

# Cores para formatar saída 
BOLD = '\033[1m'
CYANDARK  = "\033[94m"
CYAN = "\033[96m"
GREEN = '\033[92m'
RED = "\033[1;31m"
RESET = '\033[0m'

# Listas para armazenar o texto a ser impresso do arquivo .c
# incluindo o das variáveis temporárias criadas
TextoArquivo = []
TextoVariaveisTemporarias = []

# Contador para as variáveis temporárias
contadorTemporarias = 0

# Flag para avaliar erro semântico
flagErro = False

# Função que atribui tipo para tokens especificados na descrição do trabalho(n 2 pagina 3)
def atribuiTipo(tokenTupla):
    if tokenTupla['token'] == 'OPM':
        tokenTupla['tipo'] = tokenTupla['lexema']
    elif tokenTupla['token'] == 'lit':
        tokenTupla['tipo'] = 'literal'
    elif tokenTupla['token'] == 'inteiro':
        tokenTupla['tipo'] = 'int'
    elif tokenTupla['token'] == 'real':
        tokenTupla['tipo'] = 'real'
    elif tokenTupla['token'] == 'OPR':
        tokenTupla['tipo'] = tokenTupla['lexema']
    elif tokenTupla['token'] == 'RCB':
        tokenTupla['tipo'] = '='
    return tokenTupla

# Função que imprime no arquivo .c o texto traduzido do arquivo em mgol
def imprimirArquivo(nomeArquivoDestino):

    global flagErro
    print(BOLD + "----------------------------------------------------------------")
    
    # Houve erros semânticos - não gera o .c
    if flagErro:
        print("Análise Semântica finalizada: " + RESET + "foram encontrados erros. " + RED + "Falha!")
        print(RESET + BOLD + "----------------------------------------------------------------")    

    # Análise finalizada sem erros
    else:
        print("Análise Semântica finalizada: " + GREEN + "aceitou!")
        print(RESET + BOLD + "----------------------------------------------------------------")    

        # Abre(ou cria) um arquivo .c com o nome do arquivo em mgol que está sendo analisado 
        arqDestino = open(str(nomeArquivoDestino)+".c", "w+")

        # Imprimindo cabeçalho
        arqDestino.write("#include<stdio.h>\n\n")
        arqDestino.write("typedef char literal[256];\n")
        arqDestino.write("typedef double real;\n\n")
        arqDestino.write("void main(void){\n")

        # Imprimindo variáveis temporárias
        arqDestino.write("\t/*----Variaveis temporarias----*/\n")
        for texto in TextoVariaveisTemporarias:
            arqDestino.write("\t"+str(texto)+"\n")
        arqDestino.write("\t/*------------------------------*/\n")

        # Contador para identar o código de acordo com o escopo
        contadorIdentacao = 1

        # Imprimindo corpo do texto
        for texto in TextoArquivo:

            # Se ler um '}', significando o fim daquele escopo, diminui a identação
            if "}" in texto:
                contadorIdentacao -= 1

            # Imprime a quantidade de \t necessárias para o escopo atual    
            for i in range(0, contadorIdentacao):
                arqDestino.write("\t")

            # Imprime um elemento da lista TextoArquivo
            arqDestino.write(str(texto)+"\n")

            # Se ler um '{', significando o início de um novo escopo, incrementa a identação
            if "{" in texto:
                contadorIdentacao += 1

        # Fim do arquivo
        arqDestino.write("}\n")
        arqDestino.close()
        print("Arquivo " + nomeArquivoDestino +  ".c gerado")
        return

def imprimirTerminal(textoImpressao):
    
    # Questões estéticas
    print(BOLD + "\n-----------------------" + " SEMÂNTICO " + "-----------------------")
    print(textoImpressao)
    print(BOLD + "---------------------------------------------------------\n" + RESET)

def analisadorSemantico(t, A, tokensParaValidacao, TabelaSimbolos):
    
    # Declarando globais para uso
    global flagErro
    global contadorTemporarias
    Tupla = {"lexema": str(A), "token": str(A), "tipo": "", "linha": "", "coluna": ""}

    # Testes para aplicar a regra semântica correta de acordo com a regra reduzida

    # LV -> varfim;
    if t == 5:
        
        #Imprime dois \n devido ao \n impresso ao final da declaração de variáveis
        textoImpressao = "\n\n"
        TextoArquivo.append(textoImpressao)
        imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)
    
    #D -> id TIPO;
    elif t == 6:
        
        id = tokensParaValidacao.pop()
        TIPO = tokensParaValidacao.pop()
        
        # Modifica o valor do tipo na entrada da tabela de símbolos do léxico
        TabelaSimbolos[id['lexema']]['tipo'] = TIPO['tipo']
        textoImpressao = TIPO['tipo'] + " " + id['lexema'] + ";"
        TextoArquivo.append(TIPO['tipo'] + " " + id['lexema'] + ";")
        imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)

    # TIPO -> inteiro    
    elif t == 7:
        inteiro = tokensParaValidacao.pop()
        Tupla['tipo'] = inteiro['tipo']
    
    # TIPO -> real
    elif t == 8:
        real = tokensParaValidacao.pop()
        Tupla['tipo'] = real['tipo']

    # TIPO -> literal
    elif t == 9:
        literal = tokensParaValidacao.pop()
        Tupla['tipo'] = literal['tipo']

    # ES -> leia id;
    elif t == 11:
        
        # Desempilha dois símbolos para chegar no id
        id = tokensParaValidacao.pop()
        id = tokensParaValidacao.pop()

        # Verificações para saber qual opção do scanf imprimir no arquivo
        if id['tipo'] == "literal":
            textoImpressao = 'scanf("%s", ' + id['lexema'] + ");"
            TextoArquivo.append(textoImpressao)
            textoImpressao = "Impresso no arquivo: " + CYAN + textoImpressao + RESET
        elif id['tipo'] == "int":
            textoImpressao = 'scanf("%d", &' + id['lexema'] + ");"
            TextoArquivo.append(textoImpressao)
            textoImpressao = "Impresso no arquivo: " + CYAN + textoImpressao + RESET
        elif id['tipo'] == "real":
            textoImpressao = 'scanf("%lf", &' + id['lexema'] + ");"
            TextoArquivo.append(textoImpressao)
            textoImpressao = "Impresso no arquivo: " + CYAN + textoImpressao + RESET
        
        # id sem tipo, logo variável que não foi declarada
        else:
            textoImpressao = RED + "Erro Semântico: " + RESET + BOLD + "Variável não declarada!\n" + "Linha: " + RESET + id["linha"] + BOLD + " Coluna: " + RESET + id["coluna"] 
            flagErro = True
        imprimirTerminal(textoImpressao)

    # ES -> escreva ARG;        
    elif t == 12:

        # Desempilha dois símbolos para chegar no arg
        arg = tokensParaValidacao.pop()
        arg = tokensParaValidacao.pop()

        # Verificações para saber qual opção do scanf imprimir no arquivo
        # Se for literal, não é necessário imprimir as aspas, que já estão no lexema
        if arg['token'] == 'Literal':
            textoImpressao = "printf("+ arg['lexema']+");"
        elif arg['token'] == "id":
            if arg["tipo"] == 'int':
                textoImpressao = 'printf("%d", ' + arg['lexema']+');'
            elif arg["tipo"] == 'real':
                textoImpressao = 'printf("%lf", ' + arg['lexema']+');'
            elif arg["tipo"] == 'literal':
                textoImpressao = 'printf("%s", ' + arg['lexema']+');'

        # Testa se o tipo não é vazio, ou seja, a variável a ser impressa não é vazia
        if arg['tipo']:
            TextoArquivo.append(textoImpressao)
            imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)
    
    # ARG -> literal
    elif t == 13:
        literal = tokensParaValidacao.pop()
        Tupla['token'] = literal['token']
        Tupla['tipo'] = literal['tipo']
        Tupla['linha'] = literal['linha']
        Tupla['coluna'] = literal['coluna']
        Tupla['lexema'] = literal['lexema']
    
    # ARG -> num
    elif t == 14:
        num = tokensParaValidacao.pop()
        Tupla['token'] = num['token']
        Tupla['tipo'] = num['tipo']
        Tupla['linha'] = num['linha']
        Tupla['coluna'] = num['coluna']
        Tupla['lexema'] = num['lexema']

    # ARG -> id
    elif t == 15:
        id = tokensParaValidacao.pop()

        # Verificar se o identificador foi declarado
        if id['tipo'] != "null":
            Tupla['token'] = id['token']
            Tupla['tipo'] = id['tipo']
            Tupla['linha'] = id['linha']
            Tupla['coluna'] = id['coluna']
            Tupla['lexema'] = id['lexema']
        else:
            imprimirTerminal(RED + "Erro Semântico: " + RESET + BOLD + "Variável não declarada!\n" + "Linha: " + RESET + id["linha"] + BOLD + " Coluna: " + RESET + id["coluna"])
            flagErro = True
    # CMD -> id rcb LD;
    elif t == 17:
        id = tokensParaValidacao.pop()
        rcb = tokensParaValidacao.pop()
        LD = tokensParaValidacao.pop()

        # Verifica se o identificador foi declarado
        if id['tipo'] != "null":
            if id['tipo'] == LD['tipo']:
                textoImpressao = id['lexema'] + " " + rcb['tipo'] + " " + LD['lexema'] + ";"
                TextoArquivo.append(textoImpressao)
                textoImpressao = "Impresso no arquivo: " + CYAN + textoImpressao + RESET
            else:
                textoImpressao = RED + "Erro Semântico: " + RESET + BOLD + "Tipos diferentes para atribuição.\n" + "Linha: " + RESET + id["linha"] + BOLD + " Coluna: " + RESET + id["coluna"]
                flagErro = True
                imprimirTerminal(textoImpressao)
        else:
            textoImpressao = RED + "Erro Semântico: " + RESET + BOLD + "Variável não declarada!\n" + "Linha: " + RESET + id["linha"] + BOLD + " Coluna: " + RESET + id["coluna"]
            flagErro = True 
        imprimirTerminal(textoImpressao)
    
    # LD -> OPRD1 opm OPRD2;
    elif t == 18:
        
        # Gera variável temporária de acordo com o valor do contador
        imprimirTerminal("Gerada variável temporária: " + GREEN + "T"+str(contadorTemporarias) + RESET)
        OPRD1 = tokensParaValidacao.pop()
        opm = tokensParaValidacao.pop()
        OPRD2 = tokensParaValidacao.pop()
        tipo1 = OPRD1['tipo']
        tipo2 = OPRD2['tipo']

        # Comparação para verificar se os tipos são iguais ou equivalentes
        if (tipo1 == tipo2 or (tipo1 == 'real' and tipo2 == 'int') or (tipo1 == 'int' and tipo2 == 'real')) and tipo1 != "literal":
            
            # Adiciona variável temporária Tx à lista de variáveis
            TextoVariaveisTemporarias.append(str(OPRD2['tipo'])+" T"+ str(contadorTemporarias) +";")
            Tupla['lexema'] = "T"+str(contadorTemporarias)

            # Atribui tipo à Tupla para permitir futuras verificações de tipo
            if(tipo1 == tipo2):
                Tupla["tipo"] = tipo1
            else:
                Tupla["tipo"] = "real"
            textoImpressao = "T"+ str(contadorTemporarias) + " = " + OPRD1['lexema'] + " " + opm['tipo'] + " " + OPRD2['lexema'] + ";"
            TextoArquivo.append(textoImpressao)
            textoImpressao = "Impresso no arquivo: " + CYAN + textoImpressao + RESET
            contadorTemporarias += 1
        
        # Tipos diferentes
        else:
            textoImpressao = RED + "Erro Semântico: " + RESET + BOLD + "Operandos com tipos incompatíveis.\n" + "Linha: " + RESET + OPRD2["linha"] + BOLD + " Coluna: " + RESET + OPRD2["coluna"]
            flagErro = True 
        imprimirTerminal(textoImpressao)
    
    # LD -> OPRD
    elif t == 19:
        OPRD = tokensParaValidacao.pop()
        Tupla['token'] = OPRD['token']
        Tupla['tipo'] = OPRD['tipo']
        Tupla['linha'] = OPRD['linha']
        Tupla['coluna'] = OPRD['coluna']
        Tupla['lexema'] = OPRD['lexema']

    # OPRD -> id
    elif t == 20:
        id = tokensParaValidacao.pop()

        # Verifica se o identificador está declarado
        if id['tipo'] != "null":
            Tupla['token'] = id['token']
            Tupla['tipo'] = id['tipo']
            Tupla['linha'] = id['linha']
            Tupla['coluna'] = id['coluna']
            Tupla['lexema'] = id['lexema']
        else:
            imprimirTerminal(RED + "Erro Semântico: " + RESET + BOLD + "Variável não declarada!\n" + "Linha: " + RESET + id["linha"] + BOLD + " Coluna: " + RESET + id["coluna"])
            flagErro = True
    
    # OPRD -> num
    elif t == 21:
        num = tokensParaValidacao.pop()
        Tupla['token'] = num['token']
        Tupla['tipo'] = num['tipo']
        Tupla['linha'] = num['linha']
        Tupla['coluna'] = num['coluna']
        Tupla['lexema'] = num['lexema']
    
    # COND -> CABEÇALHO CORPO
    elif t == 23:
        textoImpressao = "}"
        TextoArquivo.append(textoImpressao)
        imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)
    
    # CABEÇALHO -> se (EXPR) então
    elif t == 24:
        
        # Desempilha três símbolos para chegar no EXPR
        EXP_R = tokensParaValidacao.pop()
        EXP_R = tokensParaValidacao.pop()
        EXP_R = tokensParaValidacao.pop()
        textoImpressao = "if ("+ EXP_R['lexema']+"){"
        TextoArquivo.append(textoImpressao)
        imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)
    
# EXP_R -> OPRD1 opr OPRD2
    elif t == 25:
        
        # Gera variável temporária de acordo com o valor do contador
        imprimirTerminal("Gerada variável temporária T" + str(contadorTemporarias))
        OPRD1 = tokensParaValidacao.pop()
        opr = tokensParaValidacao.pop()
        OPRD2 = tokensParaValidacao.pop()
        tipo1 = OPRD1['tipo']
        tipo2 = OPRD2['tipo']

        # Comparação para verificar se os tipos são iguais ou equivalentes
        if tipo1 == tipo2 or (tipo1 == 'real' and tipo2 == 'int') or (tipo1 == 'int' and tipo2 == 'real'):
            
            # Adiciona variável temporária Tx à lista de variáveis
            TextoVariaveisTemporarias.append(str(OPRD2['tipo']) + " T" + str(contadorTemporarias) + ";")
            Tupla['lexema'] = "T" + str(contadorTemporarias)
            if(tipo1 == tipo2):
                Tupla["tipo"] = tipo1
            else:
                Tupla["tipo"] = "real"
            textoImpressao = "T" + str(contadorTemporarias) + " = " + OPRD1['lexema'] + " " + opr['tipo'] + " " + OPRD2['lexema'] + ";"
            TextoArquivo.append(textoImpressao)

            # Armazena o valor da EXP_R para permitir o teste da condição dentro do loop
            Tupla['valorEXP'] = textoImpressao
            textoImpressao = "Impresso no arquivo: " + CYAN + textoImpressao + RESET
            contadorTemporarias += 1
            
        else:
            textoImpressao = RED + "Erro Semântico: " + RESET + BOLD + "Operandos com tipos incompatíveis.\n" + "Linha: " + RESET + OPRD2["linha"] + BOLD + " Coluna: " + RESET + OPRD2["coluna"]
            flagErro = True 
        imprimirTerminal(textoImpressao)

    # Regras para o enquanto

    # REPETE -> TESTE AÇÃO
    elif t == 31:
        textoImpressao = "}"
        TextoArquivo.append(textoImpressao)
        imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)
    
    # TESTE -> enquanto (EXP_R) faça
    elif t == 32:
        
        # Desempilha três símbolos para chegar no EXPR
        EXP_R = tokensParaValidacao.pop()
        EXP_R = tokensParaValidacao.pop()
        EXP_R = tokensParaValidacao.pop()
        textoImpressao = "while ("+ EXP_R['lexema']+"){"
        TextoArquivo.append(textoImpressao)
        imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)
        
        # Adiciona a expressão regular no corpo do loop para permitir testar 
        # a condição repetidamente
        if "valorEXP" in EXP_R:
            textoImpressao = EXP_R["valorEXP"]
            TextoArquivo.append(textoImpressao)
            imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)

    # As próximas regras não possuem regras semânticas

    # Retorna tupla para ser empilhada na pilha semântica e prosseguir a análise
    return Tupla
