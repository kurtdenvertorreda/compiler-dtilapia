vowels_lower = "aeiou"
vowels_upper = vowels_lower.upper()

consonants_lower = "bdfghjklmnptwxyz"
consonants_upper = consonants_lower.upper()

consonants_for_diagraph = "ntsl"
consonants_for_diagraph_upper = consonants_for_diagraph.upper()

second_consonants_for_diagraph_lower = "gshl"
second_consonants_for_diagraph_upper = second_consonants_for_diagraph_lower.upper()



class LatinToBaybayinConverter:
    def __init__(self):
        self.state = "start"
        self.result = ""
        self.diagraph = False

    def process_input(self, input_str):
        for char in input_str:
            stop = False
            stop = self.transition(char)
            if stop == True:
                break
        return self.result

    # Transition
    def transition(self, char):
        if self.state == "start":
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "vowel"
                self.result = self.result + char
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                if char.lower() in consonants_for_diagraph or char.upper() in consonants_for_diagraph_upper:
                    self.diagraph = True
                    self.state = "consonant"
                    self.result = self.result + char
                else:
                    self.state = "consonant"
                    self.result = self.result + char
            else:
                self.result = "Invalid input"
                return True
            
        elif self.state == "consonant":
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "syllable"
                self.result = self.result + char
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                if char.lower() in second_consonants_for_diagraph_lower or char.upper() in second_consonants_for_diagraph_upper and self.diagraph == True:
                    self.state = "digraph"
                    self.result = self.result + char
                else:
                    self.state = "dead"
                    self.result = "Input not available in Baybayin"
            else:
                self.result = "Invalid input"
                return True
            
        elif self.state == "vowel":
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "vowel"
                self.result = self.result + char
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                if char.lower() in consonants_for_diagraph or char.upper() in consonants_for_diagraph_upper:
                    self.state = "consonant"
                    self.result = self.result + char
                    self.diagraph = True
                else:
                    self.state = "consonant"
                    self.result = self.result + char
            else:
                self.result = "Invalid input"

        elif self.state == "syllable":
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "vowel"
                self.result = self.result + char
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                if char.lower() in consonants_for_diagraph or char.upper() in consonants_for_diagraph_upper:
                    self.state = "consonant"
                    self.result = self.result + char
                    self.diagraph = True
                else:
                    self.state = "consonant"
                    self.result = self.result + char
            else:
                self.result = "Invalid input"
                return True
            
        elif self.state == "digraph":
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "syllable"
                self.result = self.result + char
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                self.state = "dead"
                self.result = "Input not available in Baybayin"
            else:
                self.result = "Invalid input"
                return True
            
        elif self.state == "dead":
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "dead"
                self.result = "Input not available in Baybayin"
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                self.state = "dead"
                self.result = "Input not available in Baybayin"
            else:
                self.result = "Incomplete input"
                return True


if __name__ == "__main__":
    while True:
        converter = LatinToBaybayinConverter()
        input_str = input("Enter a Latin string (type 'exit' to quit): ")

        # Check if the user wants to exit
        if input_str.lower() == "exit":
            break

        converter.process_input(input_str)

        # Checks if final letter is a consonant
        if converter.state == "consonant":
            converter.result = "Incomplete output"

        print("Baybayin output:", converter.result)