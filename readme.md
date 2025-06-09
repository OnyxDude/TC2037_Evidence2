# Evidence 2: Generating and Cleaning a Restricted Context Free Grammar - A07184003

## Description

### The language I chose is **Esperanto**

According to Grin (2005) is "the most widely spoken constructed international auxiliary language in the world." Created by L. L. Zamenhof in 1887, Esperanto was designed with regular grammar patterns and predictable rules to make it relatively easy to learn.

Here are some interesting and distinctive grammatical features in Esperanto:

1.  Word endings that indicate part of speech:
    * Nouns end in -o (libro = book)
    * Adjectives end in -a (rapida = fast)
    * Adverbs end in -e (rapide = quickly)
    * Present tense verbs end in -as (kuras = runs)

2.  Regular plural formation:
    * All plurals are formed by adding -j to nouns and adjectives (libroj = books)
    * No irregular plurals exist in the language

3.  Accusative case marking:
    * Direct objects are marked with the -n ending (Mi legas libron = I read a book)
    * This allows for flexible word order while maintaining clarity

### Basic syntax rules

To better understand how Esperanto forms sentences, here are the basic rules that I will model in the grammar according to the official Esperanto page (Esperanto Grammar, n.d.):

1.  Basic sentence structure follows Subject-Verb-Object (SVO) order, though other orders are grammatically possible due to the accusative marking.

2.  Adjectives can precede or follow the nouns they modify and must agree in number and case.

3.  Adverbs typically precede the verbs they modify, but this is flexible.

4.  The definite article "la" precedes the noun and is invariable (doesn't change for gender, number, or case).

### List of words that will be used

**Nouns**
* `hundo:` dog
* `kato:` cat
* `libro:` book
* `viro:` man
* `domo:` house
* `tablo:` table

**Adjectives**
* `rapida:` fast
* `granda:` big
* `bela:` beautiful
* `verda:` green
* `blua:` blue

**Verbs**
* `kuras:` to run (present tense)
* `manĝas:` to eat (present tense)
* `dormas:` to sleep (present tense)
* `legas:` to read (present tense)
* `parolas:` to speak (present tense)

**Adverbs**
* `rapide:` quickly
* `bone:` well
* `klare:` clearly
* `forte:` strongly

**Determiners**
* `la:` the

## Models
### Grammar Model that Recognizes the Language (initial grammar)

```
S → NP VP
NP → DET ADJ NP | DET NP | ADJ NP | N
VP → VP ADV | V ADV | ADV | V
N → 'hundo' | 'kato' | 'libro' | 'viro' | 'domo' | 'tablo' | 'pomo' | 'floro'
ADJ → 'rapida' | 'granda' | 'bela' | 'verda' | 'blua' | 'nova'
V -> 'kuras' | 'manĝas' | 'dormas' | 'legas' | 'parolas' | 'skribas'
ADV -> 'rapide' | 'bone' | 'klare' | 'forte' | 'silente'
DET -> 'la'
```

This initial grammar has both left recursion and ambiguity issues that prevent it from being an LL(1) grammar. Let me explain each issue:

#### 1. Left Recursion

Because the grammar has left recursion in a rule:

* `VP → VP ADV`: The non-terminal VP appears at the left position.

Left recursion causes problems for LL(1) parsers because it leads to infinite recursion. For example, when trying to parse the rule `VP → VP ADV`, the parser would keep applying the same rule infinitely.

#### 2. Ambiguity Issue

Because the NP state has multiple ways to derive the same string. For example, "La rapida hundo kuras rapide" could be derived in different ways:

```
            S 
    ________|________
    NP            __VP__
 ___|_____        |     |
DET      NP       V    ADV
 |    ___|____    |     |
 |   ADJ    NP    |     |
 |    |     |     |     |
 |    |     N     |     |
 |    |     |     |     |
la rapida hundo kuras rapide
```

```
            S 
    ________|________
    NP            __VP__
 ___|________     |     |
DET  ADJ    NP    V    ADV
 |    |     |     |     |
 |    |     N     |     |
 |    |     |     |     |
la rapida hundo kuras rapide
```

The parse trees above illustrate the ambiguity problem in our initial grammar. For the noun phrase "La rapida hundo kuras rapide", we have multiple ways to derive this structure:

1. We could first apply `NP → DET ADJ NP`, which directly creates the entire noun phrase.
2. Or we could apply a sequence like `NP → DET NP` followed by the adjective and noun.

This grammar results unsuitable for LL(1) parsing because the parser cannot choose which rule to apply when it sees "la" at the beginning of a sentence.

### Eliminate Ambiguity and Left Recursion (final grammar)

#### Step 1: Eliminating Left Recursion

Left recursion occurs when a non-terminal appears as the leftmost symbol in its own production rule. In our grammar, this happens in the VP rule:

```
VP → VP ADV | V ADV | ADV | V
```

This is problematic because an LL(1) parser would enter an infinite loop when trying to expand VP.

To eliminate left recursion, I applied the standard technique from compiler theory (Aho, Sethi & Ullman, 1986) that transforms left-recursive rules into non-recursive equivalents:

1. Identify the recursive parts (VP → VP ADV) and non-recursive parts (VP → V ADV | ADV | V)
2. Create a new non-terminal VP' to handle the repetition
3. Rewrite the rule using the new non-terminal

This transforms our VP rule into:

```
VP → V VP' | ADV VP'
VP' → ADV VP' | ε
```

Where VP' represents "optional additional adverbs" and ε represents the empty string (nothing).

This later translates into a similar implementation when removing ambiguity:
```
VP → V | V_ADV
V_ADV → V ADV | ADV V
```

#### Step 2: Eliminating Ambiguity

Moving on to the next step, eliminating ambiguity, to achieve this, we need to add intermediate states and productions that indicate a precedence. The new version without ambiguity looks like the following:

```
S → NP VP | NP VP NP
NP → DET_PHRASE | N
DET_PHRASE → DET N | DET ADJ_PHRASE
ADJ_PHRASE → ADJ N
VP → V | V_ADV
V_ADV → V ADV | ADV V
N → 'hundo' | 'kato' | 'libro' | 'viro' | 'domo' | 'tablo' | 'pomo' | 'floro'
ADJ → 'rapida' | 'granda' | 'bela' | 'verda' | 'blua' | 'nova'
V -> 'kuras' | 'manĝas' | 'dormas' | 'legas' | 'parolas' | 'skribas'
ADV -> 'rapide' | 'bone' | 'klare' | 'forte' | 'silente'
DET -> 'la'
```

This new grammar ensures that there's only one way to derive noun phrases with determiners and adjectives. The explanation of the grammar is the following:

1.  `S → NP VP | NP VP NP`: A sentence consists of a noun phrase and a verb phrase, or a noun phrase, a verb phrase, and another noun phrase.
2.  `NP → DET_PHRASE | N`: A noun phrase can be either a determiner phrase or just a noun.
3.  `DET_PHRASE → DET N | DET ADJ_PHRASE`: A determiner phrase consists of a determiner followed by either a noun or an adjective phrase.
4.  `ADJ_PHRASE → ADJ N`: An adjective phrase consists of an adjective followed by a noun.
5.  `VP → V | V_ADV`: A verb phrase can be either a verb alone or a verb with an adverb.
6.  `V_ADV → V ADV | ADV V`: A verb-adverb phrase consists of either a verb followed by an adverb or an adverb followed by a verb.
7.  `N, ADJ, V, ADV, DET`: Terminal symbols representing the respective parts of speech.

```
                            S                     
         ___________________|___________           
        NP                              |         
        |                               |          
    DET_PHRASE                          VP        
  ______|__________                     |          
 |             ADJ_PHRASE             V_ADV       
 |       __________|________       _____|_____     
DET    ADJ                  N     V          ADV  
 |      |                   |     |           |    
 la   rapida              hundo kuras       rapide
```

This parse tree demonstrates how our restructured grammar eliminates the ambiguity. By introducing intermediate non-terminals like `DET_PHRASE`, `ADJ_PHRASE`, `V_ONLY`, and `V_ADV`, we create a clear hierarchical structure that ensures only one possible derivation for any valid string.

For noun phrases, we now have a clearer hierarchy:
- A noun phrase (`NP`) is either a determiner phrase (`DET_PHRASE`) or a standalone noun.
- A determiner phrase includes a determiner followed by either a simple noun or an adjective phrase.
- An adjective phrase combines an adjective with a noun.

Similarly for verb phrases, the structure is now well-defined:
- A verb phrase (`VP`) is either a simple verb (`V_ONLY`) or a verb with an adverb (`V_ADV`).
- The verb-adverb combination has clear rules for both possible word orders (V ADV or ADV V).

This restructuring eliminates ambiguity completely, making it suitable/ready for LL(1) parser.

## Implementation

To implement a tester for my grammar, I made a python program using NLTK that validates Esperanto sentences against the grammar made and generates parse trees for valid sentences

* The implementation is found in the `esperanto.py` file.
* To check if a sentence is valid in the language, simply run the program and type in the sentence into the terminal:

    ```python
    > python esperanto.py
    > la viro legas
    # this should return true because its valid in the grammar
    Result: True
    ```

* Some examples of inputs and outputs:

    ```python
    viro legas   # true
    la viro legas  # true
    la viro la libro   # false
    hundo dormas rapida   # false
    la bela viro parolas bone  # true
    ```

* To exit the program simply type in 'exit'

## Tests

The file `tests.py` contains the set of tests I could think of for my grammar.

The set of tests show both positive cases (sentences that should be accepted) and negative cases (strings that should be rejected), as requested.

### Correct Sentences

1.  `la hundo kuras`: The dog runs.
2.  `hundo kuras rapide`: A dog runs quickly.
3.  `la rapida kato dormas`: The fast cat sleeps.
4.  `viro legas libro`: A man reads a book.
5.  `la granda viro manĝas`: The big man eats.
6.  `hundo manĝas la verda libro`: A dog eats the green book.
7.  `la bela viro parolas bone`: The handsome man speaks well.
8.  `la hundo kuras rapide`: The dog runs quickly.
9.  `viro legas la granda libro`: A man reads the big book.

### Incorrect Sentences

1.  `la kuras hundo`: Incorrect word order.
2.  `hundo la kuras`: Determiner in wrong position.
3.  `rapida la hundo kuras`: Adjective before determiner.
4.  `hundo dormas rapida`: Adjective used where adverb needed.
5.  `la hundo la kato kuras`: Multiple determiners incorrectly used.
6.  `la hundo kuras la`: Sentence ending with determiner.

### LL1 Parsing Example

Here are parse trees for some of the valid sentences, showing the output of the program:

```
LL(1) Parsing for 'viro legas':
      S        
  ____|____     
 |         VP  
 |         |    
 NP      V_ONLY
 |         |    
 N         V   
 |         |    
viro     legas 
```

```
LL(1) Parsing for 'la bela viro parolas bone':
                           S                     
         __________________|_____________         
        NP                               |       
        |                                |        
    DET_PHRASE                           VP      
  ______|__________                      |        
 |             ADJ_PHRASE              V_ADV     
 |       __________|_______        ______|____    
DET    ADJ                 N      V          ADV 
 |      |                  |      |           |   
 la    bela               viro parolas       bone
```

```
LL(1) Parsing for 'la viro legas':
                S         
         _______|_____     
        NP            VP  
        |             |    
    DET_PHRASE      V_ONLY
  ______|_______      |    
DET             N     V   
 |              |     |    
 la            viro legas 
```

```
LL(1) Parsing for 'hundo kuras rapide':
        S               
   _____|_____           
  |           VP        
  |           |          
  NP        V_ADV       
  |      _____|_____     
  N     V          ADV  
  |     |           |    
hundo kuras       rapide
```

## Analysis

The level of the grammar in Chomsky’s hierarchy before and after the elimination of Ambiguity and left recursion is gonna stay the same, since the changes to the grammar were only to resolve ambiguity.

### Chomsky Hierarchy Level Before

Before eliminating ambiguity and left recursion, in the Chomsky hierarchy, this grammar would fall into the **Context-Free Grammar** (Type 2). Even with the ambiguity in the NP rule and the left recursion in both NP and VP rules, it still adheres to the characteristics of a context-free grammar.

### Chomsky Hierarchy Level After

After eliminating ambiguity and left recursion, the grammar is still a **Context-Free Grammar** (Type 2), the type of grammar stays the same in the Chomsky hierarchy. The elimintaion of ambiguity and left recursion is a technique for preparing context-free grammars for LL(1) parsing but it doesnt change their chomsky hierarchy level.

### Time Implications of Chomsky Hierarchy Levels

Based on research from various sources (Recursive and Recursively Enumerable Languages, 2023; Recursive Enumeration and Hierarchies, 2023), here are the time complexity implications for each level in the Chomsky hierarchy:

* **Regular Grammars (Type 3):**
    * Parsing/recognition is very efficient, typically **O(n) (linear)** time complexity, where *n* is the length of the input string.
    * **Example:** Identifiers.
    * **String Example:** `abc123`

* **Context Free (Type 2):**
    * Parsing is generally more complex than regular languages. It has a time complexity of **O(n³) (polynomial)**.
    * **Example:** Programming Languages (no ambiguity).
    * **String Example:** `a girl with a hat on her head`

* **Context Sensitive (Type 1):**
    * Parsing is even more complex. Time complexity is **NP complete (exponential)**.
    * **Example:** Natural Languages (ambiguity).
    * **String Example:** `John likes Mary. - John like Mary.`

* **Recursively Enumerable (Type 0):**
    * Parsing is the most complex. It is possible that the algorithm will never end, therefore the time complexity is undecidable (Google Document on Recursive Languages, n.d.).
    * **Example:** Complex Math theories.
    * **String Example:** I couldnt really think of one, and investigating i found the following, althought its still not very clear: `𝐿={𝑥𝑖∣𝑥𝑖∉𝐿(𝐺𝑖)}.` (Is there an example of a recursive language which is not context-sensitive?, n.d.).

## References

Aho, A. V., Sethi, R., & Ullman, J. D. (1986). *Compilers: Principles, Techniques, and Tools*. Addison-Wesley.

Esperanto Grammar. (n.d.). Retrieved from [https://esperanto.lingolia.com/en/grammar](https://esperanto.lingolia.com/en/grammar)

Google Document on Recursive Languages. (n.d.). Retrieved from [https://docs.google.com/document/d/1KmtIc94VDAtMQCm0xRqR7cvnKyDVDz_qwU31JokQ-Zw/edit?tab=t.0](https://docs.google.com/document/d/1KmtIc94VDAtMQCm0xRqR7cvnKyDVDz_qwU31JokQ-Zw/edit?tab=t.0)

Is there an example of a recursive language which is not context-sensitive? (n.d.). Retrieved from [https://cs.stackexchange.com/questions/56632/is-there-an-example-of-a-recursive-language-which-is-not-context-sensitive](https://cs.stackexchange.com/questions/56632/is-there-an-example-of-a-recursive-language-which-is-not-context-sensitive)

Recursive and Recursively Enumerable Languages. (2023). Retrieved from [https://btu.edu.ge/wp-content/uploads/2023/07/Lesson-8_-Introduction-to-Recursive-and-Recursively-Enumerable-Languages.pdf](https://btu.edu.ge/wp-content/uploads/2023/07/Lesson-8_-Introduction-to-Recursive-and-Recursively-Enumerable-Languages.pdf)

Recursive Enumeration and Hierarchies. (2023). Retrieved from [https://courses.cs.duke.edu/spring23/compsci334/lects/sectRecEnumH.pdf](https://courses.cs.duke.edu/spring23/compsci334/lects/sectRecEnumH.pdf)