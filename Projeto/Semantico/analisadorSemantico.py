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

TextoArquivo = []
TextoVariaveisTemporarias = []

#contador para as variáveis temporárias

contadorTemporarias = 0



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

def analisadorSemantico(t, A, tokensParaValidacao, TabelaSimbolos):
    Tupla = {"lexema": str(A), "token": str(A), "tipo": "", "linha": "", "coluna": ""}

    #para testes:
    print("Não-Terminal da regra: " + str(Tupla['lexema']))

    if t == 5:
        TextoArquivo.append("\n\n\n")
    elif t == 6:
        #D -> id TIPO;
        id = tokensParaValidacao.pop()
        TIPO = tokensParaValidacao.pop()
        #-----
        TabelaSimbolos[id['lexema']]['tipo'] = TIPO['tipo']
        #-----
        #id['tipo'] = TIPO['tipo']
        TextoArquivo.append(TIPO['tipo'] + " " + id['lexema'] + ";")
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
            TextoArquivo.append("scanf(“%s”, " + id['lexema'] + ");")
        elif id['tipo'] == "inteiro":
            TextoArquivo.append("scanf(“%d”, &" + id['lexema'] + ");")
        elif id['tipo'] == "real":
            TextoArquivo.append("scanf(“%lf”, &" + id['lexema'] + ");")
        else:
            print("Erro: Variável não declarada!")
    elif t == 12:
        # desempilhar dois símbolos, para chegar no arg
        arg = tokensParaValidacao.pop()
        arg = tokensParaValidacao.pop()
        if arg['token'] == 'Literal':
            TextoArquivo.append("printf("+ arg['lexema']+");")
        else: 
            TextoArquivo.append("printf(\""+arg['lexema']+"\");")
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
        if id['tipo']:
            Tupla['token'] = id['token']
            Tupla['tipo'] = id['tipo']
            Tupla['linha'] = id['linha']
            Tupla['coluna'] = id['coluna']
            Tupla['lexema'] = id['lexema']
        else:
            print("Erro: Variável não declarada!")
    elif t == 17:
        #CMD -> id rcb LD;
        id = tokensParaValidacao.pop()
        rcb = tokensParaValidacao.pop()
        LD = tokensParaValidacao.pop()

        # verificar se o identificador foi declarado
        if id['tipo']:
            if id['tipo'] == LD['tipo']:
                TextoArquivo.append(id['lexema'] + " " + rcb['tipo'] + " " + LD['lexema'] + ";")
            else:
                print("Erro: Tipos diferentes para atribuição.")
        else:
            print("Erro: Variável não declarada!")
    elif t == 18:
        #ATENÇÃO: coloquei esse global porquê o compilador brigou kkk se der problema tem que tirar
        global contadorTemporarias
        print("Gerada variável temporária T"+str(contadorTemporarias))

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
            TextoArquivo.append("T"+ str(contadorTemporarias) + " = " + OPRD1['lexema'] + opm['tipo'] + OPRD2['lexema'] + ";")
            contadorTemporarias += 1
        else:
            print("Erro: Operandos com tipos incompatíveis.")
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
        if id['tipo']:
            Tupla['token'] = id['token']
            Tupla['tipo'] = id['tipo']
            Tupla['linha'] = id['linha']
            Tupla['coluna'] = id['coluna']
            Tupla['lexema'] = id['lexema']
        else:
            print("Erro: Variável não declarada!")
    elif t == 21:
        num = tokensParaValidacao.pop()

        Tupla['token'] = num['token']
        Tupla['tipo'] = num['tipo']
        Tupla['linha'] = num['linha']
        Tupla['coluna'] = num['coluna']
        Tupla['lexema'] = num['lexema']
    elif t == 23:
        
        TextoArquivo.append("}")
    elif t == 24:
        #CABEÇALHO -> se (EXPR) então
        #desempilhar três símbolos para chegar no EXPR
        EXP_R = tokensParaValidacao.pop()
        EXP_R = tokensParaValidacao.pop()
        EXP_R = tokensParaValidacao.pop()

        TextoArquivo.append("if ("+ EXP_R['lexema']+"){")
    elif t == 25:
        # ATENÇÃO: coloquei esse global porquê o compilador brigou kkk se der problema tem que tirar
        global contadorTemporarias
        print("Gerada variável temporária T" + str(contadorTemporarias))

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
            TextoArquivo.append(
                "T" + str(contadorTemporarias) + " = " + OPRD1['lexema'] + opr['tipo'] + OPRD2['lexema'] + ";")
            contadorTemporarias += 1
        else:
            print("Erro: Operandos com tipos incompatíveis.")

        # As próximas regras não possuem regras semânticas
    return Tupla
