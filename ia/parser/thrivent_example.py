import nltk

SENTENCE = "Thrivent helps people"

TERMINALS = """
# Noun
    N -> 'Thrivent' | 'people' | 'savings'

# Verb
    V -> 'helps'

# Preposition
    P -> 'with'
"""

NONTERMINALS = """
# Sentence
    S -> NP VP

# Verb phrase
    VP -> V NP | V NP PP

# Noun phrase
    NP ->  N | N PP

# Prepositional phrase
    PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

for tree in parser.parse(SENTENCE.split()):
    print(tree)
    tree.pretty_print()
