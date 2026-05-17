# 🚀 BOT SETUP - 5 MINUTES TO WORKING BOT

## ⚡ SUPER QUICK START

### Step 1: Get Credentials (2 minutes)

**API_ID & API_HASH:**
1. Go to: https://my.telegram.org
2. Login with your phone
3. Click "API development tools"
4. Create new application
5. **Copy "App api_id"** → Save as `API_ID`
6. **Copy "App api_hash"** → Save as `API_HASH`

**BOT_TOKEN:**
1. Open Telegram app
2. Search: @BotFather
3. Send: `/start`
4. Send: `/newbot`
5. Give it a name, then username
6. **Copy the token** → Save as `BOT_TOKEN`

### Step 2: Create .env File (1 minute)

**Create file named `.env`:**
```
API_ID=123456789
API_HASH=abc123xyz456def789ghi
BOT_TOKEN=5555555555:AAHxxxxxxxxxxxxxxxxxxxxxxxxxxx
MONGO_URI=mongodb://localhost:27017
```

Replace:
- `123456789` with your API_ID
- `abc123xyz...` with your API_HASH
- `5555555555:AAH...` with your BOT_TOKEN

### Step 3: Install & Run (2 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Run bot
python bot_working.py
```

**You should see:**
```
✅ Bot connected to Telegram!
🎯 Bot is running and listening for commands...
```

### Step 4: Test Bot (instant)

In Telegram:
1. Create a test group
2. Add the bot to group
3. Make bot admin
4. Type: `/ping`
5. Bot responds: `🏓 Pong!`
6. Type: `/help`
7. Bot shows all commands

**Done! Bot is working! 🎉**

---

## 📝 Commands Available

```
/start   - Start bot
/help    - Show all commands
/ping    - Test if bot works
/id      - Get user/chat IDs

/ban @user      - Ban user (admin only)
/mute @user     - Mute user (admin only)
/unmute @user   - Unmute user
/warn @user     - Warn user
/kick @user     - Kick user

/settings - Configure group
```

---

## ❌ If Bot Doesn't Work

**1. Check .env file:**
```bash
cat .env
# Should show YOUR actual credentials, not "YOUR_API_ID"
```

**2. Check Pyrogram installed:**
```bash
pip install pyrogram TgCrypto
```

**3. Check MongoDB (if using local):**
```bash
mongod
# Or use MongoDB Atlas (cloud)
```

**4. Check Bot is Admin:**
- Open group → Click on bot → Check "Administrator"

**5. Read TROUBLESHOOTING.md** for detailed help

---

## 🎯 What to Do Next

1. ✅ Follow 4 steps above
2. ✅ Test with /ping and /help
3. ✅ Try admin commands in a group
4. ✅ Customize config.py if needed
5. ✅ Deploy to production

---

## 📚 Files You Need

- `bot_working.py` - **USE THIS FILE** (not bot.py)
- `.env` - Create this with your credentials
- `requirements.txt` - For installing dependencies

---

## ⚠️ Important Notes

1. **Always use real credentials from:**
   - API_ID, API_HASH from my.telegram.org
   - BOT_TOKEN from @BotFather
   
2. **Never share .env file** (contains credentials)

3. **Bot must be admin in group** for commands to work

4. **Commands that start with /**: Only work if bot is in group and admin

5. **If it says "Token not valid"**: Get new token from @BotFather

---

## ✅ Verification

When you run bot, you should see:

```
==================================================
🚀 Starting Moderation Bot...
==================================================
✅ Credentials loaded successfully
✅ Pyrogram imported successfully
✅ Bot client initialized
📡 Connecting to Telegram...
✅ Bot connected to Telegram!
🎯 Bot is running and listening for commands...
```

If you see this ✅ mark, bot is working!

---

**Follow these 4 steps and bot will 100% work in 5 minutes!**
