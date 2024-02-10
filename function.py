import constants as const
import dtilParser

def parse_funct(self):
    self.advance()
    store = "funct" + " "

    if self.current_token.value in const.KEYWORDS_DATA_TYPE:
        store += str(self.current_token.value) + " "
        self.advance()

        identifier_token = self.current_token
        if identifier_token.type == const.TT_IDENTIFIER:
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.type == const.TT_KEYWORD and str(self.current_token.value) == "given":
                store += str(self.current_token.value) + " "
                self.advance()

                if self.current_token.type == const.TT_IDENTIFIER:
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.type == const.TT_KEYWORD and str(self.current_token.value) == "is":
                        store += str(self.current_token.value) + " "
                        self.advance()
                        if self.current_token.value in const.KEYWORDS_DATA_TYPE:
                            store += str(self.current_token.value) + " "
                            self.advance()
                            if self.current_token.type == const.TT_KEYWORD and str(self.current_token.value) == "do":
                                store += str(self.current_token.value) + " "
                                self.advance()
                                if self.current_token.type == const.TT_COLON:
                                    store += str(self.current_token.value) + " "
                                    self.advance()
                                    # if self.current_token.value == "\n":
                                    #     self.advance()
                                    #     if self.current_char == "\t":
                                    #         self.advance()
                                    #         # Call parse_body function
                                    #         return dtilParser.parse_body(self)
                                else:
                                    return dtilParser.ResParse(str(self.current_token.line), store, f'Expected a ":" after "do" keyword at line {str(self.current_token.line+1)}')
                            else:
                                return dtilParser.ResParse(str(self.current_token.line), store, f'Expected a "do" keyword after data type at line {str(self.current_token.line+1)}')
                        else:
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Expected a data type after "is" keyword at line {str(self.current_token.line+1)}')
                    else:
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Expected "is" keyword after parameters at line {str(self.current_token.line+1)}')
                else:
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Expected parameters after "given" keyword at line {str(self.current_token.line+1)}')
            else:
                return dtilParser.ResParse(str(self.current_token.line), store, f'Expected "given" keyword after identifier at line {str(self.current_token.line+1)}')
        else:
            return dtilParser.ResParse(str(self.current_token.line), store, f'Expected an identifier after return type at line {str(self.current_token.line+1)}')
    else:
        return dtilParser.ResParse(str(self.current_token.line), store, f'Expected a return type after "funct" keyword at line {str(self.current_token.line+1)}')
    return dtilParser.ResParse(self.current_token.line, store, " ")