DIGITS = '0123456789'
UPPER_CASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER_CASE = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET = UPPER_CASE + LOWER_CASE
ALPHANUMERIC = ALPHABET + DIGITS

#######################################
# TOKENS
#######################################

# Data Types
TT_INT		= 'Integer'
TT_FLOAT    = 'Float'
TT_STRING   = 'String'
TT_CHAR     = 'Character'
TT_COMPL    = 'Complex'
TT_BOOL     = 'Boolean'

# Delimiters and Brackets
TT_LPAREN   = 'Left Parenthesis'
TT_RPAREN   = 'Right Parenthesis'
TT_LCBRAC   = 'Left Curly Bracket'
TT_RCBRAC   = 'Right Curly Bracket'
TT_LSQBRAC  = 'Left Square Bracket'
TT_RSQBRAC  = 'Right Curly Bracket'
TT_COLON    = 'Colon'
TT_COMMA    = 'Comma'
TT_PERIOD   = 'Period'
TT_SEMICOL  = 'Semi Colon'
TT_UNSCO    = 'Under Score'
TT_SNGQ     = 'Single Quotation Mark'
TT_DBLQ     = 'Double Quotation Mark'

# Arithmetic Operators
TT_MODULO = 'Modulo Operator'
TT_EXPONENT = 'Exponent Operator'
TT_PLUS     = 'Addition Operator'
TT_MINUS    = 'Subtraction Operator'
TT_MUL      = 'Multiplication Operator'
TT_DIV      = 'Division Operator'

# Comparison Operators
TT_GREATER_THAN = 'Greater Than Operator'
TT_LESS_THAN = 'Less Than Operator'
TT_GREATER_THAN_EQUAL = 'Greater Than or Equal To Operator'
TT_LESS_THAN_EQUAL = 'Less Than or Equal To Operator'
TT_EQUAL_TO = 'Equal To Operator'
TT_NOT_EQUAL_TO = 'Not Equal To Operator'

# Logical Operators
TT_NEGATION = 'Negation Operator'
TT_DISJUNCTION = 'Disjunction Operator'  # For \/ or ||
TT_CONJUNCTION = 'Conjunction Operator'  # For /\ or &&
TT_CONDITIONAL = 'Conditional Operator'  # For ->
TT_IMPLICATION = 'Implication Operator'  # For ==>
TT_BICONDITIONAL = 'Bi-conditional Operator'  # For <->

# Assignment Operators
TT_ASSIGNMENT = 'Assignment Operator'  # For =
TT_ADDITION_ASSIGNMENT = 'Addition Assignment Operator'  # For +=
TT_SUBTRACTION_ASSIGNMENT = 'Subtraction Assignment Operator'  # For -=
TT_MULTIPLICATION_ASSIGNMENT = 'Multiplication Assignment Operator'  # For *=
TT_DIVISION_ASSIGNMENT = 'Division Assignment Operator'  # For /=
TT_MODULUS_ASSIGNMENT = 'Modulus Assignment Operator'  # For %=

# Unary Operators
TT_UNARY_PLUS = 'Unary Plus Operator'  # For +
TT_UNARY_MINUS = 'Unary Minus Operator'  # For -
TT_INCREMENT = 'Increment Operator'  # For ++
TT_DECREMENT = 'Decrement Operator'  # For --
TT_FACTORIAL = 'Factorial Operator'  # For !

# Others <3
TT_IDENTIFIER = 'Identifier'
TT_KEYWORD = 'Keyword'
TT_RESERVE = 'Reserved Word'
TT_NOISE   = 'Noise Word'
TT_SCOM    = 'Single Line Comment'
TT_MCOM    = 'Multiple Line Comment'

KEYWORDS = {'int', 'float', 'String', 'char', 'bool', 'set', 'array', 'complex', 'let', 'be',
            'for', 'from', 'to', 'in', 'by', 'do', 'when', 'otherwise', 'funct', 'while', 'given',
            'output', 'print', 'show', 'input', 'find', 'hence'}

RESERVED_WORDS = {'True', 'False', 'permutation', 'combination', 'btree', 'preorder', 'inorder', 'postorder',
                 'null', 'search', 'add', 'remove', 'ugraph', 'dgraph', 'nodeAdd', 'removeEdge', 'UedgeAdd', 'DedgeAdd',
                 'bfs', 'dfs', 'dijkstra', 'kruskal', 'inverse', 'converse', 'contrapos', 'probability', 'cProbability',
                 'isPrime', 'isOdd', 'isEven', 'gcd', 'lcm', 'lcd', 'isDivisible', 'isPrimeF', 'ariseq', 'geomseq', 'fiboseq',
                 'series', 'union', 'intersection', 'difference', 'countSet', 'isSubset', 'isEqual', 'isSuperset', 'isDisjoint',
                 'isEmpty', 'R_notation', 'S_notation'}

NOISE_WORDS = {'eger', 'ing', 'acter', 'ion', 'ean', 'itive', 'actorization', 'uence'}

KEYWORD_NOISE_WORDS = {
    'integer': ('int', 'eger'),
    'character': ('char', 'acter'),
    'function': ('funct', 'ion'),
    'boolean': ('bool', 'ean'),
    'contrapositive': ('contrapos', 'itive'),
    'isPrimeFactorization': ('isPrimeF', 'actorization'),
    'arisequence': ('ariseq', 'uence'),
    'geomsequence': ('geomseq', 'uence'),
    'fibosequence': ('fiboseq', 'uence')
}