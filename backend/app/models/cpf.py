import re


class CPF:
    """
    Representa um CPF validado e formatado.
    Value Object para garantir a integridade dos dados no sistema AiBoi.
    """

    def __init__(self, valor: str):
        # Limpa o valor antes de qualquer operação
        valor_limpo = self._limpar(valor)
        
        if not self.validar(valor_limpo):
            raise ValueError("CPF inválido")
            
        self.valor = self.formatar(valor_limpo)

    def __str__(self) -> str:
        return self.valor

    def _limpar(self, valor: str) -> str:
        """Remove caracteres não numéricos."""
        return "".join(filter(str.isdigit, valor))

    def validar(self, cpf: str) -> bool:
        """Executa o algoritmo de validação de dígitos verificadores."""
        # CPF deve ter 11 dígitos e não pode ser uma sequência repetida
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        # Cálculo do primeiro dígito
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        dig1 = (soma * 10 % 11) % 10

        # Cálculo do segundo dígito
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        dig2 = (soma * 10 % 11) % 10

        return cpf[-2:] == f"{dig1}{dig2}"

    def formatar(self, cpf: str) -> str:
        """Aplica a máscara padrão: 000.000.000-00."""
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"