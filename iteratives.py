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
                                    return dtilParser.ResParse(str(self.current_token.line - 1), store, f'____')
                                else:
                                    self.idx = len(self.tokens)
                                    return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}')
                            else:
                                self.idx = len(self.tokens)
                                return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}')
                        else:
                            self.idx = len(self.tokens)
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}')
                    else:
                        self.idx = len(self.tokens)
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}')
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}')
        else:
            self.idx = len(self.tokens)
            return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}')
    else: 
        self.idx = len(self.tokens)
        return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}')

    

def parse_while(self):
    store = "while" + " "
    self.advance()
    if self.current_token.type in [constants.TT_INT, constants.TT_IDENTIFIER, constants.TT_FLOAT]:
        store += str(self.current_token.value) + " "
        self.advance()
        if self.current_token.type in [constants.TT_GREATER_THAN, constants.TT_LESS_THAN, constants.TT_GREATER_THAN_EQUAL, constants.TT_LESS_THAN_EQUAL, constants.TT_EQUAL_TO, constants.TT_NOT_EQUAL_TO]:
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.type in [constants.TT_INT, constants.TT_IDENTIFIER, constants.TT_FLOAT]:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.value == "do":
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.type == constants.TT_COLON:
                        store += str(self.current_token.value) + " "
                        self.advance()
                        if self.current_token.type == constants.TT_NEWLINE:
                            store += "\n"
                            self.advance()
                            if self.current_token.type == constants.TT_TAB:
                                return dtilParser.ResParse(str(self.current_token.line - 1), store, f'____')
                            else:
                                self.idx = len(self.tokens)
                                return dtilParser.ResParse(str(self.current_token.line), store, f'Expected an indented block after "while" statement at line {str(self.current_token.line + 1)}')
                        else:
                            self.idx = len(self.tokens)
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Expected a newline after ":" at line {str(self.current_token.line + 1)}')
                    else:
                        self.idx = len(self.tokens)
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Expected ":" after "do" keyword at line {str(self.current_token.line + 1)}')
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Expected "do" after condition at line {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax for condition at line {str(self.current_token.line + 1)}')
        else:
            self.idx = len(self.tokens)
            return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid operator used for condition at line {str(self.current_token.line + 1)}')
    else: 
        self.idx = len(self.tokens)
        return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax for condition at line {str(self.current_token.line + 1)}')


def parse_when(self):
    store = "when" + " "
    self.advance()
    if self.current_token.type in [constants.TT_INT, constants.TT_IDENTIFIER, constants.TT_FLOAT]:
        store += str(self.current_token.value) + " "
        self.advance()
        if self.current_token.type in [constants.TT_GREATER_THAN, constants.TT_LESS_THAN, constants.TT_GREATER_THAN_EQUAL, constants.TT_LESS_THAN_EQUAL, constants.TT_EQUAL_TO, constants.TT_NOT_EQUAL_TO]:
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.type in [constants.TT_INT, constants.TT_IDENTIFIER, constants.TT_FLOAT]:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.value == "do":
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.type == constants.TT_COLON:
                        store += str(self.current_token.value) + " "
                        self.advance()
                        if self.current_token.type == constants.TT_NEWLINE:
                            store += "\n"
                            self.advance()
                            if self.current_token.type == constants.TT_TAB:
                                return dtilParser.ResParse(str(self.current_token.line - 1), store, f'____')
                            else:
                                self.idx = len(self.tokens)
                                return dtilParser.ResParse(str(self.current_token.line), store, f'Expected an indented block after "when" statement at line {str(self.current_token.line + 1)}')
                        else:
                            self.idx = len(self.tokens)
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Expected a newline after ":" at line {str(self.current_token.line + 1)}')
                    else:
                        self.idx = len(self.tokens)
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Expected ":" after "do" keyword at line {str(self.current_token.line + 1)}')
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Expected "do" after condition at line {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax for condition at line {str(self.current_token.line + 1)}')
        else:
            self.idx = len(self.tokens)
            return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid operator used for condition at line {str(self.current_token.line + 1)}')
    else: 
        self.idx = len(self.tokens)
        return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax for condition at line {str(self.current_token.line + 1)}')


def parse_otherwise(self):
    store = "otherwise" + " "
    self.advance()
    if self.current_token.value == "do":
        store += str(self.current_token.value) + " "
        self.advance()
        if self.current_token.type == constants.TT_COLON:
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.type == constants.TT_NEWLINE:
                store += "\n"
                self.advance()
                if self.current_token.type == constants.TT_TAB:
                    return dtilParser.ResParse(str(self.current_token.line - 1), store, f'____')
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Expected an indented block after "otherwise" statement at line {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Expected a newline after ":" at line {str(self.current_token.line + 1)}')
        else:
            self.idx = len(self.tokens)
            return dtilParser.ResParse(str(self.current_token.line), store, f'Expected ":" after "do" keyword at line {str(self.current_token.line + 1)}')
    elif self.current_token.value == "when":
        store += str(self.current_token.value) + " "
        self.advance()
        if self.current_token.type in [constants.TT_INT, constants.TT_IDENTIFIER, constants.TT_FLOAT]:
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.type in [constants.TT_GREATER_THAN, constants.TT_LESS_THAN, constants.TT_GREATER_THAN_EQUAL, constants.TT_LESS_THAN_EQUAL, constants.TT_EQUAL_TO, constants.TT_NOT_EQUAL_TO]:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.type in [constants.TT_INT, constants.TT_IDENTIFIER, constants.TT_FLOAT]:
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.value == "do":
                        store += str(self.current_token.value) + " "
                        self.advance()
                        if self.current_token.type == constants.TT_COLON:
                            store += str(self.current_token.value) + " "
                            self.advance()
                            if self.current_token.type == constants.TT_NEWLINE:
                                store += "\n"
                                self.advance()
                                if self.current_token.type == constants.TT_TAB:    
                                    return dtilParser.ResParse(str(self.current_token.line - 1), store, f'____')
                                else:
                                    self.idx = len(self.tokens)
                                    return dtilParser.ResParse(str(self.current_token.line), store, f'Expected an indented block after "otherwise when" statement at line {str(self.current_token.line + 1)}')
                            else:
                                self.idx = len(self.tokens)
                                return dtilParser.ResParse(str(self.current_token.line), store, f'Expected a newline after ":" at line {str(self.current_token.line + 1)}')
                        else:
                            self.idx = len(self.tokens)
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Expected ":" after "do" keyword at line {str(self.current_token.line + 1)}')
                    else:
                        self.idx = len(self.tokens)
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Expected "do" after condition at line {str(self.current_token.line + 1)}')
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax for condition at line {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid operator used for condition at line {str(self.current_token.line + 1)}')
        else: 
            self.idx = len(self.tokens)
            return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax for condition at line {str(self.current_token.line + 1)}')
    else:
        self.idx = len(self.tokens)
        return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid syntax at line {str(self.current_token.line + 1)}')

