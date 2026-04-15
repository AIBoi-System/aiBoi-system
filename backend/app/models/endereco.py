class Endereco:

    def __init__(
        self,
        id_endereco: int,
        cep: str,
        estado: str,
        bairro: str,
        nome_rua: str,
        num: str,
        complemento: str
    ):
        self.id_endereco = id_endereco
        self.cep = cep
        self.estado = estado
        self.bairro = bairro
        self.nome_rua = nome_rua
        self.num = num
        self.complemento = complemento