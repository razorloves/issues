import json
from pathlib import Path

import pytest

from issue_parser import parse_issue, parse_template
from issue_parser.types import formatted_field_to_dict

FIXTURES = Path('tests/fixtures')


def _read(path: str) -> str:
    return (FIXTURES / path).read_text(encoding='utf-8')


def _read_json(path: str):
    return json.loads(_read(path))


def _normalize_issue_result(result):
    normalized = {}
    for key, value in result.items():
        normalized[key] = value
    return normalized


def _normalize_template_result(result):
    return {
        key: formatted_field_to_dict(value) for key, value in result.items()
    }


def test_parses_blank_issue() -> None:
    result = parse_issue(_read('blank/issue.md'), _read('blank/template.yml'))
    assert _normalize_issue_result(result) == _read_json(
        'blank/parsed-issue.json'
    )


def test_parses_example_request() -> None:
    result = parse_issue(
        _read('example/issue.md'), _read('example/template.yml')
    )
    assert _normalize_issue_result(result) == _read_json(
        'example/parsed-issue.json'
    )


def test_parses_invalid_issue() -> None:
    result = parse_issue(
        _read('invalid/issue.md'), _read('invalid/template.yml')
    )
    assert _normalize_issue_result(result) == _read_json(
        'invalid/parsed-issue.json'
    )


def test_parses_issue_with_missing_data() -> None:
    result = parse_issue(
        _read('missing/issue.md'), _read('missing/template.yml')
    )
    assert _normalize_issue_result(result) == _read_json(
        'missing/parsed-issue.json'
    )


def test_parses_issue_with_missing_headers() -> None:
    result = parse_issue(_read('header/issue.md'), _read('header/template.yml'))
    assert _normalize_issue_result(result) == _read_json(
        'header/parsed-issue.json'
    )


def test_parses_issue_without_ids() -> None:
    result = parse_issue(_read('no-ids/issue.md'), _read('no-ids/template.yml'))
    assert _normalize_issue_result(result) == _read_json(
        'no-ids/parsed-issue.json'
    )


def test_parses_issue_without_template() -> None:
    result = parse_issue(
        _read('no-template/issue.md'), options={'slugify': True}
    )
    assert _normalize_issue_result(result) == _read_json(
        'no-template/parsed-issue.json'
    )


def test_parses_issue_with_extra_fields_template() -> None:
    result = parse_issue(_read('extra/issue.md'), _read('extra/template.yml'))
    assert _normalize_issue_result(result) == _read_json(
        'extra/parsed-issue-template.json'
    )


def test_parses_issue_with_extra_fields_without_template_slugified() -> None:
    result = parse_issue(_read('extra/issue.md'), options={'slugify': True})
    assert _normalize_issue_result(result) == _read_json(
        'extra/parsed-issue-no-template.json'
    )


def test_parse_template_with_ids() -> None:
    result = parse_template(_read('example/template.yml'))
    assert _normalize_template_result(result) == _read_json(
        'example/parsed-template.json'
    )


def test_parse_template_without_ids() -> None:
    result = parse_template(_read('no-ids/template.yml'))
    assert _normalize_template_result(result) == _read_json(
        'no-ids/parsed-template.json'
    )


def test_parse_template_throws_when_not_yaml_object() -> None:
    with pytest.raises(
        ValueError, match='Issue template could not be parsed into an object.'
    ):
        parse_template('invalid')


def test_parse_template_throws_without_body_array() -> None:
    with pytest.raises(
        ValueError, match='Issue template is missing a body array property.'
    ):
        parse_template('title: Test')


def test_parse_template_empty_when_missing() -> None:
    assert parse_template() == {}
