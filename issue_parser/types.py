from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class CheckboxOption:
    label: str
    required: bool = False


@dataclass
class FormattedField:
    label: str
    type: str
    required: bool
    multiple: bool | None = None
    options: list[str | CheckboxOption] | None = None


Checkboxes = dict[str, list[str]]
ParsedValue = Checkboxes | list[str] | str | None
ParsedBody = dict[str, ParsedValue]
TemplateDict = dict[str, FormattedField]


def formatted_field_to_dict(field: FormattedField) -> dict[str, Any]:
    payload: dict[str, Any] = {
        'label': field.label,
        'type': field.type,
        'required': field.required,
    }

    if field.multiple is not None:
        payload['multiple'] = field.multiple

    if field.options is not None:
        normalized: list[Any] = []
        for option in field.options:
            if isinstance(option, CheckboxOption):
                normalized.append(
                    {'label': option.label, 'required': option.required}
                )
            else:
                normalized.append(option)
        payload['options'] = normalized

    return payload
