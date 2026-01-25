import os
import logging
import sqlite3
from datetime import datetime
from io import BytesIO
from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

DB_NAME = 'stickers.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stickers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            chat_id INTEGER,
            sticker_file_id TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_sticker_to_db(user_id, chat_id, sticker_file_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute(
        'INSERT INTO stickers (user_id, chat_id, sticker_file_id, created_at) VALUES (?, ?, ?, ?)',
        (user_id, chat_id, sticker_file_id, created_at)
    )
    conn.commit()
    conn.close()

def get_user_stats(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM stickers WHERE user_id = ?', (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Welcome to sticker bot! Send photo to me and I will change it to sticker\n\n'
        'Command for use this bot:\n'
        '/start - start bot\n'
        '/stats - show your sticker count'
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        count = get_user_stats(user_id)
        await update.message.reply_text(f'Your sticker count is {count} sticker')
    except Exception as e:
        logging.error(f'Error in stats: {e}')
        await update.message.reply_text('Error in stats')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text('Processing for your photo...')
        
        photo = update.message.photo[-1]
        photo_file = await photo.get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        
        os.makedirs('photos', exist_ok=True)
        user_id = update.effective_user.id
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        photo_path = f'photos/user_{user_id}_{timestamp}.jpg'
        with open(photo_path, 'wb') as f:
            f.write(photo_bytes)
        logging.info(f'Photo saved: {photo_path}')
        
        image = Image.open(BytesIO(photo_bytes))
        
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        width, height = image.size
        max_size = 512
        
        if width > height:
            new_width = max_size
            new_height = int((height / width) * max_size)
        else:
            new_height = max_size
            new_width = int((width / height) * max_size)
        
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        new_image = Image.new('RGBA', (max_size, max_size), (0, 0, 0, 0))
        paste_x = (max_size - new_width) // 2
        paste_y = (max_size - new_height) // 2
        new_image.paste(image, (paste_x, paste_y))
        
        output = BytesIO()
        new_image.save(output, format='WebP')
        output.seek(0)
        
        sticker_message = await update.message.reply_sticker(sticker=output)
        sticker_file_id = sticker_message.sticker.file_id
        
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        save_sticker_to_db(user_id, chat_id, sticker_file_id)
        
        await update.message.reply_text('Sticker success created')
        
    except Exception as e:
        logging.error(f'Error in handle_photo: {e}')
        await update.message.reply_text('Error in create sticker')

def main():
    init_db()
    
    token = os.getenv('BOT_TOKEN')
    if not token:
        raise ValueError('BOT_TOKEN environment variable is not set')
    
    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('stats', stats))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    logging.info('Bot started')
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
