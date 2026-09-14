from enum import StrEnum


class ErrorEnum(StrEnum):
    INTERNAL = "internal"
    NOT_FOUND = "not_found"
    CAMPAIGN_NOT_FOUND = "campaign_not_found"

    @property
    def message(self) -> str:
        return " ".join(self.value.split("_")).title()
