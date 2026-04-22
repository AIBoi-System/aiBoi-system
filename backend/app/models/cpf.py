class CPF:

    def __init__(self, valor: str):
        if not self.validar(valor):
            raise ValueError("CPF inválido")
        
        self.valor = self.formatar(valor)

    def __str__(self):
        return self.valor   

    def validar(self, cpf: str) -> bool:
        cpf = ''.join(filter(str.isdigit, cpf))

        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        # Primeiro dígito
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        dig1 = (soma * 10 % 11) % 10

        # Segundo dígito
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        dig2 = (soma * 10 % 11) % 10

        return cpf[-2:] == f"{dig1}{dig2}"

    def formatar(self, cpf: str) -> str:
        cpf = ''.join(filter(str.isdigit, cpf))
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"