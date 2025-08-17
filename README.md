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
- A Telegram Bot Token and username (from [@BotFather](https://t.me/BotFather))  
- GROQ API Key (https://console.groq.com/keys)
- Required Libraries:  
  - `python-telegram-bot`  
  - `groq`  
  - `python-dotenv`
---
## Setting up your Bot in Telegram

### 1. Start BotFather
- Open Telegram and search for BotFather (official account with blue check).
- Open chat and press `Start`

### 2. Create a New Bot
Type:
```
/newbot
```
BotFather will ask for:
- Bot Name → display name (e.g., Crypto Hunter AI)
- Username → must end with bot (e.g., crypto_hunter_bot)

If successful, BotFather replies with:
```
Done! Congratulations on your new bot. 
Use this token to access the HTTP API:
123456789:AAExampleTokenFromBotFather
```
> ⚠️This token is your secret key, do not share it!

### 3. Customize Your Bot

You can set details with commands in BotFather:
- `/setname` → change a bot's name
- `/setdescription` → change bot description
- `/setabouttext` → change bot about info
- `/setuserpic` → change bot profile photo
- `/setcommands` → change the list of commands (e.g. /start - Start the bot, /help - Show help)
- `/deletebot` → delete a bot

### 4. Setting Your Bot
- `/token` → get authorization token
- `/revoke` → revoke bot access token
- `/setjoingroups` → can your bot be added to groups? (Allow you to assign the bot to channel or group)
- `/setprivacy` → toggle privacy mode in groups
  - Enable → bot only receives messages starting with / (commands).
  - Disable → bot can see all messages in groups (useful for filter bots, auto-reply, moderation).
 
### 5. Add Bot to a Group or Channel
- Open your group → Add your bot.
- Promote it to Admin and grant the necessary permissions (delete messages, pin messages, invite users, etc.).

### 6. Connect Telegram Bot with Bot Script
- Add your Telegram bot username to .env
- Add your Telegram bot token to .env
> ⚠️Before that, let’s set up the bot script first below!

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
## 📂 Folder Structure
```
telegram-AI-assistant/
 ├── bot.py
 ├── .env
 ├── auto_start.bat
 └── requirements.txt
```
 ---
## ▶️ Usage
Once everything is configured properly, start the bot with:
```
python bot.py
```
If you prefer a simpler way to run, you can run the `auto_start.bat` file provided in the repository.

Now you can interact with AI in Telegram.

- Private Chat:
  - The bot automatically responds to all messages after `/start` without requiring the `/ai`,`!ai` command or a mention.

- Group/Channel:
  - The bot only responds when triggered with:
    - `/ai` <teks>
    - `!ai` <teks>
    - Mention @username_bot
    - Reply ke pesan bot

All command in Telegram AI Assistant:

- `/start` → start chatting with the bot
- `/end` → stop chatting with the bot
- `/ai` <question> → ask AI
- `/setmodel` <model_name> → manually select a model
- `/mymodel` → check which model is currently active
- `/listmodels` → see all available models
- `/setlang` id → switch reply language to Indonesian 🇮🇩
- `/setlang` en → switch reply language to English 🇬🇧
- `!ai` <question> → alternative AI trigger in groups
- @botname <question> → mention bot to trigger reply in groups
- (reply to bot message) → continue conversation in groups

---
## 🔄 Update the Bot
Update your Script when its availabe:
```
git pull
```


