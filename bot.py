import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from groq import Groq

# ================== LOAD ENV ==================
load_dotenv()

BOT_USERNAME = os.getenv("BOT_USERNAME")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEFAULT_LANG_PROMPT = os.getenv("DEFAULT_LANG_PROMPT", "Jawab dalam bahasa Indonesia: ")

# ================== LIST MODEL (FALLBACK ORDER) ==================
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "gemma2-9b-it",
    "qwen/qwen3-32b",
]

# Model aktif (bisa diubah dengan /setmodel)
ACTIVE_MODEL = None  

# ================== LOGGING ==================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ================== CLIENT ==================
groq_client = Groq(api_key=GROQ_API_KEY)

# ================== HANDLERS ==================
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ACTIVE_MODEL
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()
    is_command = text.lower().startswith("!ai") or text.lower().startswith("/ai")
    is_mention = f"@{BOT_USERNAME}" in text
    is_reply_to_bot = (
        update.message.reply_to_message
        and update.message.reply_to_message.from_user.username == BOT_USERNAME
    )

    if is_command or is_mention or is_reply_to_bot:
        prompt = (
            text.replace(f"@{BOT_USERNAME}", "")
            .replace("!ai", "")
            .replace("/ai", "")
            .strip()
        )
        if not prompt:
            await update.message.reply_text("Ketik pertanyaan setelah `!ai` atau `/ai` ya 🙂")
            return

        ai_text = None
        last_error = None

        # Tentukan urutan model yang dicoba
        models_to_try = []
        if ACTIVE_MODEL:
            models_to_try.append(ACTIVE_MODEL)
        models_to_try.extend([m for m in GROQ_MODELS if m != ACTIVE_MODEL])

        # Coba semua model sesuai urutan
        for model in models_to_try:
            try:
                resp = groq_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": DEFAULT_LANG_PROMPT + prompt}],
                    temperature=0.7,
                    max_tokens=800,
                )
                ai_text = resp.choices[0].message.content if resp.choices else None
                if ai_text:
                    logger.info(f"Jawaban sukses pakai model: {model}")
                    break
            except Exception as e:
                last_error = e
                logger.warning(f"Model {model} gagal, mencoba model berikutnya...")

        if ai_text:
            await update.message.reply_text(ai_text)
        else:
            logger.exception("Semua model gagal", exc_info=last_error)
            await update.message.reply_text("Maaf, semua model AI sedang tidak tersedia. Coba lagi sebentar ya 🙏")

async def cmd_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("Format: `/ai pertanyaan`")
        return
    await ai_reply(update, context)

async def set_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ACTIVE_MODEL
    if not context.args:
        await update.message.reply_text(
            "Gunakan format: `/setmodel nama_model`\n\nModel tersedia:\n" + "\n".join(GROQ_MODELS)
        )
        return

    model_name = context.args[0]
    if model_name in GROQ_MODELS:
        ACTIVE_MODEL = model_name
        await update.message.reply_text(f"✅ Model di-set ke: `{ACTIVE_MODEL}`")
    else:
        await update.message.reply_text(
            f"❌ Model `{model_name}` tidak ada.\nModel tersedia:\n" + "\n".join(GROQ_MODELS)
        )

async def my_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ACTIVE_MODEL
    if ACTIVE_MODEL:
        await update.message.reply_text(f"🔎 Model aktif saat ini: `{ACTIVE_MODEL}`")
    else:
        await update.message.reply_text(
            f"🔎 Tidak ada model khusus yang dipilih.\nBot akan pakai urutan default:\n" + "\n".join(GROQ_MODELS)
        )

async def list_models(update: Update, context: ContextTypes.DEFAULT_TYPE):
    models = "\n".join(GROQ_MODELS)
    await update.message.reply_text("📋 Daftar model tersedia:\n" + models)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)
    try:
        if isinstance(update, Update) and update.effective_message:
            await update.effective_message.reply_text("Ups, ada error di bot. Coba lagi ya 🙏")
    except Exception:
        pass

# ================== MAIN ==================
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("ai", cmd_ai))
    app.add_handler(CommandHandler("setmodel", set_model))
    app.add_handler(CommandHandler("mymodel", my_model))
    app.add_handler(CommandHandler("listmodels", list_models))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))
    app.add_error_handler(error_handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
