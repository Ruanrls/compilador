from tokens import Token
from semantic import Semantic

class Symbol:
    def __init__(self, identifier: str, type: str, line: str) -> None:
        self.identifier = identifier
        self.type = type
        self.line = line
    
    def __str__(self) -> str:
        return f" -> {self.type}, line: {self.line}"

class Symbols:
    def __init__(self) -> None:
        self.table = {}

    def addSymbol(self, symbol: Symbol) -> None:
        if symbol.identifier in self.table:
            Semantic.identifierAlreadyDeclared(symbol.identifier, symbol.line)
        self.table[symbol.identifier] = symbol
    
    def addSymbols(self, symbols: list, type: str) -> None:
        for symbol in symbols:
            self.addSymbol(Symbol(symbol.lexeme, type, symbol.line))


    def validateSymbol(self, identifier: str, line: str) -> str:
        if identifier in self.table:
            return self.table[identifier]
        else:
            Semantic.identifierNotDeclared(identifier, line)

    def validateSymbols(self, symbols: list) -> None:
        for symbol in symbols:
            self.validateSymbol(symbol.lexeme, symbol.line)
        
    def __str__(self) -> str:
        to_print = ""
        for key in self.table:
            to_print = f"{to_print}{key} -> {self.table[key]}\n"
        return to_print