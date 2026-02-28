# ====== PARSER FOR ASSIGNMENT 2 ======

from lexer_file_name import do_lexer

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
    pass



# MAIN

if __name__ == "__main__":
    filename = input("Enter source filename: ")

    tokens = do_lexer(filename)
    current = 0

    Rat26S()

    if current_token().type == "EOF":
        print("Syntax Valid")