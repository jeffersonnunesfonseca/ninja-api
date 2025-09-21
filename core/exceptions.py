class NotAllowedInNonDevelopmentEnvironmentError(Exception):
    def __init__(self):
        message = "Not allowed in non-development environment"

        super().__init__(message)


class TenantNotFoundError(Exception):
    def __init__(self, token: str):
        message = f"Tenant with token '{token}' not found"
        super().__init__(message)
