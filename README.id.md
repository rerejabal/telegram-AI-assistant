
#### *Read with other languages:*  
[![English](https://raw.githubusercontent.com/gosquared/flags/master/flags/flags/shiny/24/United-States.png)](README.md)
[![Bahasa Indonesia](https://raw.githubusercontent.com/gosquared/flags/master/flags/flags/shiny/24/Indonesia.png)](README.id.md)
--------
<img width="1098" height="580" alt="image" src="https://github.com/user-attachments/assets/537eb22f-a774-45ac-b0e8-ab65741b4fd0" />

# Telegram AI Assistant

Telegram AI Assistant adalah chatbot Telegram yang memungkinkan kamu memanggil model AI canggih langsung di obrolanmu. Mendukung banyak penyedia (Groq, Llama, Gemma, Qwen, dll.) dengan fallback otomatis jika salah satu tidak tersedia.


---


## ✨ Fitur

- Mendukung grup, channel, dan chat pribadi
- Balasan multi-bahasa (Bahasa Indonesia ID & Bahasa Inggris EN)
- Deteksi bahasa otomatis atau pengaturan manual dengan /setlang
- Konfigurasi variabel lingkungan (.env)
- Model AI dapat dikustomisasi dengan /setmodel, /mymodel, /listmodels
- Sistem fallback model (mencoba model berikutnya jika satu gagal)
- Ringan & mudah digunakan (dependensi minimal)
- Mendukung format Markdown & code
- Kontrol percakapan dengan /start dan /end
- Penanganan error yang ramah pengguna


---


## 📦 Persyaratan
- Python 3.8+ (pastikan sudah terpasang)  
- pip (manajer paket Python)  
- Token dan username Bot Telegram (dari [@BotFather](https://t.me/BotFather))  
- GROQ API Key (https://console.groq.com/keys)
- Library yang dibutuhkan:  
  - `python-telegram-bot`  
  - `groq`  
  - `python-dotenv`
  - `langdetect`
  - `art`
  - `rich`
 
  
---


## 🤖 Menyiapkan Bot di Telegram

### 1. Mulai dengan BotFather
- Buka Telegram dan cari BotFather (akun resmi dengan centang biru).
- Buka chat lalu tekan `Start`

### 2. Buat Bot Baru
Ketik:
```
/newbot
```
diff
Copy
Edit
BotFather akan menanyakan:
- Nama Bot → nama tampilan (contoh: Crypto Hunter AI)
- Username → harus diakhiri dengan bot (contoh: crypto_hunter_bot)

Jika berhasil, BotFather akan membalas dengan:
```
Done! Congratulations on your new bot.
Use this token to access the HTTP API:
123456789:AAExampleTokenFromBotFather
```

> ⚠️ Token ini adalah kunci rahasia kamu, jangan dibagikan!

### 3. Kustomisasi Bot

Kamu dapat mengatur detail bot dengan perintah di BotFather:
- `/setname` → ubah nama bot
- `/setdescription` → ubah deskripsi bot
- `/setabouttext` → ubah info tentang bot
- `/setuserpic` → ubah foto profil bot
- `/setcommands` → ubah daftar perintah (contoh: /start - Mulai bot, /help - Tampilkan bantuan)
- `/deletebot` → hapus bot

### 4. Pengaturan Bot
- `/token` → dapatkan token otorisasi
- `/revoke` → cabut token akses bot
- `/setjoingroups` → apakah bot bisa ditambahkan ke grup? (Izinkan agar bot bisa digunakan di channel atau grup)
- `/setprivacy` → atur mode privasi di grup
  - Enable → bot hanya menerima pesan yang diawali dengan / (command).
  - Disable → bot bisa melihat semua pesan di grup (berguna untuk bot filter, auto-reply, moderasi).
 
### 5. Tambahkan Bot ke Grup atau Channel
- Buka grup kamu → Tambahkan bot.
- Jadikan Admin dan berikan izin yang diperlukan (hapus pesan, pin pesan, undang pengguna, dll.).

### 6. Hubungkan Bot Telegram dengan Script
- Tambahkan username bot Telegram ke file .env
- Tambahkan token bot Telegram ke file .env
> ⚠️ Sebelum itu, pastikan kamu sudah menyiapkan script bot di bawah ini!


---


## ⚙️ Menyiapkan Script Bot
> Klik kanan folder yang diinginkan, lalu pilih Open in Terminal atau PowerShell, atau bisa juga Command Prompt jika ada.
### 1. Clone repository ini di Terminal/PowerShell/Command Prompt:
```
git clone https://github.com/rerejabal/telegram-AI-assistant.git
cd telegram-AI-assistant
```
### 2. Install dependency:
```
pip install -r requirements.txt
```
### 3. Atur variabel lingkungan di `.env`:
> Klik kanan file .env lalu pilih Edit dengan Notepad atau aplikasi lain.
```
============== TELEGRAM BOT CONFIG ==============
BOT_USERNAME=
TELEGRAM_BOT_TOKEN=

============== GROQ CONFIG ==============
GROQ_API_KEY=

Daftar fallback models (pisahkan dengan koma, urutan prioritas)
GROQ_MODELS=llama-3.3-70b-versatile,llama3-70b-8192,llama3-8b-8192,gemma2-9b-it,qwen/qwen3-32b
```

---

## 📂 Struktur Folder
```
telegram-AI-assistant/
├── bot.py
├── .env
├── auto_start.bat
├── banner_utils.py
└── requirements.txt
```

---

## 🕹️ Cara Menggunakan
Setelah semuanya dikonfigurasi dengan benar, jalankan bot dengan:
```
python bot.py
```
Jika ingin cara yang lebih mudah, cukup jalankan file `auto_start.bat` yang ada di repository.

Sekarang kamu bisa berinteraksi dengan AI di Telegram.

- Chat Pribadi:
  - Bot akan otomatis merespons semua pesan setelah `/start` tanpa perlu mengetik `/ai`,`!ai` atau mention.

- Grup/Channel:
  - Bot hanya merespons jika dipicu dengan:
    - `/start` terlebih dahulu 
    - `/ai` <teks>
    - `!ai` <teks>
    - Mention @username_bot
    - Balas pesan bot

Daftar perintah di Telegram AI Assistant:

- `/start` → mulai obrolan dengan bot
- `/end` → akhiri obrolan dengan bot
- `/ai` <pertanyaan> → tanyakan ke AI
- `/setmodel` <nama_model> → pilih model secara manual
- `/mymodel` → periksa model mana yang sedang aktif
- `/listmodels` → lihat semua model yang tersedia
- `/setlang` id → ubah bahasa balasan ke Bahasa Indonesia
- `/setlang` en → ubah bahasa balasan ke Bahasa Inggris
- `!ai` <pertanyaan> → trigger alternatif di grup
- @botname <pertanyaan> → mention bot untuk memicu balasan di grup
- (balas pesan bot) → lanjutkan percakapan di grup

---


## 🗘 Update Bot
Update script kamu saat tersedia pembaruan:
```
git pull
```



