# CompiladorMGol

Compilador para a linguagem MGol, construído para a disciplina de Compiladores, do curso de Ciência da Computação, UFG.
O compilador faz as etapas de análise gerando um código intermediário em linguagem C.
Foi desenvolvido utilizando a linguagem Python.


## Arquivos do Projeto
O projeto é desenvolvido utilizando a IDE Pycharm, portanto, existem arquivos próprios desta IDE.
```bash
.
├── Projeto
│   ├── Lexico
│	│   ├── analisadorLexico.py
│	│   ├── tabelaSimbolos.py
│	│   └── tabelaTransicao.py
│   ├── Semantico
│	│   └── analisadorSemantico.py
│   ├── Sintatico
│	│   ├── analisadorSintatico.py
│	│   ├── preencheTabelas.py
│	│   ├── Tabela Sintática - Não- Terminais.csv
│	│   ├── Tabela Sintática - Pânico.csv
│	│   ├── Tabela Sintática - qtd_SimbolosB.csv
│	│   └── Tabela Sintática - Terminais.csv
│   ├── fonte.alg
│   ├── main.py
│   ├── programa.c
│   └── teste.mgol
├── LICENCE
├── LR0.png - autômato utilizado para a geração do analisador sintático
├── DFA_Mgol.pdf - DFA utilizado para a geração do analisador léxico
└── README.md
```
* O código principal é ```main.py```

## Execução
Para execução, usa-se:
```bash
$ python3 main.py nome_do_arquivo.mgol

```

## Licença
[MIT](https://choosealicense.com/licenses/mit/)
