import re
from datetime import date, datetime

from pydantic import BeforeValidator
from pydantic_core import core_schema

EmptyToNone = BeforeValidator(lambda v: None if v in ("", "None") else v)

DATE_DEFIS_RE = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")

class DefisYearMonthOrDateOrNone(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema()
        )

    @classmethod
    def validate(cls, value):
        if value in ("", "None", None):
            return None

        if not isinstance(value, str):
            raise TypeError("must be a string or None")

        if not DATE_DEFIS_RE.match(value):
            raise ValueError("must be YYYY-MM or YYYY-MM-DD")

        parts = value.split("-")
        if len(parts) == 3:
            try:
                date.fromisoformat(value)
            except ValueError as e:
                raise ValueError(f"invalid or non‑existent date: {value}") from e
        elif len(parts) == 2:
            month = int(parts[1])
            if not (1 <= month <= 12):
                raise ValueError(f"invalid month in YYYY‑MM: {value}")

        return value


DATE_DOT_RE = re.compile(r"^\d{2}.\d{2}.\d{4}$")

class DotDateMonthYear(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema()
        )

    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise TypeError("must be a string")

        if not DATE_DOT_RE.match(value):
            raise ValueError("must be DD.MM.YYYY")

        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError as e:
            raise ValueError(f"invalid or non‑existent date: {value}") from e

        return value
