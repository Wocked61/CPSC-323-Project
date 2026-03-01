# ====== PARSER FOR ASSIGNMENT 2 (Reorganized by Rule #) ======

from assignment1 import do_lexer

tokens = []
current = 0



# Helper functions
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


# R1. <Rat26S>
def Rat26S():
    match(expected_lexeme='@')
    OptFunctionDefinitions()
    match(expected_lexeme='@')
    OptDeclarationList()
    match(expected_lexeme='@')
    StatementList()
    match(expected_lexeme='@')



# R2. <Opt Function Definitions>
def OptFunctionDefinitions():
    if current_token().lexeme == "function":
        FunctionDefinitions()
    # else empty



# R3. <Function Definitions>

def FunctionDefinitions():
    Function()
    while current_token().lexeme == "function":
        Function()



# R4. <Function>
# function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>

def Function():
    match(expected_lexeme="function")
    match(expected_type="identifier")
    match(expected_lexeme="(")
    OptParameterList()
    match(expected_lexeme=")")
    OptDeclarationList()
    Body()



# R5. <Opt Parameter List>
def OptParameterList():
    if current_token().type == "identifier":
        ParameterList()
    # else empty


# R6. <Parameter List>
def ParameterList():
    Parameter()
    while current_token().lexeme == ",":
        match(expected_lexeme=",")
        Parameter()


# R7. <Parameter>
# <IDs> <Qualifier>
def Parameter():
    IDs()
    Qualifier()


# R8. <Qualifier>
# integer | boolean | real
def Qualifier():
    if current_token().lexeme in ["integer", "boolean", "real"]:
        advance()
    else:
        error("Expected type qualifier (integer/boolean/real)")


# R9. <Body>
# { <Statement List> }
def Body():
    match(expected_lexeme="{")
    StatementList()
    match(expected_lexeme="}")


# R10. <Opt Declaration List>
def OptDeclarationList():
    if current_token().lexeme in ["integer", "boolean", "real"]:
        DeclarationList()
    # else empty


# R11. <Declaration List>
# <Declaration> ; { <Declaration> ; }
def DeclarationList():
    Declaration()
    match(expected_lexeme=";")
    while current_token().lexeme in ["integer", "boolean", "real"]:
        Declaration()
        match(expected_lexeme=";")


# R12. <Declaration>
# <Qualifier> <IDs>
def Declaration():
    Qualifier()
    IDs()


# R13. <IDs>
# <Identifier> | <Identifier> , <IDs>
def IDs():
    match(expected_type="identifier")
    while current_token().lexeme == ",":
        match(expected_lexeme=",")
        match(expected_type="identifier")


# R14. <Statement List>
# <Statement> | <Statement> <Statement List>
def StatementList():
    Statement()
    while current_token().lexeme not in ['}', '@', 'fi', 'otherwise']:
        Statement()


# R15. <Statement>
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


# R16. <Compound>
# { <Statement List> }
def Compound():
    match(expected_lexeme="{")
    StatementList()
    match(expected_lexeme="}")


# R17. <Assign>
# <Identifier> = <Expression> ;
def Assign():
    match(expected_type="identifier")
    match(expected_lexeme="=")
    Expression()
    match(expected_lexeme=";")


# R18. <If>
# if ( <Condition> ) <Statement> fi
# if ( <Condition> ) <Statement> otherwise <Statement> fi
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


# R19. <Return>
# return ; | return <Expression> ;
def Return():
    match(expected_lexeme="return")
    if current_token().lexeme != ";":
        Expression()
    match(expected_lexeme=";")


# R20. <Print>
# write ( <Expression> ) ;
def Print():
    match(expected_lexeme="write")
    match(expected_lexeme="(")
    Expression()
    match(expected_lexeme=")")
    match(expected_lexeme=";")


# R21. <Scan>
# read ( <IDs> ) ;
def Scan():
    match(expected_lexeme="read")
    match(expected_lexeme="(")
    IDs()
    match(expected_lexeme=")")
    match(expected_lexeme=";")


# R22. <While>
# while ( <Condition> ) <Statement>
def While():
    match(expected_lexeme="while")
    match(expected_lexeme="(")
    Condition()
    match(expected_lexeme=")")
    Statement()


# R23. <Condition>
# <Expression> <Relop> <Expression>
def Condition():
    Expression()
    Relop()
    Expression()


# R24. <Relop>
# == | != | > | < | <= | =>
def Relop():
    if current_token().lexeme in ["==", "!=", ">", "<", "<=", "=>"]:
        advance()
    else:
        error("Invalid relational operator")


# R25. <Expression>
def Expression():
    Term()
    while current_token().lexeme in ['+', '-']:
        advance()
        Term()


# R26. <Term>
def Term():
    Factor()
    while current_token().lexeme in ['*', '/']:
        advance()
        Factor()


# R27. <Factor>
def Factor():
    if current_token().lexeme == '-':
        advance()
        Primary()
    else:
        Primary()


# R28. <Primary>
# Identifier | Integer | Real | ( <Expression> ) | true | false | Identifier ( <IDs> )
def Primary():
    token = current_token()

    if token.type == "identifier":
        advance()
        if current_token().lexeme == "(":
            match(expected_lexeme="(")
            IDs()
            match(expected_lexeme=")")
        return

    if token.type == "integer":
        advance()
        return

    if token.type == "real":
        advance()
        return

    if token.lexeme == "(":
        advance()
        Expression()
        match(expected_lexeme=")")
        return

    if token.lexeme in ["true", "false"]:
        advance()
        return

    error("Invalid primary")


# MAIN
if __name__ == "__main__":
    filename = input("Enter source filename: ")

    tokens = do_lexer(filename)
    current = 0

    Rat26S()

    if current_token().type == "EOF":
        print("Syntax Valid")