import constants
import dtilParser
RESERVED_WORDS = {'True', 'False', 'permutation', 'combination', 'btree', 'preorder', 'inorder', 'postorder',
                 'null', 'search', 'add', 'remove', 'ugraph', 'dgraph', 'nodeAdd', 'removeEdge', 'UedgeAdd', 'DedgeAdd',
                 'bfs', 'dfs', 'dijkstra', 'kruskal', 'inverse', 'converse', 'contrapos', 'probability', 'cProbability',
                 'isPrime', 'isOdd', 'isEven', 'gcd', 'lcm', 'lcd', 'isDivisible', 'isPrimeF', 'ariseq', 'geomseq', 'fiboseq',
                 'series', 'union', 'intersection', 'difference', 'countSet', 'isSubset', 'isEqual', 'isSuperset', 'isDisjoint',
                 'isEmpty', 'R_notation', 'S_notation'}
def parse_hence(self):
    self.advance()
    store = "hence" + " "
    identifier_token = self.current_token
    if identifier_token.type in constants.TT_RESERVE and identifier_token.value not in ["True", "False","null","search","add","remove","nodeAdd","removeEdge","UedgeAdd","DedgeAdd"]:
        store += str(self.current_token.value) + " "
        return dtilParser.ResParse(self.current_token.line, store, f'Line {str(self.current_token.line + 1)} executed successfuly')
    else:
        return dtilParser.ResParse(self.current_token.line, store, "Syntax Error: Expected discrete reserve word")


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
                            return dtilParser.ResParse(self.current_token.line, store,f'Line {str(self.current_token.line + 1)} executed successfuly')
                        else:
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
                    else:
                        return dtilParser.ResParse(self.current_token.line, store,f'Line {str(self.current_token.line + 1)} executed successfuly')
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
                    return dtilParser.ResParse(self.current_token.line, store,f'Line {str(self.current_token.line + 1)} executed successfuly')
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
                    return dtilParser.ResParse(self.current_token.line, store,f'Line {str(self.current_token.line + 1)} executed successfuly')
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
                                    return dtilParser.ResParse(self.current_token.line, store,f'Line {str(self.current_token.line + 1)} executed successfuly')
                                else:
                                    return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
                            else:
                                return dtilParser.ResParse(self.current_token.line, store,f'Line {str(self.current_token.line + 1)} executed successfuly')
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
