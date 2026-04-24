from app.enums.reproduction.reproduction_type import ReproductionType


class ReproductionService:
    """
    Service responsible for the business logic and validations
    of the reproduction module in the AiBoi system.
    """

    @staticmethod
    def validate_protocol_start(
        animal_active: bool,
        animal_gender: str,
        animal_status: str,
        protocol_type: ReproductionType,
        contracted_modules: list[str],
    ) -> bool:

        # 1. Validate if the animal is active in the farm
        if not animal_active:
            raise ValueError(
                "The animal must be active in the system to start a reproduction protocol."
            )

        # 2. Validate biological gender
        if animal_gender.upper() != "F":
            raise ValueError(
                "Only female animals can participate in reproduction protocols."
            )

        # 3. Validate biological status (Cannot be pregnant)
        # We check both English and Portuguese just in case the Animal module isn't fully translated yet
        invalid_statuses = ["PREGNANT", "PRENHE", "PARIDA"]
        if animal_status.upper() in invalid_statuses:
            raise ValueError(
                f"Cannot start protocol. Animal biological status is currently: {animal_status}."
            )

        # 4. Validate Financial/Contractual Modules
        # Monta Natural (Natural Breeding) is always free/available. The others require a purchased module.
        if protocol_type != ReproductionType.MONTA_NATURAL:
            # We use protocol_type.name to check the strict Enum key (e.g., "IATF", "TE", "FIV")
            if protocol_type.name not in contracted_modules:
                raise PermissionError(
                    f"Module '{protocol_type.value}' is not contracted by the farm."
                )

        # If it passes all validations, it's safe to proceed
        return True
