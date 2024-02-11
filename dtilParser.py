from constants import *
from dtilapia import Lexer
import iteratives, discrete, input_output, function

class ResParse:
    def __init__(self, line, code, errorName):
        self.line = line
        self.code = code
        self.errorName = errorName
    
    def __repr__(self):
        if self.errorName: return f'{self.line}~{self.code}~{self.errorName}'
        return f'{self.line}:{self.code}:No Error'

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
            if self.current_token == "\n":
                self.advance()
                continue
            elif self.current_token.value == "let":
                declaration = self.parse_declaration()
                declarations.append(declaration)
            elif self.current_token.type == TT_IDENTIFIER:  # Add condition for assignment parsing
                assignment = self.parse_assignment()
                declarations.append(assignment)
            elif self.current_token.type == TT_KEYWORD and str(self.current_token.value) == "find":
                discrete_f = discrete.parse_discrete(self)
                declarations.append(discrete_f)
            elif self.current_token.value == "output":
                output = input_output.parse_output(self)
                declarations.append(output)
            elif self.current_token.value == "input":
                input = input_output.parse_input(self)
                declarations.append(input)
            elif self.current_token.value == "for":
                for_loop = iteratives.parse_for(self)
                declarations.append(for_loop)
            elif self.current_token.value == "hence":
                hence_des = discrete.parse_hence(self)
                declarations.append(hence_des)
            elif self.current_token.value == "while":
                while_loop = iteratives.parse_while(self)
                declarations.append(while_loop)
            elif self.current_token.value == "when":
                when_statement = iteratives.parse_when(self)
                declarations.append(when_statement)
            elif self.current_token.value == "otherwise":
                otherwise_statement = iteratives.parse_otherwise(self)
                declarations.append(otherwise_statement)
            elif self.current_token.type == TT_INVALID:
                invalid = self.parse_invalid()
                declarations.append(invalid)
            elif self.current_token.value == "funct":
                funct = function.parse_funct(self)
                declarations.append(funct)

            self.advance()  # Move to the next token

        return declarations  # Move the return statement outside the loop
    
    # INVALID TOKENS
    def parse_invalid(self):
        store = str(self.current_token.value) + " "
        self.idx = len(self.tokens)
        return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
        
    # BODY OF FUNCTIONS/STATEMENTS
    def parse_body(self):
        body = []
        if self.current_token.value != "{":
            raise Exception(f"Expected '{{' at line {self.current_token.line}, found {self.current_token.value}")
        
        # Consume '{'
        self.advance()

        while self.current_token.value != "}":
            if self.current_token == "\n":
                self.advance()
                continue
            elif self.current_token.type == TT_KEYWORD and self.current_token.value == "let":
                assignment = self.parse_declaration()
                body.append(assignment)
            elif self.current_token.type == TT_IDENTIFIER:  
                assignment = self.parse_assignment()
                body.append(assignment)
            elif self.current_token.type == TT_KEYWORD and self.current_token.value == "find":
                discrete = self.parse_discrete()
                body.append(discrete)
            elif self.current_token.type == TT_KEYWORD and self.current_token.value in ["when", "when_other", "when_multi_other"]:
                conditional = self.parse_conditional()
                body.append(conditional)
            elif self.current_token.value == "output":
                output = self.parse_output()
                body.append(output)
            elif self.current_token.value == "input":
                input = self.parse_input()
                body.append(input)
            elif self.current_token.type == TT_INVALID:
                self.idx = len(self.tokens)
                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}')
            else:
                raise Exception(f"Invalid token at line {self.current_token.line}: Unexpected token {self.current_token.value}")

        # Consume '}'
        self.advance()
        return body

    # DECLARATION STATEMENTS    
    def parse_declaration(self):
        self.advance()  # Move past 'let' keyword
        store = "let" + " "
        identifier_token = self.current_token

        if identifier_token.type == TT_IDENTIFIER:
            store += str(self.current_token.value) + " "
            self.advance()  # Move past identifier
            if self.current_token.type == TT_KEYWORD and self.current_token.value == "be":
                store += str(self.current_token.value) + " "
                self.advance()  # Move past 'be' keyword
                if self.current_token.type == TT_KEYWORD:
                    if self.current_token.value in KEYWORDS_DATA_TYPE:  # Check if the token type is one of the data types
                        store += str(self.current_token.value) + " "
                        data_type = self.current_token.value  # Get the value of the data type token
                        self.advance()
                        if self.current_token.type == TT_PERIOD:
                            store += str(self.current_token.value) + " "
                            self.advance()
                            if self.current_token.type == TT_KEYWORD:
                                if self.current_token.value == 'array':
                                    store += str(self.current_token.value) + " "
                                    self.advance()
                                    if self.current_token.type == TT_LSQBRAC:
                                        store += str(self.current_token.value) + " "
                                        self.advance()
                                        if self.current_token.type == TT_INT:
                                            size = self.current_token.value
                                            store += str(self.current_token.value) + " "
                                            self.advance()
                                            if self.current_token.type == TT_RSQBRAC:
                                                store += str(self.current_token.value) + " "
                                                self.advance()
                                                if self.current_token.type == TT_ASSIGNMENT:
                                                    store += str(self.current_token.value) + " "
                                                    self.advance()
                                                    if self.current_token.type == TT_LCBRAC:
                                                        store += str(self.current_token.value) + " "
                                                        self.advance()
                                                        if self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER or self.current_token.type == TT_FLOAT or self.current_token.type == TT_STRING or self.current_token.type == TT_CHAR or self.current_token.type == TT_COMPL:
                                                            value = [self.current_token.value]
                                                            data_type = self.current_token.type
                                                            store += str(self.current_token.value) + " "
                                                            self.advance()
                                                            if self.current_token.type == TT_RCBRAC:
                                                                store += str(self.current_token.value) + " "
                                                                self.advance()
                                                                return ResParse(self.current_token.line, store, " ")
                                                            elif self.current_token.type == TT_COMMA:
                                                                size_allowed = size - 1 
                                                                while self.current_token.type == TT_COMMA:
                                                                    store += str(self.current_token.value) + " "
                                                                    self.advance()
                                                                    if self.current_token.type == data_type:
                                                                        size_allowed = size_allowed - 1
                                                                        value.append(self.current_token.value)
                                                                        store += str(self.current_token.value) + " "
                                                                        self.advance()                
                                                                        if self.current_token.type == TT_RCBRAC:
                                                                            store += str(self.current_token.value) + " "
                                                                            self.advance()
                                                                            return ResParse(self.current_token.line, store, " ")                  
                                                                    else:
                                                                        self.idx = len(self.tokens)
                                                                        return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected all values in array to be similar at line {str(self.current_token.line + 1)}')
                                                                    if size_allowed <= 0:
                                                                        self.idx = len(self.tokens)
                                                                        return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected correct size of array at line {str(self.current_token.line + 1)}')
                                                                if self.current_token.type == TT_RCBRAC:
                                                                    return ResParse(self.current_token.line, store, " ")
                                                                else:
                                                                    self.idx = len(self.tokens)
                                                                    return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected comma at line {str(self.current_token.line + 1)}')
                                                            else:
                                                                self.idx = len(self.tokens)
                                                                return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected }} or comma at line at line {str(self.current_token.line + 1)}')
                                                        else:
                                                            self.idx = len(self.tokens)
                                                            return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a valid data value at line {str(self.current_token.line + 1)}')
                                                    else:
                                                        self.idx = len(self.tokens)
                                                        return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected {{ at line {str(self.current_token.line + 1)}')
                                                else:
                                                    return ResParse(self.current_token.line, store, " ")
                                            else:
                                                self.idx = len(self.tokens)
                                                return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a "]" for closing the size specification of the array at line {str(self.current_token.line + 1)}')
                                        else:
                                            self.idx = len(self.tokens)
                                            return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected size to be an integer at line {str(self.current_token.line + 1)}')
                                    else:
                                        self.idx = len(self.tokens)
                                        return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a size specification for the array at line {str(self.current_token.line + 1)}')
                                else:
                                    self.idx = len(self.tokens)
                                    return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "array" keyword at line {str(self.current_token.line + 1)}')
                            else:
                                self.idx = len(self.tokens)
                                return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "array" keyword at line {str(self.current_token.line + 1)}')
                        elif self.current_token.type == TT_ASSIGNMENT:
                            store += str(self.current_token.value) + " "
                            self.advance()
                            if self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER or self.current_token.type == TT_FLOAT or self.current_token.type == TT_BOOL or self.current_token.type == TT_COMPL:
                                store += str(self.current_token.value) + " "
                                data_type = self.current_token.type
                                self.advance()
                                if self.current_token.type == TT_COMMA:
                                    while self.current_token.type == TT_COMMA:
                                        store += str(self.current_token.value) + " "
                                        self.advance()
                                        if self.current_token.type == data_type:
                                            store += str(self.current_token.value) + " "
                                            self.advance()
                                        else:
                                            self.idx = len(self.tokens)
                                            return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected all values in array to be similar at line {str(self.current_token.line + 1)}')
                                    return ResParse(self.current_token.line, store, " ")
                                else:
                                    return ResParse(self.current_token.line, store, " ")
                            elif self.current_token.type == TT_SNGQ:
                                store += str(self.current_token.value) + " "
                                self.advance()
                                if self.current_token.type == TT_CHAR:
                                    store += str(self.current_token.value) + " "
                                    self.advance()
                                    if self.current_token.type == TT_SNGQ:
                                        store += str(self.current_token.value) + " "
                                        self.advance()
                                        return ResParse(self.current_token.line, store, " ")
                                    else:
                                        self.idx = len(self.tokens)
                                        return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected " \' " at line {str(self.current_token.line + 1)}')
                                else:
                                    return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected character at line {str(self.current_token.line + 1)}')
                            elif self.current_token.type == TT_DBLQ:
                                store += str(self.current_token.value) + " "
                                self.advance()
                                if self.current_token.type == TT_STRING:
                                    store += str(self.current_token.value) + " "
                                    self.advance()
                                    if self.current_token.type == TT_DBLQ:
                                        store += str(self.current_token.value) + " "
                                        self.advance()
                                        return ResParse(self.current_token.line, store, " ")
                                    else:
                                        self.idx = len(self.tokens)
                                        return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected " " " at line {str(self.current_token.line + 1)}')
                                else:
                                    self.idx = len(self.tokens)
                                    return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected string at line {str(self.current_token.line + 1)}')
                            else:
                                self.idx = len(self.tokens)
                                return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a valid data value at line {str(self.current_token.line + 1)}')
                        else:
                            return ResParse(self.current_token.line, store, " ")
                    elif self.current_token.value == 'set':
                        store += str(self.current_token.value) + " "
                        self.advance()
                        if self.current_token.type == TT_ASSIGNMENT:
                            store += str(self.current_token.value) + " "
                            self.advance()
                            if self.current_token.type == TT_LCBRAC:
                                store += str(self.current_token.value) + " "
                                self.advance()
                                if self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER or self.current_token.type == TT_FLOAT or self.current_token.type == TT_STRING or self.current_token.type == TT_CHAR or self.current_token.type == TT_COMPL:
                                    value = [self.current_token.value]
                                    data_type = [self.current_token.type]
                                    store += str(self.current_token.value) + " "
                                    self.advance()
                                    if self.current_token.type == TT_RCBRAC:
                                        store += str(self.current_token.value) + " "
                                        self.advance()
                                        return ResParse(self.current_token.line, store, " ")
                                    elif self.current_token.type == TT_COMMA:
                                        while self.current_token.type == TT_COMMA:
                                            store += str(self.current_token.value) + " "
                                            self.advance()
                                            if self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER or self.current_token.type == TT_FLOAT or self.current_token.type == TT_STRING or self.current_token.type == TT_CHAR or self.current_token.type == TT_COMPL:
                                                value.append(self.current_token.value)
                                                data_type.append(self.current_token.type)
                                                store += str(self.current_token.value) + " "
                                                self.advance()                        
                                                if self.current_token.type == TT_RCBRAC:
                                                    store += str(self.current_token.value) + " "
                                                    self.advance()
                                                    return ResParse(self.current_token.line, store, " ")
                                            else:
                                                self.idx = len(self.tokens)
                                                return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected valid data type value at line {str(self.current_token.line + 1)}')
                                        if self.current_token.type == TT_RCBRAC:
                                            store += str(self.current_token.value) + " "
                                            self.advance()
                                            return ResParse(self.current_token.line, store, " ")
                                        else:
                                            self.idx = len(self.tokens)
                                            return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "}}" at line {str(self.current_token.line + 1)}')
                                    else:
                                        self.idx = len(self.tokens)
                                        return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "=" or "}}" at line {str(self.current_token.line + 1)}')
                                else:
                                    self.idx = len(self.tokens)
                                    return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected valid data type value at line {str(self.current_token.line + 1)}')
                            else:
                                self.idx = len(self.tokens)
                                return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "{{" at line {str(self.current_token.line + 1)}')
                        else:
                            self.idx = len(self.tokens)
                            return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "=" at line {str(self.current_token.line + 1)}')
                    else:
                        self.idx = len(self.tokens)
                        return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a keyword representing a data type or a keyword representing a data structure at line {str(self.current_token.line + 1)}')
                else:
                    self.idx = len(self.tokens)
                    return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a keyword representing a data type or a keyword representing a data structure at line {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "be" keyword at line {str(self.current_token.line + 1)}')
        else:
            self.idx = len(self.tokens)
            return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected an identifier at line {str(self.current_token.line + 1)}')
    
    # DATA TYPE
    def parse_data_type(self):
        data_type = ''
        while self.current_token.type in (TT_IDENTIFIER, TT_PERIOD):
            data_type += str(self.current_token.value)
            self.advance()
        return data_type
    
    # ASSIGNMENT
    def parse_assignment(self):
        # Move past the first identifier
        store = self.current_token.value + " "
        self.advance()
        if self.current_token.type == TT_ASSIGNMENT:
            store += str(self.current_token.value) + " "
            self.advance()  # Move past the assignment operator
            
            # Check for identifier or literal types
            if self.current_token.type in [TT_IDENTIFIER, TT_INT, TT_FLOAT, TT_COMPL, TT_BOOL]:
                store += str(self.current_token.value) + " "
                return ResParse(self.current_token.line, store, " ")
            elif self.current_token.type == TT_DBLQ:
                store += '"'
                self.advance()
                if self.current_token.type == TT_STRING:
                    store += str(self.current_token.value) 
                    self.advance()
                    if self.current_token.type == TT_DBLQ:
                        store += '"'
                        return ResParse(self.current_token.line, store, " ")
                    else:
                        self.idx = len(self.tokens)
                        return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected double quotation at line {str(self.current_token.line + 1)}')
                else:
                    self.idx = len(self.tokens)
                    return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected string value at line {str(self.current_token.line + 1)}')
            elif self.current_token.type == TT_SNGQ:
                store += "'"
                self.advance()
                if self.current_token.type == TT_CHAR:
                    store += self.current_token.value 
                    self.advance()
                    if self.current_token.type == TT_SNGQ:
                        store += "'"
                        return ResParse(self.current_token.line, store, " ")
                    else:
                        self.idx = len(self.tokens)
                        return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected single quotation at line {str(self.current_token.line + 1)}')
                else:
                    self.idx = len(self.tokens)
                    return ResParse(str(self.current_token.line), store, f'Syntax Error: Expected char value at line {str(self.current_token.line + 1)}')
            else:
                return ResParse(self.current_token.line, store, f'Syntax Error: Expecting an identifier or literal at line {self.current_token.line}')
        elif self.current_token.type == TT_ADDITION_ASSIGNMENT:
            store += str(self.current_token.value) + " "
            self.advance()  # Move past the addition assignment operator
            
            # Check for identifier or literal types
            if self.current_token.type in [TT_INT, TT_FLOAT]:
                store += str(self.current_token.value) + " "
                return ResParse(self.current_token.line, store, " ")
            else:
                self.idx = len(self.tokens)
                return ResParse(self.current_token.line, store, f'Syntax Error: Expecting an integer or float at line {self.current_token.line}')
        elif self.current_token.type == TT_SUBTRACTION_ASSIGNMENT:
            store += str(self.current_token.value) + " "
            self.advance()  # Move past the subtraction assignment operator
            
            # Check for identifier or literal types
            if self.current_token.type in [TT_INT, TT_FLOAT]:
                store += str(self.current_token.value) + " "
                return ResParse(self.current_token.line, store, " ")
            else:
                self.idx = len(self.tokens)
                return ResParse(self.current_token.line, store, f'Syntax Error: Expecting an integer or float at line {self.current_token.line}')
        elif self.current_token.type == TT_MULTIPLICATION_ASSIGNMENT:
            store += str(self.current_token.value) + " "
            self.advance()  # Move past the multiplication assignment operator
        else:
            self.idx = len(self.tokens)
            return ResParse(self.current_token.line, store, f'Syntax Error: Invalid operator at line {self.current_token.line}')
            


# MAIN
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