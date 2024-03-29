from constants import *
from dtilapia import Lexer

class ResParse:
    def __init__(self, line, code, errorName, errorDesc):
        self.line = line
        self.code = code
        self.errorName = errorName
        self.errorDesc = errorDesc
    
    def __repr__(self):
        if self.errorName: return f'{self.line}:{self.code}:{self.errorName}: {self.errorDesc}'
        return f'{self.line}:{self.code}:No Error:No Error'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.current_token = self.tokens[self.idx]

    def parse(self):
        declarations = []
        if self.current_token.type == TT_KEYWORD and self.current_token.value == "let":
            declaration = self.parse_declaration()
            declarations.append(declaration)
        else:
            raise Exception("Invalid token at line {}: Expected 'let' keyword".format(self.current_token.line))
        return declarations
    
    def parse_declaration(self):
        self.advance()  # Move past 'let' keyword
        store = "let" + " "
        identifier_token = self.current_token

        if identifier_token.type == TT_IDENTIFIER:
            store += self.current_token.value + " "
            self.advance()  # Move past identifier
            if self.current_token.type == TT_KEYWORD and self.current_token.value == "be":
                store += self.current_token.value + " "
                self.advance()  # Move past 'be' keyword
                if self.current_token.type == TT_KEYWORD:
                    if self.current_token.value in KEYWORDS_DATA_TYPE:  # Check if the token type is one of the data types
                        store += self.current_token.value + " "
                        data_type = self.current_token.value  # Get the value of the data type token
                        self.advance()
                        if self.current_token.type == TT_PERIOD:
                            store += self.current_token.value + " "
                            self.advance()
                            if self.current_token.type == TT_KEYWORD:
                                if self.current_token.value == 'array':
                                    store += self.current_token.value + " "
                                    self.advance()
                                    if self.current_token.type == TT_LSQBRAC:
                                        store += self.current_token.value + " "
                                        self.advance()
                                        if self.current_token.type == TT_INT:
                                            size = self.current_token.value
                                            store += self.current_token.value + " "
                                            self.advance()
                                            if self.current_token.type == TT_RSQBRAC:
                                                store += self.current_token.value + " "
                                                self.advance()
                                                if self.current_token.type == TT_ASSIGNMENT:
                                                    store += self.current_token.value + " "
                                                    self.advance()
                                                    if self.current_token.type == TT_LCBRAC:
                                                        store += self.current_token.value + " "
                                                        self.advance()
                                                        if self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER or self.current_token.type == TT_FLOAT or self.current_token.type == TT_STRING or self.current_token.type == TT_CHAR or self.current_token.type == TT_COMPL:
                                                            value = [self.current_token.value]
                                                            data_type = self.current_token.type
                                                            store += self.current_token.value + " "
                                                            self.advance()
                                                            if self.current_token.type == TT_RCBRAC:
                                                                store += self.current_token.value + " "
                                                                self.advance()
                                                                return ResParse(self.current_token.line, store, "No Error", "No Error")
                                                            elif self.current_token.type == TT_COMMA:
                                                                size_allowed = size
                                                                while self.current_token.type == TT_COMMA:
                                                                    store += self.current_token.value + " "
                                                                    self.advance()
                                                                    if self.current_token.type == data_type:
                                                                        value.append(self.current_token.value)
                                                                        store += self.current_token.value + " "
                                                                        self.advance()                
                                                                        size_allowed -= 1                                  
                                                                    else:
                                                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                                                if size_allowed == 0:
                                                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                                                elif self.current_token.type == TT_RCBRAC:
                                                                    return ResParse(self.current_token.line, store, "No Error", "No Error")
                                                                else:
                                                                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                                            else:
                                                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                                        else:
                                                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                                    else:
                                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                                else:
                                                    return ResParse(self.current_token.line, store, "No Error", "No Error")
                                            else:
                                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                        else:
                                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                    else:
                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                else:
                                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                            else:
                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                        elif self.current_token.value not in KEYWORDS_DATA_TYPE:
                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                        else:
                            return ResParse(self.current_token.line, store, "No Error", "No Error")
                    elif self.current_token.value == 'set':
                        store += self.current_token.value + " "
                        self.advance()
                        if self.current_token.type == TT_ASSIGNMENT:
                            store += self.current_token.value + " "
                            self.advance()
                            if self.current_token.type == TT_LCBRAC:
                                store += self.current_token.value + " "
                                self.advance()
                                if self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER or self.current_token.type == TT_FLOAT or self.current_token.type == TT_STRING or self.current_token.type == TT_CHAR or self.current_token.type == TT_COMPL:
                                    value = [self.current_token.value]
                                    data_type = [self.current_token.type]
                                    store += self.current_token.value + " "
                                    self.advance()
                                    if self.current_token.type == TT_RCBRAC:
                                        store += self.current_token.value + " "
                                        self.advance()
                                        return ResParse(self.current_token.line, store, "No Error", "No Error")
                                    elif self.current_token.type == TT_COMMA:
                                        while self.current_token.type == TT_COMMA:
                                            store += self.current_token.value + " "
                                            self.advance()
                                            if self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER or self.current_token.type == TT_FLOAT or self.current_token.type == TT_STRING or self.current_token.type == TT_CHAR or self.current_token.type == TT_COMPL:
                                                value.append(self.current_token.value)
                                                data_type.append(self.current_token.type)
                                                store += self.current_token.value + " "
                                                self.advance()                                           
                                            else:
                                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                        if self.current_token.type == TT_RCBRAC:
                                            return ResParse(self.current_token.line, store, "No Error", "No Error")
                                        else:
                                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                    else:
                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                else:
                                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                            else:
                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")


                        elif self.current_token.type == TT_IDENTIFIER:
                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                        else:
                           return ResParse(self.current_token.line, store, "No Error", "No Error")
                    else:
                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                else:
                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
            else:
                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
        else:
            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")


    def parse_data_type(self):
        data_type = ''
        while self.current_token.type in (TT_IDENTIFIER, TT_PERIOD):
            data_type += self.current_token.value
            self.advance()
        return data_type

def main():
    while True:
        # Take input from the user
        print("Enter your code (type 'exit' to quit):")
        input_text = input()
        
        if input_text.lower() == 'exit':
            print("Exiting...")
            break

        # Generate tokens using the lexer
        lexer = Lexer("dtilapia.py", input_text)
        tokens, error = lexer.make_tokens()

        if error:
            print(error.as_string())
        else:
            # Instantiate the parser with the generated tokens
            parser = Parser(tokens)
            
            try:
                # Parse the tokens and retrieve the declarations
                declarations = parser.parse()
                
                # Print the parsed declarations
                for declaration in declarations:
                    print(declaration)
            except Exception as e:
                print("Parser error:", str(e))


if __name__ == "__main__":
    main()