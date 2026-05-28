class DomainException(Exception):
    """Exceção base do domínio AiBoi."""


class EntityNotFoundError(DomainException):
    def __init__(self, entity_name: str, identifier: object):
        self.entity_name = entity_name
        self.identifier = identifier
        super().__init__(f"{entity_name} não encontrado(a): {identifier}")


class DuplicateEntityError(DomainException):
    def __init__(self, entity_name: str, field: str, value: object):
        self.entity_name = entity_name
        self.field = field
        self.value = value
        super().__init__(f"{entity_name} com {field}={value} já existe.")
