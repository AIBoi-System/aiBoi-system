import re

class CPF:
    """
    Representa um CPF validado e formatado.
    Value Object para garantir a integridade dos dados no sistema AiBoi.
    """

    def __init__(self, valor: str):
        # 1. Garante que recebemos uma string e limpamos caracteres extras
        valor_str = str(valor)
        valor_limpo = self._limpar(valor_str)
        
        # 2. Valida o cálculo matemático
        if not self.validar(valor_limpo):
            raise ValueError("CPF inválido")
            
        # 3. Guarda o valor formatado com máscara (000.000.000-00)
        self.valor = self.formatar(valor_limpo)

    def __str__(self) -> str:
        return self.valor

    def _limpar(self, valor: str) -> str:
        """Remove caracteres não numéricos."""
        return "".join(filter(str.isdigit, valor))

    def validar(self, cpf: str) -> bool:
        """Executa o algoritmo oficial de validação de dígitos verificadores."""
        # Verifica se tem 11 dígitos ou se é uma sequência repetida (ex: 11111111111)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        # Cálculo do primeiro dígito (dig1)
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        
        resto = (soma * 10) % 11
        dig1 = 0 if resto >= 10 else resto

        # Cálculo do segundo dígito (dig2)
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        
        resto = (soma * 10) % 11
        dig2 = 0 if resto >= 10 else resto

        # Comparação final: verifica se os dígitos calculados batem com os informados
        return int(cpf[9]) == dig1 and int(cpf[10]) == dig2

    def formatar(self, cpf: str) -> str:
        """Aplica a máscara padrão: 000.000.000-00."""
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"









































