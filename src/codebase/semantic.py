class Semantic:
    def identifierAlreadyDeclared(identifier, line):
        raise Exception("Erro Semantico: " + identifier + " ja declarado na linha " + str(line))

    def identifierNotDeclared(identifier, line):
        raise Exception("Erro Semantico: " + identifier + " nao declarado na linha " + str(line))
    
    def invalidExpressionType(command: str, line: str):
        raise Exception("Erro Semantico: Comando " + command + " deve receber uma expressao booleana na linha " + str(line))

    def invalidDifferentTypes(command: str, line: str):
        raise Exception("Erro Semantico: Comando " + command + " deve receber expressoes do mesmo tipo na linha " + str(line))

    def invalidBooleanOrStringOperator(type: str, line: str):
        raise Exception("Operadores do tipo " + type + " so podem ser utilizados com os operadores '<>, ='" + str(line))
    
    def invalidAritmeticOperands(type: str, line: str):
        raise Exception("Operadores aritmeticos so podem ser utilizados com os tipos numericos (REAL, INTEIRO)" + str(line))