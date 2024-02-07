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
        store = ""
        self.advance()  # Move past 'let' keyword
        store = "let" + " "
        identifier_token = self.current_token
        if identifier_token.type == TT_IDENTIFIER:
              # Move past identifier
            store += self.current_token.value + " "
            self.advance()
            if self.current_token.type == TT_KEYWORD and self.current_token.value == "be":
                 # Move past 'be' keyword
                store += self.current_token.value + " "
                self.advance() 
                if self.current_token.type == TT_KEYWORD:
                    if self.current_token.value in KEYWORDS_DATA_TYPE:  # Check if the token type is one of the data types
                        data_type = self.current_token.value  # Get the value of the data type token
                        store += self.current_token.value + " "
                        self.advance()
                        if self.current_token.type == TT_PERIOD:
                            store += self.current_token.value + " "
                            self.advance()
                            if self.current_token.type == TT_KEYWORD:
                                store += self.current_token.value + " "
                                if self.current_token.value == 'array':
                                    store += self.current_token.value + " "
                                    self.advance()
                                    if self.current_token.type == TT_LSQBRAC:
                                        store += self.current_token.value + " "
                                        self.advance()
                                        if self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER:
                                            size = self.current_token.value
                                            store += identifier_token.value + " "
                                            self.advance()
                                            if self.current_token.type == TT_RSQBRAC:
                                                store += identifier_token.value + " "
                                                self.advance()
                                                return ResParse(self.current_token.line, store, "No Error", "No Error")
                                                #return {'keyword: let ' 'identifier': identifier_token.value, 'keyword: be ' 'data_type': data_type, 'data_struct': 'array', 'size:': size}
                                            else:
                                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                        else:
                                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected Expected Integer value")
                                    else:
                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected '['")
                                else:
                                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected array")
                            else:
                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected keyword (array)")
                        elif self.current_token.value not in KEYWORDS_DATA_TYPE:
                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected data type or structure")
                        else:
                            return ResParse(self.current_token.line, store, "No Error", "No Error")
                    elif self.current_token.value == 'set':
                        data_struct = self.current_token.value
                        store += self.current_token.value + " "
                        self.advance()
                        return ResParse(self.current_token.line, store, "No Error", "No Error")
                    else:
                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected data type or structure")
                else:
                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected data type or structure")
            else:
                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected 'be' keyword")
        else:
            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected an identifier")


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