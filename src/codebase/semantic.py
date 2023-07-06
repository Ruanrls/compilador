class Semantic:
    def identifierAlreadyDeclared(identifier, line):
        raise Exception("Erro Semantico: " + identifier + " ja declarado na linha " + str(line))

    def identifierNotDeclared(identifier, line):
        raise Exception("Erro Semantico: " + identifier + " nao declarado na linha " + str(line))