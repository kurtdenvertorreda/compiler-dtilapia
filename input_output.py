import constants
import dtilParser

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
            return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line+1)}')
        return dtilParser.dtilParser.ResParse(self.current_token.line, store, "No Error")
    else:
        return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line+1)}')
    

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
        elif self.current_token.value == "\"":
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.type == constants.TT_STRING:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.value == "\"":
                    store += str(self.current_token.value) + " "
                    self.advance()
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
            return dtilParser.ResParse(str(self.current_token.line), store, f'Expected an expression, or variable after ":" at line {str(self.current_token.line+1)}')
    else:
        return dtilParser.ResParse(str(self.current_token.line), store, f'Expected a ":" after the keyword "output" at line {str(self.current_token.line+1)}')