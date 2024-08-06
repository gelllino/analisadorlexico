import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.symbols = {}
        self.errors = []
        
    def tokenize(self):
        token_specification = [
            ('KEYWORD', r'\b(if|else|while|return)\b'),  # Palavras-chave
            ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),  # Identificadores
            ('NUMBER', r'\b\d+\b'),  # Números
            ('OPERATOR', r'[+\-*/=]'),  # Operadores
            ('DELIMITER', r'[(){};]'),  # Delimitadores
            ('SKIP', r'[ \t\n]+'),  # Espaços em branco a serem ignorados
            ('MISMATCH', r'.')  # Qualquer outro caractere não esperado
        ]
        
        token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        for match in re.finditer(token_regex, self.source_code):
            kind = match.lastgroup
            value = match.group()
            if kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                self.errors.append(f"Unexpected character: {value} at position {match.start()}")
            else:
                self.tokens.append((kind, value))
                if kind == 'IDENTIFIER':
                    if value not in self.symbols:
                        self.symbols[value] = len(self.symbols) + 1
        
    def save_output(self, filename='output.txt'):
        with open(filename, 'w') as file:
            file.write("Tabela de Tokens:\n")
            for token in self.tokens:
                file.write(f"{token[0]}: {token[1]}\n")
            
            file.write("\nTabela de Símbolos:\n")
            for symbol, index in self.symbols.items():
                file.write(f"{index}: {symbol}\n")
                
            if self.errors:
                file.write("\nErros:\n")
                for error in self.errors:
                    file.write(f"{error}\n")

# Exemplo de uso
source_code = '''
if (a == 5) {
    return a + b;
}
else {
    while (b < 10) {
        b = b + 1;
    }
}
'''

lexer = Lexer(source_code)
lexer.tokenize()
lexer.save_output()

print("Análise léxica concluída. Verifique o arquivo output.txt para os resultados.")
