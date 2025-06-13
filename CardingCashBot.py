import re
import requests
import random
import time
from faker import Faker
from datetime import datetime
from pyrogram import Client, filters

fake = Faker()

# --- CONFIG ---

API_ID =  "your api id" # int, not str!
API_HASH = "your api hash"
BOT_TOKEN = "bot token"

app = Client("beast_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

linked_channel = None
scanning = False
stats = {"scanned": 0, "valid": 0}

# --- UTILS ---

cc_pattern = re.compile(r"\b(\d{12,19})\b")

def luhn(cc):
    sum_ = 0
    reverse = cc[::-1]
    for i, d in enumerate(reverse):
        n = int(d)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        sum_ += n
    return sum_ % 10 == 0

def bin_lookup(bin_num):
    try:
        res = requests.get(f"https://lookup.binlist.net/{bin_num}").json()
        return {
            "bank": res.get("bank", {}).get("name", "N/A"),
            "country": res.get("country", {}).get("name", "N/A"),
            "type": res.get("type", "N/A"),
            "scheme": res.get("scheme", "N/A"),
            "brand": res.get("brand", "N/A"),
        }
    except Exception:
        return None

def generate_card(card_type):
    bin_map = {
        "visa": "4",
        "mastercard": "5",
        "amex": "3"
    }
    prefix = bin_map.get(card_type.lower(), "4")
    cc = prefix + "".join([str(random.randint(0, 9)) for _ in range(15)])
    cc = cc[:15] + str((10 - sum([int(x) for x in cc[:15]]) % 10) % 10)
    exp = f"{random.randint(1,12):02}|{random.randint(26,30)}"
    cvv = f"{random.randint(100,999)}"
    return f"{cc}|{exp}|{cvv}"

def fake_info():
    return {
        "name": fake.name(),
        "address": fake.address().replace("\n", ", "),
        "phone": fake.phone_number()
    }

# --- HANDLERS ---

@app.on_message(filters.command("start"))
def start(client, msg):
    msg.reply(
        "👋 Welcome to Beast CC Monitor Bot\n"
        "Commands:\n"
        "/link <@channel> → Link a group/channel to monitor\n"
        "/scrape_check → Start scraping + validation\n"
        "/check <cc> → Check card format\n"
        "/gen <visa/mastercard/amex> → Generate fake card\n"
        "/bin <bin> → BIN info\n"
        "/cc_info <cc> → Simulated CC info\n"
        "/stats → View stats\n"
        "/stop → Stop scraping"
    )

@app.on_message(filters.command("link"))
def link_channel(client, msg):
    global linked_channel
    try:
        linked_channel = msg.text.split()[1]
        msg.reply(f"✅ Linked to {linked_channel}")
    except Exception:
        msg.reply("❌ Usage: /link @channel")

@app.on_message(filters.command("scrape_check"))
def scrape(client, msg):
    global scanning
    if not linked_channel:
        return msg.reply("❌ First link a channel using /link")
    scanning = True
    msg.reply("🔍 Scraping started...")
    for i in range(100):
        if not scanning:
            break
        # Simulated card, in real scraping you'd use messages from the linked_channel history
        cc = f"457173{random.randint(1000000000, 9999999999)}"
        stats["scanned"] += 1
        if luhn(cc):
            stats["valid"] += 1
            bin_info = bin_lookup(cc[:6]) or {}
            info = fake_info()
            msg.reply(
                f"💳 Valid CC Found:\n"
                f"Card: {cc}\n"
                f"BIN: {cc[:6]} - {bin_info.get('bank', 'N/A')} ({bin_info.get('country', 'N/A')})\n"
                f"Type: {bin_info.get('type', 'N/A')} - {bin_info.get('scheme', 'N/A')}\n"
                f"Name: {info['name']}\n"
                f"Address: {info['address']}\n"
                f"Phone: {info['phone']}\n"
            )
        if (i + 1) % 10 == 0:
            msg.reply(f"✅ Checked: {i+1} cards")
        time.sleep(0.5)
    msg.reply("✅ Scrape complete.")

@app.on_message(filters.command("stop"))
def stop(client, msg):
    global scanning
    scanning = False
    msg.reply("🛑 Scanning stopped.")

@app.on_message(filters.command("check"))
def check_card(client, msg):
    try:
        cc = msg.text.split()[1]
        if not cc.isdigit() or not (12 <= len(cc) <= 19):
            msg.reply("❌ Invalid card (wrong format/length).")
            return
        if luhn(cc):
            msg.reply("✅ This card looks valid (Luhn passed).")
        else:
            msg.reply("❌ Invalid card (Luhn failed).")
    except Exception:
        msg.reply("❌ Usage: /check <card_number>")

@app.on_message(filters.command("gen"))
def gen_card(client, msg):
    try:
        typ = msg.text.split()[1]
        card = generate_card(typ)
        msg.reply(f"🎲 Generated: {card}")
    except Exception:
        msg.reply("❌ Usage: /gen <visa/mastercard/amex>")

@app.on_message(filters.command("bin"))
def bin_cmd(client, msg):
    try:
        bin_num = msg.text.split()[1][:6]
        bin_info = bin_lookup(bin_num)
        if bin_info:
            msg.reply(
                f"🔎 BIN Info:\n"
                f"Bank: {bin_info['bank']}\n"
                f"Country: {bin_info['country']}\n"
                f"Type: {bin_info['type']}\n"
                f"Brand: {bin_info['brand']}\n"
                f"Scheme: {bin_info['scheme']}\n"
            )
        else:
            msg.reply("❌ BIN not found.")
    except Exception:
        msg.reply("❌ Usage: /bin <first6>")

@app.on_message(filters.command("cc_info"))
def ccinfo(client, msg):
    try:
        cc = msg.text.split()[1]
        info = fake_info()
        msg.reply(
            f"📦 Simulated Info:\n"
            f"Card: {cc}\n"
            f"Name: {info['name']}\n"
            f"Address: {info['address']}\n"
            f"Phone: {info['phone']}\n"
        )
    except Exception:
        msg.reply("❌ Usage: /cc_info <card>")

@app.on_message(filters.command("stats"))
def stats_cmd(client, msg):
    msg.reply(
        f"📊 Bot Stats:\n"
        f"Cards Scanned: {stats['scanned']}\n"
        f"Valid Found: {stats['valid']}\n"
        f"Linked Channel: {linked_channel or 'None'}"
    )

if __name__ == "__main__":
    app.run()
