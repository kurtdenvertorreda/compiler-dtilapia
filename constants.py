DIGITS = '0123456789'
UPPER_CASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER_CASE = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET = UPPER_CASE + LOWER_CASE
ALPHANUMERIC = ALPHABET + DIGITS

#######################################
# TOKENS
#######################################

# LITERALS
TT_INT		= 'Integer'
TT_FLOAT    = 'Float'
TT_STRING   = 'String'
TT_CHAR     = 'Character'
TT_COMPL    = 'Complex'
TT_BOOL     = 'Boolean'

# Delimiters and Brackets
<<<<<<< HEAD
TT_LPAREN   = 'Left Parenthesis'
TT_RPAREN   = 'Right Parenthesis'
TT_LCBRAC   = 'Left Curly Bracket'
TT_RCBRAC   = 'Right Curly Bracket'
TT_LSQBRAC  = 'Left Square Bracket'
TT_RSQBRAC  = 'Right Curly Bracket'
TT_COLON    = 'Colon'
TT_COMMA    = 'Comma'
TT_PERIOD   = 'Period'
<<<<<<< HEAD:constants.py
TT_SEMICOL  = 'Semi Colon'
TT_UNSCO    = 'Underscore'
TT_SNGQ     = 'Single Quotation Mark'
TT_DBLQ     = 'Double Quotation Mark'
=======
>>>>>>> e6a134f (fix reserved words):sample_lexer/ppl/constants.py
=======
TT_LPAREN   = 'DELIBRA_Left_Parenthesis'
TT_RPAREN   = 'DELIBRA_Right_Parenthesis'
TT_LCBRAC   = 'DELIBRA_Left_Curly_Bracket'
TT_RCBRAC   = 'DELIBRA_Right_Curly_Bracket'
TT_LSQBRAC  = 'DELIBRA_Left_Square_Bracket'
TT_RSQBRAC  = 'DELIBRA_Right_Curly_Bracket'
TT_COLON    = 'DELIBRA_Colon'
TT_COMMA    = 'DELIBRA_Comma'
TT_PERIOD   = 'DELIBRA_Period'
TT_SEMICOL  = 'DELIBRA_Semi_Colon'
TT_SNGQ     = 'DELIBRA_Single_Quotation_Mark'
TT_DBLQ     = 'DELIBRA_Double_Quotation_Mark'
>>>>>>> origin/main

# Arithmetic Operators
TT_MODULO   = 'ARIOP_Modulo_Operator'
TT_EXPONENT = 'ARIOP_Exponent_Operator'
TT_PLUS     = 'ARIOP_Addition_Operator'
TT_MINUS    = 'ARIOP_Subtraction_Operator'
TT_MUL      = 'ARIOP_Multiplication_Operator'
TT_DIV      = 'ARIOP_Division_Operator'

# Comparison Operators
TT_GREATER_THAN = 'RELOP_Greater_Than_Operator'
TT_LESS_THAN = 'RELOP_Less_Than_Operator'
TT_GREATER_THAN_EQUAL = 'RELOP_Greater_Than_or_Equal_To_Operator'
TT_LESS_THAN_EQUAL = 'RELOP_Less_Than_or_Equal_To_Operator'
TT_EQUAL_TO = 'RELOP_Equal_To_Operator'
TT_NOT_EQUAL_TO = 'RELOP_Not_Equal_To_Operator'
TT_INVALID ='Invalid Token'

# Logical Operators
TT_NEGATION = 'LOGOP_Negation_Operator'
TT_DISJUNCTION = 'LOGOP_Disjunction_Operator'  # For \/ or ||
TT_CONJUNCTION = 'LOGOP_Conjunction_Operator'  # For /\ or &&
TT_CONDITIONAL = 'LOGOP_Conditional_Operator'  # For ->
TT_IMPLICATION = 'LOGOP_Implication_Operator'  # For ==>
TT_BICONDITIONAL = 'LOGOP_Bi-conditional_Operator'  # For <->

# Assignment Operators
TT_ASSIGNMENT = 'ASSOP_Assignment_Operator'  # For =
TT_ADDITION_ASSIGNMENT = 'ASSOP_Addition_Assignment_Operator'  # For +=
TT_SUBTRACTION_ASSIGNMENT = 'ASSOP_Subtraction_Assignment_Operator'  # For -=
TT_MULTIPLICATION_ASSIGNMENT = 'ASSOP_Multiplication_Assignment_Operator'  # For *=
TT_DIVISION_ASSIGNMENT = 'ASSOP_Division_Assignment_Operator'  # For /=
TT_MODULUS_ASSIGNMENT = 'ASSOP_Modulus_Assignment_Operator'  # For %=

# Unary Operators
TT_UNARY_PLUS = 'UNAOP_Unary_Plus_Operator'  # For +
TT_UNARY_MINUS = 'UNAOP_Unary_Minus_Operator'  # For -
TT_INCREMENT = 'UNAOP_Increment_Operator'  # For ++
TT_DECREMENT = 'UNAOP_Decrement_Operator'  # For --
TT_FACTORIAL = 'UNAOP_Factorial_Operator'  # For !

# Others <3
TT_IDENTIFIER = 'Identifier'
TT_KEYWORD = 'Keyword'
<<<<<<< HEAD
TT_RESERVE = 'Reserved Word'
TT_NOISE   = 'Noise Word'
TT_SCOM    = 'Single Line Comment'
TT_MCOM    = 'Multiple Line Comment'
TT_INVALID = 'Invalid Token'
=======
TT_RESERVE = 'Reserved_Word'
TT_NOISE   = 'Noise_Word'
TT_INVALID = 'Invalid_Token'

# Comments
TT_SCOM    = 'COM_Single_Line_Comment'
TT_MCOM    = 'COM_Multiple_Line_Comment'
>>>>>>> origin/main

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