# telegram-sticker-bot

A Telegram bot that converts any photo into a **ready-to-use sticker** with automatic resizing and transparent padding.

Built with [python-telegram-bot](https://docs.python-telegram-bot.org/), [Pillow](https://python-pillow.org/), and SQLite — outputs stickers in **WebP format, 512x512** with proportional padding, exactly as Telegram requires.

## ✨ Features

- 🖼️ Photo → Sticker conversion (WebP, 512x512, proportional padding)
- 🗄️ SQLite database to store sticker history
- ▶️ `/start` — start the bot
- 📊 `/stats` — show your sticker count
- 🛡️ User-friendly error handling

## 🛠️ Tech Stack

- [Python](https://www.python.org/) 3.8+
- [python-telegram-bot](https://docs.python-telegram-bot.org/) 20.8
- [Pillow](https://python-pillow.org/) 10.2.0
- SQLite

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/h1ntz0/telegram-sticker-bot.git
cd telegram-sticker-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a bot token

Talk to [@BotFather](https://t.me/botfather) in Telegram to create a bot and get its token.

### 4. Set the token

```bash
export BOT_TOKEN="your_bot_token_here"
```

### 5. Run the bot

```bash
python bot.py
```

## 📖 How to Use

1. Start a chat with your bot and send `/start`
2. Send a **photo** (not as a file) to the bot
3. The bot processes it and sends back a ready-to-use sticker
4. Use `/stats` anytime to see how many stickers you've created

## 🗄️ Database Structure

`stickers.db` contains the `stickers` table:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Row ID |
| `user_id` | INTEGER | Telegram user ID |
| `chat_id` | INTEGER | Chat ID |
| `sticker_file_id` | TEXT | Sticker file identifier |
| `created_at` | TEXT (ISO format) | Creation timestamp |

## 📄 License

This project is licensed under the MIT License.
