# Research Digest - Automated Paper Scanner

Automatically scan 200+ research papers from multiple sources every week and get the 15 most relevant ones delivered to your inbox. Uses AI to filter papers based on your specific research interests.

## What You Get

- Personalized weekly/biweekly digest of research papers
- AI-powered relevance filtering using Google Gemini
- Automatic scanning of NBER, ArXiv, CEPR, and custom RSS feeds
- Free to run (GitHub Actions + Gemini API)
- 10-minute setup

## Quick Start (10 minutes)

### Step 1: Fork This Repository

1. Click the "Fork" button at the top right of this page
2. This creates your own copy of the project

### Step 2: Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

**Cost:** Free tier includes 15 requests/minute, which is more than enough for this project.

### Step 3: Set Up Gmail App Password (for email delivery)

1. Go to your [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification if not already enabled
3. Search for "App passwords" or go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Select "Mail" and your device
5. Copy the 16-character password (no spaces)

### Step 4: Add Secrets to GitHub

1. In YOUR forked repository, go to: **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"** and add these three secrets:

   **Secret 1:**
   - Name: `GEMINI_API_KEY`
   - Value: Your Gemini API key from Step 2

   **Secret 2:**
   - Name: `GMAIL_ADDRESS`
   - Value: Your Gmail address (e.g., `your.email@gmail.com`)

   **Secret 3:**
   - Name: `GMAIL_APP_PASSWORD`
   - Value: The 16-character app password from Step 3

### Step 5: Customize Your Research Interests

1. Edit `config.yaml` in your repository:
   - Replace `your.email@example.com` with your actual email
   - Update `research_interests` with your specific research topics
   - The more specific you are, the better the filtering

Example:
```yaml
email: "jane.doe@university.edu"

research_interests: |
  I am a PhD student in Economics studying political economy and public finance.
  Focus areas:
  - Tax compliance and enforcement
  - Political institutions and corruption
  - Text analysis of political discourse
  - Methods: Event studies, RDD, text-as-data

  Prioritize:
  - Causal identification
  - Novel administrative datasets
  - Machine learning methods

  Skip:
  - Pure theory papers
  - Papers outside economics/political science
```

### Step 6: Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. Click **"I understand my workflows, enable them"**

### Step 7: Test It

1. Go to **Actions** → **Research Digest**
2. Click **"Run workflow"** → **"Run workflow"**
3. Wait 2-3 minutes
4. Check your email inbox (and spam folder)

**Done!** Your digest will now run automatically every Monday at 9 AM UTC.

## Customization

### Change Schedule

Edit `.github/workflows/digest.yml`:

```yaml
schedule:
  - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
  # - cron: '0 9 1,15 * *'  # 1st and 15th of each month (biweekly)
  # - cron: '0 18 * * 5'  # Every Friday at 6 PM UTC
```

[Cron expression help](https://crontab.guru/)

### Add More RSS Feeds

Edit `config.yaml`:

```yaml
feeds:
  - name: "NBER Working Papers"
    url: "https://www.nber.org/rss/new.xml"

  - name: "VoxEU"
    url: "https://voxeu.org/index.php/rss.xml"

  - name: "Your Favorite Blog"
    url: "https://blog.example.com/feed"
```

### Adjust Number of Papers

Edit `config.yaml`:

```yaml
max_papers: 20  # Get more papers per digest
```

## How It Works

1. **Fetch Papers:** Scans RSS feeds from NBER, ArXiv, CEPR, and other sources
2. **AI Filtering:** Uses Gemini to read abstracts and rank by relevance to your interests
3. **Email Delivery:** Sends top papers via Gmail with summary and links
4. **Automation:** Runs automatically on GitHub Actions (free)

## Cost Breakdown

- **GitHub Actions:** Free (2,000 minutes/month on free tier)
- **Gemini API:** Free tier (15 requests/min, plenty for this use)
- **Gmail SMTP:** Free
- **Total:** €0/month

## Troubleshooting

### No email received?
- Check spam/junk folder
- Verify email address in `config.yaml`
- Check Gmail app password is correct in GitHub Secrets
- Go to Actions tab and check workflow logs for errors

### Workflow fails?
- Verify all three secrets are set correctly:
  - `GEMINI_API_KEY`
  - `GMAIL_ADDRESS`
  - `GMAIL_APP_PASSWORD`
- Check Actions logs for specific error messages

### Empty digest or no relevant papers?
- Make your research interests more broad in `config.yaml`
- Add more RSS feeds
- Lower `min_relevance_score` in `config.yaml`

### Gmail says "Less secure app"?
- You must use an **App Password**, not your regular Gmail password
- Make sure 2-Step Verification is enabled first
- Follow Step 3 above carefully

## Privacy & Security

- Your API keys and passwords are stored as GitHub Secrets (encrypted)
- Your research interests stay in your forked repository
- No data is shared with third parties
- You control everything

## Advanced Options

### Use Preview Mode (No Email)

If you want to test without sending emails, set in `config.yaml`:

```yaml
email_method: "print"  # Just preview, don't send
```

Then check the Actions logs to see what would have been sent.

### Customize Email Template

Edit the `generate_html_email()` function in `digest.py` to change styling, add your logo, etc.

## Support

Questions or issues?

- Open an issue in this repository
- Email: stanislaw.zytynski@psemail.eu
- Check the Actions logs for debugging

## License

MIT License - Feel free to use and modify for your research.

## Credits

Created by [Stanislaw Zytynski](https://zytynski.github.io/) | [Paris School of Economics](https://www.parisschoolofeconomics.eu/)
