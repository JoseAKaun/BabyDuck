# Jose A. Kaun - A01720829
#Analisis Semantico
import ply.yacc as yacc
import ply.lex as lex
from lexer import tokens

# Variables Globales
currToken = ''
prevToken = ''

# Operadores tipo tabla
opTypeTable = {
    'NUMBER_CONST': ['NUMBER_CONST', 'int', 'real'],
    'STRING_CONST': ['STRING_CONST'],
    'BOOLEAN': ['BOOLEAN'],
}


class Quadruple:
    def __init__(self, index, operator, operand1, operand2, result):
        self.index = index
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.result = result

    def print(self):
        print(self.index, self.operator, self.operand1,
              self.operand2, self.result)



# Tabla de Variables
varTable = {
    # 'a' : ['int', value]
}

varTempArr = []


# Gramatica
def p_program(p):
    'program : PROGRAM IDENTIFIER LCURLYBRACE vars block RCURLYBRACE'
    p[0] = p[1]


def p_vars(_):
    '''vars : VAR varsp COLON type seentype SEMICOLON
            | VAR varsp COLON type seentype SEMICOLON vars
            | empty '''


def p_varsp(_):
    '''varsp : IDENTIFIER seenid
            | IDENTIFIER seenid COMMA varsp'''


def p_seenid(p):
    '''seenid : '''
    # agregar a tabla de variables
    global varTempArr
    varTempArr.append(p[-1])


def p_seentype(p):
    'seentype : '
    global varTempArr
    global varTable

    for id in varTempArr:
        # checar si la variable esta en uso en la tabla
        if id in varTable:
            print('Error, duplicate variable')
            p_error(p)
        if p[-1] in ['int', 'real']:
            varTable[id] = ['NUMBER_CONST', 0]
        elif p[-1] in ['boolean']:
            varTable[id] = ['BOOLEAN', None]
        elif p[-1] in ['string']:
            varTable[id] = ['STRING_CONST', None]

    # Resetear variable arraytemp
    varTempArr = []


def p_type(p):
    '''type : INT
            | REAL
            | STRING
            | BOOLEAN'''
    p[0] = p[1]


def p_block(_):
    'block : BEGIN SEMICOLON statement END SEMICOLON'


def p_statement(_):
    '''statement : empty
                | assign
                | assign statement
                | writefunction
                | writefunction statement
                | condition
                | condition statement
                | while
                | while statement
                | for
                | for statement
                | IDENTIFIER PLUSPLUS seenunary checknum SEMICOLON
                | IDENTIFIER MINUSMINUS seenunary checknum SEMICOLON
                | IDENTIFIER PLUSPLUS seenunary checknum SEMICOLON statement
                | IDENTIFIER MINUSMINUS seenunary checknum SEMICOLON statement'''


def p_condition(p):
    '''condition : IF LPAREN expression RPAREN checkbool seenif THEN LCURLYBRACE statement RCURLYBRACE seencurlyif seencurlyelse
                | IF LPAREN expression RPAREN checkbool seenif THEN LCURLYBRACE statement RCURLYBRACE seencurlyif ELSE condition seencurlyelse
                | IF LPAREN expression RPAREN checkbool seenif THEN LCURLYBRACE statement RCURLYBRACE seencurlyif ELSE LCURLYBRACE statement RCURLYBRACE seencurlyelse'''


def p_for(_):
    '''for : FOR LPAREN assign expression checkbool seenboolfor SEMICOLON expression seenchangefor RPAREN LCURLYBRACE statement RCURLYBRACE seencurlyfor
            | FOR LPAREN assign expression checkbool seenboolfor SEMICOLON assignfor checknum seenchangefor RPAREN LCURLYBRACE statement RCURLYBRACE seencurlyfor'''


def p_assign(_):
    'assign : IDENTIFIER ASSIGNOP expression assignnow SEMICOLON'


def p_assignfor(_):
    'assignfor : IDENTIFIER ASSIGNOP expression pushtype assignnowfor'


def p_simpleexpression(p):
    '''simpleexpression : term seenterm simpleexpressionp'''



def p_simpleexpressionp(p):
    '''simpleexpressionp : empty
                        | PLUS seenoperator simpleexpression
                        | MINUS seenoperator simpleexpression
                        | OR seenoperator simpleexpression'''


def p_term(p):
    '''term : factor seenfactor termp'''


def p_termp(p):
    '''termp : empty
            | MULTIPLY seenoperator term
            | DIV seenoperator term
            | DIVIDE seenoperator term
            | MOD seenoperator term
            | AND seenoperator term
            | PLUSPLUS seenoperator
            | MINUSMINUS seenoperator'''

def p_factor(p):
    '''factor : const
                | LPAREN seenoperator expression RPAREN exitparen'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]



def p_empty(p):
    'empty : '


# Errores de syntax
def p_error(p):
    print("Syntax error in input! Near '%s' line: %s" % (p.value, p.lineno))


input_file_path = "lexerOut.txt"
input_file = open(input_file_path, "r")
raw_input = input_file.read().split('~')
input_file.close()


