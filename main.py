import feedparser
import os
import sys
import json
import time
import socket
from datetime import datetime, timedelta, timezone
from google import genai

# Prevent hangs on slow websites
socket.setdefaulttimeout(10)

def load_feeds_config(filepath="feeds.json"):
    """Loads the RSS feed URLs from an external JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        sys.exit(1)

def fetch_recent_news(feeds_dict, hours_back=48):
    """Iterates through the dictionary of feeds and extracts recent articles."""
    print(f"Fetching RSS feeds from the last {hours_back} hours...")
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_back)
    compiled_news = ""

    for category, urls in feeds_dict.items():
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
                print(f"   [!] Error/Timeout parsing {url}: {e}")

    if not compiled_news.strip():
        return "No new articles found."
        
    # --- THE TOKEN LIMIT FIX ---
    # Cap the output at 200,000 characters to stay well under the Token Per Minute limit.
    max_chars = 200000
    if len(compiled_news) > max_chars:
        print(f"Warning: News volume high ({len(compiled_news)} chars). Truncating to fit API limits.")
        compiled_news = compiled_news[:max_chars] + "\n\n...[DATA TRUNCATED TO PREVENT API 429 ERROR]..."
        
    return compiled_news

def get_yesterdays_memory(filepath="yesterday.md"):
    """Loads the previous day's briefing to prevent redundant reporting."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return content if content and content != "null" else "No previous briefing found."
    except FileNotFoundError:
        return "No previous briefing found."

def generate_briefing(news_data, memory_data):
    """Sends the compiled data and memory to the Gemini API."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY secret is missing!")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    model_name = 'gemini-3.8-flash'
    
    prompt = f"""
    You are an elite intelligence analyst specializing in the intersection of cybersecurity, geopolitics, and geoeconomics, with a specific focus on Hungary and the CEE region.

    CRITICAL ANTI-REDUNDANCY RULE:
    Below is the briefing you generated YESTERDAY. You must cross-reference today's raw data against yesterday's briefing. 
    - DO NOT repeat a story from yesterday unless there is a significant new development.
    - If today's data contains a major new development to a story from yesterday, label it with [UPDATE] and briefly explain what changed.
    - Focus heavily on NET-NEW intelligence.

    Structure the output exactly as follows using Markdown:
    ## 1. The Macro Picture (Geopolitics & Geoeconomics)
    ## 2. Critical Infrastructure & ICS Threat Landscape
    ## 3. Hungarian Cyber & Tech Sector
    ## 4. Global Cybercrime & APT Activity
    ## 5. Recommended Deep Dives

    === YESTERDAY'S BRIEFING (YOUR MEMORY) ===
    {memory_data}

    === TODAY'S RAW INTELLIGENCE DATA ===
    {news_data}
    """

    print("Contacting Gemini API...")
    max_retries = 4
    for attempt in range(max_retries):
        try:
            chat = client.chats.create(model=model_name)
            response = chat.send_message(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            print(f"Error on attempt {attempt + 1}: {error_msg}")
            if "503" in error_msg or "429" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 20
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print("Max retries reached.")
                    sys.exit(1)
            else:
                sys.exit(1)

def save_briefing(content, filepath="briefing.md"):
    """Saves the final generated string to a markdown file."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Briefing saved to {filepath}")

# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    feeds_config = load_feeds_config("feeds.json")
    news_data = fetch_recent_news(feeds_config, hours_back=48)
    memory_data = get_yesterdays_memory("yesterday.md")
    
    final_briefing = generate_briefing(news_data, memory_data)
    save_briefing(final_briefing, "briefing.md")
