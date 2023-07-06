from lexer import Lexer, TOKEN_TYPE
from symbol import Symbols

'''
P = {
    PROG → programa id pvirg DECLS C-COMP
    DECLS → _ | variaveis LIST-DECLS
    LIST-DECLS → DECL-TIPO D
    D → _ | LIST-DECLS
    DECL-TIPO → LIST-ID dpontos TIPO pvirg
    LIST-ID → id E
    E → _ | virg LIST-ID
    TIPO → inteiro | real | logico | caracter
    C-COMP → abrech LISTA-COMANDOS fechach
    LISTA-COMANDOS → COMANDOS G
    G → _ | LISTA-COMANDOS
    COMANDOS → IF | WHILE | READ | WRITE | ATRIB
    IF → se abrepar EXPR fechapar C-COMP H
    H → _ | senao C-COMP
    WHILE → enquanto abrepar EXPR fechapar C-COMP
    READ → leia abrepar LIST-ID fechapar pvirg
    ATRIB → id atrib EXPR pvirg
    WRITE → escreva abrepar LIST-W fechapar pvirg
    LIST-W → ELEM-W L
    L → _ | virg LIST-W
    ELEM-W → EXPR | cadeia
    EXPR → SIMPLES P
    P → _ | oprel SIMPLES
    SIMPLES → TERMO R
    R → _ | opad SIMPLES
    TERMO → FAT S
    S → _ | opmul TERMO
    FAT → id | cte | abrepar EXPR fechapar | verdadeiro | falso | opneg FAT
}
'''

class Syntactic:
    def __init__(self) -> None:
        self.current_token = None
        self.lexer = None
        self.get_next_token = None
        self.symbol_table = Symbols()
        self.comparison_type = None

    def interpreter(self, file_name):
        if self.lexer != None:
            raise Exception("Interpreter already initialized")

        self.lexer = Lexer()
        self.lexer.load(file_name)
        self.lexer.parse_tokens()
    
    def initialize(self):
        if(self.lexer == None):
            raise Exception("Interpreter not initialized")

        self.get_next_token = self.lexer.get_next_token()
        self.current_token = next(self.get_next_token)
        self.prog()

    def validate_token(self, token):
        (token_type, message) = token
        if self.current_token == None:
            raise Exception(f'invalid token {self.current_token}')

        if self.current_token.type[0] != token_type:
            raise Exception(f'Expected {token} but found {self.current_token.type} on line {self.current_token.line}')
        
    def consume(self, token):
        if(self.lexer == None or self.current_token == None or self.get_next_token == None):
            raise Exception("Interpreter not initialized")

        last_token = self.current_token
        self.validate_token(token)
        self.current_token = next(self.get_next_token)
        return last_token

    def prog(self):
        self.consume(TOKEN_TYPE.PROGRAMA)
        self.consume(TOKEN_TYPE.IDENT)
        self.consume(TOKEN_TYPE.PVIRG)
        self.decls()
        self.c_comp()
        self.consume(TOKEN_TYPE.EOF)
    
    def decls(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        if self.current_token.type == TOKEN_TYPE.VARIAVEIS:
            self.consume(TOKEN_TYPE.VARIAVEIS)
            self.list_decls()
        else:
            return

    def list_decls(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        self.decl_type()
        self.d()

    def d(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        if self.current_token.type == TOKEN_TYPE.IDENT:
            self.list_decls()
        else:
            return

    def decl_type(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        identifiers = self.list_id()
        self.consume(TOKEN_TYPE.DPONTOS)
        identify_type = self._type()
        self.consume(TOKEN_TYPE.PVIRG)  

        self.symbol_table.addSymbols(identifiers, identify_type.type)


    def list_id(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        identify = self.consume(TOKEN_TYPE.IDENT)
        identify_list = self.e()

        if(identify_list != None):
            list = []
            list.append(identify)
            list.extend(identify_list)
            return list

        return [identify]

    def _type(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        if self.current_token.type == TOKEN_TYPE.INTEIRO:
            return self.consume(TOKEN_TYPE.INTEIRO)
        elif self.current_token.type == TOKEN_TYPE.REAL:
            return self.consume(TOKEN_TYPE.REAL)
        elif self.current_token.type == TOKEN_TYPE.LOGICO:
            return self.consume(TOKEN_TYPE.LOGICO)
        elif self.current_token.type == TOKEN_TYPE.CARACTER:
            return self.consume(TOKEN_TYPE.CARACTER)
        else:
            raise Exception(f'Expected a type but found {self.current_token.type} on line {self.current_token.line}')

    def c_comp(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        self.consume(TOKEN_TYPE.ABRECH)
        self.command_list()
        self.consume(TOKEN_TYPE.FECHACH)
    
    def e(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        if self.current_token.type == TOKEN_TYPE.VIRG:
            self.consume(TOKEN_TYPE.VIRG)
            return self.list_id()
        else:
            return
    
    def command_list(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        self.command()
        self.g()

    def command(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")
        
        if self.current_token.type == TOKEN_TYPE.SE:
            self._if()
        elif self.current_token.type == TOKEN_TYPE.ENQUANTO:
            self._while()
        elif self.current_token.type == TOKEN_TYPE.LEIA:
            self.read()
        elif self.current_token.type == TOKEN_TYPE.ESCREVA:
            self.write()
        elif self.current_token.type == TOKEN_TYPE.IDENT:
            self.attrib()
        else:
            raise Exception(f'expected a command or idenfier, received {self.current_token.type}')

    def g(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        possible_commands = [TOKEN_TYPE.SE, TOKEN_TYPE.ENQUANTO, TOKEN_TYPE.LEIA, TOKEN_TYPE.ESCREVA,  TOKEN_TYPE.IDENT]
        if self.current_token.type in possible_commands:
            self.command_list()
        else:
            return

    def _if(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        self.consume(TOKEN_TYPE.SE)
        self.consume(TOKEN_TYPE.ABREPAR)
        expr_type = self.expr()
        
        #condicoes devem ser logicas
        if expr_type != TOKEN_TYPE.LOGICO[1]:
            raise Exception("A expressão condicional do SE deve retornar um valor lógico linha " + str(self.current_token.line))

        self.consume(TOKEN_TYPE.FECHAPAR)
        self.c_comp()
        self.h()

    def expr(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        expression_type = self.simple()
        expression_type = self.p(expression_type)
        return expression_type

    def simple(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        term_type = self.term()
        return self.r(term_type)


    def term(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        fact_type = self.fact()
        return self.s(fact_type)

    def fact(self):
        if(self.current_token == None):
            raise Exception("Interpreter not initialized")
        
        if self.current_token.type == TOKEN_TYPE.IDENT:
            identifier = self.consume(TOKEN_TYPE.IDENT)
            symbol = self.symbol_table.validateSymbol(identifier.lexeme, identifier.line)
            symbol_type = symbol.type[1]
            if(symbol_type in [TOKEN_TYPE.INTEIRO[1], TOKEN_TYPE.REAL[1]]):
                return TOKEN_TYPE.NUM[1]
            elif(symbol_type in [TOKEN_TYPE.VERDADEIRO[1], TOKEN_TYPE.FALSO[1]]):
                return TOKEN_TYPE.LOGICO[1]
            elif(symbol_type == TOKEN_TYPE.CARACTER[1]):
                return TOKEN_TYPE.CADEIA[1]
            return symbol_type
        elif self.current_token.type == TOKEN_TYPE.NUM:
            self.consume(TOKEN_TYPE.NUM)
            return TOKEN_TYPE.NUM[1]
        elif self.current_token.type == TOKEN_TYPE.ABREPAR:
            self.consume(TOKEN_TYPE.ABREPAR)
            expr_type = self.expr()
            self.consume(TOKEN_TYPE.FECHAPAR)
            return expr_type
        elif self.current_token.type == TOKEN_TYPE.VERDADEIRO:
            self.consume(TOKEN_TYPE.VERDADEIRO)
            return TOKEN_TYPE.LOGICO[1]
        elif self.current_token.type == TOKEN_TYPE.FALSO:
            self.consume(TOKEN_TYPE.FALSO)
            return TOKEN_TYPE.LOGICO[1]
        elif self.current_token.type == TOKEN_TYPE.OPNEG:
            self.consume(TOKEN_TYPE.OPNEG)
            return self.fact()
        else:
            raise Exception(f'Expected a factor but found {self.current_token.type} on line {self.current_token.line}')
    
    def _while(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        self.consume(TOKEN_TYPE.ENQUANTO)
        self.consume(TOKEN_TYPE.ABREPAR)
        expr_type = self.expr()

        #while deve receber operadores logicos
        if expr_type != TOKEN_TYPE.LOGICO[1]:
            raise Exception("A expressão condicional do ENQUANTO deve retornar um valor lógico linha " + str(self.current_token.line))

        self.consume(TOKEN_TYPE.FECHAPAR)
        self.c_comp()
    
    def read(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        self.consume(TOKEN_TYPE.LEIA)
        self.consume(TOKEN_TYPE.ABREPAR)
        identifier_list = self.list_id()
        self.symbol_table.validateSymbols(identifier_list)
        self.consume(TOKEN_TYPE.FECHAPAR)
        self.consume(TOKEN_TYPE.PVIRG)
    
    def write(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        self.consume(TOKEN_TYPE.ESCREVA)
        self.consume(TOKEN_TYPE.ABREPAR)
        self.list_write()
        self.consume(TOKEN_TYPE.FECHAPAR)
        self.consume(TOKEN_TYPE.PVIRG)
    
    def list_write(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        self.elem_w()
        self.l()
    
    def l(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        if self.current_token.type == TOKEN_TYPE.VIRG:
            self.consume(TOKEN_TYPE.VIRG)
            self.list_write()
        else:
            return
    
    def elem_w(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        if self.current_token.type == TOKEN_TYPE.CADEIA:
            self.consume(TOKEN_TYPE.CADEIA)
        else:
            self.expr()
    
    def attrib(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")
        
        identifier = self.consume(TOKEN_TYPE.IDENT)
        self.symbol_table.validateSymbol(identifier.lexeme, identifier.line)
        self.consume(TOKEN_TYPE.ATRIB)
        self.expr()
        self.consume(TOKEN_TYPE.PVIRG)
    
    def h(self):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        if self.current_token.type == TOKEN_TYPE.SENAO:
            self.consume(TOKEN_TYPE.SENAO)
            self.c_comp()
        else:
            return
        
    def p(self, left_expr_type):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        if self.current_token.type == TOKEN_TYPE.OPREL:
            oprel_token = self.consume(TOKEN_TYPE.OPREL)
            right_expr_type = self.simple()

            #operadores diferentes nao podem ser comparados
            if(left_expr_type != right_expr_type):
                raise Exception(f'Operador relacional {oprel_token.lexeme} usado com operandos de tipos diferentes (linha {self.current_token.line})')

            #operadores booleanos e strings so podem ser diferentes ou iguais
            if((left_expr_type == TOKEN_TYPE.LOGICO[1] or left_expr_type == TOKEN_TYPE.CADEIA[1]) and oprel_token.lexeme not in ['<>', '=']):
                raise Exception(f'Operador relacional {oprel_token.lexeme} usado com operandos lógicos ou strings (linha {self.current_token.line})')
            
            return TOKEN_TYPE.LOGICO[1]
        else:
            return left_expr_type
    
    def r(self, left_expr_type):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        if self.current_token.type == TOKEN_TYPE.OPAD:
            oprel_token = self.consume(TOKEN_TYPE.OPAD)
            right_expr_type = self.simple()
            #operadores diferentes nao podem ser comparados
            if(left_expr_type != right_expr_type):
                raise Exception(f'Operador relacional {oprel_token.lexeme} usado com operandos de tipos diferentes (linha {self.current_token.line})')

            #soma apenas com valores numericos
            if(left_expr_type != TOKEN_TYPE.NUM[1]):
                raise Exception(f'Operador relacional {oprel_token.lexeme} usado com operandos numericos (linha {self.current_token.line})')
            
            return TOKEN_TYPE.LOGICO[1]
        else:
            return left_expr_type

    def s(self, left_expr_type):
        if self.current_token == None:
            raise Exception("Interpreter not initialized")

        if self.current_token.type == TOKEN_TYPE.OPMUL:
            self.consume(TOKEN_TYPE.OPMUL)
            return self.term()
        else:
            return left_expr_type