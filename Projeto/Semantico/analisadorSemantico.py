# -*- coding: utf-8 -*-

# # Universidade Federal de Goiás
# Instituto de Informática - INF
# Compiladores - Compilador para MGol
#
# Módulo: Analisador Semantico
#
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

TextoArquivo = []
TextoVariaveisTemporarias = []

#contador para as variáveis temporárias
contadorTemporarias = 0

#flag para avaliar erro semântico
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

def imprimirArquivo(nomeArquivoDestino):

    global flagErro
    print(BOLD + "----------------------------------------------------------------")
    # Houve erros semânticos
    if flagErro:
        print("Análise Semântica finalizada: " + RESET + "foram encontrados erros. " + RED + "Falha!")
    # Análise finalizada sem erros
    else:
        print("Análise Semântica finalizada: " + GREEN + "aceitou!")
    print(RESET + BOLD + "----------------------------------------------------------------")    

    arqDestino = open(str(nomeArquivoDestino)+".c", "w+")

    #imprimindo cabeçalho
    arqDestino.write("#include<stdio.h>\n\n")
    arqDestino.write("typedef char literal[256];\n")
    arqDestino.write("typedef double real;\n\n")
    arqDestino.write("void main(void){\n")

    #imprimindo variáveis temporárias
    arqDestino.write("\t/*----Variaveis temporarias----*/\n")
    for texto in TextoVariaveisTemporarias:
        arqDestino.write("\t"+str(texto)+"\n")
    arqDestino.write("\t/*------------------------------*/\n")

    #contador para identar o código de acordo com o escopo
    contadorIdentacao = 1

    #imprimindo corpo do texto
    for texto in TextoArquivo:

        if "}" in texto:
            contadorIdentacao -= 1
            
        for i in range(0, contadorIdentacao):
            arqDestino.write("\t")
        arqDestino.write(str(texto)+"\n")

        if "{" in texto:
            contadorIdentacao += 1

    #fim do arquivo
    arqDestino.write("}\n")

    arqDestino.close()
    return

def imprimirTerminal(textoImpressao):
    print(BOLD + "\n-----------------------" + " SEMÂNTICO " + "-----------------------")
    print(textoImpressao)
    print(BOLD + "---------------------------------------------------------\n" + RESET)

def analisadorSemantico(t, A, tokensParaValidacao, TabelaSimbolos):
    global flagErro
    global contadorTemporarias
    Tupla = {"lexema": str(A), "token": str(A), "tipo": "", "linha": "", "coluna": ""}

    #para testes:
    #print("Não-Terminal da regra: " + str(Tupla['lexema']))

    if t == 5:
        textoImpressao = "\n\n\n"
        TextoArquivo.append(textoImpressao)
        imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)
    elif t == 6:
        #D -> id TIPO;
        id = tokensParaValidacao.pop()
        TIPO = tokensParaValidacao.pop()
        #-----
        TabelaSimbolos[id['lexema']]['tipo'] = TIPO['tipo']
        #-----
        #id['tipo'] = TIPO['tipo']
        textoImpressao = TIPO['tipo'] + " " + id['lexema'] + ";"
        TextoArquivo.append(TIPO['tipo'] + " " + id['lexema'] + ";")
        imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)
    elif t == 7:
        inteiro = tokensParaValidacao.pop()
        Tupla['tipo'] = inteiro['tipo']
    elif t == 8:
        real = tokensParaValidacao.pop()
        Tupla['tipo'] = real['tipo']
    elif t == 9:
        literal = tokensParaValidacao.pop()
        Tupla['tipo'] = literal['tipo']
    elif t == 11:
        #ES -> leia id;
        #desempilhar dois símbolos, para chegar no id
        id = tokensParaValidacao.pop()
        id = tokensParaValidacao.pop()

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
        else:
            textoImpressao = RED + "Erro Semântico: " + RESET + BOLD + "Variável não declarada!\n" + "Linha: " + RESET + id["linha"] + BOLD + " Coluna: " + RESET + id["coluna"] 
            flagErro = True
        imprimirTerminal(textoImpressao)
            
    elif t == 12:
        # desempilhar dois símbolos, para chegar no arg
        arg = tokensParaValidacao.pop()
        arg = tokensParaValidacao.pop()
        if arg['token'] == 'Literal':
            textoImpressao = "printf("+ arg['lexema']+");"
            TextoArquivo.append(textoImpressao)
        else: 
            textoImpressao = "printf(\""+arg['lexema']+"\");"
            TextoArquivo.append(textoImpressao)
        imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)
    elif t == 13:
        literal = tokensParaValidacao.pop()
        Tupla['token'] = literal['token']
        Tupla['tipo'] = literal['tipo']
        Tupla['linha'] = literal['linha']
        Tupla['coluna'] = literal['coluna']
        Tupla['lexema'] = literal['lexema']
    elif t == 14:
        num = tokensParaValidacao.pop()
        Tupla['token'] = num['token']
        Tupla['tipo'] = num['tipo']
        Tupla['linha'] = num['linha']
        Tupla['coluna'] = num['coluna']
        Tupla['lexema'] = num['lexema']
    elif t == 15:
        id = tokensParaValidacao.pop()

        #verificar se o identificador foi declarado
        if id['tipo'] != "null":
            Tupla['token'] = id['token']
            Tupla['tipo'] = id['tipo']
            Tupla['linha'] = id['linha']
            Tupla['coluna'] = id['coluna']
            Tupla['lexema'] = id['lexema']
        else:
            imprimirTerminal(RED + "Erro Semântico: " + RESET + BOLD + "Variável não declarada!\n" + "Linha: " + RESET + id["linha"] + BOLD + " Coluna: " + RESET + id["coluna"])
            flagErro = True
    elif t == 17:
        #CMD -> id rcb LD;
        id = tokensParaValidacao.pop()
        rcb = tokensParaValidacao.pop()
        LD = tokensParaValidacao.pop()

        # verificar se o identificador foi declarado
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
    elif t == 18:
        #ATENÇÃO: coloquei esse global porquê o compilador brigou kkk se der problema tem que tirar
        contadorTemporarias
        imprimirTerminal("Gerada variável temporária: " + GREEN + "T"+str(contadorTemporarias) + RESET)

        # LD -> OPRD1 opm OPRD2;
        OPRD1 = tokensParaValidacao.pop()
        opm = tokensParaValidacao.pop()
        OPRD2 = tokensParaValidacao.pop()

        tipo1 = OPRD1['tipo']
        tipo2 = OPRD2['tipo']

        #tipos iguais ou equivalentes
        if (tipo1 == tipo2 or (tipo1 == 'real' and tipo2 == 'int') or (tipo1 == 'int' and tipo2 == 'real')) and tipo1 != "literal":
            #gerar uma variável temporária Tx
            TextoVariaveisTemporarias.append(str(OPRD2['tipo'])+" T"+ str(contadorTemporarias) +";")
            Tupla['lexema'] = "T"+str(contadorTemporarias)
            if(tipo1 == tipo2):
                Tupla["tipo"] = tipo1
            else:
                Tupla["tipo"] = "real"
            textoImpressao = "T"+ str(contadorTemporarias) + " = " + OPRD1['lexema'] + " " + opm['tipo'] + " " + OPRD2['lexema'] + ";"
            TextoArquivo.append(textoImpressao)
            textoImpressao = "Impresso no arquivo: " + CYAN + textoImpressao + RESET
            contadorTemporarias += 1
        else:
            textoImpressao = RED + "Erro Semântico: " + RESET + BOLD + "Operandos com tipos incompatíveis.\n" + "Linha: " + RESET + OPRD2["linha"] + BOLD + " Coluna: " + RESET + OPRD2["coluna"]
            flagErro = True 
        imprimirTerminal(textoImpressao)
    elif t == 19:
        OPRD = tokensParaValidacao.pop()
        Tupla['token'] = OPRD['token']
        Tupla['tipo'] = OPRD['tipo']
        Tupla['linha'] = OPRD['linha']
        Tupla['coluna'] = OPRD['coluna']
        Tupla['lexema'] = OPRD['lexema']
    elif t == 20:
        id = tokensParaValidacao.pop()

        #verificar se o identificador está declarado
        if id['tipo'] != "null":
            Tupla['token'] = id['token']
            Tupla['tipo'] = id['tipo']
            Tupla['linha'] = id['linha']
            Tupla['coluna'] = id['coluna']
            Tupla['lexema'] = id['lexema']
        else:
            imprimirTerminal(RED + "Erro Semântico: " + RESET + BOLD + "Variável não declarada!\n" + "Linha: " + RESET + id["linha"] + BOLD + " Coluna: " + RESET + id["coluna"])
            flagErro = True
    elif t == 21:
        num = tokensParaValidacao.pop()

        Tupla['token'] = num['token']
        Tupla['tipo'] = num['tipo']
        Tupla['linha'] = num['linha']
        Tupla['coluna'] = num['coluna']
        Tupla['lexema'] = num['lexema']
    elif t == 23:
        textoImpressao = "}"
        TextoArquivo.append(textoImpressao)
        imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)
    elif t == 24:
        #CABEÇALHO -> se (EXPR) então
        #desempilhar três símbolos para chegar no EXPR
        EXP_R = tokensParaValidacao.pop()
        EXP_R = tokensParaValidacao.pop()
        EXP_R = tokensParaValidacao.pop()

        textoImpressao = "if ("+ EXP_R['lexema']+"){"
        TextoArquivo.append(textoImpressao)
        imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)
    elif t == 25:
        # ATENÇÃO: coloquei esse global porquê o compilador brigou kkk se der problema tem que tirar
        # global contadorTemporarias
        imprimirTerminal("Gerada variável temporária T" + str(contadorTemporarias))

        # EXP_R -> OPRD1 opr OPRD2
        OPRD1 = tokensParaValidacao.pop()
        opr = tokensParaValidacao.pop()
        OPRD2 = tokensParaValidacao.pop()

        tipo1 = OPRD1['tipo']
        tipo2 = OPRD2['tipo']

        # tipos iguais ou equivalentes
        if tipo1 == tipo2 or (tipo1 == 'real' and tipo2 == 'int') or (tipo1 == 'int' and tipo2 == 'real'):
            # gerar uma variável temporária Tx
            TextoVariaveisTemporarias.append(str(OPRD2['tipo']) + " T" + str(contadorTemporarias) + ";")
            Tupla['lexema'] = "T" + str(contadorTemporarias)
            if(tipo1 == tipo2):
                Tupla["tipo"] = tipo1
            else:
                Tupla["tipo"] = "real"
            textoImpressao = "T" + str(contadorTemporarias) + " = " + OPRD1['lexema'] + " " + opr['tipo'] + " " + OPRD2['lexema'] + ";"
            TextoArquivo.append(textoImpressao)
            textoImpressao = "Impresso no arquivo: " + CYAN + textoImpressao + RESET
            contadorTemporarias += 1
        else:
            textoImpressao = RED + "Erro Semântico: " + RESET + BOLD + "Operandos com tipos incompatíveis.\n" + "Linha: " + RESET + OPRD2["linha"] + BOLD + " Coluna: " + RESET + OPRD2["coluna"]
            flagErro = True 
        imprimirTerminal(textoImpressao)

    #regras para o enquanto
    elif t == 31:
        textoImpressao = "}"
        TextoArquivo.append(textoImpressao)
        imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)
    elif t == 32:
        #TESTE -> enquanto (EXP_R) faça
        #desempilhar três símbolos para chegar no EXPR
        EXP_R = tokensParaValidacao.pop()
        EXP_R = tokensParaValidacao.pop()
        EXP_R = tokensParaValidacao.pop()
        textoImpressao = "while ("+ EXP_R['lexema']+"){"
        TextoArquivo.append(textoImpressao)
        imprimirTerminal("Impresso no arquivo: " + CYAN + textoImpressao + RESET)
    # As próximas regras não possuem regras semânticas
    return Tupla
