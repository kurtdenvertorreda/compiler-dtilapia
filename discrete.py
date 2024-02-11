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
        return dtilParser.ResParse(self.current_token.line, store, " ")
    else:
        self.idx = len(self.tokens)
        return dtilParser.ResParse(self.current_token.line, store, f'Syntax Error: Expected discrete reserve word at line {str(self.current_token.line + 1)}')


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
                            return dtilParser.ResParse(self.current_token.line, store," ")
                        else:
                            self.idx = len(self.tokens)
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "Integer" or "Identifier" at line {str(self.current_token.line + 1)}')
                    else:
                        return dtilParser.ResParse(self.current_token.line, store," ")
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "Integer" or "Identifier" at line {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a "given" keyword at line {str(self.current_token.line + 1)}')
        elif self.current_token.value in ["inorder", "preorder","postorder"]:
            if self.current_token.value == "given":
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.type == constants.TT_IDENTIFIER:
                    store += str(self.current_token.value)
                    return dtilParser.ResParse(self.current_token.line, store," ")
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected an "Identifier" at line {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a "given" keyword at line {str(self.current_token.line + 1)}')
        elif self.current_token.value == "R_notation":
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.value == "given":
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.type == constants.TT_DBLQ:
                    store += '\"'
                    self.advance()
                    if self.current_token.type == constants.TT_STRING:
                        store += str(self.current_token.value)
                        self.advance()
                        if self.current_token.type == constants.TT_DBLQ:
                            store += '\"'
                            return dtilParser.ResParse(str(self.current_token.line), store," ")
                        else:
                            self.idx = len(self.tokens)
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a \" {str(self.current_token.line + 1)}')
                    else:
                        self.idx = len(self.tokens)
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a string value at line {str(self.current_token.line + 1)}')
                elif self.current_token.type == constants.TT_IDENTIFIER:
                    store += str(self.current_token.value)
                    return dtilParser.ResParse(str(self.current_token.line)," ")
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a \" {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a "given" keyword at line {str(self.current_token.line + 1)}')
        elif self.current_token.value in ["isPrime", "isOdd", "isEven","isPrimeF"]:
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.value == "given":
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.type in [constants.TT_INT, constants.TT_IDENTIFIER]:
                    store += str(self.current_token.value)
                    self.advance()
                    return dtilParser.ResParse(self.current_token.line, store, " ")
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected an "Integer Value" or "Identifier" at line {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a "given" keyword at line {str(self.current_token.line + 1)}')
        elif self.current_token.value in ["ugraph", "dgraph","union","intersection","symmetric","difference","isSubset","isSuperset","isDisjoint"]:
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.value == "given":
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.value == "{":
                    store += str(self.current_token.value)
                    self.advance()
                    while(True):
                        if self.current_token.type == constants.TT_INT or self.current_token.type == constants.TT_IDENTIFIER:
                            store += str(self.current_token.value)
                            self.advance()
                            if self.current_token.type == constants.TT_COMMA:
                                store += str(self.current_token.value)
                                self.advance()
                            elif self.current_token.value == "}":
                                store += str(self.current_token.value)
                                self.advance()
                                if self.current_token.type == constants.TT_COMMA:
                                    store += str(self.current_token.value)
                                    self.advance()
                                    if self.current_token.value == "{":
                                        store += str(self.current_token.value)
                                        self.advance()
                                        while(True):
                                            if self.current_token.type == constants.TT_INT or self.current_token.type == constants.TT_IDENTIFIER:
                                                store += str(self.current_token.value)
                                                self.advance()
                                                if self.current_token.type == constants.TT_COMMA:
                                                    store += str(self.current_token.value)
                                                    self.advance()
                                                elif self.current_token.value == "}":
                                                    store += str(self.current_token.value)
                                                    self.advance()
                                                    return dtilParser.ResParse(self.current_token.line, store," ")
                                                else:
                                                    self.idx = len(self.tokens)
                                                    return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a "," or an "End Curly Brace" keyword at line {str(self.current_token.line + 1)}')
                                            elif self.current_token.value == "}":
                                                store += str(self.current_token.value)
                                                self.advance()
                                                return dtilParser.ResParse(self.current_token.line, store," ")
                                            else:
                                                self.idx = len(self.tokens)
                                                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected set of values or "End Curly Brace" keyword at line {str(self.current_token.line + 1)}')
                                    elif self.current_token.type == constants.TT_IDENTIFIER:
                                        store += str(self.current_token.value)
                                        self.advance()
                                        return dtilParser.ResParse(self.current_token.line, store," ")
                                else:
                                    self.idx = len(self.tokens)
                                    return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a comma  at line {str(self.current_token.line + 1)}')
                            else:
                                self.idx = len(self.tokens)
                                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a "," or an "End Curly Brace" keyword at line {str(self.current_token.line + 1)}')
                        elif self.current_token.value == "}":
                            store += str(self.current_token.value)
                            self.advance()
                            if self.current_token.type == constants.TT_COMMA:
                                store += str(self.current_token.value)
                                self.advance()
                                if self.current_token.value == "{":
                                    store += str(self.current_token.value)
                                    self.advance()
                                    while(True):
                                        if self.current_token.type == constants.TT_INT or self.current_token.type == constants.TT_IDENTIFIER:
                                            store += str(self.current_token.value)
                                            self.advance()
                                            if self.current_token.type == constants.TT_COMMA:
                                                store += str(self.current_token.value)
                                                self.advance()
                                            elif self.current_token.value == "}":
                                                store += str(self.current_token.value)
                                                self.advance()
                                                return dtilParser.ResParse(self.current_token.line, store," ")
                                            else:
                                                self.idx = len(self.tokens)
                                                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a "," or an "End Curly Brace" keyword at line {str(self.current_token.line + 1)}')
                                        elif self.current_token.value == "}":
                                            store += str(self.current_token.value)
                                            self.advance()
                                            return dtilParser.ResParse(self.current_token.line, store," ")
                                        else:
                                            self.idx = len(self.tokens)
                                            return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected set of values or "End Curly Brace" keyword at line {str(self.current_token.line + 1)}')
                                elif self.current_token.type == constants.TT_IDENTIFIER:
                                    store += str(self.current_token.value)
                                    self.advance()
                                    return dtilParser.ResParse(self.current_token.line, store," ")
                            else:
                                self.idx = len(self.tokens)
                                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a comma  at line {str(self.current_token.line + 1)}')
                        else:
                            self.idx = len(self.tokens)
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected set of values or "End Curly Brace" keyword at line {str(self.current_token.line + 1)}')
                elif self.current_token.type == constants.TT_IDENTIFIER:
                    store += str(self.current_token.value)
                    self.advance()
                    if self.current_token.type == constants.TT_COMMA:
                        store += str(self.current_token.value)
                        self.advance()
                        if self.current_token.value == "{":
                            store += str(self.current_token.value)
                            self.advance()
                            while(True):
                                if self.current_token.type == constants.TT_INT or self.current_token.type == constants.TT_IDENTIFIER:
                                    store += str(self.current_token.value)
                                    self.advance()
                                    if self.current_token.type == constants.TT_COMMA:
                                        store += str(self.current_token.value)
                                        self.advance()
                                    elif self.current_token.value == "}":
                                        store += str(self.current_token.value)
                                        self.advance()
                                        return dtilParser.ResParse(self.current_token.line, store," ")
                                    else:
                                        self.idx = len(self.tokens)
                                        return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a "," or an "End Curly Brace" keyword at line {str(self.current_token.line + 1)}')
                                elif self.current_token.value == "}":
                                    store += str(self.current_token.value)
                                    self.advance()
                                    return dtilParser.ResParse(self.current_token.line, store," ")
                                else:
                                    self.idx = len(self.tokens)
                                    return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected set of values or "End Curly Brace" keyword at line {str(self.current_token.line + 1)}')
                        elif self.current_token.type == constants.TT_IDENTIFIER:
                            store += str(self.current_token.value)
                            self.advance()
                            return dtilParser.ResParse(self.current_token.line, store," ")
                    else:
                        self.idx = len(self.tokens)
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a comma  at line {str(self.current_token.line + 1)}')
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a Set values  at line {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "given" keyword at line {str(self.current_token.line + 1)}')
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
                                    return dtilParser.ResParse(self.current_token.line, store," ")
                                else:
                                    self.idx = len(self.tokens)
                                    return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected an "Integer Value" or "Identifier" at line {str(self.current_token.line + 1)}')
                            else:
                                return dtilParser.ResParse(self.current_token.line, store," ")
                        else:
                            self.idx = len(self.tokens)
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected an "Integer Value" or "Identifier" at line {str(self.current_token.line + 1)}')
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Invalid token at line {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "given" keyword at line {str(self.current_token.line + 1)}')
        elif self.current_token.value in ["bfs","dfs","kruskal","dijkstra"]:
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.value == "given":
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.type == constants.TT_IDENTIFIER:
                    store += str(self.current_token.value)
                    self.advance()
                    if self.current_token.type == constants.TT_COMMA:
                        store += str(self.current_token.value) + " "
                        self.advance()
                        if self.current_token.type == constants.TT_INT:
                            store += str(self.current_token.value)
                            self.advance()
                            if self.current_token.type == constants.TT_COMMA:
                                store += str(self.current_token.value) + " "
                                self.advance()
                                if self.current_token.type == constants.TT_INT:
                                    store += str(self.current_token.value)
                                    self.advance()
                                    return dtilParser.ResParse(self.current_token.line, store," ")
                                else:
                                    self.idx = len(self.tokens)
                                    return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected an "Integer" at line {str(self.current_token.line + 1)}')
                            else:
                                self.idx = len(self.tokens)
                                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a "Comma" at line {str(self.current_token.line + 1)}')
                        else:
                            self.idx = len(self.tokens)
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected an "Integer" at line {str(self.current_token.line + 1)}')
                    else:
                        self.idx = len(self.tokens)
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a "Comma" at line {str(self.current_token.line + 1)}')
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected an "Identifier" at line {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "given" keyword at line {str(self.current_token.line + 1)}')
        elif self.current_token.value in ["isEmpty","btree","series","countSet","S_notation"]:
            store += str(self.current_token.value) + " "
            self.advance()
            if self.current_token.value == "given":
                store += str(self.current_token.value) + " "
                self.advance()
                if self.current_token.value == "{":
                    store += str(self.current_token.value)
                    self.advance()
                    while(True):
                        if self.current_token.type == constants.TT_INT or self.current_token.type == constants.TT_IDENTIFIER:
                            store += str(self.current_token.value)
                            self.advance()
                            if self.current_token.type == constants.TT_COMMA:
                                store += str(self.current_token.value)
                                self.advance()
                            elif self.current_token.value == "}":
                                store += str(self.current_token.value)
                                self.advance()
                                return dtilParser.ResParse(self.current_token.line, store," ")
                            else:
                                self.idx = len(self.tokens)
                                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a "," or an "End Curly Brace" keyword at line {str(self.current_token.line + 1)}')
                        elif self.current_token.value == "}":
                            store += str(self.current_token.value)
                            self.advance()
                            return dtilParser.ResParse(self.current_token.line, store," ")
                        else:
                            self.idx = len(self.tokens)
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected set of values or "End Curly Brace" keyword at line {str(self.current_token.line + 1)}')
                elif self.current_token.type == constants.TT_IDENTIFIER:
                    store += str(self.current_token.value)
                    self.advance()
                    return dtilParser.ResParse(self.current_token.line, store," ")
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected a Set values  at line {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "given" keyword at line {str(self.current_token.line + 1)}')
        elif self.current_token.type == constants.TT_IDENTIFIER:
            if self.current_token.type == constants.TT_PERIOD:
                store += str(self.current_token.value)
                self.advance()
                if self.current_token.value in ["add","remove","search","nodeAdd","removeNode","removeEdge","UedgeAdd","DedgeAdd"]:
                    store += str(self.current_token.value)
                    self.advance()
                    if self.current_token.value in ["add","remove","search","nodeAdd","removeNode","removeEdge","UedgeAdd","DedgeAdd"]:
                        store += str(self.current_token.value)
                        self.advance()
                        if self.current_token.value == "given":
                            store += str(self.current_token.value)
                            self.advance()
                            if self.current_token.type in [constants.TT_IDENTIFIER, constants.TT_INT]:
                                store += str(self.current_token.value)
                                self.advance()
                                return dtilParser.ResParse(self.current_token.line, store," ")
                            else:
                                self.idx = len(self.tokens)
                                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "Integer Value" or "Identifier" at line {str(self.current_token.line + 1)}')
                        else:
                            self.idx = len(self.tokens)
                            return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected "given" keyword at line {str(self.current_token.line + 1)}')
                    else:
                        self.idx = len(self.tokens)
                        return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected operation at line {str(self.current_token.line + 1)}')
                else:
                    self.idx = len(self.tokens)
                    return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected operation at line {str(self.current_token.line + 1)}')
            else:
                self.idx = len(self.tokens)
                return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected period operation at line {str(self.current_token.line + 1)}')
        else:
            self.idx = len(self.tokens)
            return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected discrete operation at line {str(self.current_token.line + 1)}')
    else:
        self.idx = len(self.tokens)
        return dtilParser.ResParse(str(self.current_token.line), store, f'Syntax Error: Expected discrete operation at line {str(self.current_token.line + 1)}')
