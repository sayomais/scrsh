import re
import asyncio
import httpx
from telethon import TelegramClient, events

# Telegram API credentials
api_id = 22092598
api_hash = "93de73c78293c85fd6feddb92f91b81a"
session_name = "cc_scraper"

# Telegram groups to scrape from
group_id = (-1002682944548, -1001793269672)
channel_id = -1002698542107  # Channel to send results

client = TelegramClient(session_name, api_id, api_hash)

# Patterns to match CCs
cc_patterns = [
    r'(\d{13,16})[\s|/|\-|~]?\s*(\d{1,2})[\s|/|\-|~]?\s*(\d{2,4})[\s|/|\-|~]?\s*(\d{3,4})',
    r'(\d{13,16})\n(\d{1,2})\n(\d{2,4})\n(\d{3,4})',
    r'(\d{13,16})\s(\d{1,2})\s(\d{2,4})\s(\d{3,4})'
]

# Already sent CCs
sent_ccs = set()

# Format CC to standard format
def format_cc(match):
    cc, mm, yy, cvv = match.groups()
    yy = yy[-2:]  # Convert YYYY to YY
    return f"{cc}|{mm}|{yy}|{cvv}"

# Get BIN information
async def get_bin_info(bin_number):
    url = f"https://bins.antipublic.cc/bins/{bin_number}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10)
