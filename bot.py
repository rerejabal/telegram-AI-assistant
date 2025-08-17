import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from groq import Groq

# ====== OPTIONAL: auto-detect language (fallback ke ID kalau lib tak ada) ======
try:
    from langdetect import detect as _lang_detect
except Exception:
    _lang_detect = None

# ====== RICH & ART BANNER ======
from art import text2art
from rich.console import Console
from rich.panel import Panel

console = Console()

# ================== LOAD ENV ==================
load_dotenv()

BOT_USERNAME_ENV = (os.getenv("BOT_USERNAME") or "").lower().strip()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ================== LIST MODEL (FALLBACK ORDER) ==================
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "gemma2-9b-it",
    "qwen/qwen3-32b",
]

ACTIVE_MODEL = None           # Model aktif
LANG_PREFS = {}              # bahasa pilihan per chat (id/en)
ACTIVE_CHATS = {}            # status aktif chat

# ================== TRANSLATIONS ==================
TRANSLATIONS = {
    "id": {
        "start": "Halo! 👋 Saya adalah AI bot.\n\n"
                 "Perintah:\n"
                 "/ai <pertanyaan> → tanya AI\n"
                 "/setmodel <nama_model> → pilih model AI\n"
                 "/mymodel → lihat model aktif\n"
                 "/listmodels → daftar model tersedia\n"
                 "/setlang <id|en> → ganti bahasa jawaban\n"
                 "/end → hentikan chat dengan bot\n\n"
                 "Default: Bahasa Indonesia",
        "end": "👋 Oke, chat dihentikan. Ketik /start untuk memulai lagi.",
        "setlang_usage": "Gunakan: /setlang <id|en>",
        "setlang_success_id": "✅ Bahasa diubah ke: Bahasa Indonesia",
        "setlang_success_en": "✅ Language set to: English",
        "setlang_invalid": "❌ Bahasa tidak valid. Pilih: id atau en",
        "ai_empty": "Ketik pertanyaan setelah `!ai` atau `/ai` ya 🙂",
        "ai_fail": "Maaf, semua model AI sedang tidak tersedia. Coba lagi sebentar ya 🙏",
        "setmodel_usage": "Gunakan format: `/setmodel nama_model`\n\nModel tersedia:\n",
        "setmodel_ok": "✅ Model di-set ke: ",
        "setmodel_invalid": "❌ Model tidak ada.\nModel tersedia:\n",
        "mymodel_none": "🔎 Tidak ada model khusus yang dipilih.\nBot akan pakai urutan default:\n",
        "mymodel_active": "🔎 Model aktif saat ini: ",
        "listmodels": "📋 Daftar model tersedia:\n",
        "error": "Ups, ada error di bot. Coba lagi ya 🙏",
    },
    "en": {
        "start": "Hello! 👋 I am an AI bot.\n\n"
                 "Commands:\n"
                 "/ai <question> → ask AI\n"
                 "/setmodel <model_name> → choose AI model\n"
                 "/mymodel → check active model\n"
                 "/listmodels → list available models\n"
                 "/setlang <id|en> → change reply language\n"
                 "/end → stop chatting with the bot\n\n"
                 "Default: English",
        "end": "👋 Okay, chat ended. Type /start to begin again.",
        "setlang_usage": "Usage: /setlang <id|en>",
        "setlang_success_id": "✅ Bahasa diubah ke: Bahasa Indonesia",
        "setlang_success_en": "✅ Language set to: English",
        "setlang_invalid": "❌ Invalid language. Choose: id or en",
        "ai_empty": "Type your question after `!ai` or `/ai` 🙂",
        "ai_fail": "Sorry, all AI models are currently unavailable. Please try again later 🙏",
        "setmodel_usage": "Usage: `/setmodel model_name`\n\nAvailable models:\n",
        "setmodel_ok": "✅ Model set to: ",
        "setmodel_invalid": "❌ Model not found.\nAvailable models:\n",
        "mymodel_none": "🔎 No specific model selected.\nBot will use default order:\n",
        "mymodel_active": "🔎 Current active model: ",
        "listmodels": "📋 Available models:\n",
        "error": "Oops, an error occurred in the bot. Please try again 🙏",
    }
}

def t(chat_id, key):
    lang = LANG_PREFS.get(chat_id, "id")
    return TRANSLATIONS[lang][key]

# ================== LOGGING ==================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ================== CLIENT ==================
groq_client = Groq(api_key=GROQ_API_KEY)

# ================== BANNER ==================
def show_banner():
    banner = text2art("        MYSTIC   BOT   SCRIPT", font="small")
    console.print(
        Panel(
            banner,
            title="🤖 Telegram AI Assistant",
            subtitle="by rerejabal",
            style="bold magenta",
        )
    )
    console.print(f"[cyan]Bot username:[/cyan] @{BOT_USERNAME_ENV or 'unknown'}")
    console.print(f"[yellow]Active models order:[/yellow]\n- " + "\n- ".join(GROQ_MODELS))

# ================== HANDLERS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    chat = update.effective_chat
    if not msg or not chat:
        return
    ACTIVE_CHATS[chat.id] = True
    await msg.reply_text(t(chat.id, "start"))

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    chat = update.effective_chat
    if not msg or not chat:
        return
    ACTIVE_CHATS[chat.id] = False
    await msg.reply_text(t(chat.id, "end"))

async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    chat = update.effective_chat
    if not msg or not chat:
        return

    if not context.args:
        await msg.reply_text(t(chat.id, "setlang_usage"))
        return

    lang = context.args[0].lower()
    if lang not in ["id", "en"]:
        await msg.reply_text(t(chat.id, "setlang_invalid"))
        return

    LANG_PREFS[chat.id] = lang
    await msg.reply_text(
        t(chat.id, "setlang_success_id") if lang == "id" else t(chat.id, "setlang_success_en")
    )

def _resolve_lang(chat_id: int, text: str) -> str:
    """Prioritaskan preferensi manual; kalau tidak ada, deteksi otomatis."""
    if LANG_PREFS.get(chat_id):
        return LANG_PREFS[chat_id]
    if _lang_detect:
        try:
            return "id" if _lang_detect(text).startswith("id") else "en"
        except Exception:
            pass
    return "id"  # default aman

async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    chat = update.effective_chat
    if not msg or not chat or not msg.text:
        return

    if not ACTIVE_CHATS.get(chat.id, True):
        return

    text = msg.text.strip()
    chat_type = chat.type  # "private", "group", "supergroup", "channel"
    lang = _resolve_lang(chat.id, text)
    system_prompt = "Jawab dalam bahasa Indonesia: " if lang == "id" else "Answer in English: "

    # Ambil username bot fallback dari context kalau env kosong/salah
    bot_username = (BOT_USERNAME_ENV or (getattr(context.bot, "username", "") or "")).lower()
    text_lower = text.lower()

    if chat_type == "private":
        is_triggered = True
        prompt = text
    else:
        is_command = text_lower.startswith("!ai") or text_lower.startswith("/ai")
        is_mention = (bot_username and f"@{bot_username}" in text_lower)
        is_reply_to_bot = (
            msg.reply_to_message
            and msg.reply_to_message.from_user
            and msg.reply_to_message.from_user.id == context.bot.id
        )

        is_triggered = is_command or is_mention or is_reply_to_bot
        prompt = (
            text.replace(f"@{bot_username}", "", 1) if bot_username else text
        ).replace("!ai", "", 1).replace("/ai", "", 1).strip()

    if not is_triggered or not prompt:
        if chat_type == "private":
            await msg.reply_text(t(chat.id, "ai_empty"))
        return

    ai_text = None
    last_error = None

    models_to_try = [ACTIVE_MODEL] if ACTIVE_MODEL else []
    models_to_try += [m for m in GROQ_MODELS if m != ACTIVE_MODEL]

    for model in models_to_try:
        try:
            resp = groq_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": system_prompt + prompt}],
                temperature=0.7,
                max_tokens=800,
            )
            ai_text = resp.choices[0].message.content if resp.choices else None
            if ai_text:
                logger.info(f"Sukses pakai model: {model}")
                break
        except Exception as e:
            last_error = e
            logger.warning(f"Model {model} gagal: {e}")

    if ai_text:
        await msg.reply_text(ai_text)
    else:
        logger.exception("Semua model gagal", exc_info=last_error)
        await msg.reply_text(t(chat.id, "ai_fail"))

async def cmd_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    chat = update.effective_chat
    if not msg or not chat:
        return
    prompt = " ".join(context.args)
    if not prompt:
        await msg.reply_text(t(chat.id, "ai_empty"))
        return
    # delegasi ke ai_reply (akan menangani bahasa & model)
    update.effective_message.text = prompt
    await ai_reply(update, context)

async def set_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    chat = update.effective_chat
    if not msg or not chat:
        return

    global ACTIVE_MODEL
    if not context.args:
        await msg.reply_text(t(chat.id, "setmodel_usage") + "\n".join(GROQ_MODELS))
        return

    model_name = context.args[0]
    if model_name in GROQ_MODELS:
        ACTIVE_MODEL = model_name
        await msg.reply_text(t(chat.id, "setmodel_ok") + f"`{ACTIVE_MODEL}`")
    else:
        await msg.reply_text(t(chat.id, "setmodel_invalid") + "\n".join(GROQ_MODELS))

async def my_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    chat = update.effective_chat
    if not msg or not chat:
        return

    global ACTIVE_MODEL
    if ACTIVE_MODEL:
        await msg.reply_text(t(chat.id, "mymodel_active") + f"`{ACTIVE_MODEL}`")
    else:
        await msg.reply_text(t(chat.id, "mymodel_none") + "\n".join(GROQ_MODELS))

async def list_models(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    chat = update.effective_chat
    if not msg or not chat:
        return
    await msg.reply_text(t(chat.id, "listmodels") + "\n".join(GROQ_MODELS))

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = None
    if isinstance(update, Update) and update.effective_chat:
        chat_id = update.effective_chat.id
    logger.error("Exception while handling an update:", exc_info=context.error)
    try:
        if isinstance(update, Update) and update.effective_message and chat_id:
            await update.effective_message.reply_text(t(chat_id, "error"))
    except Exception:
        pass

# ================== MAIN ==================
def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN belum di-set di .env")
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY belum di-set di .env")

    # tampilkan banner dulu
    show_banner()

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("end", end))
    app.add_handler(CommandHandler("setlang", set_lang))
    app.add_handler(CommandHandler("ai", cmd_ai))
    app.add_handler(CommandHandler("setmodel", set_model))
    app.add_handler(CommandHandler("mymodel", my_model))
    app.add_handler(CommandHandler("listmodels", list_models))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
