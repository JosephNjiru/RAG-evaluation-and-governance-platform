from pathlib import Path

import pandas as pd


def test_improved_rag_answers_preserve_schema_when_present() -> None:
    path = Path("outputs/answers/improved_rag_answers.parquet")
    if not path.exists():
        return
    answers = pd.read_parquet(path)
    assert {"question_id", "answer_text", "citations", "refusal_flag"}.issubset(answers.columns)
    assert len(answers) == 60
