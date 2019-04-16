# Universidade Federal de Goiás
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


def analisadorLexico(arquivo):

    ##Leitura caractere a caractere
    while 1:
        char = arq.read(1)
        print(char)
        if not char: break


#para testes
arq = open("./teste.mgol", encoding="utf8")
analisadorLexico(arq)
arq.close()