import nltk
from nltk import CFG, ChartParser

# Define the context-free grammar
esperanto_grammar = CFG.fromstring("""
    S -> NP VP | NP VP NP
    NP -> DET_PHRASE | N
    DET_PHRASE -> DET N | DET ADJ_PHRASE
    ADJ_PHRASE -> ADJ N
    VP -> V_ONLY | V_ADV
    V_ONLY -> V
    V_ADV -> V ADV | ADV V
    
    N -> 'hundo' | 'kato' | 'libro' | 'viro' | 'domo' | 'tablo' | 'pomo' | 'floro'
    ADJ -> 'rapida' | 'granda' | 'bela' | 'verda' | 'blua' | 'nova'
    V -> 'kuras' | 'manĝas' | 'dormas' | 'legas' | 'parolas' | 'skribas'
    ADV -> 'rapide' | 'bone' | 'klare' | 'forte' | 'silente'
    DET -> 'la'
""")

# Create a parser with the defined grammar
parser = ChartParser(esperanto_grammar)

def test_esperanto_sentence(sentence):

    # Tokenize the sentence
    words = sentence.lower().split()

    # Parse the sentence
    try:
        trees = list(parser.parse(words))
        if trees:
            print(f"LL(1) Parsing for '{sentence}':")
            trees[0].pretty_print()
            return True
        for tree in trees:
            tree.pretty_print()
        else:
            print(f"'{sentence}' does not match our Esperanto grammar.")
            return False
    except:
        print(f"Error parsing '{sentence}'")
        return False

if __name__ == "__main__":
    print("Enter Esperanto sentences to test (type 'exit' to quit):")
    
    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            break
        result = test_esperanto_sentence(user_input)
        print(f"Result: {result}")
        print("\n")