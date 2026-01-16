#!/usr/bin/env python3
"""
Research Digest Generator
Scans RSS feeds and generates personalized research digest using Gemini AI
"""

import os
import yaml
import feedparser
import google.generativeai as genai
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def load_config():
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def fetch_papers(feeds):
    """Fetch papers from RSS feeds"""
    papers = []
    for feed_info in feeds:
        print(f"Fetching from {feed_info['name']}...")
        feed = feedparser.parse(feed_info['url'])

        for entry in feed.entries[:50]:  # Limit to 50 recent papers per feed
            papers.append({
                'title': entry.get('title', ''),
                'summary': entry.get('summary', ''),
                'link': entry.get('link', ''),
                'source': feed_info['name']
            })

    return papers


def filter_and_rank_papers(papers, research_interests, max_papers):
    """Use Gemini to filter and rank papers by relevance"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
You are a research assistant. Given the following research interests:

{research_interests}

Review these papers and return the TOP {max_papers} most relevant ones.
For each relevant paper, provide:
1. Title
2. One sentence explaining why it's relevant
3. Key contribution in one sentence

Papers to review:
{chr(10).join([f"- {p['title']} ({p['source']}): {p['summary'][:200]}..." for p in papers[:100]])}

Format your response as:
## Paper Title (Source)
**Why relevant:** ...
**Key contribution:** ...
[Link]

Only include the most relevant papers.
"""

    response = model.generate_content(prompt)
    return response.text


def generate_html_email(digest_content, config):
    """Generate HTML email from digest content"""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            h1 {{ color: #0060df; }}
            h2 {{ color: #003d99; border-bottom: 2px solid #e0e0e0; padding-bottom: 5px; }}
            .paper {{ margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }}
            .meta {{ color: #666; font-size: 0.9em; }}
            a {{ color: #0060df; text-decoration: none; }}
        </style>
    </head>
    <body>
        <h1>Your Research Digest</h1>
        <p class="meta">Generated: {datetime.now().strftime('%Y-%m-%d')}</p>

        {digest_content}

        <hr>
        <p style="color: #666; font-size: 0.9em;">
            Generated automatically by your personal research digest.
            <br>To modify preferences, edit config.yaml in your repository.
        </p>
    </body>
    </html>
    """
    return html


def send_email(html_content, config):
    """Send digest via email using Gmail SMTP"""
    email_method = config.get('email_method', 'print')

    if email_method == 'print':
        # Preview mode - just print the digest
        print("Email generation successful!")
        print(f"Would send to: {config['email']}")
        print("\nPreview:")
        print(html_content[:500])
        return

    elif email_method == 'gmail':
        # Gmail SMTP
        sender_email = os.environ.get('GMAIL_ADDRESS')
        sender_password = os.environ.get('GMAIL_APP_PASSWORD')

        if not sender_email or not sender_password:
            raise ValueError("Gmail credentials not found. Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD in secrets.")

        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Research Digest - {datetime.now().strftime('%Y-%m-%d')}"
        msg['From'] = sender_email
        msg['To'] = config['email']

        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
            print(f"Email sent successfully to {config['email']}")
        except Exception as e:
            print(f"Failed to send email: {e}")
            raise

    else:
        raise ValueError(f"Unknown email method: {email_method}. Use 'print' or 'gmail'")


def main():
    """Main execution"""
    print("Starting Research Digest Generator...")

    # Load configuration
    config = load_config()
    print(f"Configuration loaded for: {config['email']}")

    # Fetch papers
    papers = fetch_papers(config['feeds'])
    print(f"Fetched {len(papers)} papers from {len(config['feeds'])} sources")

    # Filter and rank
    print("Analyzing papers with AI...")
    digest_content = filter_and_rank_papers(
        papers,
        config['research_interests'],
        config['max_papers']
    )

    # Generate email
    html_email = generate_html_email(digest_content, config)

    # Send email
    send_email(html_email, config)

    print("Digest generation complete!")


if __name__ == "__main__":
    main()
