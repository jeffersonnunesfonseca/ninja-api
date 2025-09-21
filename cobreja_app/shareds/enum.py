from enum import Enum


class ChannelEnum(str, Enum):
    SMS = "SMS"
    EMAIL = "EMAIL"
    WHATSAPP = "WHATSAPP"


class RuleStatusEnum(str, Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class EnvrionmentEnum(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
