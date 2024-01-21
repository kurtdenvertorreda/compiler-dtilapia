from constants import *

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

            # Exponent Operator
            elif self.current_char == '^':
                tokens.append(Token(TT_EXPONENT))
                self.advance()

            # Greater Than or Equal To Operator
            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TT_GREATER_THAN_EQUAL))
                    self.advance()
                else:
                    # Greater Than Operator
                    tokens.append(Token(TT_GREATER_THAN))

            # Less Than or Equal To Operator or Biconditional Operator
            elif self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TT_LESS_THAN_EQUAL))
                    self.advance()
                elif self.current_char == '-':
                    self.advance()
                    if self.current_char == '>':
                        # Bi-conditional Operator
                        tokens.append(Token(TT_BICONDITIONAL))
                        self.advance()
                else:
                    # Less Than Operator
                    tokens.append(Token(TT_LESS_THAN))

            # Conditional Operator
            elif self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char == '>':
                        tokens.append(Token(TT_CONDITIONAL))
                        self.advance()
                    else:
                        # Equal To Operator
                        tokens.append(Token(TT_EQUAL_TO))
                else:
                    # Assignment Operator
                    tokens.append(Token(TT_ASSIGNMENT))


            # Not Equal To Operator or Negation Operator or Factorial Operator
            elif self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TT_NOT_EQUAL_TO))
                    self.advance()
                elif self.current_char:
                    # Negation Operator
                    tokens.append(Token(TT_NEGATION))
                else:
                    # Factorial Operator
                    tokens.append(Token(TT_FACTORIAL))
                    self.advance()

            # Disjunction Operator
            elif self.current_char == '\\':
                self.advance()
                if self.current_char == '/':
                    tokens.append(Token(TT_DISJUNCTION))
                    self.advance()

            # Alternative Disjunction Operator
            elif self.current_char == '|':
                self.advance()
                if self.current_char == '|':
                    tokens.append(Token(TT_DISJUNCTION))
                    self.advance()

            # Conjunction Operator
            elif self.current_char == '/':
                self.advance()
                if self.current_char == '\\':
                    tokens.append(Token(TT_CONJUNCTION))
                    self.advance()
                elif self.current_char == '=':
                     tokens.append(Token(TT_DIVISION_ASSIGNMENT))
                     self.advance()
                else:
                    # Division Operator
                    tokens.append(Token(TT_DIV))

            # Alternative Conjunction Operator
            elif self.current_char == '&':
                self.advance()
                if self.current_char == '&':
                    tokens.append(Token(TT_CONJUNCTION))
                    self.advance()

            # Alternate Conditional Operator
            elif self.current_char == '-':
                if self.pos.idx > 0 and self.text[self.pos.idx - 1].isalnum() or self.text[self.pos.idx - 1].isspace():
                    self.advance()
                    if self.current_char == '>':
                        tokens.append(Token(TT_CONDITIONAL))
                        self.advance()
                    elif self.current_char == '=':
                        # Subtraction Assignment Operator
                        tokens.append(Token(TT_SUBTRACTION_ASSIGNMENT))
                        self.advance()
                    elif self.current_char == '-':
                        # Decrement Operator
                        tokens.append(Token(TT_DECREMENT))
                        self.advance()
                    else:
                        # Subtraction Operator
                        tokens.append(Token(TT_MINUS))
                else:
                    tokens.append(Token(TT_UNARY_MINUS))
                    self.advance()

            # Addition Assignment Operator
            elif self.current_char == '+':
                if self.pos.idx > 0 and (self.text[self.pos.idx - 1].isalnum() or self.text[self.pos.idx - 1].isspace()):
                    self.advance()
                    if self.current_char == '=':
                        tokens.append(Token(TT_ADDITION_ASSIGNMENT))
                        self.advance()
                    elif self.current_char == '+':
                        if self.pos.idx > 0 and (self.text[self.pos.idx - 1].isalnum() or self.text[self.pos.idx - 1].isspace() == '('):
                        # Increment Operator
                            tokens.append(Token(TT_INCREMENT))
                            self.advance()
                        if self.current_char == '+':
                            print("Invalid")
                    else:
                        # Addition Operator
                        tokens.append(Token(TT_PLUS))
                else:
                    # Unary Plus Operator
                    tokens.append(Token(TT_UNARY_PLUS))
                    self.advance()


            # Multiplication Assignment Operator
            elif self.current_char == '*':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TT_MULTIPLICATION_ASSIGNMENT))
                    self.advance()
                elif self.current_char == '*' or '':
                    print("invalid")
                    self.advance()
                else:
                    # Multiplication Operator
                    tokens.append(Token(TT_MUL))

            # Modulus Assignment Operator
            elif self.current_char == '%':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TT_MODULUS_ASSIGNMENT))
                    self.advance()
                else:
                    # Modulus Operator
                    tokens.append(Token(TT_MODULO))
                    self.advance()
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == '\'':
                tokens.append(self.make_character())
            elif self.current_char in ALPHABET:
                tokens.append(self.make_identifier_or_keyword())
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TT_LCBRAC))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_RCBRAC))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(TT_LSQBRAC))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(TT_RSQBRAC))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(TT_COLON))
                self.advance()
            elif self.current_char == '.':
                tokens.append(Token(TT_PERIOD))
                self.advance()
            elif self.current_char == 'i' or self.current_char == 'j':
                tokens.append(self.make_complex())
            elif self.current_char == 't' or self.current_char == 'f':
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
        if self.current_char == '\'':
            self.advance()  # Skip the opening single quote
            char = self.current_char

            if char.isalnum():  # Check if the character is alphanumeric
                self.advance()  # Move to the next character

                if self.current_char == '\'':
                    self.advance()  # Skip the closing single quote
                    return Token(TT_CHAR, char)
                else:
                    raise Exception("Invalid character format: Missing closing single quote")
    
    def make_complex(self):
        complex_str = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.' or self.current_char == 'j'):
            complex_str += self.current_char
            self.advance()

        return Token(TT_COMPL, complex_str)

    def make_boolean(self):
        bool_str = ''
        while self.current_char is not None and (self.current_char.isalpha()):
            bool_str += self.current_char
            self.advance()

        bool_value = bool_str.lower() == 'true'
        return Token(TT_BOOL, bool_value)
    
    def make_identifier_or_keyword(self):
        identifier = ''
        while self.current_char is not None and (self.current_char in ALPHANUMERIC + '_'):
            identifier += self.current_char
            self.advance()
        
        token_type = TT_KEYWORD if identifier in KEYWORDS else TT_RESERVE if identifier in RESERVED_WORDS else TT_IDENTIFIER
        return self.handle_identifier_type(token_type, identifier)
    
    def handle_identifier_type(self, token_type, identifier):
        if token_type == TT_IDENTIFIER:
            return self.handle_variable(identifier)
        elif token_type == TT_KEYWORD:
            keyword = identifier
            noise_word = None
            if self.current_char is not None:
                if self.current_char in ALPHABET:
                    noise_word = self.make_noise_word()
                    return Token(TT_KEYWORD, keyword), noise_word
                    
            return Token(TT_KEYWORD, keyword)
        elif token_type == TT_RESERVE:
            return self.handle_reserved(identifier)
        elif token_type == TT_LCBRAC:
            return Token(token_type, identifier)
        elif token_type == TT_RCBRAC:
            return Token(token_type, identifier)
        elif token_type == TT_LSQBRAC:
            return Token(token_type, identifier)
        elif token_type == TT_RSQBRAC:
            return Token(token_type, identifier)
        elif token_type == TT_COLON:
            return Token(token_type, identifier)
        elif token_type == TT_PERIOD:
            return Token(token_type, identifier)
        else:
            return Token(token_type, identifier)
    
    def make_noise_word(self):
        noise_word = ''
        while self.current_char is not None and (self.current_char in ALPHABET or self.current_char in DIGITS):
            noise_word += self.current_char
            self.advance()
        return Token(TT_NOISE, noise_word) if noise_word in NOISE_WORDS else None

    def handle_variable(self, identifier):
        if identifier[0].isalpha():
            return Token(TT_IDENTIFIER, identifier)
        else:
            raise Exception(f"Invalid variable name: {identifier}")

    def handle_reserved(self, identifier):
        if identifier in RESERVED_WORDS:
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