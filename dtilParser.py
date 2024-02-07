from constants import *
from dtilapia import Lexer

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
        elif self.current_token.type == TT_KEYWORD and self.current_token.value == "when":
            declaration = self.parse_conditional()
            declarations.append(declaration)
        elif self.current_token.type == TT_KEYWORD and self.current_token.value == "output":
            declaration = self.parse_output()
            declarations.append(declaration)
        else:
            raise Exception("Invalid token at line {}: Expected 'let' keyword".format(self.current_token.line))
        return declarations

    def parse_declaration(self):
        self.advance()  # Move past 'let' keyword
        identifier_token = self.current_token
        if identifier_token.type == TT_IDENTIFIER:
            self.advance()  # Move past identifier
            if self.current_token.type == TT_KEYWORD and self.current_token.value == "be":
                self.advance()  # Move past 'be' keyword
                if self.current_token.type == TT_KEYWORD:
                    if self.current_token.value in KEYWORDS_DATA_TYPE:  # Check if the token type is one of the data types
                        data_type = self.current_token.value  # Get the value of the data type token
                        self.advance()
                        if self.current_token.type == TT_PERIOD:
                            self.advance()
                            if self.current_token.type == TT_KEYWORD:
                                if self.current_token.value == 'array':
                                    self.advance()
                                    if self.current_token.type == TT_LSQBRAC:
                                        self.advance()
                                        if self.current_token.type == TT_INT:
                                            size = self.current_token.value
                                            self.advance()
                                            if self.current_token.type == TT_RSQBRAC:
                                                self.advance()
                                                if self.current_token.type == TT_ASSIGNMENT:
                                                    self.advance()
                                                    if self.current_token.type == TT_LCBRAC:
                                                        self.advance()
                                                        if self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER or self.current_token.type == TT_FLOAT or self.current_token.type == TT_STRING or self.current_token.type == TT_CHAR or self.current_token.type == TT_COMPL:
                                                            value = [self.current_token.value]
                                                            data_type = self.current_token.type
                                                            self.advance()
                                                            if self.current_token.type == TT_RCBRAC:
                                                                self.advance()
                                                                return {'keyword: let ' 'identifier': identifier_token.value, 'keyword: be ' 'data_type': data_type, 'data_struct': 'array', 'size:': size, 'value': value}
                                                            elif self.current_token.type == TT_COMMA:
                                                                size_allowed = size
                                                                while self.current_token.type == TT_COMMA:
                                                                    self.advance()
                                                                    if self.current_token.type == data_type:
                                                                        value.append(self.current_token.value)
                                                                        self.advance()                
                                                                        size_allowed -= 1                                  
                                                                    else:
                                                                        raise Exception("Invalid token at line {}: Expected same data type value".format(self.current_token.line))
                                                                if size_allowed == 0:
                                                                        raise Exception("Invalid token at line {}: Expected size".format(self.current_token.line))
                                                                elif self.current_token.type == TT_RCBRAC:
                                                                    return {'keyword: let ' 'identifier': identifier_token.value, 'keyword: be ' 'data_type': data_type, 'data_struct': 'array', 'size:': size, 'value': value}
                                                                else:
                                                                    raise Exception("Invalid token at line {}: Expected '}'".format(self.current_token.line))
                                                            else:
                                                                raise Exception("Invalid token at line {}: Expected ',' or ']".format(self.current_token.line))
                                                        else:
                                                            raise Exception("Invalid token at line {}: Expected data type value".format(self.current_token.line))
                                                    else:
                                                        raise Exception("Invalid token at line {}: Expected '{'".format(self.current_token.line))
                                                else:
                                                    return {'keyword: let ' 'identifier': identifier_token.value, 'keyword: be ' 'data_type': data_type, 'data_struct': 'array', 'size:': size}
                                            else:
                                                raise Exception("Invalid token at line {}: Expected ']'.".format(self.current_token.line))
                                        else:
                                            raise Exception("Invalid token at line {}: Expected Expected Integer value".format(self.current_token.line))
                                    else:
                                        raise Exception("Invalid token at line {}: Expected '['".format(self.current_token.line))
                                else:
                                    raise Exception("Invalid token at line {}: Expected array".format(self.current_token.line))
                            else:
                                raise Exception("Invalid token at line {}: Expected keyword (array)".format(self.current_token.line))
                        elif self.current_token.value not in KEYWORDS_DATA_TYPE:
                            raise Exception("Invalid token at line {}: Expected data type or structure".format(self.current_token.line))
                        else:
                            return {'keyword: let ' 'identifier': identifier_token.value, 'keyword: be ' 'data_type': data_type}  # Return identifier and data type
                    elif self.current_token.value == 'set':
                        data_struct = self.current_token.value
                        self.advance()
                        return {'keyword: let ' 'identifier': identifier_token.value, 'keyword: be ' 'data_type': data_struct}
                    else:
                        raise Exception("Invalid token at line {}: Expected data type or structure".format(self.current_token.line))
                else:
                    raise Exception("Invalid token at line {}: Expected data type or structure".format(self.current_token.line))
            else:
                raise Exception("Invalid token at line {}: Expected 'be' keyword".format(self.current_token.line))
        else:
            raise Exception("Invalid token at line {}: Expected an identifier".format(identifier_token.line))

## OUTPUT ##
    def parse_output(self):
        if self.current_token.type == TT_KEYWORD and self.current_token.value == "output":
            self.advance()  # Move past 'output' keyword
            if self.current_token.type == TT_COLON:
                self.advance()  # Move past ':'
                identifier_token = self.current_token
                if identifier_token.type == TT_IDENTIFIER:
                    self.advance()
                    return {'type': 'output', 'identifier': identifier_token.value}
                elif self.current_token.type == TT_INT:
                    value = self.current_token.value
                    self.advance()
## CONDITIONAL STATEMENTS ##
    def parse_conditional(self):
        if self.current_token.type == TT_KEYWORD and self.current_token.value == "when":
            self.advance()  # Move past 'when' keyword
            condition = self.parse_condition()
            if self.current_token.type == TT_KEYWORD and self.current_token.value == "do":
                self.advance()  # Move past 'do' keyword
                self.eat(TT_COLON)  # Consume ':'
                body = self.parse_body()
                return {'type': 'when-do', 'condition': condition, 'body': body}
            else:
                raise Exception("Invalid token at line {}: Expected 'do' keyword".format(self.current_token.line))
        elif self.current_token.type == TT_KEYWORD and self.current_token.value == "when_other":
            return self.parse_when_other_statement()
        elif self.current_token.type == TT_KEYWORD and self.current_token.value == "when_multi_other":
            return self.parse_when_multi_other_statement()
        else:
            raise Exception("Invalid token at line {}: Expected 'when', 'when_other', or 'when_multi_other' keyword".format(self.current_token.line))

    def parse_condition(self):
        # handling <identifier> <rel_op> <bool_val>
        identifier_token = self.current_token
        if identifier_token.type == TT_IDENTIFIER:
            self.advance()
            if self.current_token.type == TT_REL_OP: #checks if current char is a rel_op
                self.advance()
                if self.current_token.type == TT_BOOL:
                    self.advance()
                else:
                    raise Exception("Invalid token at line {}: Expected boolean value".format(self.current_token.line))
                if self.current_token.type == DIGITS:
                    self.advance()
                else:
                    raise Exception("Invalid token at line {}: Expected integer value".format(self.current_token.line))
                if self.current_token.type == TT_IDENTIFIER:
                    self.advance()
                else:
                    raise Exception("Invalid token at line {}: Expected identifier".format(self.current_token.line))
            return {'identifier': identifier_token.value, 'rel_op': self.current_token.value, 'bool_val': self.current_token.value}




################################
#
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