"""Local TF-IDF embedding baseline."""

from __future__ import annotations

from pathlib import Path

import joblib
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfEmbeddingModel:
    """Transparent local TF-IDF text representation."""

    def __init__(self, vectorizer: TfidfVectorizer | None = None) -> None:
        self.vectorizer = vectorizer or TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            stop_words="english",
            norm="l2",
        )

    def fit_transform(self, texts: list[str]) -> sparse.csr_matrix:
        return self.vectorizer.fit_transform(texts).tocsr()

    def transform(self, texts: list[str]) -> sparse.csr_matrix:
        return self.vectorizer.transform(texts).tocsr()

    def save(self, path: Path) -> None:
        joblib.dump(self.vectorizer, path)

    @classmethod
    def load(cls, path: Path) -> TfidfEmbeddingModel:
        vectorizer = joblib.load(path)
        return cls(vectorizer=vectorizer)
