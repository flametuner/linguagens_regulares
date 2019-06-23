Universidade Federal de Santa Catarina - UFSC
Departamento de Informática e Estatística - INE
Gustavo Inácio Raimundo
10 de maio de 2019

Linguagem Utilizada: Python

Bibliotecas Utilizadas: Pikle(Serialization), Tkinter(GUI)

Como utilizar:
Para rodar qualquer teste é só utilizar o comando "py <nome-do-teste>"

Para utilizar o programa é só clicar 2 vezes no "main.py" da pasta 'Aplicação'
ou rodar utilizando o comando "py main.py"

Detalhes:
A parte de GUI inclui todos os arquivos: main.py, mainview.py, menus.py,
automata_gui.py, grammar_gui.py e regex_gui.py
Nestes arquivos tem o programa que está rodando em cima de uma "biblioteca" em
imports/finiteautomaton.py
Na biblioteca existem todas as representações de Automato Finito (Deterministico
e Nao-Deterministico), Gramatica Regular e Expressão Regular e todos os métodos:
conversão, carregar de arquivo, adicionar/remover elementos.

Estruturas de Datos utilizadas:
Para criação de um AFD foi utilizado um dicionário de dicionários com chaves e
valores no seguinte formato:
{
  "Estado1": {
    "Transição-a": "Estado2",
    "Transicao-b": "Estado2"
  },
  "Estado2": {
    "Transição-a": "Estado1",
    "Transição-b": "Estado2"
  }
}
Um AFND usa uma estrutura similar com diferenção que quando tem uma transição,
ao invés de retornar um Estado, ele retorna um set() de estados.

Os AF possuem um set() para estados de aceitação.

Utiliza-se set() ao invés de list() pois a ordem não importa e não queremos
repetir o mesmo estado(tendo vista que o set() possui o elemento).


Para criação de uma Gramatica Regular foi utilizado novamente um dicionário,
mas cada não terminal possui um list de produções

{
  NT1: [ prod1NT1, prod2NT2 ],
  NT2: [ prod3NT2, prod4 ]
}

Uma produção é uma concatenação de um string terminal (minusculo) com um String
nao-terminal (maiusculo) sendo que o não-terminal pode ou nao ser nulo.

Cada produção tem um ID q é utilizado para geração de palavras da Gramatica

Para criação de uma Expressão regular é utilizada um set() onde ocorrem as unions
e quando ocorre outra operação, essa union é formada com parenteses e é utilizada
como nova expressão regular para as outras operações.
