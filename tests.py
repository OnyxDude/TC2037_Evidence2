# Import the parser
from esperanto import parser

def test_esperanto_sentence(sentence, expected_valid=True):
    # tokenize the sentence
    words = sentence.lower().split()
    
    # Parse the sentence and print the result
    try:
        trees = list(parser.parse(words))
        if trees:
            if expected_valid:
                print(f"✓ '{sentence}' - Valid")
                return True
            else:
                print(f"✗ '{sentence}' - Should be invalid but was accepted")
                return False
        else:
            if expected_valid:
                print(f"✗ '{sentence}' - Should be valid but was rejected")
                return False
            else:
                print(f"✓ '{sentence}' - Correctly rejected")
                return True
    except ValueError as e:
        if expected_valid:
            print(f"✗ '{sentence}' - Should be valid but got error: {e}")
            return False
        else:
            print(f"✓ '{sentence}' - Correctly rejected")
            return True

def run_tests():
    # Running a set of tests to check the Esperanto grammar
    print("Running Esperanto Grammar Tests...\n")

    # Valid strings
    print("=== Valid Sentences ===")
    test_esperanto_sentence("la kato dormas")
    test_esperanto_sentence("la libro legas")
    test_esperanto_sentence("la hundo kuras")
    test_esperanto_sentence("la viro parolas")
    test_esperanto_sentence("viro legas libro")
    test_esperanto_sentence("hundo kuras rapide")
    test_esperanto_sentence("la kato dormas bone")
    test_esperanto_sentence("la libro legas klare")
    test_esperanto_sentence("la nova viro skribas")
    test_esperanto_sentence("la granda viro manĝas")
    test_esperanto_sentence("la viro parolas forte")
    test_esperanto_sentence("la rapida hundo kuras")
    test_esperanto_sentence("la granda kato dormas")
    test_esperanto_sentence("la hundo kuras rapide")
    test_esperanto_sentence("la viro legas la libro")
    test_esperanto_sentence("la hundo manĝas la kato")
    test_esperanto_sentence("la rapida hundo kuras bone")
    test_esperanto_sentence("la verda pomo parolas rapide")
    test_esperanto_sentence("la granda kato dormas silente")
    test_esperanto_sentence("la blua floro manĝas la granda hundo")
    
    # Invalid strings
    print("\n=== Invalid Sentences ===")
    test_esperanto_sentence("hundoj kuras.", expected_valid=False)
    test_esperanto_sentence("la viro hundo", expected_valid=False)
    test_esperanto_sentence("la kuras hundo", expected_valid=False)
    test_esperanto_sentence("hundo la kuras", expected_valid=False)
    test_esperanto_sentence("la hundoj kuras", expected_valid=False)
    test_esperanto_sentence("la hundo kuras la", expected_valid=False)
    test_esperanto_sentence("rapide kuras hundo", expected_valid=False)
    test_esperanto_sentence("hundo dormas rapida", expected_valid=False)
    test_esperanto_sentence("rapida la hundo kuras", expected_valid=False)
    test_esperanto_sentence("la hundo la kato kuras", expected_valid=False)
    test_esperanto_sentence("La hundo estas rapida.", expected_valid=False)
    test_esperanto_sentence("la grandaj hundoj kuras", expected_valid=False)
    test_esperanto_sentence("la hundo manĝas la katon", expected_valid=False)
    test_esperanto_sentence("la hundo kuras al la domo", expected_valid=False)
    test_esperanto_sentence("La hundo manĝas la katojn.", expected_valid=False)
    test_esperanto_sentence("La hundo kuras tre rapide.", expected_valid=False)
    test_esperanto_sentence("la hundo kuras rapide bone", expected_valid=False)
    test_esperanto_sentence("La hundo kaj la kato dormas.", expected_valid=False)
    test_esperanto_sentence("la hundo kuras rapide en la domo", expected_valid=False)
    test_esperanto_sentence("La hundo manĝas la grandan katon", expected_valid=False)

if __name__ == "__main__":
    run_tests()