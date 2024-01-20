DIGITS = '0123456789'
UPPER_CASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER_CASE = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET = UPPER_CASE + LOWER_CASE

TT_INT		= 'Integer'
TT_FLOAT    = 'Float'
TT_STRING   = 'String'
TT_CHAR     = 'Character'
TT_COMPL    = 'Complex'
TT_BOOL     = 'Boolean'
TT_SET      = 'Set'
TT_ARR      = 'Array'
TT_PLUS     = 'Addition Operator'
TT_MINUS    = 'Subtraction Operator'
TT_MUL      = 'Multiplication Operator'
TT_DIV      = 'Division Operator'
TT_LPAREN   = 'Left Parenthesis'
TT_RPAREN   = 'Right Parenthesis'
TT_IDENTIFIER = 'Identifier'
TT_KEYWORD = 'Keyword'
TT_RESERVE = 'Reserved Words'
TT_NOISE = 'Noise Words'
TT_LCBRAC = 'Left Curly Bracket'
TT_RCBRAC = 'Right Curly Bracket'
TT_LSQBRAC = 'Left Square Bracket'
TT_RSQBRAC = 'Right Square Bracket'
TT_ASSOP = 'Assignment Operator'

KEYWORDS = {'int', 'float', 'String', 'char', 'bool', 'set', 'array', 'complex', 'let', 'be',
            'for', 'from', 'to', 'in', 'by', 'do', 'when', 'otherwise', 'funct', 'while', 'given',
            'output', 'print', 'show', 'input', 'find', 'hence', 'integer'}

RESERVED_WORDS = {'true', 'false', 'permutation', 'combination', 'btree', 'preorder', 'inorder', 'postorder',
                 'null', 'search', 'add', 'remove', 'ugraph', 'dgraph', 'nodeAdd', 'removeEdge', 'UedgeAdd', 'DedgeAdd',
                 'bfs', 'dfs', 'dijkstra', 'kruskal', 'inverse', 'converse', 'contrapos', 'probability', 'cProbability',
                 'isPrime', 'isOdd', 'isEven', 'gcd', 'lcm', 'lcd', 'isDivisible', 'isPrimeF', 'ariseq', 'geomseq', 'fiboseq',
                 'series', 'union', 'intersection', 'difference', 'countSet', 'isSubset', 'isEqual', 'isSuperset', 'isDisjoint',
                 'isEmpty', 'R_notation', 'S_notation'}

NOISE_WORDS = {'eger', 'ing', 'acter', 'ion', 'ean', 'itive', 'actorization', 'uence'}