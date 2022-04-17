keywords = {
    "program" : "PROG",
    "declare" : "DECL",
    "if"      : "IF",
    "else"    : "ELSE",
    "while"   : "WHILE",
    "switchcase" : "SWITCH",
    "forcase" : "FOR",
    "incase"  : "INCS",
    "case"    : "CASE",
    "default" : "DFLT",
    "not"     : "NOT",
    "and"     : "AND",
    "or"      : "OR",
    "function" : "FUNC",
    "procedure" : "PROC",
    "call"    : "CALL",
    "return"  : "RET",
    "in"      : "IN", 
    "inout"   : "INOUT",
    "input"   : "INPUT",
    "print"   : "PRINT"
}

def checkIfKeyword(string):
    return keywords.get(string)

class Lexer:
        def __init__(self, input):
            self.source = input + '\n' # source is the source code of the program
            self.curChar = '' # curChar is the current char that is pointed by the lexer
            self.curPos  = -1 # curPos is the position of the curChar in the source
            self.nextChar()
            
        def nextChar(self):
            self.curPos += 1
            if self.curPos >= len(self.source):
                self.curChar = '\0'
            else:
                self.curChar = self.source[self.curPos]
                
        def peek(self):
            nextPos = self.curPos + 1
            if  nextPos >= len(self.source):
                return '\0'
            else:
                return self.source[nextPos]
        
        def abort(self, message):
            sys.exit("Lexing error. " + message)
        
        def skipWhitescape(self):
                while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r' or self.curChar == '\n':
                    self.nextChar()
                    
        # We open comments with # and ends with \n
        def skipComment(self):
            if self.curChar == '#':
                while self.curChar != '\n':
                    self.nextChar()
                    
        def getToken(self):
            self.skipWhitescape()
            self.skipComment()
            self.skipWhitescape()
            
            token = ""
            
            if self.curChar == '+': # Plus symbol
                token = ["PLUS", "+"]
            elif  self.curChar == '-': # Rest symbol
                token = ["MINUS", "-"]
            elif self.curChar == '*': # Multiplication symbol
                token = ["MULT", "*"]
            elif self.curChar == '/': # Division symbol
                token = ["DIV", "/"]
            elif self.curChar == '=': # Comparing eq
                token = ["EQ", "="]
            elif self.curChar == ',': # Comma char
                token = ["COM", ","]
            elif self.curChar == '.': # End of program
                token = ["EOP", "."]
            elif self.curChar == ';': # Semicolon char
                token = ["SMCOL", ";"]
            elif self.curChar == '(': # Open parenthesis
                token = ["OPAR", "("]
            elif self.curChar == ')': # Close parenthesis
                token = ["CPAR", ")"]
            elif self.curChar == '[': # Open square bracket
                token = ["OBRA", "["]
            elif self.curChar == ']': # Close square bracket
                token = ["CBRA", "]"]
            elif self.curChar == '{': # Open curly bracket
                token = ["OCB", "{"]
            elif self.curChar == '}': # Close curly bracket
                token = ["CCB", "}"]
                
            elif self.curChar == ':': # symbols starting in :
                lkahead = self.peek()
                if lkahead == '=':
                    self.nextChar()
                    token = ["ASIG", ":="]
                else:
                    token = ["COLON", ":"]
            elif self.curChar == '<': # symbols starting in <
                lkahead = self.peek()
                if lkahead == '=':
                    self.nextChar()
                    token = ["LTEQ", "<="]
                elif lkahead == '>':
                    self.nextChar()
                    token = ["NOTEQ", "<>"]
                else:
                    token = ["LT", "<"]
            elif self.curChar == '>': # symbols starting in >
                lkahead = self.peek()
                if lkahead == '=':
                    self.nextChar()
                    token = ["GTEQ", ">="]
                else:
                    token = ["GT", ">"]
                    
            elif self.curChar.isdigit(): # Reading integer number
                integer = ""
                integer += self.curChar
                while self.peek().isdigit():
                    self.nextChar()
                    integer += self.curChar
                    
                token = ["NUMB", integer]
            elif self.curChar.isalpha(): # Reading alphanumeric string
                identifier = ""
                identifier += self.curChar
                while self.peek().isalnum():
                    self.nextChar()
                    identifier += self.curChar
                    
                keyword = checkIfKeyword(identifier)
                if (keyword == None):
                    token = ["ID", identifier]
                else:
                    token = [keyword, identifier]
            
            # elif self.curChar == '\n':
            #     token = ["NEWLN", "\n"]
            elif self.curChar == '\0':
                token = ["EOF", "\0"]
            else:
                self.abort("Uknown token " + self.curChar)
                
            self.nextChar()
            return token
            
            
            
            