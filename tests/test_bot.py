"""Tests for the customer-service FAQ matching engine."""
import tempfile
import unittest
from pathlib import Path

from faq_engine import FAQ, FAQBot, load_faqs, normalize


class FAQBotTests(unittest.TestCase):
    def setUp(self):
        self.bot = FAQBot([
            FAQ("Hours", "Are you open on Sundays?", "Yes, 9 AM to 3 PM.",
                ("What are your Sunday hours?",)),
            FAQ("Menu", "Do you have vegan options?", "Yes, a few.",
                ("Do you serve plant based food?",)),
        ])

    def test_normalization(self):
        self.assertEqual(normalize("  HELLO,   World!! "), "hello world")

    def test_exact_question(self):
        reply = self.bot.answer("Are you open on Sundays?")
        self.assertEqual(reply.text, "Yes, 9 AM to 3 PM.")
        self.assertFalse(reply.is_fallback)

    def test_alias_question(self):
        reply = self.bot.answer("What are your Sunday hours?")
        self.assertEqual(reply.category, "Hours")

    def test_unrelated_question_falls_back(self):
        reply = self.bot.answer("Can you repair my spaceship engine?")
        self.assertTrue(reply.is_fallback)
        self.assertIsNone(reply.matched_question)

    def test_empty_question(self):
        self.assertTrue(self.bot.answer("  ").is_fallback)

    def test_greeting(self):
        self.assertIn("Hi there", self.bot.answer("Hi!").text)

    def test_csv_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            csv_file = Path(directory) / "faqs.csv"
            csv_file.write_text(
                "category,question,answer,alternatives\n"
                "Hours,Are you open today?,Yes,Are you open now?|Opening hours\n",
                encoding="utf-8",
            )
            faq = load_faqs(csv_file)
            self.assertEqual(len(faq), 1)
            self.assertEqual(faq[0].alternatives[0], "Are you open now?")

    def test_bad_csv_columns(self):
        with tempfile.TemporaryDirectory() as directory:
            csv_file = Path(directory) / "bad.csv"
            csv_file.write_text("question,answer\nWhat time?,Now\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_faqs(csv_file)

    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            FAQBot([FAQ("A", "test", "answer")], threshold=2)


if __name__ == "__main__":
    unittest.main()
