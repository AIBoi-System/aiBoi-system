import pytest

from app.shared.domain.exceptions import ValidationException
from app.shared.domain.registration import Registration
from app.shared.domain.value_objects import (
    BrazilianAddress,
    BrazilianPhone,
    CPF,
    EmailAddress,
)


def valid_address(**changes) -> BrazilianAddress:
    data = {
        "zip_code": "01001-000",
        "state": "sp",
        "neighborhood": " Sé ",
        "street_name": " Praça da Sé ",
        "number": " 100 ",
        "complement": " Lado ímpar ",
    }
    data.update(changes)
    return BrazilianAddress(**data)


@pytest.mark.parametrize("value", ["52998224725", "529.982.247-25"])
def test_cpf_accepts_valid_digits_and_mask(value):
    cpf = CPF(value)

    assert cpf.value == "52998224725"
    assert cpf.valor == "529.982.247-25"
    assert str(cpf) == "529.982.247-25"
    assert CPF.validar(value)


@pytest.mark.parametrize(
    "value",
    ["", "123", "11111111111", "52998224724", "12345678900"],
)
def test_cpf_rejects_invalid_length_sequences_and_check_digits(value):
    with pytest.raises(ValidationException):
        CPF(value)


def test_email_and_phone_are_normalized_value_objects():
    assert EmailAddress(" Owner@Example.COM ").value == "owner@example.com"
    assert BrazilianPhone("(11) 99876-5432").value == "11998765432"


@pytest.mark.parametrize("value", ["invalid", "owner@localhost", "@example.com"])
def test_email_rejects_invalid_addresses(value):
    with pytest.raises(ValidationException):
        EmailAddress(value)


@pytest.mark.parametrize("value", ["123", "00998765432", "20998765432"])
def test_phone_rejects_invalid_length_or_area_code(value):
    with pytest.raises(ValidationException):
        BrazilianPhone(value)


def test_brazilian_address_normalizes_cep_uf_and_required_fields():
    address = valid_address()

    assert address.zip_code == "01001000"
    assert address.state == "SP"
    assert address.neighborhood == "Sé"
    assert address.street_name == "Praça da Sé"
    assert address.number == "100"
    assert address.complement == "Lado ímpar"


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"zip_code": "0100100"}, "CEP"),
        ({"state": "AA"}, "UF"),
        ({"neighborhood": " "}, "Bairro"),
        ({"street_name": " "}, "Logradouro"),
        ({"number": " "}, "Número"),
    ],
)
def test_brazilian_address_rejects_invalid_fields(changes, message):
    with pytest.raises(ValidationException, match=message):
        valid_address(**changes)


def test_registration_requires_both_contacts_before_password():
    registration = Registration.start(
        email="owner@example.com",
        phone="11998765432",
    )

    with pytest.raises(ValidationException, match="E-mail e telefone"):
        registration.set_password_hash("argon2-hash")

    registration.verify_email("OWNER@example.com")
    with pytest.raises(ValidationException, match="E-mail e telefone"):
        registration.set_password_hash("argon2-hash")

    registration.verify_phone("(11) 99876-5432")
    registration.set_password_hash("argon2-hash")


def test_registration_rejects_verification_for_another_destination():
    registration = Registration.start(
        email="owner@example.com",
        phone="11998765432",
    )

    with pytest.raises(ValidationException, match="não corresponde"):
        registration.verify_email("attacker@example.com")
    with pytest.raises(ValidationException, match="não corresponde"):
        registration.verify_phone("21998765432")


def test_registration_completion_returns_immutable_persistence_contract():
    registration = Registration.start(
        email=" Owner@Example.COM ",
        phone="(11) 99876-5432",
    )
    registration.set_profile(
        name=" Fazenda Silva ",
        cpf="529.982.247-25",
        address=valid_address(),
    )

    with pytest.raises(ValidationException, match="E-mail e telefone"):
        registration.complete()

    registration.verify_email("owner@example.com")
    registration.verify_phone("11998765432")
    with pytest.raises(ValidationException, match="Senha"):
        registration.complete()

    registration.set_password_hash("argon2-hash")
    completed = registration.complete()

    assert completed.name == "Fazenda Silva"
    assert completed.email == "owner@example.com"
    assert completed.phone == "11998765432"
    assert completed.cpf == "52998224725"
    assert completed.address.state == "SP"
    assert completed.password_hash == "argon2-hash"
    assert "argon2-hash" not in repr(completed)
