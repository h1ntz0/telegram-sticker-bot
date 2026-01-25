# Bot Telegram Photo to Sticker

Bot Telegram that changes photo to sticker with WebP format 512x512.

## Features

- Changes photo to sticker (format WebP, size 512x512 with proportional padding)
- SQLite database to store sticker history
- Command `/start` to start bot
- Command `/stats` to show your sticker count
- Error handling that is friendly to users

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get Bot Token from [@BotFather](https://t.me/botfather) in Telegram

3. Set environment variable BOT_TOKEN:
```bash
export BOT_TOKEN="your_bot_token_here"
```

## How to Run

```bash
python bot.py
```

## How to Use Bot

1. Start chat with bot and send `/start`
2. Send photo (not as file) to bot
3. Bot will process and send sticker
4. Use `/stats` to see how many stickers you have

## Database Structure

Database `stickers.db` has table `stickers` with column:
- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `user_id`: INTEGER
- `chat_id`: INTEGER
- `sticker_file_id`: TEXT
- `created_at`: TEXT (ISO format)

## Requirements

- Python 3.8+
- python-telegram-bot 20.8
- Pillow 10.2.0
