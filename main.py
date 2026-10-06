import feedparser
import os
import sys
import socket
from datetime import datetime, timedelta, timezone
from google import genai

# Prevent the script from hanging if a news website is down/slow (10 seconds max)
socket.setdefaulttimeout(10)

# 1. Initialize the new 2026 Gemini API Client
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY secret is missing!")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
model_name = 'gemini-3.8-flash'
print(f"Initializing model: {model_name}")

# 2. Categorized Intelligence Feeds
FEEDS = {
    "Hungarian Core & Geoeconomics": [
        "https://www.portfolio.hu/rss/all.xml",
        "https://telex.hu/rss",
        "https://www.hwsw.hu/xml/latest_news.xml",
        "https://nki.gov.hu/feed/"
    ],
    "Geopolitics & CEE Region": [
        "https://vsquare.org/feed/",
        "https://warontherocks.com/feed/",
        "https://balkaninsight.com/feed/",
        "https://cepa.org/feed/"
    ],
    "Critical Infrastructure (ICS/OT)": [
        "https://www.cisa.gov/uscert/ics/advisories/advisories.xml",
        "https://www.dragos.com/feed/",
        "https://www.securityweek.com/feed/"
    ],
    "Global Cyber & Threat Intel": [
        "https://idovan.substack.com/feed",
        "https://cyberthreatreport.substack.com/feed",
        "https://ryanmcbeth.substack.com/feed",
        "https://osintnewsletter.com/feed",
        "https://zetter.substack.com/feed",
        "https://danielmiessler.com/feed/",
        "https://www.bleepingcomputer.com/feed/",
        "https://feeds.feedburner.com/TheHackersNews",
        "https://www.cyberscoop.com/feed/"
    ]
}

# 3. Fetch and filter articles
print("Fetching RSS feeds...")
cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
compiled_news = ""

for category, urls in FEEDS.items():
    compiled_news += f"\n### CATEGORY: {category} ###\n"
    for url in urls:
        print(f" - Checking {url}...")
        try:
            parsed = feedparser.parse(url)
            for entry in parsed.entries:
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    entry_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                    if entry_date > cutoff:
                        summary = entry.get('summary', 'No summary provided')
                        summary = summary.replace("<p>", "").replace("</p>", "").strip()[:500] 
                        compiled_news += f"- Source: {parsed.feed.title}\n  Title: {entry.title}\n  Summary: {summary}...\n  Link: {entry.link}\n\n"
        except Exception as e:
            print(f"   [!] Error or Timeout parsing {url}: {e}")

if not compiled_news.strip():
    compiled_news = "No new articles found in the last 48 hours."

# 4. The Upgraded System Prompt for Gemini
print("Sending massive dataset to Gemini for synthesis...")
prompt = f"""
You are an elite intelligence analyst specializing in the intersection of cybersecurity, geopolitics, and geoeconomics, with a specific focus on Hungary and the CEE region.

Your task is to analyze a massive influx of open-source intelligence from the last 48 hours and synthesize it into a highly actionable, structured briefing. You must connect the dots. If a geopolitical event in the news could impact Hungarian energy prices (geoeconomics) or trigger Russian cyber activity against critical infrastructure, you must highlight that connection.

Structure the output exactly as follows using Markdown:

## 1. The Macro Picture (Geopolitics & Geoeconomics)
(Summarize the top global and regional geopolitical/economic shifts. Explicitly state how these events currently impact, or could impact, Hungary's strategic position or economy.)

## 2. Critical Infrastructure & ICS Threat Landscape
(Focus heavily on Dragos, CISA, and industrial threats. What is targeting power grids, manufacturing, or water? Explain the potential kinetic impact.)

## 3. Hungarian Cyber & Tech Sector
(Synthesize NKI alerts, Telex, HWSW, and local substacks. What is happening in the Hungarian IT and cyber space right now?)

## 4. Global Cybercrime & APT Activity
(Summarize the major breaches, ransomware trends, and nation-state (APT) operations globally. Keep technical jargon accessible for an intermediate learner.)

## 5. Recommended Deep Dives
(Select 3 specific articles from the provided data that provide the best educational value for someone learning about the intersection of these fields. Provide a 1-sentence hook and the link.)

Here is the categorized raw intelligence data to analyze:
{compiled_news}
"""

# 5. Generate and save the output
try:
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    with open("briefing.md", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Briefing successfully generated and saved to briefing.md")
except Exception as e:
    print(f"Error during Gemini generation: {e}")
    sys.exit(1)
