"""Tests for template renderer."""

import pytest

from drt.templates.renderer import render_template


def test_render_simple(sample_row: dict) -> None:
    result = render_template('{"text": "Hello {{ row.name }}"}', sample_row)
    assert result == '{"text": "Hello Alice"}'


def test_render_missing_variable(sample_row: dict) -> None:
    with pytest.raises(ValueError, match="Template error"):
        render_template("{{ row.missing_field }}", sample_row)
