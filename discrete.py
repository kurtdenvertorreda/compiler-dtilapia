import constants
import dtilParser

def parse_discrete(self):
        self.advance()
        store = "find" + " "
        identifier_token = self.current_token
        if identifier_token.type in constants.TT_RESERVE:
            if self.current_token.value in ["permutation", "combination","gcd","lcm","lcd","isDivisible"]:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.value == "given":
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.type in [constants.TT_INT, constants.TT_IDENTIFIER]:
                        store += str(self.current_token.value)
                        self.advance()
                        if self.current_token.value == ",":
                            store += str(self.current_token.value)
                            self.advance()
                            if self.current_token.type in [constants.TT_INT, constants.TT_IDENTIFIER]:
                                store += str(self.current_token.value)
                                return dtilParser.ResParse(self.current_token.line, store, "No Error")
                            else:
                                return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
                        else:
                            return dtilParser.ResParse(self.current_token.line, store, "No Error")
                    else:
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
                else:
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
            elif self.current_token.value in ["inorder", "preorder","postorder"]:
                if self.current_token.value == "given":
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.type == constants.TT_IDENTIFIER:
                        store += str(self.current_token.value)
                        return dtilParser.ResParse(self.current_token.line, store, "No Error")
                    else:
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
                else:
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
            elif self.current_token.value in ["isPrime", "isOdd", "isEven"]:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.value == "given":
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.type in [constants.TT_INT, constants.TT_IDENTIFIER]:
                        store += str(self.current_token.value)
                        self.advance()
                        return dtilParser.ResParse(self.current_token.line, store, "No Error")
                    else:
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
                else:
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
            elif self.current_token.value in ["permutation", "combination","gcd","lcm","lcd","isDivisible"]:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.value == "given":
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.type in [constants.TT_INT, constants.TT_IDENTIFIER]:
                        store += str(self.current_token.value)
                        self.advance()
                        if self.current_token.value == ",":
                            store += str(self.current_token.value)
                            self.advance()
                            if self.current_token.type in [constants.TT_INT,constants.TT_IDENTIFIER]:
                                store += str(self.current_token.value)
                                return dtilParser.ResParse(self.current_token.line, store, "No Error")
                            else:
                                return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
                        else:
                            return dtilParser.ResParse(self.current_token.line, store, "No Error")
                    else:
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
                else:
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
            elif self.current_token.value in ["ariseq", "geomseq","fiboseq"]:
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.value == "given":
                    store += str(self.current_token.value) + " "
                    self.advance()
                    if self.current_token.type in [constants.TT_INT, constants.TT_IDENTIFIER]:
                        store += str(self.current_token.value)
                        self.advance()
                        if self.current_token.value == ",":
                            store += str(self.current_token.value)
                            self.advance()
                            if self.current_token.type in [constants.TT_INT, constants.TT_IDENTIFIER]:
                                store += str(self.current_token.value)
                                self.advance()
                                if self.current_token.value == ",":
                                    store += str(self.current_token.value)
                                    self.advance()
                                    if self.current_token.type in [constants.TT_INT, constants.TT_IDENTIFIER]:
                                        store += str(self.current_token.value)
                                        return dtilParser.ResParse(self.current_token.line, store, "No Error")
                                    else:
                                        return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
                                else:
                                    return dtilParser.ResParse(self.current_token.line, store, "No Error")
                            else:
                                return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
                        else:
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
                    else:
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
                else:
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
            else:
                return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
        else:
            return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
    