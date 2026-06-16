class DomainError(Exception):
    """Base class for domain errors."""


class SecurityReportNotFoundError(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"SecurityReport not found: {id}")
        self.id = id


class InvalidInputError(DomainError):
    pass
