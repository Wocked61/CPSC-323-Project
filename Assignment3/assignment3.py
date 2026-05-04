# ====== COMPILER ASSIGNMENT 3 BUILT FROM ASSIGNMENT 2  ======

from assignment1 import do_lexer
output_file = None
PRINT_PRODUCTIONS = False
tokens = []
current = 0

# Create symbol table
symbol_table = {}
Memory_Address = 10000

# Create instruction table
instruction_table = []
instruction_address = 1

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
    write_output(f" Error: {msg}. Found '{token.lexeme}' of type '{token.type}'")
    exit()

def match(expected_lexeme=None, expected_type=None):
    token = current_token()

    if expected_lexeme and token.lexeme != expected_lexeme:
        error(f"Expected '{expected_lexeme}' but found '{token.lexeme}'")

    if expected_type and token.type != expected_type:
        error(f"Expected {expected_type} but found {token.type}")

    write_output(f"Token: {token.type}    Lexeme: {token.lexeme}")
    advance()

def insert_symbol(name, sym_type):
    global Memory_Address
    if name in symbol_table:
        error(f"Variable '{name}' already declared")
    symbol_table[name] = {"type": sym_type, "address": Memory_Address}
    Memory_Address += 1

def lookup_symbol(name):
    if name not in symbol_table:
        error(f"Variable '{name}' not declared")
    return symbol_table[name]["address"]

def get_symbol_type(name):
    if name not in symbol_table:
        error(f"Variable '{name}' not declared")
    return symbol_table[name]["type"]

def check_assignment(name, value_type):
    if name not in symbol_table:
        error(f"Variable '{name}' not declared")
    var_type = symbol_table[name]["type"]
    if var_type != value_type:
        error(f"Type mismatch: cannot assign {value_type} to {var_type}")

def check_arithmetic_types(type1, type2):
    if type1 == "integer" and type2 == "integer":
        return "integer"
    error(f"Type mismatch in arithmetic operation: {type1} and {type2}")

def emit(opcode, operand=None):
    global instruction_address
    instruction_table.append({"address": instruction_address, "opcode": opcode, "operand": operand})
    instruction_address += 1

# R1. <Rat26S>
def Rat26S():
    if PRINT_PRODUCTIONS:
        write_output("<Rat26S> -> @ <Opt Declaration List> @ <Statement List> @")
    match(expected_lexeme='@')
    OptDeclarationList()
    match(expected_lexeme='@')
    StatementList()
    match(expected_lexeme='@')
    

# R8. <Qualifier>
# integer | boolean
def Qualifier():
    if PRINT_PRODUCTIONS:
        write_output("<Qualifier> -> integer | boolean")
    token = current_token()
    if token.lexeme in ["integer", "boolean"]:
        type_name = token.lexeme
        match(expected_type="keyword")
        return type_name
    else:
        error("Expected type qualifier (integer/boolean)")


# R10. <Opt Declaration List>
def OptDeclarationList():
    if PRINT_PRODUCTIONS:
        write_output("<Opt Declaration List> -> <Declaration List> | ε")

    if current_token().lexeme in ["integer", "boolean"]:
        DeclarationList()
    # else empty


# R11. <Declaration List>
# <Declaration> ; { <Declaration> ; }
def DeclarationList():
    if PRINT_PRODUCTIONS:
        write_output("<Declaration List> -> <Declaration> ; { <Declaration> ; }")

    Declaration()
    match(expected_lexeme=";")
    while current_token().lexeme in ["integer", "boolean"]:
        Declaration()
        match(expected_lexeme=";")


# R12. <Declaration>
# <Qualifier> <IDs>
def Declaration():
    if PRINT_PRODUCTIONS:
        write_output("<Declaration> -> <Qualifier> <IDs>")

    type_name = Qualifier()
    id_list = IDs()
    for var_name in id_list:
        insert_symbol(var_name, type_name)


# R13. <IDs>
# <Identifier> | <Identifier> , <IDs>
def IDs():
    if PRINT_PRODUCTIONS:
        write_output("<IDs> -> <Identifier> | <Identifier> , <IDs>")

    names = []
    names.append(current_token().lexeme)
    match(expected_type="identifier")
    while current_token().lexeme == ",":
        match(",")
        names.append(current_token().lexeme)
        match(expected_type="identifier")
    return names

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
    id_name = current_token().lexeme
    match(expected_type="identifier")
    match(expected_lexeme="=")
    expression_type = Expression()
    check_assignment(id_name, expression_type)
    address = lookup_symbol(id_name)
    emit("POPM", address)
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

    # Emit JMPZ placeholder
    jmpz_address = instruction_address
    emit("JMPZ", None)

    Statement()

    if current_token().lexeme == "otherwise":
        jmp_over_else_address = instruction_address
        emit("JMP", None)

    
        instruction_table[jmpz_address - 1] = {
            "address": jmpz_address,
            "opcode": "JMPZ",
            "operand": instruction_address
        }

        match(expected_lexeme="otherwise")
        Statement()

        instruction_table[jmp_over_else_address - 1] = {
            "address": jmp_over_else_address,
            "opcode": "JMP",
            "operand": instruction_address
        }

    else:
        instruction_table[jmpz_address - 1] = {
            "address": jmpz_address,
            "opcode": "JMPZ",
            "operand": instruction_address
        }

    match(expected_lexeme="fi")


# R20. <Print>
# write ( <Expression> ) ;
def Print():
    if PRINT_PRODUCTIONS:
        write_output("<Print> -> write ( <Expression> ) ;")
    match(expected_lexeme="write")
    match(expected_lexeme="(")
    expression_type = Expression()
    match(expected_lexeme=")")
    match(expected_lexeme=";")
    emit("SOUT")


# R21. <Scan>
# read ( <IDs> ) ;
def Scan():
    if PRINT_PRODUCTIONS:
        write_output("<Scan> -> read ( <IDs> ) ;")

    match(expected_lexeme="read")
    match(expected_lexeme="(")
    id_list = IDs()
    match(expected_lexeme=")")
    match(expected_lexeme=";")
    for name in id_list:
        address = lookup_symbol(name)
        emit("SIN")
        emit("POPM", address)


# R22. <While>
# while ( <Condition> ) <Statement>
def While():
    if PRINT_PRODUCTIONS:
        write_output("<While> -> while ( <Condition> ) <Statement>")

    match(expected_lexeme="while")

    start_of_loop = instruction_address
    emit("LABEL")

    match(expected_lexeme="(")
    Condition()
    match(expected_lexeme=")")

    jmpz_address = instruction_address
    emit("JMPZ", None)
    Statement()
    emit("JMP", start_of_loop)

    instruction_table[jmpz_address - 1] = {
        "address": jmpz_address,
        "opcode": "JMPZ",
        "operand": instruction_address
    }


# R23. <Condition>
# <Expression> <Relop> <Expression>
def Condition():
    if PRINT_PRODUCTIONS:
        write_output("<Condition> -> <Expression> <Relop> <Expression>")
    left_type = Expression()
    op = Relop()
    right_type = Expression()
    if left_type != right_type:
        error("Type mismatch in condition")
    if left_type == "boolean":
        if op not in ["==", "!="]:
            error("Invalid operator for boolean condition")
    else: 
        if op == "<":
            emit("LES")
        elif op == ">":
            emit("GRT")
        elif op == "==":
            emit("EQU")
        elif op == "!=":
            emit("NEQ")
        elif op == "<=":
            emit("LEQ")
        elif op == "=>":
            emit("GEQ")
        else:
            error("Invalid relational operator")
        return
    if op == "==":
        emit("EQU")
    elif op == "!=":
        emit("NEQ")



# R24. <Relop>
# == | != | > | < | <= | =>
def Relop():
    if PRINT_PRODUCTIONS:
        write_output("<Relop> -> == | != | > | < | <= | =>")
    token = current_token()
    if token.lexeme in ["==", "!=", ">", "<", "<=", "=>"]:
        op = token.lexeme
        match(expected_lexeme=current_token().lexeme)
        return op
    else:
        error("Invalid relational operator")


# R25. <Expression>
def Expression():
    if PRINT_PRODUCTIONS:
        write_output("<Expression> -> <Term> | <Term> + <Expression> | <Term> - <Expression>")

    t_type = Term()
    while current_token().lexeme in ['+', '-']:
        op = current_token().lexeme
        match(expected_lexeme=op)
        rhs_type = Term()
        check_arithmetic_types(t_type, rhs_type)
        if op == '+':
            emit("A")
        else:
            emit("S")
        t_type = "integer"
    return t_type
        


# R26. <Term>
def Term():
    if PRINT_PRODUCTIONS:
        write_output("<Term> -> <Factor> | <Factor> * <Term> | <Factor> / <Term>")

    f_type = Factor()
    while current_token().lexeme in ['*', '/']:
        op = current_token().lexeme
        match(expected_lexeme=op)
        rhs_type = Factor()
        check_arithmetic_types(f_type, rhs_type)
        if op == '*':
            emit("M")
        else:
            emit("D")
        f_type = "integer"
    return f_type


# R27. <Factor>
def Factor():
    if PRINT_PRODUCTIONS:
        write_output("<Factor> -> - <Primary> | <Primary>")


    if current_token().lexeme == '-':
        match(expected_lexeme='-')
        p_type = Primary()
        if p_type != "integer":
            error("Unary '-' operator requires integer operand")
        emit("PUSHI", 0)
        emit("S")
        return "integer"
    else:
        return Primary()


# R28. <Primary>
# Identifier | Integer | ( <Expression> ) | true | false)
def Primary():
    if PRINT_PRODUCTIONS:
        write_output("<Primary> -> Identifier | Integer | ( <Expression> ) | true | false")
    token = current_token()

    if token.type == "identifier":
        name = token.lexeme
        match(expected_type="identifier")
        if current_token().lexeme == "(":
            error("Function calls not supported in this assignment")
        addr = lookup_symbol(name)
        emit("PUSHM", addr)
        return get_symbol_type(name)
        

    if token.type == "integer":
        value = int(token.lexeme)
        match(expected_type="integer")
        emit("PUSHI", value)
        return "integer"

    if token.lexeme == "(":
        match(expected_lexeme="(")
        t = Expression()
        match(expected_lexeme=")")
        return t

    if token.lexeme in ["true", "false"]:
        value = 1 if token.lexeme == "true" else 0
        match(expected_lexeme=token.lexeme)
        emit("PUSHI", value)
        return "boolean"

    error("Invalid primary")

def print_instruction_table():
    write_output("Assembly Instructions:")
    for instr in instruction_table:
        addr = instr["address"]
        op = instr["opcode"]
        operand = instr["operand"]
        if operand is None:
            write_output(f"{addr}: {op}")
        else:
            write_output(f"{addr}: {op} {operand}")

def print_symbol_table():
    write_output("Symbol Table:")
    write_output(f"{'Identifier':<20} {'Memory Address':<15} {'Type':<10}")
    for name, info in symbol_table.items():
        write_output(f"{name:<20} {info['address']:<15} {info['type']:<10}")


# MAIN
if __name__ == "__main__":
    filename = input("Enter source filename: ")

    base = filename.split('.')[0]
    output_file = open(base + "_compiler_output.txt", "w", encoding="utf-8") 

    tokens = do_lexer(filename)
    current = 0

    Rat26S()

    if current_token().type == "EOF":
        write_output("Syntax Valid")

    print_instruction_table()
    print_symbol_table()

    output_file.close()