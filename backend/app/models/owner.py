from typing import List

from app.models.user import User
from app.models.address import Address
from app.models.property import Property
from backend.app.enums.owner.owner_subscription_status import OwnerSubscriptionStatus
from cpf import CPF


class Owner(User):

    def __init__(
        self,
        id_user: int,
        name: str,
        email: str,
        password: str,
        phone: str,
        account_status: str,
        address: Address,
        cpf: CPF,
        subscription_status: OwnerSubscriptionStatus
    ):
        super().__init__(
            id_user,
            name,
            email,
            password,
            phone,
            account_status,
            address,
            cpf
        )

        self.subscription_status = subscription_status
        self.properties: List[Property] = []