# LocalBiz AI Support Assistant

A customizable customer-service chatbot for local businesses, built using **Python, Streamlit, and scikit-learn**. The example business is a fictional café, but the business name, greeting, and approved FAQ answers are easy to replace.

**Status:** Initial prototype published. Local testing and live deployment still need verification.

## Features

- Natural-language FAQ matching with TF-IDF and cosine similarity
- Alternative ways to phrase the same customer question
- Chat history and clickable suggested questions
- Confidence threshold and fallback for unanswered questions
- Optional explanation of which FAQ was matched
- Free local operation without an API key or paid LLM

**How the AI works:** This is an NLP retrieval chatbot, **not** a generative large-language-model chatbot. It chooses an approved FAQ response instead of inventing answers.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in the downloaded project folder (download as ZIP from GitHub, or clone it):

```bash
git clone https://github.com/damndwit/localbiz-ai-support-chatbot.git
cd localbiz-ai-support-chatbot
```

3. Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Start the application:

```bash
python -m streamlit run app.py
```

5. Open http://localhost:8501 if your browser doesn't open automatically.

On Windows, use `py` instead of `python` if necessary.

To run the automated tests:

```bash
python -m unittest discover -s tests -v
```

## Customize it

- Edit `business.json` for the business name, tagline, and popular questions.
- Edit `data/faqs.csv` to add factual answers approved by the business. Its columns are `category`, `question`, `answer`, and `alternatives`. Separate alternative questions with `|`.
- Edit `app.py` to change the layout or color scheme.
- Edit `faq_engine.py` to study or adjust how similarity matching works.

## Project structure

```text
app.py              Streamlit chat interface
faq_engine.py       FAQ matching logic
business.json       Fictional café settings
data/faqs.csv       Sample business knowledge base
tests/test_bot.py   Basic automated tests
requirements.txt    Dependencies
.gitignore          Local file exclusions
LICENSE             MIT license
```

## Safety and limitations

All sample data describes a fictional café. This prototype cannot place orders, take reservations, access accounts, issue refunds, or communicate with an actual business. It is not production-ready: it has no authentication, staff dashboard, or persistent customer ticket management. For commercial deployment, business owners must approve their FAQ content and review hosting, security, privacy, and a human escalation path. Never add passwords, real customer data, or API keys to this repository.

## Learning references

I reviewed these MIT-licensed projects for design inspiration, but implemented this chatbot separately:

- [rajanv29/customer-service-chatbot](https://github.com/rajanv29/customer-service-chatbot)
- [madhushalini06785/Customer-Support-FAQ-Chatbot](https://github.com/madhushalini06785/Customer-Support-FAQ-Chatbot)

## Next steps

- [ ] Run the app locally and confirm key questions work
- [ ] Run the unit tests
- [ ] Add screenshots from the real app
- [ ] Deploy a public demo using Streamlit Community Cloud
- [ ] Extend to multiple businesses and consider optional local LLM integration

**Created by [Dwit Patel](https://github.com/damndwit).**
