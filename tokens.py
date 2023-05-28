''' 
    Palavras reservadas:
    PROGRAMA, VARIAVEIS, INTEIRO, REAL, LOGICO, CARACTER, SE, SENAO, ENQUANTO, LEIA, ESCREVA, FALSO, VERDADEIRO
'''

class TOKEN_TYPE:
    PROGRAMA = (0, 'PROGRAMA')
    VARIAVEIS = (1, 'VARIAVEIS')
    INTEIRO = (2, 'INTEIRO')
    REAL = (3, 'REAL')
    LOGICO = (4, 'LOGICO')
    CARACTER = (5, 'CARACTER')
    SE = (6, 'SE')
    SENAO = (7, 'SENAO')
    ENQUANTO = (8, 'ENQUANTO')
    LEIA = (9, 'LEIA')
    ESCREVA = (10, 'ESCREVA')
    FALSO = (11, 'FALSO')
    VERDADEIRO = (12,'VERDADEIRO')
    ATRIB = (13, ':=')
    OPREL = (14, '< > = <= >= <>')
    OPAD = (15, '+ -')
    OPMUL = (16, '* /')
    OPNEG = (17, '!')
    PVIRG = (18, ';')
    DPONTOS = (19, ':')
    VIRG = (20, ',')
    ABREPAR = (21, '(')
    FECHAPAR = (22, ')')
    ABRECH = (23, '{')
    FECHACH = (24, '}')
    IDENT = (25, 'IDENT')
    CADEIA = (26, 'CADEIA')
    NUM = (27, 'NUM')
    EOF = (28, 'EOF')

class Token:
    def __init__(self, type, lexeme, line, inline_position):
        self.type = type
        self.lexeme = lexeme
        self.line = line
        self.inline_position = inline_position
    
    def __str__(self) -> str:
        return f'{self.type[0]} -- {self.type[1]}: {self.lexeme} - line {self.line}'
