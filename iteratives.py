import constants
import dtilParser
def parse_for(self):
    store = "for" + " "
    self.advance()
    if self.current_token.type == constants.TT_IDENTIFIER:
        store += str(self.current_token.value) + " "
        self.advance()
        if self.current_token.value == "in":
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.type in [constants.TT_INT, constants.TT_STRING, constants.TT_IDENTIFIER]:
                store += str(self.current_token.value) + " "
                self.advance()
                if str(self.current_token.value) == "by":
                    store += self.current_token.value + " "
                    self.advance()
                    if self.current_token.type == constants.TT_INT:
                        store += str(self.current_token.value) + " "
                        self.advance()
                        if self.current_token.type == constants.TT_COLON:
                            store += str(self.current_token.value) + " "
                            self.advance()
                            if self.current_token.type == constants.TT_NEWLINE:
                                store += "\n"
                                self.advance()
                                if self.current_token.type == constants.TT_TAB:
                                    return dtilParser.ResParse(str(self.current_token.line - 1), store, f'____', "____'.")
                                else:
                                    return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}', "Expected 'Loop Body'.")
                            else:
                                return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}', "Expected 'Loop Body'.")
                        else:
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}', "Expected 'Colon'.")
                    else:
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}', "Expected 'looping value'.")
                else:
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}', "Expected 'by'.")
            else:
                return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}', "Expected 'Iteratives'.")
        else:
             return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}', "Expected 'in'.")
    else: 
        return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}', "Expected 'Identifier'.")