# Tg-bot-cc

# Beast CC Monitor Bot

**Ethical Research Only — Security Researchers & Awareness**

This is a professional Telegram bot for monitoring channels or groups for credit card (CC) patterns, validating them using the Luhn algorithm, retrieving BIN information, generating test cards, and providing simulated (fake) cardholder info.  
**Strictly for educational and informational use. Do NOT use for illegal or unauthorized activities.**

---

## Features

- **/start** — Shows menu and intro
- **/link <@channel>** — Links a Telegram channel for monitoring
- **/scrape_check** — Scrapes and checks for credit card numbers in messages (simulated in this version)
- **/check <cc>** — Checks a single card for validity (Luhn)
- **/gen <visa/mastercard/amex>** — Generates fake/test cards
- **/bin <first6>** — Fetches BIN info (bank, country, etc)
- **/cc_info <cc>** — Shows simulated cardholder info
- **/stats** — Shows statistics (scanned, valid, etc)
- **/stop** — Stops monitoring/scraping

---

## Setup

1. **Clone the repository**
    ```bash
    git clone <repo-url>
    cd <repo-folder>
    ```

2. **Install dependencies**
    ```bash
    pip install pyrogram faker requests tgcrypto
    ```

3. **Configure your Telegram bot**
    - Get your `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org).
    - Create a bot with [@BotFather](https://t.me/botfather) for the `BOT_TOKEN`.
    - Edit these in your script (`API_ID`, `API_HASH`, `BOT_TOKEN`).

4. **Run the bot**
    ```bash
    python beast_bot.py
    ```

---

## Example Commands & Responses

- **/start**
    ```
    👋 Welcome to Beast CC Monitor Bot
    Commands:
    /link <@channel> → Link a group/channel to monitor
    /scrape_check → Start scraping + validation
    /check <cc> → Check card format
    /gen <visa/mastercard/amex> → Generate fake card
    /bin <bin> → BIN info
    /cc_info <cc> → Simulated CC info
    /stats → View stats
    /stop → Stop scraping
    ```

- **/link @yourchannel**
    ```
    ✅ Linked to @yourchannel
    ```
- **/scrape_check**
    ```
    🔍 Scraping started...
    ✅ Checked: 10 cards
    💳 Valid CC Found:
    Card: 4571731234567890
    ...
    ```
- **/stop**
    ```
    🛑 Scanning stopped.
    ```
- **/check 4571731234567890**
    ```
    ✅ This card looks valid (Luhn passed).
    ```
- **/gen visa**
    ```
    🎲 Generated: 4571739876543210|03|28|123
    ```
- **/bin 457173**
    ```
    🔎 BIN Info:
    Bank: Chase
    Country: United States
    Type: Debit
    Brand: VISA
    Scheme: Classic
    ```
- **/cc_info 4571731234567890**
    ```
    📦 Simulated Info:
    Card: 4571731234567890
    Name: John Doe
    Address: 123 Main St, NY
    Phone: +1 555-123-4567
    ```
- **/stats**
    ```
    📊 Bot Stats:
    Cards Scanned: 100
    Valid Found: 7
    Linked Channel: @yourchannel
    ```

---

## ⚠️ Ethics Warning

- **This tool is for security research, awareness, and educational purposes only.**
- **Do NOT use for real card theft, fraud, or unauthorized data access.**
- **Always comply with all applicable laws and Telegram’s TOS.**

---

## 📝 License

MIT License — see [LICENSE](LICENSE)  
Use responsibly.

Repostiory Owner Telegram - @FreakinMortal , @BetLuckers

---
