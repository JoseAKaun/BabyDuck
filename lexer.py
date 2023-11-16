#Jose Kaun - A01720829
# Analizador Lexico

import ply.lex as lex

# Lista de tokens
tokens = (
    # Keywords
    'PROGRAM',
    'VAR',
    'BEGIN',
    'END',
    'IDENTIFIER',

    # Tipos
    'STRING_CONST',
    'BOOLEAN',
    'INT',
    'REAL',
    'CHAR',
    'NUMBER_CONST',

    # Operadores aritmeticos
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'MOD',
    'PLUSPLUS',
    'MINUSMINUS',
    'DIV',


    # Operadores logicos
    'AND',
    'OR',
    'EQUALS',
    'NOT_EQUALS',
    'LESS_THAN',
    'LESS_THAN_EQUALS',
    'GREATER_THAN',
    'GREATER_THAN_EQUALS',
    'ASSIGNOP',

    # Elementos del syntax
    'LPAR',
    'RPAR',
    'LBRAC',
    'RBRAC',
    'LCURLY',
    'RCURLY',
    'COMMA',
    'SEMICOLON',
    'COLON',
    'PERIOD',

    # Repetidores
    'FOR',
    'WHILE',
    'DO',

    # Condicionales
    'IF',
    'ELSE',
    'THEN',
    'STRING',
    'TRUE',
    'FALSE',
    'NOT',

    # Print y Write
    'WRITE',
    'PRINT',

)

# Expresiones para los tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_ASSIGNOP = r':='
t_EQUALS = r'='
t_NOT_EQUALS = r'<>'
t_LESS_THAN = r'<'
t_LESS_THAN_EQUALS = r'<='
t_GREATER_THAN = r'>'
t_GREATER_THAN_EQUALS = r'>='
t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRAC = r'\['
t_RBRAC = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_COLON = r':'
t_PERIOD = r'\.'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'

# Los identificadores pueden empezar con letra o guion-bajo. Igual pueden pueden ser compuestos de cualquier cantidad de letras, numeros o guion-bajos.
# Pero NO pueden empezar con un numero/digito.
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = t.value.upper() if t.value.upper() in tokens else 'IDENTIFIER'
    return t


def t_NUMBER_CONST(t):
    r'\d+(\.\d*)?([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t


# Constante String
def t_STRING_CONST(t):
    r'\"([^\\\n]|(\\.))*?\"' # Aqui le habilitamos el uso de espacios en strings
    t.value = t.value[1:-1]  # Quitar comillas
    return t


# Regla de error
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Regla para definir numeros de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Ignorar whitespace 
t_ignore = ' \t\r\n'

#Construccion del lexer
lexer = lex.lex()

input_file_path = "input.txt"
input_file = open(input_file_path, "r")
file_contents = input_file.read()
lexer.input(file_contents)
output_file_path = "lexerOut.txt"
output_file = open(output_file_path, "w")

# Tokenizar? como se diga jaja
while True:
    tok = lexer.token()
    if not tok:
        break  # Si no hay input
    output_file.write(str(tok.value) + '~')
    output_file.write(str(tok.lineno) + '~')
    output_file.write(str(tok.type) + '~')

output_file.close()