# LocalBiz AI Support Assistant

A customizable customer-service chatbot for local businesses, built using **Python, Streamlit, and scikit-learn**. The example business is a fictional café, but the business name, greeting, and approved FAQ answers are easy to replace.

**Status:** Public demo deployed. The owner confirmed successful local operation and five live checks: page loading, opening-hours response, vegan-options response, unknown-question fallback, and mobile presentation. Automated test execution remains unverified.

### Try the demo

**[Open the live chatbot](https://localbiz-support-demo-dwit.streamlit.app/)** · [Source code](https://github.com/dwitdev/localbiz-ai-support-chatbot)

This public demo uses a **fictional café** and example business policies. No customer records or real business integrations are involved.

[**Live demo**](https://localbiz-support-demo-dwit.streamlit.app/) · [**Source**](https://github.com/dwitdev/localbiz-ai-support-chatbot) · [**Automated test workflow**](https://github.com/dwitdev/localbiz-ai-support-chatbot/actions/workflows/tests.yml)

## Screenshots

Screenshots are being collected from the deployed application. For a real screenshot, open the live demo, ask about Sunday hours, and use **Win + Shift + S** on Windows to capture the visible conversation. Save it as `screenshots/chat-demo.png` and upload it through GitHub's **Add file → Upload files**. A second screenshot showing the fallback and one on mobile are useful.

Do not upload screenshots containing private or real customer data. The demo uses a fictional café.

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
git clone https://github.com/dwitdev/localbiz-ai-support-chatbot.git
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

## Quality checks

- `tests/test_bot.py` tests normalization, matching, fallbacks, CSV validation, and threshold handling.
- `tests/test_demo.py` checks all published FAQ questions, alternative phrasings, popular questions, and unknown-message behavior.
- `.github/workflows/tests.yml` is configured to run both test files when code is pushed or a pull request is opened. **Do not assume tests have passed until the Actions page shows a green check.**
- This is **NLP-based FAQ retrieval**, not a generative LLM service or a production customer service platform.

## Learning references

I reviewed these MIT-licensed projects for design inspiration, but implemented this chatbot separately:

- [rajanv29/customer-service-chatbot](https://github.com/rajanv29/customer-service-chatbot)
- [madhushalini06785/Customer-Support-FAQ-Chatbot](https://github.com/madhushalini06785/Customer-Support-FAQ-Chatbot)

## Next steps

- [x] Run the app locally and confirm key questions work (developer confirmed)
- [ ] Confirm the automated unit and integration tests pass on GitHub Actions
- [ ] Add genuine screenshots from the deployed app
- [x] Deploy a demo URL on Streamlit Community Cloud ([open app](https://localbiz-support-demo-dwit.streamlit.app/))
- [x] Confirm five live demo checks (owner-reported, October 29, 2026)
- [ ] Extend to multiple businesses and consider optional local LLM integration

**Created by [Dwit Patel](https://github.com/dwitdev).**
