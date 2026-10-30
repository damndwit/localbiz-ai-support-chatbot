"""End-to-end checks of the fictional business knowledge base.

These assertions verify that published demo content matches what the bot returns.
They do not establish accuracy for an actual business or measure model reliability.
"""
import json
import unittest
from pathlib import Path

from faq_engine import FAQBot, load_faqs


ROOT = Path(__file__).resolve().parents[1]


class PublishedDemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.faqs = load_faqs(ROOT / "data" / "faqs.csv")
        cls.bot = FAQBot(cls.faqs)
        cls.config = json.loads((ROOT / "business.json").read_text(encoding="utf-8"))

    def test_sample_data_is_complete(self):
        self.assertEqual(len(self.faqs), 19)
        self.assertEqual(self.config["business_name"], "Maple Street Café")
        self.assertEqual(len(self.config["quick_questions"]), 6)

    def test_all_canonical_questions_are_answerable(self):
        for faq in self.faqs:
            with self.subTest(category=faq.category, question=faq.question):
                response = self.bot.answer(faq.question)
                self.assertEqual(response.text, faq.answer)
                self.assertFalse(response.is_fallback)

    def test_all_declared_aliases_are_answerable(self):
        for faq in self.faqs:
            for alias in faq.alternatives:
                with self.subTest(alias=alias):
                    response = self.bot.answer(alias)
                    self.assertEqual(response.text, faq.answer)
                    self.assertFalse(response.is_fallback)

    def test_demo_quick_questions_match_expected_faqs(self):
        for question in self.config["quick_questions"]:
            with self.subTest(question=question):
                response = self.bot.answer(question)
                self.assertFalse(response.is_fallback)
                self.assertIsNotNone(response.matched_question)

    def test_unknown_question_does_not_invent_business_policy(self):
        response = self.bot.answer("Can you repair the engine on my spaceship?")
        self.assertTrue(response.is_fallback)
        self.assertIsNone(response.matched_question)
        self.assertIn("not sure", response.text.lower())

    def test_empty_question_is_handled(self):
        self.assertTrue(self.bot.answer("   ").is_fallback)


if __name__ == "__main__":
    unittest.main()
