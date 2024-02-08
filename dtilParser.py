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
        return f'{self.line}:{self.code} :No Error:No Error'

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
        while self.idx < len(self.tokens):
            if self.current_token.type == TT_KEYWORD and str(self.current_token.value) == "let":
                declaration = self.parse_declaration()
                declarations.append(declaration)
            elif self.current_token.type == TT_KEYWORD and str(self.current_token.value) == "when":
                when_do = self.parse_conditional()
                declarations.append(when_do)
            elif self.current_token.type == TT_KEYWORD and str(self.current_token.value) == "output":
                output = self.parse_output()
                declarations.append(output)
            else:
                raise Exception("Invalid token at line {}: Expected 'let' keyword".format(str(self.current_token.line)))

            self.advance()  # Move to the next token

        return declarations  # Move the return statement outside the loop
    
    def parse_declaration(self):
        error = ""
        errorDesc = ""
        self.advance()  # Move past 'let' keyword
        store = "let" + " "
        identifier_token = self.current_token

        if identifier_token.type == TT_IDENTIFIER:
              # Move past identifier
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.type == TT_KEYWORD and str(self.current_token.value) == "be":
                 # Move past 'be' keyword
                store += str(self.current_token.value) + " "
                self.advance() 
                if self.current_token.type == TT_KEYWORD:
                    if str(self.current_token.value) in KEYWORDS_DATA_TYPE:  # Check if the token type is one of the data types
                        data_type = str(self.current_token.value)  # Get the value of the data type token
                        store += str(self.current_token.value) + " "
                        self.advance()
                        if self.current_token.type == TT_PERIOD:
                            store += str(self.current_token.value) + " "
                            self.advance()
                            if self.current_token.type == TT_KEYWORD:
                                store += str(self.current_token.value) + " "
                                if str(self.current_token.value) == 'array':
                                    store += str(self.current_token.value) + " "
                                    self.advance()
                                    if self.current_token.type == TT_LSQBRAC:
                                        store += str(self.current_token.value) + " "
                                        self.advance()
                                        if self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER:
                                            size = str(self.current_token.value)
                                            store += identifier_token.value + " "
                                            self.advance()
                                            if self.current_token.type == TT_RSQBRAC:
                                                store += identifier_token.value + " "
                                                self.advance()
                                                return ResParse(str(self.current_token.line), store, "No Error", "No Error")
                                                #return {'keyword: let ' 'identifier': identifier_token.value, 'keyword: be ' 'data_type': data_type, 'data_struct': 'array', 'size:': size}
                                            else:
                                                return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line)}', "Expected ']'.")
                                        else:
                                            return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line)}', "Expected Expected Integer value")
                                    else:
                                        return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line)}', "Expected '['")
                                else:
                                    return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line)}', "Expected array")
                            else:
                                return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line)}', "Expected keyword (array)")
                        elif str(self.current_token.value) not in KEYWORDS_DATA_TYPE:
                            return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line)}', "Expected data type or structure")
                        else:
                            return ResParse(str(self.current_token.line), store, "No Error", "No Error")
                    elif str(self.current_token.value) == 'set':
                        data_struct = str(self.current_token.value)
                        store += str(self.current_token.value) + " "
                        self.advance()
                        return ResParse(str(self.current_token.line), store, "No Error", "No Error")
                    else:
                        return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line)}', "Expected data type or structure")
                else:
                    return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line)}', "Expected data type or structure")
            else:
                return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line)}', "Expected 'be' keyword")
        else:
            return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line)}', "Expected an identifier")

    ## OUTPUT ##
    def parse_output(self):
        self.advance()  # Move past 'OUTPUT' keyword
        store =  "output" + " "
        
        if self.current_token.type == TT_COLON:
            store += str(self.current_token.value) + " "
            self.advance()

            identifier_token = self.current_token
            if identifier_token.type == TT_IDENTIFIER:
                store += str(self.current_token.value) + " "
                self.advance()
                return ResParse(self.current_token.line, store, "No Error", "No Error")
            else:
                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected identifier after ':'.")
        else:
            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ':'.")



# ## CONDITIONAL STATEMENTS ##
    def parse_conditional(self):
        self.advance()  # Move past 'OUTPUT' keyword
        store = "when" + " "
        identifier_token = self.current_token
        if identifier_token.type == TT_IDENTIFIER:
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.type in [TT_GREATER_THAN, TT_LESS_THAN, TT_GREATER_THAN_EQUAL, TT_LESS_THAN_EQUAL, TT_EQUAL_TO, TT_NOT_EQUAL_TO]:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.type in [TT_BOOL, TT_INT, TT_IDENTIFIER]:
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.type == TT_KEYWORD and str(self.current_token.value) == "do":
                        store += str(self.current_token.value) + " "
                        self.advance()
                        if self.current_token.value == ';':
                            store += str(self.current_token.value) + " "
                            self.advance()
                        else:
                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ';'.")
                    else:
                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected 'do'.")
                else:
                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected a boolean, integer, or identifier value.")
            else:
                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected relational operator.")
            return ResParse(self.current_token.line, store, "No Error", "No Error")
        else:
            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected an identifier.")

    def parse_data_type(self):
        data_type = ''
        while self.current_token.type in (TT_IDENTIFIER, TT_PERIOD):
            data_type += str(self.current_token.value)
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