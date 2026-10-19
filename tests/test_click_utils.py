"""Regression tests for the CLIcK task's multiple-choice prompts."""

import pytest

from lm_eval.tasks.click.click_cul import utils as click_cul_utils
from lm_eval.tasks.click.click_lang import utils as click_lang_utils


@pytest.mark.parametrize(
    "click_utils",
    [click_cul_utils, click_lang_utils],
    ids=["click_cul", "click_lang"],
)
@pytest.mark.parametrize("paragraph", ["A short context", ""])
def test_click_five_option_prompt_includes_option_e(click_utils, paragraph):
    doc = {
        "id": "CSAT_geography_07_3",
        "paragraph": paragraph,
        "question": "Which statement is correct?",
        "choices": [
            "Option A",
            "Option B",
            "Option C",
            "Option D",
            "Option E",
        ],
        "answer": "Option E",
    }

    prompt = click_utils.get_context(doc)

    assert "A, B, C, D, E 중에" in prompt
    assert "E: Option E" in prompt
    assert click_utils.get_choices(doc) == ["A", "B", "C", "D", "E"]
    assert click_utils.get_target(doc) == "E"


@pytest.mark.parametrize(
    "click_utils",
    [click_cul_utils, click_lang_utils],
    ids=["click_cul", "click_lang"],
)
@pytest.mark.parametrize("paragraph", ["A short context", ""])
def test_click_four_option_prompt_remains_unchanged(click_utils, paragraph):
    doc = {
        "id": "Kedu_16_01",
        "paragraph": paragraph,
        "question": "Which statement is correct?",
        "choices": ["Paris", "Rome", "Oslo", "Lima"],
        "answer": "Rome",
    }

    if paragraph:
        expected = (
            "주어진 맥락을 천천히 읽고, 질문에 대한 적절한 정답을 A, B, C, D 중에 "
            "골라 알파벳 하나로 답하시오.\n\n"
            f"맥락: {paragraph}\n질문: {doc['question']}\n보기:\n"
            "A:Paris, B: Rome, C: Oslo, D: Lima\n정답:"
        )
    else:
        expected = (
            "주어진 질문을 천천히 읽고, 적절한 정답을 A, B, C, D 중에 "
            "골라 알파벳 하나로 답하시오.\n\n"
            f"질문: {doc['question']}\n보기:\n"
            "A:Paris, B: Rome, C: Oslo, D: Lima\n정답:"
        )

    assert click_utils.get_context(doc) == expected
    assert click_utils.get_choices(doc) == ["A", "B", "C", "D"]
    assert click_utils.get_target(doc) == "B"
