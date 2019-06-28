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

def imprimirArquivo(arquivoDestino):
    arquivoDestino.write()
    return
def analisadorSemantico(t, A, tokensParaValidacao):
    
    if t == 5:
        TextoArquivo.append("\n\n\n")
    elif t == 6:
        #D -> id TIPO;
        id = tokensParaValidacao.pop()
        TIPO = tokensParaValidacao.pop()
        id['tipo'] = TIPO['tipo']
        TextoArquivo.append(TIPO['tipo'] + " " + id['lexema'] + ";")
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
    
    return