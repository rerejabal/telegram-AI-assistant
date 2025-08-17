# Telegram AI Assistant

Telegram AI Assistant is a Telegram chatbot that lets you summon powerful AI models directly in your chat. It supports multiple providers (Groq, Llama, Gemma, Qwen, etc.) with automatic fallback when one is unavailable.

---

## ✨ Features

- Supports group and private chat  
- Environment variable configuration (.env)  
- Markdown & code formatting support  
- Lightweight & easy to deploy
  - Call AI using:
  - `/ai` command  
  - `!ai` shortcut  
  - Mention bot username  
  - Replying to a message
    
---
## 📦 Requirements
- Python 3.8+ (make sure it's installed)  
- pip (Python package manager)  
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))  
- An GROQ API Key https://console.groq.com/keys
- Required Libraries:  
  - `python-telegram-bot`  
  - `groq`  
  - `python-dotenv`
---
## 📂 Folder Structure
```
telegram-AI-assistant/
 ├── bot.py
 ├── .env
 ├── auto_start.bat
 └── requirements.txt
```
---
## ⚙️ Setup
> Right-click the desired folder location, then select Open in Terminal or PowerShell or even Command Prompt if available.
### 1. Clone this repository on Terminal or PowerShell or Command Prompt:
```
git clone https://github.com/your-username/ai-chat-bot.git
cd ai-chat-bot
```
### 2. Install dependency:
```
pip install -r requirements.txt
```
### 3. Set your environment variables in `.env`:
> Right-click on the .env file then select Edit in Notepad or anything.
```
# ============== TELEGRAM BOT CONFIG ==============
BOT_USERNAME=
TELEGRAM_BOT_TOKEN=

# ============== GROQ CONFIG ==============
GROQ_API_KEY=

# List of fallback models (separated by commas, priority order)
GROQ_MODELS=llama-3.3-70b-versatile,llama3-70b-8192,llama3-8b-8192,gemma2-9b-it,qwen/qwen3-32b

# Default language instruction for the AI
DEFAULT_LANG_PROMPT=Answer in Indonesian:
```
---
## ▶️ Usage
Once everything is configured properly, start the bot with:
```
python bot.py
```
If you prefer a simpler way to run, you can run the `auto_start.bat` file provided in the repository.

Now you can interact with AI in Telegram, for example:
> You can interact with the bot using /ai, !ai, mentions, or by replying to a message.
- /ai hello world
- !ai write me a poem
- @yourbotusername explain quantum physics
- Reply to any message with /ai to get a smart response

Command in Telegram:
- /ai question → ask AI
- /setmodel model_name → manually select a model
- /mymodel → check which model is currently active
- /listmodels → see all available models

---
## 🔄 Update the Bot
Update your Script when its availabe:
```
git pull
```
