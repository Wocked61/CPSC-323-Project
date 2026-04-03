# ====== PARSER FOR ASSIGNMENT 2  ======

from assignment1 import do_lexer
output_file = None
PRINT_PRODUCTIONS = True
tokens = []
current = 0

def write_output(text):
    global output_file
    print(text)
    if output_file:
        output_file.write(text + "\n")

# Helper functions
def current_token():
    return tokens[current]


def advance():
    global current
    current += 1


def error(msg):
    token = current_token()
    write_output(f"Syntax Error: {msg}. Found '{token.lexeme}' of type '{token.type}'")
    exit()


def match(expected_lexeme=None, expected_type=None):
    token = current_token()

    if expected_lexeme and token.lexeme != expected_lexeme:
        error(f"Expected '{expected_lexeme}' but found '{token.lexeme}'")

    if expected_type and token.type != expected_type:
        error(f"Expected {expected_type} but found {token.type}")

    write_output(f"Token: {token.type}    Lexeme: {token.lexeme}")
    advance()


# R1. <Rat26S>
def Rat26S():
    if PRINT_PRODUCTIONS:
        write_output("<Rat26S> -> @ <Opt Function Definitions> @ <Opt Declaration List> @ <Statement List> @")
    match(expected_lexeme='@')
    OptFunctionDefinitions()
    match(expected_lexeme='@')
    OptDeclarationList()
    match(expected_lexeme='@')
    StatementList()
    match(expected_lexeme='@')



# R2. <Opt Function Definitions>
def OptFunctionDefinitions():
    if PRINT_PRODUCTIONS:
        write_output("<Opt Function Definitions> -> <Function Definitions> | ε")
    if current_token().lexeme == "function":
        FunctionDefinitions()
    # else empty



# R3. <Function Definitions>

def FunctionDefinitions():
    if PRINT_PRODUCTIONS:
        write_output("<Function Definitions> -> <Function> | <Function> <Function Definitions>")
    Function()
    while current_token().lexeme == "function":
        Function()



# R4. <Function>
# function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>

def Function():
    if PRINT_PRODUCTIONS:
        write_output("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
    match(expected_lexeme="function")
    match(expected_type="identifier")
    match(expected_lexeme="(")
    OptParameterList()
    match(expected_lexeme=")")
    OptDeclarationList()
    Body()



# R5. <Opt Parameter List>
def OptParameterList():
    if PRINT_PRODUCTIONS:
        write_output("<Opt Parameter List> -> <Parameter List> | ε")

    if current_token().type == "identifier":
        ParameterList()
    # else empty


# R6. <Parameter List>
def ParameterList():
    if PRINT_PRODUCTIONS:
        write_output("<Parameter List> -> <Parameter> | <Parameter> , <Parameter List>")

    Parameter()
    while current_token().lexeme == ",":
        match(expected_lexeme=",")
        Parameter()


# R7. <Parameter>
# <IDs> <Qualifier>
def Parameter():
    if PRINT_PRODUCTIONS:
        write_output("<Parameter> -> <IDs> <Qualifier>")

    IDs()
    Qualifier()


# R8. <Qualifier>
# integer | boolean | real
def Qualifier():
    if PRINT_PRODUCTIONS:
        write_output("<Qualifier> -> integer | boolean | real")

    if current_token().lexeme in ["integer", "boolean", "real"]:
        match(expected_type="keyword")
    else:
        error("Expected type qualifier (integer/boolean/real)")


# R9. <Body>
# { <Statement List> }
def Body():
    if PRINT_PRODUCTIONS:
        write_output("<Body> -> { <Statement List> }")

    match(expected_lexeme="{")
    StatementList()
    match(expected_lexeme="}")


# R10. <Opt Declaration List>
def OptDeclarationList():
    if PRINT_PRODUCTIONS:
        write_output("<Opt Declaration List> -> <Declaration List> | ε")

    if current_token().lexeme in ["integer", "boolean", "real"]:
        DeclarationList()
    # else empty


# R11. <Declaration List>
# <Declaration> ; { <Declaration> ; }
def DeclarationList():
    if PRINT_PRODUCTIONS:
        write_output("<Declaration List> -> <Declaration> ; { <Declaration> ; }")

    Declaration()
    match(expected_lexeme=";")
    while current_token().lexeme in ["integer", "boolean", "real"]:
        Declaration()
        match(expected_lexeme=";")


# R12. <Declaration>
# <Qualifier> <IDs>
def Declaration():
    if PRINT_PRODUCTIONS:
        write_output("<Declaration> -> <Qualifier> <IDs>")

    Qualifier()
    IDs()


# R13. <IDs>
# <Identifier> | <Identifier> , <IDs>
def IDs():
    if PRINT_PRODUCTIONS:
        write_output("<IDs> -> <Identifier> | <Identifier> , <IDs>")

    match(expected_type="identifier")
    while current_token().lexeme == ",":
        match(expected_lexeme=",")
        match(expected_type="identifier")


# R14. <Statement List>
# <Statement> | <Statement> <Statement List>
def StatementList():
    if PRINT_PRODUCTIONS:
        write_output("<Statement List> -> <Statement> | <Statement> <Statement List>")

    Statement()
    while current_token().lexeme not in ['}', '@', 'fi', 'otherwise']:
        Statement()


# R15. <Statement>
def Statement():
    if PRINT_PRODUCTIONS:
        write_output("<Statement> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")


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
    if PRINT_PRODUCTIONS:
        write_output("<Compound> -> { <Statement List> }")

    match(expected_lexeme="{")
    StatementList()
    match(expected_lexeme="}")


# R17. <Assign>
# <Identifier> = <Expression> ;
def Assign():
    if PRINT_PRODUCTIONS:
        write_output("<Assign> -> <Identifier> = <Expression> ;")
    match(expected_type="identifier")
    match(expected_lexeme="=")
    Expression()
    match(expected_lexeme=";")


# R18. <If>
# if ( <Condition> ) <Statement> fi
# if ( <Condition> ) <Statement> otherwise <Statement> fi
def If():
    if PRINT_PRODUCTIONS:
        write_output("<If> -> if ( <Condition> ) <Statement> fi | if ( <Condition> ) <Statement> otherwise <Statement> fi")


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
    if PRINT_PRODUCTIONS:
        write_output("<Return> -> return ; | return <Expression> ;")
    match(expected_lexeme="return")
    if current_token().lexeme != ";":
        Expression()
    match(expected_lexeme=";")


# R20. <Print>
# write ( <Expression> ) ;
def Print():
    if PRINT_PRODUCTIONS:
        write_output("<Print> -> write ( <Expression> ) ;")
    match(expected_lexeme="write")
    match(expected_lexeme="(")
    Expression()
    match(expected_lexeme=")")
    match(expected_lexeme=";")


# R21. <Scan>
# read ( <IDs> ) ;
def Scan():
    if PRINT_PRODUCTIONS:
        write_output("<Scan> -> read ( <IDs> ) ;")

    match(expected_lexeme="read")
    match(expected_lexeme="(")
    IDs()
    match(expected_lexeme=")")
    match(expected_lexeme=";")


# R22. <While>
# while ( <Condition> ) <Statement>
def While():
    if PRINT_PRODUCTIONS:
        write_output("<While> -> while ( <Condition> ) <Statement>")


    match(expected_lexeme="while")
    match(expected_lexeme="(")
    Condition()
    match(expected_lexeme=")")
    Statement()


# R23. <Condition>
# <Expression> <Relop> <Expression>
def Condition():
    if PRINT_PRODUCTIONS:
        write_output("<Condition> -> <Expression> <Relop> <Expression>")
    Expression()
    Relop()
    Expression()


# R24. <Relop>
# == | != | > | < | <= | =>
def Relop():
    if PRINT_PRODUCTIONS:
        write_output("<Relop> -> == | != | > | < | <= | =>")
    if current_token().lexeme in ["==", "!=", ">", "<", "<=", "=>"]:
        match(expected_lexeme=current_token().lexeme)
    else:
        error("Invalid relational operator")


# R25. <Expression>
def Expression():
    if PRINT_PRODUCTIONS:
        write_output("<Expression> -> <Term> | <Term> + <Expression> | <Term> - <Expression>")

    Term()
    while current_token().lexeme in ['+', '-']:
        match(expected_lexeme=current_token().lexeme)
        Term()


# R26. <Term>
def Term():
    if PRINT_PRODUCTIONS:
        write_output("<Term> -> <Factor> | <Factor> * <Term> | <Factor> / <Term>")

    Factor()
    while current_token().lexeme in ['*', '/']:
        match(expected_lexeme=current_token().lexeme)
        Factor()


# R27. <Factor>
def Factor():
    if PRINT_PRODUCTIONS:
        write_output("<Factor> -> - <Primary> | <Primary>")


    if current_token().lexeme == '-':
        match(expected_lexeme='-')
        Primary()
    else:
        Primary()


# R28. <Primary>
# Identifier | Integer | Real | ( <Expression> ) | true | false | Identifier ( <IDs> )
def Primary():
    if PRINT_PRODUCTIONS:
        write_output("<Primary> -> Identifier | Integer | Real | ( <Expression> ) | true | false | Identifier ( <IDs> )")
    token = current_token()

    if token.type == "identifier":
        match(expected_type="identifier")
        if current_token().lexeme == "(":
            match(expected_lexeme="(")
            IDs()
            match(expected_lexeme=")")
        return

    if token.type == "integer":
        match(expected_type="integer")
        return

    if token.type == "real":
        match(expected_type="real")
        return

    if token.lexeme == "(":
        match(expected_lexeme="(")
        Expression()
        match(expected_lexeme=")")
        return

    if token.lexeme in ["true", "false"]:
        match(expected_lexeme=token.lexeme)
        return

    error("Invalid primary")


# MAIN
if __name__ == "__main__":
    filename = input("Enter source filename: ")

    base = filename.split('.')[0]
    output_file = open(base + "_parser_output.txt", "w", encoding="utf-8") 

    tokens = do_lexer(filename)
    current = 0

    Rat26S()

    if current_token().type == "EOF":
        write_output("Syntax Valid")

    output_file.close()