Universidade Federal de Santa Catarina - UFSC
Departamento de Inform�tica e Estat�stica - INE
Gustavo In�cio Raimundo
10 de maio de 2019

Linguagem Utilizada: Python

Bibliotecas Utilizadas: Pikle(Serialization), Tkinter(GUI)

Como utilizar:
Para rodar qualquer teste � s� utilizar o comando "py <nome-do-teste>"

Para utilizar o programa � s� clicar 2 vezes no "main.py" da pasta 'Aplica��o'
ou rodar utilizando o comando "py main.py"

Detalhes:
A parte de GUI inclui todos os arquivos: main.py, mainview.py, menus.py,
automata_gui.py, grammar_gui.py e regex_gui.py
Nestes arquivos tem o programa que est� rodando em cima de uma "biblioteca" em
imports/finiteautomaton.py
Na biblioteca existem todas as representa��es de Automato Finito (Deterministico
e Nao-Deterministico), Gramatica Regular e Express�o Regular e todos os m�todos:
convers�o, carregar de arquivo, adicionar/remover elementos.

Estruturas de Datos utilizadas:
Para cria��o de um AFD foi utilizado um dicion�rio de dicion�rios com chaves e
valores no seguinte formato:
{
  "Estado1": {
    "Transi��o-a": "Estado2",
    "Transicao-b": "Estado2"
  },
  "Estado2": {
    "Transi��o-a": "Estado1",
    "Transi��o-b": "Estado2"
  }
}
Um AFND usa uma estrutura similar com diferen��o que quando tem uma transi��o,
ao inv�s de retornar um Estado, ele retorna um set() de estados.

Os AF possuem um set() para estados de aceita��o.

Utiliza-se set() ao inv�s de list() pois a ordem n�o importa e n�o queremos
repetir o mesmo estado(tendo vista que o set() possui o elemento).


Para cria��o de uma Gramatica Regular foi utilizado novamente um dicion�rio,
mas cada n�o terminal possui um list de produ��es

{
  NT1: [ prod1NT1, prod2NT2 ],
  NT2: [ prod3NT2, prod4 ]
}

Uma produ��o � uma concatena��o de um string terminal (minusculo) com um String
nao-terminal (maiusculo) sendo que o n�o-terminal pode ou nao ser nulo.

Cada produ��o tem um ID q � utilizado para gera��o de palavras da Gramatica

Para cria��o de uma Express�o regular � utilizada um set() onde ocorrem as unions
e quando ocorre outra opera��o, essa union � formada com parenteses e � utilizada
como nova express�o regular para as outras opera��es.
