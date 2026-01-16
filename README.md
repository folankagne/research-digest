# Research Digest

AI-filtered research papers delivered to your inbox weekly. Free and automated.

## Setup (5 minutes)

**1. Fork this repo**

**2. Get API keys**
- [Gemini API key](https://aistudio.google.com/apikey) (free)
- [Gmail App Password](https://myaccount.google.com/apppasswords) (needs 2FA enabled)

**3. Add secrets**

Go to **Settings → Secrets and variables → Actions**, add:
- `GEMINI_API_KEY` - your Gemini key
- `GMAIL_ADDRESS` - your Gmail
- `GMAIL_APP_PASSWORD` - 16-char password

**4. Edit config.yaml**
- Add your email
- Describe your research interests (be specific)
- Add/remove RSS feeds

**5. Enable & test**
- **Actions** tab → Enable workflows
- Run manually to test
- Check your email

Done. Runs weekly on Mondays.

## Troubleshooting

**No email?** Check spam, verify secrets are set correctly

**Wrong papers?** Be more specific in config.yaml research interests

**Questions?** Open an issue or check Actions logs

---

Made by [Stanislaw Zytynski](https://zytynski.github.io/) | MIT License
