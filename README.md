# regular-language-automata

## Libraries
- Pikle(Serialization)
- Tkinter(GUI)

## How to run:

To run any test, use the command: 
```bash
python <test-name>
```

To use the program, run:
```bash
python main.py
```

## Details
The GUI part includes all the following files:

- `main.py`
- `mainview.py`
- `menus.py`
- `automata_gui.py`
- `grammar_gui.py`
- `regex_gui.py`


These files contain the program running on top of a library in `imports/finiteautomaton.py`.
In the library, all representations of Finite Automata (Deterministic and Non-Deterministic), Regular Grammar, and Regular Expression, as well as all methods for conversion, loading from file, adding/removing elements are stored.

## Data Structures
For creating a DFA, a dictionary of dictionaries with keys and values in the following format was used:

```
{
  "State1": {
    "Transition-a": "State2",
    "Transition-b": "State2"
  },
  "State2": {
    "Transition-a": "State1",
    "Transition-b": "State2"
  }
}
```
An NFA uses a similar structure, with the difference being that when there is a transition, instead of returning a State, it returns a set() of states.

Both DFAs and NFAs have a set() for accepting states.

A set() is used instead of a list() because the order does not matter and we do not want to repeat the same state (since the set() has unique elements).

For creating a Regular Grammar, a dictionary was used again, but each non-terminal has a list of productions:

```
{
  NT1: [ prod1NT1, prod2NT2 ],
  NT2: [ prod3NT2, prod4 ]
}
```
A production is a concatenation of a terminal string (lowercase) and a non-terminal string (uppercase), where the non-terminal can or cannot be null.

Each production has an ID that is used for generating words from the Grammar.

For creating a Regular Expression, a set() is used where unions occur, and when another operation occurs, this union is formed with parentheses and used as a new regular expression for other operations.




