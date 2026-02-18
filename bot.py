import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Token တွေကို ဒီမှာ တိုက်ရိုက်မထည့်ဘဲ Render ရဲ့ Environment Variable ကနေ ဆွဲယူမယ် (ပိုလုံခြုံအောင်)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# AI Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="မင်းက Blitz ရဲ့ အနီးကပ်လက်ထောက် Bot ဖြစ်တယ်။ Blitz က MLBB မှာ Chou ဆော့တာ အရမ်းတော်တဲ့ Streamer ဖြစ်တယ်။ လူတွေနဲ့ ရင်းရင်းနှီးနှီး Gamer ဆန်ဆန် စကားပြောပေးပါ။"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ဟေး! ငါ Blitz ရဲ့ AI Bot ပါ။ ၂၄ နာရီ နိုးနေပြီနော်။ ဘာမေးမလဲ?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    # Render မှာ Run ဖို့ ApplicationBuilder ကို သုံးတယ်
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    app.run_polling()
