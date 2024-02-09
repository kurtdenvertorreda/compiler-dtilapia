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
                discrete = self.parse_discrete()
                declarations.append(discrete)
            elif self.current_token.value == "output":
                output = self.parse_output()
                declarations.append(output)
            elif self.current_token.value == "input":
                input = self.parse_input()
                declarations.append(input)
            elif self.current_token.type == TT_KEYWORD and str(self.current_token.value) == "when":
                when_do = self.parse_conditional()
                declarations.append(when_do)
            elif self.current_token.type == TT_INVALID:
                invalid = self.parse_invalid()
                declarations.append(invalid)

            self.advance()  # Move to the next token

        return declarations  # Move the return statement outside the loop
    def parse_invalid(self):
        store = str(self.current_token.value) + " "
        return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected valid symbols")
        
    def parse_discrete(self):
        self.advance()
        store = "find" + " "
        identifier_token = self.current_token
        if identifier_token.type in TT_RESERVE:
            if self.current_token.value in ["permutation", "combination","gcd","lcm","lcd","isDivisible"]:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.value == "given":
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.type in [TT_INT, TT_IDENTIFIER]:
                        store += str(self.current_token.value)
                        self.advance()
                        if self.current_token.value == ",":
                            store += str(self.current_token.value)
                            self.advance()
                            if self.current_token.type in [TT_INT, TT_IDENTIFIER]:
                                store += str(self.current_token.value)
                                return ResParse(self.current_token.line, store, "No Error", "No Error")
                            else:
                                return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'Identifier' or 'Integer'.")
                        else:
                            return ResParse(self.current_token.line, store, "No Error", "No Error")
                    else:
                        return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'Identifier' or 'Integer'.")
                else:
                    return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'Keyword'.")
            elif self.current_token.value in ["inorder", "preorder","postorder"]:
                if self.current_token.value == "given":
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.type == TT_IDENTIFIER:
                        store += str(self.current_token.value)
                        return ResParse(self.current_token.line, store, "No Error", "No Error")
                    else:
                        return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'Identifier'.")
                else:
                    return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'given'.")
            elif self.current_token.value in ["isPrime", "isOdd", "isEven"]:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.value == "given":
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.type in [TT_INT, TT_IDENTIFIER]:
                        store += str(self.current_token.value)
                        self.advance()
                        return ResParse(self.current_token.line, store, "No Error", "No Error")
                    else:
                        return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'Identifier'.")
                else:
                    return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'given'.")
            elif self.current_token.value in ["permutation", "combination","gcd","lcm","lcd","isDivisible"]:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.value == "given":
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.type in [TT_INT, TT_IDENTIFIER]:
                        store += str(self.current_token.value)
                        self.advance()
                        if self.current_token.value == ",":
                            store += str(self.current_token.value)
                            self.advance()
                            if self.current_token.type in [TT_INT, TT_IDENTIFIER]:
                                store += str(self.current_token.value)
                                return ResParse(self.current_token.line, store, "No Error", "No Error")
                            else:
                                return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'Identifier' or 'Integer'.")
                        else:
                            return ResParse(self.current_token.line, store, "No Error", "No Error")
                    else:
                        return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'Identifier' or 'Integer'.")
                else:
                    return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'Keyword'.")
            elif self.current_token.value in ["ariseq", "geomseq","fiboseq"]:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.value == "given":
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.type in [TT_INT, TT_IDENTIFIER]:
                        store += str(self.current_token.value)
                        self.advance()
                        if self.current_token.value == ",":
                            store += str(self.current_token.value)
                            self.advance()
                            if self.current_token.type in [TT_INT, TT_IDENTIFIER]:
                                store += str(self.current_token.value)
                                self.advance()
                                if self.current_token.value == ",":
                                    store += str(self.current_token.value)
                                    self.advance()
                                    if self.current_token.type in [TT_INT, TT_IDENTIFIER]:
                                        store += str(self.current_token.value)
                                        return ResParse(self.current_token.line, store, "No Error", "No Error")
                                    else:
                                        return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'Identifier' or 'Integer'.")
                                else:
                                    return ResParse(self.current_token.line, store, "No Error", "No Error")
                            else:
                                return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'Identifier' or 'Integer'.")
                        else:
                            return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected ','.")
                    else:
                        return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'Identifier' or 'Integer'.")
                else:
                    return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'Keyword'.")
            else:
                return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'Reserve Word'.")
        else:
            return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}', "Expected 'Reserve Word'.")
    
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
                assignment = self.parse_assignment()
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
                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected array.")
            else:
                raise Exception(f"Invalid token at line {self.current_token.line}: Unexpected token {self.current_token.value}")

        # Consume '}'
        self.advance()
        return body
    
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
                                                                return ResParse(self.current_token.line, store, "No Error", "No Error")
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
                                                                            return ResParse(self.current_token.line, store, "No Error", "No Error")                                  
                                                                    else:
                                                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected same data type.")
                                                                    if size_allowed <= 0:
                                                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected exact size.")
                                                                if self.current_token.type == TT_RCBRAC:
                                                                    return ResParse(self.current_token.line, store, "No Error", "No Error")
                                                                else:
                                                                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                                            else:
                                                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ','.")
                                                        else:
                                                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected data type value.")
                                                    else:
                                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected '{'.")
                                                else:
                                                    return ResParse(self.current_token.line, store, "No Error", "No Error")
                                            else:
                                                return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line+1)}', "Expected ']'.")
                                        else:
                                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected integer.")
                                    else:
                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected '[]'.")
                                else:
                                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected array.")
                            else:
                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected array.")
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
                                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected same data type value.")
                                    return ResParse(self.current_token.line, store, "No Error", "No Error")
                                else:
                                    return ResParse(self.current_token.line, store, "No Error", "No Error")
                            elif self.current_token.type == TT_SNGQ:
                                store += str(self.current_token.value) + " "
                                self.advance()
                                if self.current_token.type == TT_CHAR:
                                    store += str(self.current_token.value) + " "
                                    self.advance()
                                    if self.current_token.type == TT_SNGQ:
                                        store += str(self.current_token.value) + " "
                                        self.advance()
                                        return ResParse(self.current_token.line, store, "No Error", "No Error")
                                    else:
                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected '}'.")
                                else:
                                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected character.")
                            elif self.current_token.type == TT_DBLQ:
                                store += str(self.current_token.value) + " "
                                self.advance()
                                if self.current_token.type == TT_STRING:
                                    store += str(self.current_token.value) + " "
                                    self.advance()
                                    if self.current_token.type == TT_DBLQ:
                                        store += str(self.current_token.value) + " "
                                        self.advance()
                                        return ResParse(self.current_token.line, store, "No Error", "No Error")
                                    else:
                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected '}'.")
                                else:
                                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected string.")
                            else:
                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected data type value.")
                        elif self.current_token.value not in KEYWORDS_DATA_TYPE:
                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected data type or period or assignment")
                        else:
                            return ResParse(self.current_token.line, store, "No Error", "No Error")
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
                                        return ResParse(self.current_token.line, store, "No Error", "No Error")
                                    elif self.current_token.type == TT_COMMA:
                                        while self.current_token.type == TT_COMMA:
                                            store += str(self.current_token.value) + " "
                                            self.advance()
                                            if self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER or self.current_token.type == TT_FLOAT or self.current_token.type == TT_STRING or self.current_token.type == TT_CHAR or self.current_token.type == TT_COMPL:
                                                value.append(self.current_token.value)
                                                data_type.append(self.current_token.type)
                                                store += str(self.current_token.value) + " "
                                                self.advance()                                           
                                            else:
                                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected data type value.")
                                        if self.current_token.type == TT_RCBRAC:
                                            return ResParse(self.current_token.line, store, "No Error", "No Error")
                                        else:
                                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected '}'.")
                                    else:
                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected comma.")
                                else:
                                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected data type value.")
                            else:
                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected '{'.")
                        elif self.current_token.type == TT_IDENTIFIER:
                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected assignment.")
                        else:
                           return ResParse(self.current_token.line, store, "No Error", "No Error")
                else:
                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected data type or structure.")
            else:
                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected 'be'.")
        else:
            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected identifier.")


    
    def parse_condition(self):
        # handling <identifier> <rel_op> <bool_val>
        identifier_token = self.current_token
        if identifier_token.type == TT_IDENTIFIER:
            self.advance()
            if self.current_token.type in {TT_GREATER_THAN, TT_LESS_THAN, TT_GREATER_THAN_EQUAL, TT_LESS_THAN_EQUAL, TT_EQUAL_TO, TT_NOT_EQUAL_TO}:
                rel_op_token = self.current_token
                self.advance()
                if self.current_token.type == TT_BOOL:
                    val_token = self.current_token
                    value_type = 'bool_val'
                    self.advance()
                elif self.current_token.type == TT_INT:
                    val_token = int(self.current_token.value)
                    value_type = 'integer'
                    self.advance()
                elif self.current_token.type == TT_IDENTIFIER:
                    val_token = self.current_token.value
                    value_type = 'identifier'
                    self.advance()
                else:
                    raise Exception("Invalid token at line {}: Expected boolean, digit, or identifier value".format(self.current_token.line))
                
                # Check for logical operator
                if self.current_token.type in {TT_NEGATION, TT_DISJUNCTION, TT_CONJUNCTION, TT_CONDITIONAL, TT_IMPLICATION, TT_BICONDITIONAL}:
                    logical_op_token = self.current_token
                    self.advance()
                else:
                    logical_op_token = None
            else:
                raise Exception("Invalid token at line {}: Expected relational operator".format(self.current_token.line))
        else:
            raise Exception("Invalid token at line {}: Expected identifier".format(self.current_token.line))
        return {'identifier': identifier_token.value, 'rel_op': rel_op_token.value, 'value_type': value_type, 'value': val_token, 'logical_op': logical_op_token.value if logical_op_token else None}    
    
    
    def parse_data_type(self):
        data_type = ''
        while self.current_token.type in (TT_IDENTIFIER, TT_PERIOD):
            data_type += str(self.current_token.value)
            self.advance()
        return data_type
    
    def parse_input(self):
        self.advance()
        store = "input" + " "
        if self.current_token.value == "':'":
            store += str(self.current_token.value) + " "
            self.advance()  # Move past ':'
            identifier_token = self.current_token
            if identifier_token.type == TT_IDENTIFIER:
                store += str(self.current_token.value) + " "
                self.advance()
                return ResParse(self.current_token.line, store, "No Error", "No Error")
            else:
                return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line+1)}', "Expected ':.")
        else:
            return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line+1)}', "Expected ':.")
        
    
    def parse_output(self):
        self.advance()  # Move past 'OUTPUT' keyword
        store = "output" + " "

        if self.current_token.type == TT_COLON:
            store += str(self.current_token.value) + " "
            self.advance()  # Move past ':'
            identifier_token = self.current_token

            if identifier_token.type == TT_IDENTIFIER:
                store += str(self.current_token.value) + " "
                self.advance()
                return ResParse(self.current_token.line, store, "No Error", "No Error")
            elif self.current_token.type == TT_INT:
                store += str(self.current_token.value) + " "
                int_token = self.current_token
                self.advance()
                return ResParse(str(self.current_token.line), store, "No Error", "No Error")
            elif self.current_token.type == TT_FLOAT:
                store += str(self.current_token.value) + " "
                float_token = self.current_token
                self.advance()
                return ResParse(str(self.current_token.line), store, "No Error", "No Error")
            elif self.current_token.value == "'":
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.type == TT_CHAR:
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.value == "'":
                        store += str(self.current_token.value) + " "
                        self.advance()
                return ResParse(str(self.current_token.line), store, "No Error", "No Error")
            elif self.current_token.type == TT_CHAR:
                store += str(self.current_token.value) + " "
                char_token = self.current_token
                self.advance()
                return ResParse(str(self.current_token.line), store, "No Error", "No Error")
            elif self.current_token.type == TT_COMPL:
                store += str(self.current_token.value) + " "
                complex_token = self.current_token
                self.advance()
                return ResParse(str(self.current_token.line), store, "No Error", "No Error")
            elif self.current_token.type == TT_BOOL:
                store += str(self.current_token.value) + " "
                bool_token = self.current_token
                self.advance()
                return ResParse(str(self.current_token.line), store, "No Error", "No Error")
            else:
                return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line+1)}', "Expected 'identifier/expression'.")
        else:
            return ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line+1)}', "Expected ':.")
    
    
    def parse_assignment(self):
        # Move past the first identifier
        store = self.current_token.value + " "
        self.advance()
        if self.current_token.type == TT_ASSIGNMENT:
            store += str(self.current_token.value) + " "
            self.advance()  # Move past the assignment operator
            
            # Check for identifier or literal types
            if self.current_token.type in [TT_IDENTIFIER, TT_INT, TT_FLOAT, TT_STRING, TT_CHAR, TT_COMPL, TT_BOOL]:
                store += str(self.current_token.value) + " "
                return ResParse(self.current_token.line, store, "No Error", "No Error")
            else:
                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected identifier or literal after '=' operator.")
        elif self.current_token.type == TT_ADDITION_ASSIGNMENT:
            store += str(self.current_token.value) + " "
            self.advance()  # Move past the addition assignment operator
            
            # Check for identifier or literal types
            if self.current_token.type in [TT_INT, TT_FLOAT]:
                store += str(self.current_token.value) + " "
                return ResParse(self.current_token.line, store, "No Error", "No Error")
            else:
                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected numeric literal after '+=' operator.")
        elif self.current_token.type == TT_SUBTRACTION_ASSIGNMENT:
            store += str(self.current_token.value) + " "
            self.advance()  # Move past the subtraction assignment operator
            
            # Check for identifier or literal types
            if self.current_token.type in [TT_INT, TT_FLOAT]:
                store += str(self.current_token.value) + " "
                return ResParse(self.current_token.line, store, "No Error", "No Error")
            else:
                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected numeric literal after '-=' operator.")
        elif self.current_token.type == TT_MULTIPLICATION_ASSIGNMENT:
            store += str(self.current_token.value) + " "
            self.advance()  # Move past the multiplication assignment operator
            

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