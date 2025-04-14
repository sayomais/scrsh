import os
import re
import asyncio
import threading
import httpx
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Flask setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Userbot Scraper is Live!"

# Flask runner
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# Start Flask in a separate thread
threading.Thread(target=run_flask).start()

# Telegram setup
api_id = 22092598
api_hash = "93de73c78293c85fd6feddb92f91b81a"
session = os.getenv("STRING_SESSION")  # Must be set in Render

client = TelegramClient(StringSession(session), api_id, api_hash)

group_ids = [-1002682944548, -1001793269672]
channel_id = -1002698542107

# Regex patterns
cc_patterns = [
    r'(\d{13,16})[\s|/|\-|~]?\s*(\d{1,2})[\s|/|\-|~]?\s*(\d{2,4})[\s|/|\-|~]?\s*(\d{3,4})',
    r'(\d{13,16})\n(\d{1,2})\n(\d{2,4})\n(\d{3,4})',
    r'(\d{13,16})\s(\d{1,2})\s(\d{2,4})\s(\d{3,4})'
]

sent_ccs = set()

def format_cc(match):
    cc, mm, yy, cvv = match.groups()
    yy = yy[-2:]
    return f"{cc}|{mm}|{yy}|{cvv}"

async def get_bin_info(bin_number):
    url = f"https://bins.antipublic.cc/bins/{bin_number}"
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, timeout=10)
            data = res.json()
            return {
                "country": data.get("country_name", "Unknown"),
                "flag": data.get("country_flag", "🏳"),
                "bank": data.get("bank", "Unknown"),
                "type": f"{data.get('type', 'Unknown')} - {data.get('brand', 'Unknown')}"
            }
        except:
            return {"country": "Unknown", "flag": "🏳", "bank": "Unknown", "type": "Unknown"}

@client.on(events.NewMessage(chats=group_ids))
async def cc_scraper(event):
    text = event.raw_text
    found = set()

    for pattern in cc_patterns:
        for match in re.finditer(pattern, text):
            formatted = format_cc(match)
            found.add(formatted)

    for cc in found:
        if cc in sent_ccs:
            continue
        sent_ccs.add(cc)
        bin_info = await get_bin_info(cc[:6])

        msg = f"""
[<a href="https://t.me/Barry_Scrapper">⌬</a>] 𝑩𝒂𝒓𝒓𝒚 𝑺𝒄𝒓𝒂𝒑𝒑𝒆𝒓    
━━━━━━━━━━━━━━━━━━  
[<a href="https://t.me/Barry_Scrapper">⌬</a>] 𝗖𝗮𝗿𝗱 :- <code>{cc}</code>  
[<a href="https://t.me/Barry_Scrapper">⌬</a>] 𝗦𝘁𝗮𝘁𝘂𝘀 :- <code>Approved ✅</code>
━━━━━━━━━━━━━━━━━━  
[<a href="https://t.me/Barry_Scrapper">⌬</a>] 𝗕𝗶𝗻 :- <code>{cc[:6]}</code>  
[<a href="https://t.me/Barry_Scrapper">⌬</a>] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 :- <code>{bin_info['country']} {bin_info['flag']}</code>
[<a href="https://t.me/Barry_Scrapper">⌬</a>] 𝗜𝘀𝘀𝘂𝗲𝗿: <code>{bin_info['bank']}</code>
[<a href="https://t.me/Barry_Scrapper">⌬</a>] 𝗧𝘆𝗽𝗲: <code>{bin_info['type']}</code>
━━━━━━━━━━━━━━━━━━  
[<a href="https://t.me/Barry_Scrapper">⌬</a>] 𝗦𝗰𝗿𝗮𝗽𝗽𝗲𝗱 𝗕𝘆: <a href="https://t.me/Barry_Scrapper">𝑩𝒂𝒓𝒓𝒚</a>
"""
        await client.send_message(channel_id, msg, parse_mode="HTML")

async def main():
    await client.start()
    print("✅ Telegram Scraper Running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
