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
        tokenTupla['tipo'] = tokenTupla.lexema
    elif tokenTupla['token'] == 'lit':
        tokenTupla['tipo'] = 'literal'
    elif tokenTupla['token'] == 'inteiro':
        tokenTupla['tipo'] = 'int'
    elif tokenTupla['token'] == 'real':
        tokenTupla['tipo'] = 'real'
    elif tokenTupla['token'] == 'OPR':
        tokenTupla['tipo'] = tokenTupla.lexema
    elif tokenTupla['token'] == 'RCB':
        tokenTupla['tipo'] = '='
    return tokenTupla

def imprimirArquivo(nomeArquivoDestino):
    arqDestino = open(str(nomeArquivoDestino)+".c", "w+")

    #imprimindo cabeçalho
    arqDestino.write("#include<stdio.h>")
    arqDestino.write("typedef char literal[256];")
    arqDestino.write("void main(void){")

    #imprimindo variáveis temporárias
    arqDestino.write("\t/*----Variaveis temporarias----*/")
    for texto in TextoVariaveisTemporarias:
        arqDestino.write("\t"+str(texto))
    arqDestino.write("\t/*------------------------------*/")

    #imprimindo corpo do texto
    for texto in TextoArquivo:
        arqDestino.write("\t"+str(texto))

    #fim do arquivo
    arqDestino.write("}")

    arqDestino.close()
    return

#função que dá o nome para o não terminal que será retornada pelo analisador semântico
def naoTerminal(t):
    if t == 1:
        return "P'"
    elif t == 2:
        return "P"
    elif t == 3:
        return "V"
    elif t == 4 or t == 5:
        return "LV"
    elif t == 6:
        return "D"
    elif t == 7 or t == 8 or t == 9:
        return "TIPO"
    elif t == 10 or t == 16 or t == 22 or t == 30:
        return "A"
    elif t == 11 or t == 12:
        return "ES"
    elif t == 13 or t == 14 or t == 15:
        return "ARG"
    elif t == 17:
        return "CMD"
    elif t == 18 or t == 19:
        return "LD"
    elif t == 20 or t == 21:
        return "OPRD"
    elif t == 23:
        return "COND"
    elif t == 24:
        return "CABEÇALHO"
    elif t == 25:
        return "EXPR"
    elif t == 26 or t == 27 or t == 28 or t == 29:
        return "CORPO"


def analisadorSemantico(t, A, tokensParaValidacao, TabelaSimbolos):
    Tupla = {"lexema": naoTerminal(t), "token": naoTerminal(t), "tipo": "", "linha": "", "coluna": ""}

    #para testes:
    print("Não-Terminal da regra: " + Tupla['lexema'])

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
        TextoArquivo.append("printf(\""+arg['lexema']+"\");")
    elif t == 13:
        literal = tokensParaValidacao.pop()
        Tupla['token'] = literal['token']
        Tupla['tipo'] = literal['tipo']
        Tupla['linha'] = literal['linha']
        Tupla['coluna'] = literal['coluna']
    elif t == 14:
        num = tokensParaValidacao.pop()
        Tupla['token'] = num['token']
        Tupla['tipo'] = num['tipo']
        Tupla['linha'] = num['linha']
        Tupla['coluna'] = num['coluna']
    elif t == 15:
        id = tokensParaValidacao.pop()

        #verificar se o identificador foi declarado
        if id['tipo']:
            Tupla['token'] = id['token']
            Tupla['tipo'] = id['tipo']
            Tupla['linha'] = id['linha']
            Tupla['coluna'] = id['coluna']
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

        # LD -> OPRD1 opm OPRD2;
        OPRD1 = tokensParaValidacao.pop()
        opm = tokensParaValidacao.pop()
        OPRD2 = tokensParaValidacao.pop()

        if OPRD1['tipo'] == OPRD2['tipo'] and OPRD1['tipo'] != "literal":
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
    elif t == 20:
        id = tokensParaValidacao.pop()

        #verificar se o identificador está declarado
        if id['tipo']:
            Tupla['token'] = id['token']
            Tupla['tipo'] = id['tipo']
            Tupla['linha'] = id['linha']
            Tupla['coluna'] = id['coluna']
        else:
            print("Erro: Variável não declarada!")
    return Tupla
