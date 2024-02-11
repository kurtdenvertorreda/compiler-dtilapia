import constants
import dtilParser

# INPUT
def parse_input(self):
    self.advance()
    store = "input" + " "
    
    if self.current_token.type == constants.TT_COLON:
        store += str(self.current_token.value) + " "
        self.advance()  # Move past ':'
        identifier_token = self.current_token
        
        if identifier_token.type == constants.TT_IDENTIFIER:
            store += str(self.current_token.value) + " "
            self.advance()
        else:
            self.idx = len(self.tokens)
            return dtilParser.ResParse(str(self.current_token.line), store, f'Expected an identifier after ":" at line {str(self.current_token.line+1)}')
        return dtilParser.ResParse(self.current_token.line, store, " ")
    else:
        self.idx = len(self.tokens)
        return dtilParser.ResParse(str(self.current_token.line), store, f'Expected a ":" after "input" keyword at line {str(self.current_token.line+1)}')
    

# OUTPUT
def parse_output(self):
    self.advance()  # Move past 'OUTPUT' keyword
    store = "output" + " "

    if self.current_token.type == constants.TT_COLON:
        store += str(self.current_token.value) + " "
        self.advance()  # Move past ':'
        identifier_token = self.current_token

        if identifier_token.type == constants.TT_IDENTIFIER:
            store += str(self.current_token.value) + " "
            self.advance()
            while self.current_token.type in [constants.TT_MODULO, constants.TT_EXPONENT, constants.TT_PLUS, constants.TT_MINUS, constants.TT_MUL, constants.TT_DIV]:
                store += str(self.current_token.value) + " "
                self.advance()

                if self.current_token.type == constants.TT_IDENTIFIER:
                    store += str(self.current_token.value) + " "
                    self.advance()
                else:
                    break
            return dtilParser.ResParse(self.current_token.line, store, " ")
        elif self.current_token.type == constants.TT_INT:
            store += str(self.current_token.value) + " "
            int_token = self.current_token
            self.advance()
            return dtilParser.ResParse(str(self.current_token.line), store, " ")
        elif self.current_token.type == constants.TT_FLOAT:
            store += str(self.current_token.value) + " "
            float_token = self.current_token
            self.advance()
            return dtilParser.ResParse(str(self.current_token.line), store, " ")
        elif self.current_token.value == "'":
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.type == constants.TT_CHAR:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.value == "'":
                    store += str(self.current_token.value) + " "
                    self.advance()
            return dtilParser.ResParse(str(self.current_token.line), store, " ")
        elif self.current_token.type == constants.TT_DBLQ:
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.type == constants.TT_STRING:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.type == constants.TT_DBLQ:
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.value == "+":
                        store += str(self.current_token.value) + " "
                        self.advance()
                        if self.current_token.type == constants.TT_IDENTIFIER:
                            store += str(self.current_token.value) + " "
                            self.advance()
                        else:
                            self.idx = len(self.tokens)
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Expected an identifier after "+" at line {str(self.current_token.line+1)}')
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Expected a closing double quotation mark after String value at line {str(self.current_token.line+1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Expected a String value after opening double quotation mark at line {str(self.current_token.line+1)}')
            return dtilParser.ResParse(str(self.current_token.line), store, " ")
        elif self.current_token.type == constants.TT_COMPL:
            store += str(self.current_token.value) + " "
            complex_token = self.current_token
            self.advance()
            return dtilParser.ResParse(str(self.current_token.line), store, " ")
        elif self.current_token.type == constants.TT_BOOL:
            store += str(self.current_token.value) + " "
            bool_token = self.current_token
            self.advance()
            return dtilParser.ResParse(str(self.current_token.line), store, " ")
        else:
            self.idx = len(self.tokens)
            return dtilParser.ResParse(str(self.current_token.line), store, f'Expected an expression, or variable after ":" at line {str(self.current_token.line+1)}')
    else:
        self.idx = len(self.tokens)
        return dtilParser.ResParse(str(self.current_token.line), store, f'Expected a ":" after "output" keyword at line {str(self.current_token.line+1)}')