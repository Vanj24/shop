from enum import Enum


class CurrencyEnum(Enum):
    USD = "US Dollars"
    PHP = "Philippine Peso"


class StatusEnum(Enum):
    ACTIVE = "Active"
    TERMINATED = "Terminated"
