import feedparser
import google.generativeai as genai
import os
from datetime import datetime, timedelta, timezone

# 1. Initialize Gemini API
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Your Curated List of RSS Feeds
FEEDS = [
    "https://idovan.substack.com/feed",
    "https://cyberthreatreport.substack.com/feed",
    "https://vsquare.org/feed/",
    "https://ryanmcbeth.substack.com/feed",
    "https://osintnewsletter.com/feed",
    "https://zetter.substack.com/feed",
    "https://danielmiessler.com/feed/",
    "https://nki.gov.hu/feed/" # Hungarian National Cyber Security Center
]

# 3. Fetch and filter articles (only keep the last 48 hours to avoid stale data)
print("Fetching RSS feeds...")
cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
compiled_news = ""

for url in FEEDS:
    try:
        parsed = feedparser.parse(url)
        for entry in parsed.entries:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                entry_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                if entry_date > cutoff:
                    # Clean up the summary text
                    summary = entry.get('summary', 'No summary provided')
                    compiled_news += f"Source: {parsed.feed.title}\nTitle: {entry.title}\nSummary: {summary}\nLink: {entry.link}\n\n"
    except Exception as e:
        print(f"Error parsing {url}: {e}")

if not compiled_news.strip():
    compiled_news = "No new articles found in the last 48 hours."

# 4. The System Prompt for Gemini
print("Sending to Gemini for synthesis...")
prompt = f"""
You are an expert cybersecurity intelligence analyst. Your task is to review the following compiled RSS feed data from the last 48 hours and synthesize a clear, highly structured daily briefing.

The target audience is a beginner/intermediate cybersecurity learner based in Hungary. 
Always provide context for technical jargon. Ensure the tone is educational.

Structure the output exactly as follows using Markdown:
## 1. Executive Summary
(Provide a 3-bullet TL;DR of the most critical geopolitical or cyber events. Prioritize Hungarian/Central European impacts if present in the data.)

## 2. Governmental Warnings & Context
(Summarize alerts from sources like NKI. Do not just list CVE numbers—explain *how* the vulnerabilities are being used and why they matter in plain English.)

## 3. Industry News & Trends
(Synthesize the deep-dives from the Substacks and OSINT newsletters. Explain the 'why' behind the news.)

## 4. Deep Dive Recommendations
(Highlight 2-3 specific articles or podcast show notes from the data that are worth a manual deep-dive today, with a 1-sentence hook for each and the link.)

Here is the raw data to analyze:
{compiled_news}
"""

# 5. Generate and save the output to a markdown file
response = model.generate_content(prompt)

with open("briefing.md", "w", encoding="utf-8") as f:
    f.write(response.text)

print("Briefing successfully generated and saved to briefing.md")
