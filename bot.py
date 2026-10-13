import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from fake_useragent import UserAgent

ua = UserAgent()

# এখানে আপনার টেলিগ্রাম বটের টোকেনটি বসাবেন
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

def get_instagram_ua(locale="en_US"):
    devices = [
        {"model": "SM-S918B", "brand": "Samsung", "dpi": "480dpi", "res": "1080x2340", "hw": "kalama", "sdk": "33", "os": "13"},
        {"model": "Pixel 8 Pro", "brand": "Google", "dpi": "560dpi", "res": "1440x3120", "hw": "husky", "sdk": "34", "os": "14"},
        {"model": "2312DRA50G", "brand": "Xiaomi", "dpi": "440dpi", "res": "1080x2400", "hw": "zircon", "sdk": "34", "os": "14"}
    ]
    dev = random.choice(devices)
    ig_ver = f"{random.randint(310, 340)}.0.0.{random.randint(10, 50)}.{random.randint(50, 150)}"
    ver_code = str(random.randint(500000000, 650000000))
    return f"Instagram {ig_ver} Android ({dev['sdk']}/{dev['os']}; {dev['dpi']}; {dev['res']}; {dev['brand']}; {dev['model']}; {dev['hw']}; {locale}; {ver_code})"

def get_facebook_ua(locale="en_US"):
    devices = [
        {"model": "SM-G998B", "brand": "Samsung", "sdk": "33", "os": "13"},
        {"model": "2201116PG", "brand": "Xiaomi", "sdk": "32", "os": "12"}
    ]
    the_dev = random.choice(devices)
    fb_ver = f"{random.randint(430, 470)}.0.0.{random.randint(10, 40)}.{random.randint(100, 120)}"
    chrome_ver = f"{random.randint(120, 128)}.0.0.0"
    return f"Mozilla/5.0 (Linux; Android {the_dev['os']}; {the_dev['model']} Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{chrome_ver} Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/{fb_ver};FBNV/1;FBLC/{locale};FBBV/563914820;FBMD/{the_dev['brand']};FBSN/Android;FBSV/{the_dev['os']};FBPN/com.facebook.katana;]"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📱 Android Chrome", callback_data="android_chrome"),
            InlineKeyboardButton("🍎 iPhone Safari", callback_data="ios_safari")
        ],
        [
            InlineKeyboardButton("📸 Instagram (US)", callback_data="ig_us"),
            InlineKeyboardButton("📸 Instagram (DE)", callback_data="ig_de")
        ],
        [
            InlineKeyboardButton("📘 Facebook (US)", callback_data="fb_us"),
            InlineKeyboardButton("💻 Desktop Chrome", callback_data="desktop_chrome")
        ],
        [
            InlineKeyboardButton("🎲 Random Anything", callback_data="random_all")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 **User-Agent Generator Bot-এ স্বাগতম!**\n\nনিচের বাটন থেকে আপনার প্রয়োজনীয় ইউজার-এজেন্ট সিলেক্ট করুন:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    res_ua = ""

    if data == "android_chrome":
        res_ua = ua.android
    elif data == "ios_safari":
        res_ua = ua.iphone
    elif data == "desktop_chrome":
        res_ua = ua.chrome
    elif data == "ig_us":
        res_ua = get_instagram_ua("en_US")
    elif data == "ig_de":
        res_ua = get_instagram_ua("de_DE")
    elif data == "fb_us":
        res_ua = get_facebook_ua("en_US")
    elif data == "random_all":
        res_ua = ua.random

    reply_text = f"✅ **Generated User-Agent:**\n\n`{res_ua}`\n\n*(কোডটিতে ক্লিক করলেই কপি হয়ে যাবে)*"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Generate Again", callback_data=data)],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
    ]
    
    if data == "main_menu":
        await start(query, context)
    else:
        await query.edit_message_text(
            text=reply_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    print("Bot is running...")
    app.run_polling()
