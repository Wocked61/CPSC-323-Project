import string
import os

class Token:
    """
    This class holds information about a token.
    
    Attributes:
        type (str): The type of the token.
        lexeme (str): The actual text of the token.
    """

    def __init__(self, token_type, lexeme):
        self.type = token_type
        self.lexeme = lexeme

    def __repr__(self):
        return f"{self.type:<12} {self.lexeme}"



# Set of valid characters for letters and digits
LETTERS = string.ascii_letters
DIGITS = string.digits
 
# List of operators, separators, and keywords
OPERATORS = {"=", "==", "!=", "<", "<=", ">", ">=", "+", "-", "*", "/", "+=", "-=", "*=", "/=", "++", "--", "&&", "||", "!"}
SEPARATORS = {"(", ")", "{", "}", ";", ",", "@"}
KEYWORDS = {
    "integer", "boolean", "real", "if", "otherwise",
    "fi", "while", "return", "read", "write", "function", "true", "false"
}




def DFSM(lexeme, table, accepting_states, column_function):
    """
    This function evaluates a DFSM for a given lexeme based off the template provided in class.
    
    Parameters:
        lexeme (str): The input string to evaluate.
        table (list): The DFSM table.
        accepting_states (set): The set of accepting states.
        char_to_col (function): A function that maps a character to a column index.
    """
    state = 1

    for char in lexeme:
        column = column_function(char)

        # Check boundary conditions
        if state < 0 or column < 0 or state >= len(table) or column >= len(table[state]):
            return False

        # Get the next state from the table
        state = table[state][column]

    return state in accepting_states

# Function to return the column that identifies the next state based on the current character
def char_to_col(ch):
    match ch:
        case ch if ch in LETTERS:
            return 0
        case ch if ch in DIGITS:
            return 1
        case "_":
            return 2
        case _:
            return -1

def identifier_fsm(source, i):
    """
    This function determines if the token is an identifier.
    
    Parameters:
        source (str): The entire source code string.
        i (int): The current index in the source string where the token starts.
    """    
    lexeme = ""

    # Build the Lexeme
    while i < len(source) and (source[i] in LETTERS or source[i] in DIGITS or source[i] == "_"):
        lexeme += source[i]
        i += 1

    # DFSM table for identifier with states: 0 = initial state, 1 = start, 2 = identifier, 3 = unknown
    ident_table = [
    [],                
    [2, 3, 3],          
    [2, 2, 2],          
    [3, 3, 3]              
    ]


    # Call the DFSM to determine if the lexeme is an identifier
    if DFSM(lexeme, ident_table, {2}, char_to_col):
        return Token("identifier", lexeme), i

    # Lexeme is unknown
    return Token("unknown", lexeme), i

# Function to determine if a character is just an integer
def int_to_col(ch):
     match ch:
        case ch if ch in DIGITS:
            return 0
        case _:
            return -1

# Function to determine if a character is a real number
def real_to_col(ch):
    match ch:
        case ch if ch in DIGITS:
            return 0
        case ".":
            return 1
        case _:
            return -1


def number_fsm(source, i):
    """
    This function determines if the token is a number (integer or real).
    
    Parameters:
        source (str): The entire source code string.
        i (int): The current index in the source string where the token starts.
    """      
    lexeme = ""

    # Build the Lexeme
    while i < len(source) and (source[i] in DIGITS or source[i] == "."):
        lexeme += source[i]
        i += 1

    # DFSM table for integer with states: 0 = initial state, 1 = start, 2 = integer, 3 = unknown
    int_table = [
    [],           
    [2, 3],       
    [2, 3],       
    [3, 3]        
    ]
     
    # DFSM table for real with states: 0 = initial state, 1 = integer part, 2 = dot, 3 = fraction part, 4 = real, 5 = unknown
    real_table = [
    [],           
    [2, 5, 5],    
    [2, 3, 5],  
    [4, 5, 5],   
    [4, 5, 5],   
    [5, 5, 5]     
    ]

   
    # Use integer DFSM table
    if DFSM(lexeme, int_table, {2}, int_to_col):
        return Token("integer", lexeme), i

    # Use real number DFSM table
    if DFSM(lexeme, real_table, {4}, real_to_col):
        return Token("real", lexeme), i

    # Lexeme is unknown
    return Token("unknown", lexeme), i

def skip_comment(source, i):
    """
    This function skips over comments in the source code.
    
    Parameters:
        source (str): The entire source code string.
        i (int): The current index in the source string where the comment starts.
    """

    # Skip the opening "/*" and then continue until the closing "*/" is found
    if source[i:i+2] == "/*":
        i += 2
        while i < len(source) - 1 and source[i:i+2] != "*/":
            i += 1
        return i + 2
    return i

def lexer(source, i):
    """
    This function is the main lexer function that identifies tokens in the source code.
    
    Parameters:
        source (str): The entire source code string.
        i (int): The current index in the source string where the token starts.
    """
    # Skip whitespace
    while i < len(source) and source[i].isspace():
        i += 1

    # Check for end of file (EOF)
    if i >= len(source):
        return Token("EOF", ""), i

    # Skip comments by checking for "/*" and calling the skip_comment function
    if source[i:i+2] == "/*":
        i = skip_comment(source, i)
        return lexer(source, i)

    char = source[i]

    # Identifier or keyword
    if char in LETTERS:
        token, i = identifier_fsm(source, i)
        if token.lexeme in KEYWORDS:
            token.type = "keyword"
        return token, i

    # Number (integer or real)
    if char in DIGITS:
        return number_fsm(source, i)

    # Operators (check 2-char first)
    if source[i:i+2] in OPERATORS:
        return Token("operator", source[i:i+2]), i + 2

    if char in OPERATORS:
        return Token("operator", char), i + 1

    # Separators
    if char in SEPARATORS:
        return Token("separator", char), i + 1

    # Unknown character
    return Token("unknown", char), i + 1

def do_lexer(filename):
    """
    This function runs the lexer on a given source file and prints the tokens.
    
    Parameters:
        filename (str): The name of the source file to lex.
    """    
    with open(filename) as file:
        source = file.read()

    file_index = 0
    tokens = []


    # Loop through the source code and call the lexer function until we reach the end of the file (EOF)
    while True:
        token, file_index = lexer(source, file_index)
        tokens.append(token)
        if token.type == "EOF":
            break

    # Create output text file
    base, _ = os.path.splitext(filename)
    out_filename = f"{base}_output.txt"
    out_file = open(out_filename, 'w')
    
    out_file.write(f"{'Token':<12} {'Lexeme'}\n")
    out_file.write(f"{'-'*12} {'-'*6}\n")
    for t in tokens:
        out_file.write(f"{t}\n")
    out_file.close()
    print(f"Output written to {out_filename}")
    return tokens       


# Main loop to run the lexer on user-provided files until they choose to quit
if __name__ == "__main__":
    while True: 
        filename = input("Enter source filename (or 'quit' to exit): ")
        if filename == "quit":
            break
        try:    
            do_lexer(filename)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")


