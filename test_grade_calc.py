import io
import random
from unittest import mock

import pytest
from hypothesis import given, example, strategies as st


from gradesCalc import final_grade, check_strings


@pytest.mark.parametrize(
    ("expected", "s1", "s2"),
    (
            (True, "aabbcc", "abcabc"),
            (True, "caba", "abcabc"),
            (False, "aaa", "abcabc"),
            (True, "naanb", "baNaNa"),
            (False, "ananas", "baNaNa"),
            (False, "bannn", "baNaNa"),
    )
)
def test_check_strings(expected, s1, s2):
    assert check_strings(s1, s2) is expected


@given(st.text())
@example("")
def test_check_strings_same_value(text):
    assert check_strings(text, text)


@given(st.integers(min_value=0, max_value=100), st.text())
def test_check_strings_some_removed_letters_reversed(count, text):
    substring = "".join(random.sample(text, count * len(text) // 100))
    assert check_strings(substring, text)


@given(st.integers(min_value=0, max_value=100), st.text())
def test_check_strings_some_removed_letters(count, text):
    substring = "".join(random.sample(text, count * len(text) // 100))
    assert not check_strings(text, substring) or len(substring) == len(text)


class UnclosableStringIO(io.StringIO):
    def close(self) -> None:
        # do not close the fake file to allow inspection after close
        pass


@pytest.mark.parametrize(
    ("expected_result", "raw_input", "expected_output"),
    (
            (60, "39401830,  Zeev Jabotinsky, 2 ,     78\n29441133 ,Joseph Trumpeldor,     1 , 99", "29441133, 99, 66\n39401830, 78, 54\n"),
    )
)
def test_final_grade(expected_result, raw_input, expected_output):
    input_file = UnclosableStringIO(raw_input)
    output_file = UnclosableStringIO()

    def patched_open(path: str, mode: str):
        return {"input": input_file, "output": output_file}[path]

    with mock.patch("builtins.open", patched_open):
        assert expected_result == final_grade("input", "output")
    assert output_file.getvalue() == expected_output
