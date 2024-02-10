from constants import *

#######################################
# ERROR
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

#######################################
# ILLEGAL CHARACTER ERROR
#######################################
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

    def advance(self, current_char = None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#######################################
# TOKENIZATION
#######################################
class Token:
    def __init__(self, line, type_, value=None):
        self.line = line
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.line}:{self.type}:{self.value}'
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
            if self.current_char in '\n':
                tokens.append(Token(self.pos.ln,TT_NEWLINE,value="newline"))
                self.advance()
            elif self.current_char == '\t' or self.current_char == " ":
                self.advance()
                if self.current_char == '\t' or self.current_char == " ":
                    self.advance()
                    if self.current_char == '\t' or self.current_char == " ":
                        self.advance()
                        if self.current_char == '\t' or self.current_char == " ":
                            tokens.append(Token(self.pos.ln,TT_TAB,value="tab"))
                            self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())

            # Exponent Operator
            elif self.current_char == '^':
                tokens.append(Token(self.pos.ln,TT_EXPONENT, value='^'))
                self.advance()

            elif self.current_char == '>':
                            token_value = '>'
                            self.advance()
                            if self.current_char == '=':
                                token_value += '='
                                self.advance()
                            
                            if self.current_char is not None and not self.current_char.isspace():
                                if self.current_char.isalnum() or self.current_char in {'(', ')'}:  # Add other valid characters if needed
                                    # The character is valid for starting a new token, so we tokenize the operator
                                    tokens.append(Token(self.pos.ln,TT_GREATER_THAN_EQUAL if token_value == '>=' else self.pos.ln,TT_GREATER_THAN, value=token_value))
                                else:
                                    # Accumulate invalid characters until a space is encountered
                                    invalid_chars = ''
                                    while self.current_char is not None and not self.current_char.isspace():
                                        invalid_chars = invalid_chars + self.current_char
                                        self.advance()

                                    # Tokenize the accumulated invalid characters
                                    tokens.append(Token(self.pos.ln,TT_INVALID, value= token_value + invalid_chars))
                                    self.advance()
                            else:
                                # The '>' operator is followed by a space or the end of input, so tokenize it
                                tokens.append(Token(self.pos.ln,TT_GREATER_THAN_EQUAL if token_value == '>=' else TT_GREATER_THAN, value=token_value))

            # Greater Than or Equal To Operator
            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(self.pos.ln,TT_GREATER_THAN_EQUAL, value='>='))
                    self.advance()
                else:
                    # Greater Than Operator
                    tokens.append(Token(self.pos.ln,TT_GREATER_THAN, value='>'))

            # Less Than or Equal To Operator or Biconditional Operator
            elif self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char == '=':
                        self.advance()
                        if self.current_char == '>':
                            # Bi-conditional Operator
                            tokens.append(Token(self.pos.ln,TT_BICONDITIONAL, value='<==>'))
                            self.advance()
                    else:
                        tokens.append(Token(self.pos.ln,TT_LESS_THAN_EQUAL, value='<='))
                elif self.current_char == '-':
                    self.advance()
                    if self.current_char == '>':
                        # Bi-conditional Operator
                        tokens.append(Token(self.pos.ln,TT_BICONDITIONAL, value='<->'))
                        self.advance()
                else:
                    # Less Than Operator
                    tokens.append(Token(self.pos.ln,TT_LESS_THAN, value='<'))

           # Conditional Operator
            elif self.current_char == '=':
                            token_value = '='
                            self.advance()
                            if self.current_char == '=':
                                token_value += '='
                                self.advance()
                                if self.current_char == '>':
                                    token_value += '>'
                                    self.advance()
                            elif self.current_char == '=':
                                token_value += '='
                                self.advance()
                            if self.current_char is None or self.current_char.isspace() or self.current_char.isdigit() or self.current_char.isalpha() or self.current_char in {'(', ')'}:
                                # If it's a valid character, tokenize accordingly
                                if token_value == '==':
                                    tokens.append(Token(self.pos.ln,TT_EQUAL_TO, value=token_value))
                                elif token_value == '==>':
                                    tokens.append(Token(self.pos.ln,TT_CONDITIONAL, value=token_value))
                                else:
                                    # If token_value is just '+', it's a plus token
                                    tokens.append(Token(self.pos.ln,TT_ASSIGNMENT, value=token_value))
                            else:
                                # If the next character is not valid, raise an error and exit
                                invalid_chars = ''
                                while self.current_char is not None and not self.current_char.isspace():
                                    invalid_chars = invalid_chars + self.current_char
                                    self.advance()

                                # Tokenize the accumulated invalid characters
                                tokens.append(Token(self.pos.ln,TT_INVALID, value= token_value + invalid_chars))
                                self.advance()


            # Not Equal To Operator or Negation Operator or Factorial Operator
            elif self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(self.pos.ln,TT_NOT_EQUAL_TO, value='!='))
                    self.advance()
                elif self.current_char:
                    # Negation Operator
                    tokens.append(Token(self.pos.ln,TT_NEGATION, value='!'))
                else:
                    # Factorial Operator
                    tokens.append(Token(self.pos.ln,TT_FACTORIAL, value='!'))
                    self.advance()

            # Disjunction Operator
            elif self.current_char == '\\':
                self.advance()
                if self.current_char == '/':
                    tokens.append(Token(self.pos.ln,TT_DISJUNCTION, value='\\/'))
                    self.advance()

            # Alternative Disjunction Operator
            elif self.current_char == '|':
                self.advance()
                if self.current_char == '|':
                    tokens.append(Token(self.pos.ln,TT_DISJUNCTION, value='||'))
                    self.advance()

                       # Conjunction Operator
            elif self.current_char == '/':
                token_value = '/'
                self.advance()
                if self.current_char == '\\':
                    token_value = token_value + '\\'
                    self.advance()
                    if self.current_char == '\\':
                        token_value = token_value + '\\'
                        self.advance()
                elif self.current_char == '=':
                    token_value = token_value + '='
                    self.advance()
                elif self.current_char == '/':
                    token_value = token_value + '/'
                    self.advance
                    comment_text = self.advance_until('\n')
                    tokens.append(Token(self.pos.ln,TT_SCOM, value=f'/{comment_text}'))
                elif self.current_char == '~':
                    self.advance()
                    comment_text = self.advance_until('~')
                    self.advance()  # Skip the '~'
                    x = False
                    while x == False:
                        if self.current_char == '/':
                            tokens.append(Token(self.pos.ln,TT_MCOM, value=f'/~{comment_text}~/'))
                            x = True
                        else:
                            comment_text += self.advance_until('~')
                            self.advance()
                    self.advance()
                elif self.current_char is None or self.current_char.isspace() or self.current_char.isdigit() or self.current_char.isalpha() or self.current_char in {'(', ')'}:
                    # If it's a valid character, tokenize accordingly
                    if token_value == '/\\':
                        tokens.append(Token(self.pos.ln,TT_CONJUNCTION, value=token_value))
                    elif token_value == '/=':
                        tokens.append(Token(self.pos.ln,TT_DIVISION_ASSIGNMENT, value=token_value))
                    elif token_value == '//':
                        tokens.append(Token(self.pos.ln,TT_SCOM, value=f'//{comment_text}'))
                    elif token_value == '/~':
                        tokens.append(Token(self.pos.ln,TT_MCOM, value=f'{comment_text}'))
                    else:
                        # If token_value is just '+', it's a plus token
                        tokens.append(Token(self.pos.ln,TT_DIV, value=token_value))
                else:
                    # If the next character is not valid, raise an error and exit
                    invalid_chars = ''
                    while self.current_char is not None and not self.current_char.isspace():
                        invalid_chars = invalid_chars + self.current_char
                        self.advance()

                    # Tokenize the accumulated invalid characters
                    tokens.append(Token(self.pos.ln,TT_INVALID, value= token_value + invalid_chars))
                    self.advance()

            # Alternative Conjunction Operator
            elif self.current_char == '&':
                self.advance()
                if self.current_char == '&':
                    tokens.append(Token(self.pos.ln,TT_CONJUNCTION, value='&&'))
                    self.advance()

            # Alternate Conditional Operator
            elif self.current_char == '-':
                            token_value = '-'
                            self.advance()  # Move past the first '+'

                            if self.current_char == '=':
                                # If the next character is '=', it's an addition assignment
                                token_value += '='
                                self.advance()  # Move past '='
                            elif self.current_char == '-':
                                # If the next character is another '+', it's an increment
                                token_value += '-'
                                self.advance()  # Move past the second '+'
                            elif self.current_char == '>':
                                # If the next character is another '+', it's an increment
                                token_value += '>'
                                self.advance()  # Move past the second '+'

                            if self.current_char is None or self.current_char.isspace() or self.current_char.isdigit() or self.current_char.isalpha() or self.current_char in {'(', ')'}:
                                # If it's a valid character, tokenize accordingly
                                if token_value == '--':
                                    tokens.append(Token(self.pos.ln,TT_DECREMENT, value=token_value))
                                elif token_value == '-=':
                                    tokens.append(Token(self.pos.ln,TT_SUBTRACTION_ASSIGNMENT, value=token_value))
                                elif token_value == '->':
                                    tokens.append(Token(self.pos.ln,TT_CONDITIONAL, value=token_value))
                                else:
                                    # If token_value is just '+', it's a plus token
                                    tokens.append(Token(self.pos.ln,TT_MINUS, value=token_value))
                            else:
                                # If the next character is not valid, raise an error and exit
                                invalid_chars = ''
                                while self.current_char is not None and not self.current_char.isspace():
                                    invalid_chars = invalid_chars + self.current_char
                                    self.advance()

                                # Tokenize the accumulated invalid characters
                                tokens.append(Token(self.pos.ln,TT_INVALID, value= token_value + invalid_chars))
                                self.advance()

            # Addition Assignment Operator
            elif self.current_char == '+':
                token_value = '+'
                self.advance()  # Move past the first '+'

                if self.current_char == '=':
                    # If the next character is '=', it's an addition assignment
                    token_value += '='
                    self.advance()  # Move past '='
                elif self.current_char == '+':
                    # If the next character is another '+', it's an increment
                    token_value += '+'
                    self.advance()  # Move past the second '+'

                if self.current_char is None or self.current_char.isspace() or self.current_char.isdigit() or self.current_char.isalpha() or self.current_char in {'(', ')'}:
                    # If it's a valid character, tokenize accordingly
                    if token_value == '++':
                        tokens.append(Token(self.pos.ln,TT_INCREMENT, value=token_value))
                    elif token_value == '+=':
                        tokens.append(Token(self.pos.ln,TT_ADDITION_ASSIGNMENT, value=token_value))
                    else:
                        # If token_value is just '+', it's a plus token
                        tokens.append(Token(self.pos.ln,TT_PLUS, value=token_value))
                else:
                    # If the next character is not valid, raise an error and exit
                    invalid_chars = ''
                    while self.current_char is not None and not self.current_char.isspace():
                        invalid_chars = invalid_chars + self.current_char
                        self.advance()

                    # Tokenize the accumulated invalid characters
                    tokens.append(Token(self.pos.ln,TT_INVALID, value= token_value + invalid_chars))
                    self.advance()

             # Multiplication Assignment Operator
            elif self.current_char == '*':
                token_value = '*'
                self.advance()
                if self.current_char == '=':
                    token_value += '='
                    tokens.append(Token(self.pos.ln,TT_MULTIPLICATION_ASSIGNMENT, value='*='))
                    self.advance()
                else:
                    # Check for invalid characters after '*'
                    if self.current_char is not None and not self.current_char.isspace():
                        if self.current_char.isalnum() or self.current_char in {'(', ')'}:  # Add other valid characters if needed
                            # The character is valid for starting a new token, so we tokenize the operator
                            tokens.append(Token(self.pos.ln,TT_MUL, value='*'))
                            self.advance()
                        else:
                            # Accumulate invalid characters until a space is encountered
                            invalid_chars = ''
                            while self.current_char is not None and not self.current_char.isspace():
                                invalid_chars = invalid_chars + self.current_char
                                self.advance()

                            # Tokenize the accumulated invalid characters
                            tokens.append(Token(self.pos.ln,TT_INVALID, value= token_value + invalid_chars))
                            self.advance()
                    else:
                        # The '*' operator is followed by a space or the end of input, so tokenize it
                        tokens.append(Token(self.pos.ln,TT_MUL, value='*'))
            # Multiplication Assignment Operator
            #elif self.current_char == '*':
               # self.advance()
                #if self.current_char == '=':
                  #  tokens.append(Token(TT_MULTIPLICATION_ASSIGNMENT, value='*='))
               #     self.advance()
             #   elif self.current_char == '*' or '':
                #    print("invalid")
               #     self.advance()
               # else:
                    # Multiplication Operator
              #      tokens.append(Token(TT_MUL, value='*'))

            # Modulus Assignment Operator
            elif self.current_char == '%':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(self.pos.ln,TT_MODULUS_ASSIGNMENT, value='%='))
                    self.advance()
                else:
                    # Modulus Operator
                    tokens.append(Token(self.pos.ln,TT_MODULO, value='%'))
                    self.advance()
            elif self.current_char == '"':
                tokens.append(Token(self.pos.ln,TT_DBLQ, value='"'))
                tokens.append(self.make_string())
                tokens.append(Token(self.pos.ln,TT_DBLQ, value='"'))
            elif self.current_char == '\'':
                tokens.append(Token(self.pos.ln,TT_SNGQ, value='\''))
                tokens.append(self.make_character())
                tokens.append(Token(self.pos.ln,TT_SNGQ, value='\''))
            elif self.current_char in ALPHABET:
                tokens.append(self.make_identifier_or_keyword())
            elif self.current_char == '(':
                tokens.append(Token(self.pos.ln,TT_LPAREN, value='('))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(self.pos.ln,TT_RPAREN, value=')'))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(self.pos.ln,TT_LCBRAC, value='{'))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(self.pos.ln,TT_RCBRAC, value='}'))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(self.pos.ln,TT_LSQBRAC, value='['))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(self.pos.ln,TT_RSQBRAC, value=']'))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(self.pos.ln,TT_COLON, value=':'))
                self.advance()
            elif self.current_char == '.':
                tokens.append(Token(self.pos.ln,TT_PERIOD, value='.'))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(self.pos.ln,TT_COMMA, value=','))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(self.pos.ln,TT_SEMICOL, value=';'))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                continue
                #return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    def advance_until(self, target):
        result = ''
        while self.current_char is not None and self.current_char != target:
            result += self.current_char
            self.advance()
        return result
    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.' or self.current_char.lower() in {'i', 'j'} or self.current_char.isalpha()):
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            elif self.current_char.isalpha():
                if self.current_char.lower() in {'i', 'j'}:
                    num_str = num_str + self.current_char
                    self.advance()
                    if self.current_char:
                        invalid_chars = ''
                        while self.current_char is not None and not self.current_char.isspace():
                            invalid_chars = invalid_chars + self.current_char
                            self.advance()
                        return Token(self.pos.ln,TT_INVALID, value = num_str + invalid_chars)
                    else:
                        return Token(self.pos.ln,TT_COMPL, num_str)
                else:
                    invalid_chars = ''
                    while self.current_char is not None and not self.current_char.isspace():
                        invalid_chars = invalid_chars + self.current_char
                        self.advance()
                    return Token(self.pos.ln,TT_INVALID, value= num_str + invalid_chars)
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(self.pos.ln,TT_INT, int(num_str))
        else:
            return Token(self.pos.ln,TT_FLOAT, float(num_str))
        
    def make_string(self):
        string = ''
        self.advance() 
        while self.current_char is not None and self.current_char != '"':
            string += self.current_char
            self.advance()
        self.advance() 
        return Token(self.pos.ln,TT_STRING, string)
   
    def make_character(self):
        if self.current_char == '\'':
            self.advance()  # Skip the opening single quote
            char = self.current_char

            if char.isalnum():  # Check if the character is alphanumeric
                self.advance()  # Move to the next character

                if self.current_char == '\'':
                    self.advance()  # Skip the closing single quote
                    return Token(self.pos.ln,TT_CHAR, char)
                else:
                    raise Exception("Invalid character format: Missing closing single quote")
    
    def make_identifier_or_keyword(self):
        identifier = ''
        while self.current_char is not None and (self.current_char in ALPHANUMERIC + '_'):
            identifier += self.current_char
            self.advance()

        if identifier in KEYWORD_NOISE_WORDS:
            keyword, noise = KEYWORD_NOISE_WORDS[identifier]
            return Token(self.pos.ln,TT_KEYWORD, keyword), Token(self.pos.ln,TT_NOISE, noise)

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
                    return Token(self.pos.ln,TT_KEYWORD, keyword), noise_word
                    
            return Token(self.pos.ln,TT_KEYWORD, keyword)
        elif token_type == TT_RESERVE:
            return self.handle_reserved(identifier)
        elif token_type == TT_LCBRAC:
            return Token(self.pos.ln,token_type, identifier)
        elif token_type == TT_RCBRAC:
            return Token(self.pos.ln,token_type, identifier)
        elif token_type == TT_LSQBRAC:
            return Token(self.pos.ln,token_type, identifier)
        elif token_type == TT_RSQBRAC:
            return Token(self.pos.ln,token_type, identifier)
        elif token_type == TT_COLON:
            return Token(self.pos.ln,token_type, identifier)
        elif token_type == TT_PERIOD:
            return Token(self.pos.ln,token_type, identifier)
        elif token_type == TT_COMMA:
            return Token(self.pos.ln,token_type, identifier)
        elif token_type == TT_SEMICOL:
            return Token(self.pos.ln,token_type, identifier)
        else:
            return Token(self.pos.ln,token_type, identifier)
    
    def make_noise_word(self):
        noise_word = ''
        while self.current_char is not None and (self.current_char in ALPHABET or self.current_char in DIGITS):
            noise_word += self.current_char
            self.advance()
        return Token(self.pos.ln,TT_NOISE, noise_word) if noise_word in NOISE_WORDS else None

    def handle_variable(self, identifier):
        if identifier[0].isalpha():
            return Token(self.pos.ln,TT_IDENTIFIER, identifier)
        else:
            raise Exception(f"Invalid variable name: {identifier}")

    def handle_reserved(self, identifier):
        bool_str = identifier.lower()
        if bool_str == 'true':
            return Token(self.pos.ln,TT_BOOL, value='True')
        elif bool_str == 'false':
            return Token(self.pos.ln,TT_BOOL, value='False')
        elif identifier in RESERVED_WORDS:
            return Token(self.pos.ln,TT_RESERVE, identifier)
        else:
            raise Exception(f"Invalid usage of reserved keyword: {identifier}")
#######################################
# RUN
#######################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error