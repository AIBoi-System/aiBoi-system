from pydantic import Field, field_validator
from .user_base import UserBaseSchema

class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=6)

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, value: str) -> str:
        # 1. Remove qualquer caractere que não seja número
        cleaned = "".join(filter(str.isdigit, str(value)))
        
        # 2. Verifica se tem 11 dígitos antes de mandar para o Service
        if len(cleaned) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos numéricos")
            
        # 3. Retorna os números limpos
        return cleaned








































