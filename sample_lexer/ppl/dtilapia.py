#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

#######################################
# ERRORS
#######################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

#######################################
# POSITION
#######################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#######################################
# TOKENS
#######################################

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

KEYWORDS = {'int', 'float', 'String', 'char', 'bool', 'set', 'array', 'complex', 'let', 'be',
            'for', 'from', 'to', 'in', 'by', 'do', 'when', 'otherwise', 'funct', 'while', 'given',
            'output', 'print', 'show', 'input', 'find', 'hence'}

RESERVED_WORDS = {'true', 'false', 'permutation', 'combination', 'btree', 'preorder', 'inorder', 'postorder',
                 'null', 'search', 'add', 'remove', 'ugraph', 'dgraph', 'nodeAdd', 'removeEdge', 'UedgeAdd', 'DedgeAdd',
                 'bfs', 'dfs', 'dijkstra', 'kruskal', 'inverse', 'converse', 'contrapos', 'probability', 'cProbability',
                 'isPrime', 'isOdd', 'isEven', 'gcd', 'lcm', 'lcd', 'isDivisible', 'isPrimeF', 'ariseq', 'geomseq', 'fiboseq',
                 'series', 'union', 'intersection', 'difference', 'countSet', 'isSubset', 'isEqual', 'isSuperset', 'isDisjoint',
                 'isEmpty', 'R_notation', 'S_notation'}

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == '\'':
                tokens.append(self.make_character())
            elif self.current_char == '{':
                tokens.append(self.make_set())
            elif self.current_char == '[':
                tokens.append(self.make_array())
            elif self.current_char in ALPHABET:
                tokens.append(self.make_identifier_or_keyword())
            elif self.current_char == 'i' or self.current_char == 'j':
                tokens.append(self.make_complex())
            elif self.current_char == 'T' or self.current_char == 'F':
                tokens.append(self.make_boolean())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))
    
    def make_string(self):
        string = ''
        self.advance() 
        while self.current_char is not None and self.current_char != '"':
            string += self.current_char
            self.advance()
        self.advance() 
        return Token(TT_STRING, string)
    
    def make_character(self):
        char = self.current_char
        self.advance() 
        if self.current_char == '\'':
            self.advance() 
            return Token(TT_CHAR, char)
        else:
            raise Exception("Invalid character format")

    def make_set(self):
        set_contents = ''
        self.advance() 
        while self.current_char is not None and self.current_char != '}':
            set_contents += self.current_char
            self.advance()
        self.advance()  
        return Token(TT_SET, set_contents)

    def make_array(self):
        array_contents = ''
        self.advance() 
        while self.current_char is not None and self.current_char != ']':
            array_contents += self.current_char
            self.advance()
        self.advance()  
        return Token(TT_ARR, array_contents)
   
    def make_complex(self):
        complex_str = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            complex_str += self.current_char
            self.advance()

        return Token(TT_COMPL, complex_str + 'j')

    def make_boolean(self):
        bool_str = ''
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_'):
            bool_str += self.current_char
            self.advance()

        bool_value = bool_str.lower() == 'true'
        return Token(TT_BOOL, bool_value)
    
    def make_identifier_or_keyword(self):
        identifier = ''
        while self.current_char is not None and (self.current_char in ALPHABET or self.current_char in DIGITS):
            identifier += self.current_char
            self.advance()

        token_type = TT_KEYWORD if identifier in KEYWORDS else TT_RESERVE if identifier in RESERVED_WORDS else TT_IDENTIFIER
        return self.handle_identifier_type(token_type, identifier)
    
    def handle_identifier_type(self, token_type, identifier):
        if token_type == TT_IDENTIFIER:
            return self.handle_variable(identifier)
        elif token_type == TT_KEYWORD:
            return Token(token_type, identifier)
        elif token_type == TT_RESERVE:
            return self.handle_reserved(identifier)
        else:
            return Token(token_type, identifier)
    
    def handle_variable(self, identifier):
        if identifier[0].islower():
            return Token(TT_IDENTIFIER, identifier)
        else:
            raise Exception(f"Invalid variable name: {identifier}")

    def handle_reserved(self, identifier):
        if identifier.startswith(TT_RESERVE):
            return Token(TT_RESERVE, identifier)
        else:
            raise Exception(f"Invalid usage of reserved keyword: {identifier}")
#######################################
# RUN
#######################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error