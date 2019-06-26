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

# Função para imprimir no arquivo .c
def imprimir(texto, arquivo):
    arquivo.write(texto)
    print("mensagem impressa no arquivo: " + texto)
    return

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


def analisadorSemantico(t, A, tokensParaValidacao, arquivoDestino):
    #acho que isso vai dar problema. Temos que fazer isso quando o sintático recebe um token!
    for i in range(0, len(tokensParaValidacao)):
        aux = atribuiTipo(tokensParaValidacao[i])
        tokensParaValidacao[i] = aux

    if t == 5:
        imprimir("\n\n\n", arquivoDestino)
    elif t == 6:
        #D -> id TIPO;
        id = tokensParaValidacao.pop()
        TIPO = tokensParaValidacao.pop()
        id['tipo'] = TIPO['tipo']
        imprimir(TIPO['tipo'] + " " + id['lexema'] + ";")
    elif t == 7:
        inteiro = tokensParaValidacao.pop()
        TIPO = {"lexema": "TIPO", "token": "TIPO", "tipo": inteiro['tipo'], "linha": "","coluna": ""}
    elif t == 8:
        real = tokensParaValidacao.pop()
        TIPO = {"lexema": "TIPO", "token": "TIPO", "tipo": real['tipo'], "linha": "", "coluna": ""}
    elif t == 9:
        literal = tokensParaValidacao.pop()
        TIPO = {"lexema": "TIPO", "token": "TIPO", "tipo": literal['tipo'], "linha": "", "coluna": ""}
    elif t == 11:
        #ES -> leia id;
        #desempilhar dois símbolos, para chegar no id
        id = tokensParaValidacao.pop()
        id = tokensParaValidacao.pop()

        if id['tipo'] == "literal":
            imprimir("scanf(“%s”, " + id['lexema'] + ");",arquivoDestino)
        elif id['tipo'] == "inteiro":
            imprimir("scanf(“%d”, &" + id['lexema'] + ");",arquivoDestino)
        elif id['tipo'] == "real":
            imprimir("scanf(“%lf”, &" + id['lexema'] + ");", arquivoDestino)
        else:
            print("Erro: Variável não declarada!")
    elif t == 12:
        # desempilhar dois símbolos, para chegar no arg
        arg = tokensParaValidacao.pop()
        arg = tokensParaValidacao.pop()
        imprimir("printf(\""+arg['lexema']+"\");", arquivoDestino)
    
    return