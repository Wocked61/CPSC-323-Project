# ====== PARSER FOR ASSIGNMENT 2 ======

from assignment1 import do_lexer

tokens = []
current = 0


def current_token():
    return tokens[current]


def advance():
    global current
    current += 1


def error(msg):
    print("Syntax Error:", msg)
    exit()


def match(expected_lexeme=None, expected_type=None):
    token = current_token()

    if expected_lexeme and token.lexeme != expected_lexeme:
        error(f"Expected '{expected_lexeme}' but found '{token.lexeme}'")

    if expected_type and token.type != expected_type:
        error(f"Expected {expected_type} but found {token.type}")

    advance()



# Grammar Rule Functions


# R1
def Rat26S():
    match(expected_lexeme='@')
    OptFunctionDefinitions()
    match(expected_lexeme='@')
    OptDeclarationList()
    match(expected_lexeme='@')
    StatementList()
    match(expected_lexeme='@')


# R2
def OptFunctionDefinitions():
    if current_token().lexeme == "function":
        FunctionDefinitions()


def FunctionDefinitions():
    Function()
    while current_token().lexeme == "function":
        Function()


# placeholder (expand later)
def Function():
    match(expected_lexeme="function")
    match(expected_type="identifier")
    match(expected_lexeme="(")
    match(expected_lexeme=")")
    Body()


def Body():
    match(expected_lexeme="{")
    StatementList()
    match(expected_lexeme="}")


# placeholder
def OptDeclarationList():
    pass


# placeholder
def StatementList():
    # if next token is an end-of-list token, treat as empty list
    if current_token().lexeme in ['}', '@', 'fi', 'otherwise']:
        return
    Statement()
    while current_token().lexeme not in ['}', '@', 'fi', 'otherwise']:
        Statement()


def Statement():
    token = current_token()

    if token.lexeme == "{":
        Compound()
    elif token.type == "identifier":
        Assign()
    elif token.lexeme == "if":
        If()
    elif token.lexeme == "return":
        Return()
    elif token.lexeme == "write":
        Print()
    elif token.lexeme == "read":
        Scan()
    elif token.lexeme == "while":
        While()
    else:
        error("Invalid statement")


def Assign():
    match(expected_type="identifier")
    match(expected_lexeme="=")
    Expression()
    match(expected_lexeme=";")

def Expression():
    Term()
    while current_token().lexeme in ['+', '-']:
        advance()
        Term()

def Term():
    Factor()
    while current_token().lexeme in ['*', '/']:
        advance()
        Factor()

def Factor():
    if current_token().lexeme == '-':
        advance()
        Primary()
    else:
        Primary()

def Primary():
    token = current_token()

    if token.type == "identifier":
        advance()
    elif token.type == "integer":
        advance()
    elif token.type == "real":
        advance()
    elif token.lexeme == "(":
        advance()
        Expression()
        match(expected_lexeme=")")
    elif token.lexeme in ["true", "false"]:
        advance()
    else:
        error("Invalid primary")


    def Compound():
    match(expected_lexeme="{")
    StatementList()
    match(expected_lexeme="}")

    def Return():
    match(expected_lexeme="return")
    if current_token().lexeme != ";":
        Expression()
    match(expected_lexeme=";")

    def Print():
    match(expected_lexeme="write")
    match(expected_lexeme="(")
    Expression()
    match(expected_lexeme=")")
    match(expected_lexeme=";")


    def IDs():
    match(expected_type="identifier")
    while current_token().lexeme == ",":
        match(expected_lexeme=",")
        match(expected_type="identifier")


        def Scan():
    match(expected_lexeme="read")
    match(expected_lexeme="(")
    IDs()
    match(expected_lexeme=")")
    match(expected_lexeme=";")


    def Relop():
    if current_token().lexeme in ["==", "!=", ">", "<", "<=", "=>"]:
        advance()
    else:
        error("Invalid relational operator")


        def Condition():
    Expression()
    Relop()
    Expression()


    def While():
    match(expected_lexeme="while")
    match(expected_lexeme="(")
    Condition()
    match(expected_lexeme=")")
    Statement()



    def If():
    match(expected_lexeme="if")
    match(expected_lexeme="(")
    Condition()
    match(expected_lexeme=")")
    Statement()

    if current_token().lexeme == "otherwise":
        match(expected_lexeme="otherwise")
        Statement()

    match(expected_lexeme="fi")

# MAIN


if __name__ == "__main__":
    filename = input("Enter source filename: ")

    tokens = do_lexer(filename)
    current = 0

    Rat26S()

    if current_token().type == "EOF":
        print("Syntax Valid")