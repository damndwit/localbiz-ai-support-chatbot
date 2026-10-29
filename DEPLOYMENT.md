# Deploy LocalBiz AI Support Assistant

The demo can be hosted for free using [Streamlit Community Cloud](https://share.streamlit.io), connected to this public GitHub repository. No API keys or secrets are required.

## Deployment settings

| Setting | Value |
| --- | --- |
| Repository | `damndwit/localbiz-ai-support-chatbot` |
| Branch | `main` |
| Main file path | `app.py` |
| Python version | `3.12` (current Community Cloud default) |
| App URL | Choose an available short name, such as `localbiz-support-demo` |
| Secrets | Leave empty |

## Publish

1. Go to [Streamlit Community Cloud](https://share.streamlit.io) and sign in with your GitHub account.
2. If prompted, authorize Streamlit to access your **public** GitHub repositories.
3. Click **Create app** and then **Yup, I have an app**.
4. Choose the repository, branch, and main file path from the table above. Alternatively, paste this URL when offered:  
   `https://github.com/damndwit/localbiz-ai-support-chatbot/blob/main/app.py`
5. Optionally select a custom subdomain if available. Under **Advanced settings**, use Python 3.12 and leave secrets blank.
6. Click **Deploy**.
7. Test the live URL with:
   - `Are you open on Sundays?`
   - `Do you have vegan options?`
   - `Can I book a table?`
   - `Can you repair my spaceship?` (should decline to invent an answer)
8. Copy the **actual** `https://...streamlit.app` URL into the README, GitHub repository website field, and your portfolio after checking that it works.

**Important:** Do not guess the live URL. Streamlit might add a suffix if you do not choose an available subdomain.

## Troubleshooting

- **ModuleNotFoundError:** Check that `requirements.txt` is in the root of the repository, and look at the deployment logs.
- **FileNotFoundError:** The app expects `business.json` and `data/faqs.csv` next to `app.py`; keep that relative structure.
- **Build fails on Python dependencies:** Redeploy with Python 3.12 from the Advanced settings screen and review install logs.
- **GitHub repository not in picker:** Paste the GitHub file URL from step 4, or grant Streamlit access to public repositories.
- **Changes not showing:** Check that you deployed branch `main`. New commits generally trigger redeployment.

This is a learning demonstration using a fictional café. It is not configured to receive real customers, payment information, or private business data.

Official instructions: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
