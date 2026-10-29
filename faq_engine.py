"""FAQ matching engine for the LocalBiz support demo.

This is a retrieval chatbot: it selects approved answers from business FAQ data.
It is not a generative language model and does not invent business policies.
"""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True)
class FAQ:
    category: str
    question: str
    answer: str
    alternatives: tuple[str, ...] = ()


@dataclass(frozen=True)
class Reply:
    text: str
    category: str | None = None
    confidence: float = 0.0
    matched_question: str | None = None
    is_fallback: bool = False


def normalize(text: str) -> str:
    """Normalize whitespace and basic punctuation without changing meaning."""
    text = re.sub(r"[^\w\s]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def load_faqs(csv_path: str | Path) -> list[FAQ]:
    """Load approved business answers from a CSV file.

    Columns: category, question, answer, alternatives.
    Multiple alternatives are separated with the | character.
    """
    records: list[FAQ] = []
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"category", "question", "answer", "alternatives"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("FAQ CSV must include: category, question, answer, alternatives.")
        for line_number, row in enumerate(reader, start=2):
            category = (row["category"] or "").strip()
            question = (row["question"] or "").strip()
            answer = (row["answer"] or "").strip()
            if not category or not question or not answer:
                raise ValueError(f"Missing required FAQ data on CSV line {line_number}.")
            alternatives = tuple(
                item.strip() for item in (row["alternatives"] or "").split("|")
                if item.strip()
            )
            records.append(FAQ(category, question, answer, alternatives))
    if not records:
        raise ValueError("FAQ CSV has no question-and-answer rows.")
    return records


class FAQBot:
    """Match a customer's message to an approved FAQ with word-based TF-IDF."""

    def __init__(self, faqs: list[FAQ], threshold: float = 0.39):
        if not faqs:
            raise ValueError("Provide at least one FAQ.")
        if not 0 <= threshold <= 1:
            raise ValueError("threshold must be between 0 and 1")

        self.faqs = faqs
        self.threshold = threshold
        self.sample_to_faq: list[int] = []
        samples: list[str] = []
        for index, faq in enumerate(faqs):
            for phrase in (faq.question, *faq.alternatives):
                clean = normalize(phrase)
                if clean:
                    samples.append(clean)
                    self.sample_to_faq.append(index)
        if not samples:
            raise ValueError("No usable FAQ questions found.")

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
        self.matrix = self.vectorizer.fit_transform(samples)

    def answer(self, message: str) -> Reply:
        clean = normalize(message)
        if not clean:
            return Reply("Type a question and I'll look for an answer in our FAQ.", is_fallback=True)

        if clean in {"hi", "hello", "hey", "good morning", "good afternoon", "good evening"}:
            return Reply("Hi there! Ask me about our hours, menu, orders, or other café questions.")
        if clean in {"bye", "goodbye", "thanks", "thank you"}:
            return Reply("Happy to help! Have a great day.")

        vector = self.vectorizer.transform([clean])
        scores = cosine_similarity(vector, self.matrix)[0]
        best_index = int(scores.argmax())
        score = float(scores[best_index])
        if score < self.threshold:
            return Reply(
                "I'm not sure about that, and I don't want to give you incorrect information. "
                "Please contact the business directly for help.",
                confidence=score,
                is_fallback=True,
            )
        faq = self.faqs[self.sample_to_faq[best_index]]
        return Reply(
            text=faq.answer,
            category=faq.category,
            confidence=score,
            matched_question=faq.question,
        )
