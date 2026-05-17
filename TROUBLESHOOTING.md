# 🔧 TROUBLESHOOTING GUIDE

## ❌ Bot Not Responding to Commands

### Issue 1: API_ID / API_HASH Error

**Problem:**
```
❌ Missing credentials in .env file!
```

**Solution:**
```bash
1. Go to https://my.telegram.org
2. Login with your phone number
3. Click "API development tools"
4. Create new app (if not exists)
5. Copy App api_id → API_ID in .env
6. Copy App api_hash → API_HASH in .env
7. Save .env file
8. Restart bot
```

**Verify:**
```bash
# Before running bot, check .env
cat .env
# Should show:
# API_ID=123456789
# API_HASH=abc123xyz...
# BOT_TOKEN=987654321:ABC-XYZ...
```

---

## ❌ Bot Not Starting

### Issue 2: "No module named pyrogram"

**Problem:**
```
ModuleNotFoundError: No module named 'pyrogram'
```

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or install Pyrogram specifically
pip install pyrogram
pip install TgCrypto
pip install motor pymongo python-dotenv
```

**Verify:**
```bash
python -c "import pyrogram; print(pyrogram.__version__)"
# Should show: 2.0.106
```

---

### Issue 3: "Port Already in Use"

**Problem:**
```
Error: Port 8080 already in use
```

**Solution:**
```bash
# Kill existing bot
pkill -f "python bot_working.py"

# Or on Windows:
taskkill /F /IM python.exe

# Then restart
python bot_working.py
```

---

## ❌ MongoDB Connection Error

### Issue 4: "MongoDB Connection Failed"

**Problem:**
```
❌ MongoDB connection failed: connection refused
```

**Solution A - Local MongoDB:**
```bash
# Install MongoDB
# macOS:
brew install mongodb-community
brew services start mongodb-community

# Ubuntu:
sudo apt-get install mongodb
sudo systemctl start mongodb

# Windows:
# Download from mongodb.com and install
# Then run: mongod

# Verify:
mongosh localhost:27017
```

**Solution B - MongoDB Atlas (Cloud):**
```bash
# Go to mongodb.com/cloud/atlas
# Create free account
# Create cluster
# Get connection string
# In .env set:
MONGO_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

---

## ✅ How to Setup (Step by Step)

### Step 1: Get Credentials
```
A. API_ID & API_HASH:
   1. Visit https://my.telegram.org
   2. Login with phone
   3. Click "API development tools"
   4. Create app
   5. Copy api_id and api_hash

B. BOT_TOKEN:
   1. Open Telegram
   2. Search @BotFather
   3. Send /start
   4. Send /newbot
   5. Follow steps
   6. Copy token
```

### Step 2: Create .env File
```bash
# Copy example
cp .env.example .env

# Edit .env with your credentials
nano .env

# Add:
API_ID=123456789
API_HASH=abc123xyz
BOT_TOKEN=987654321:ABC-XYZ
MONGO_URI=mongodb://localhost:27017
```

### Step 3: Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 4: Start Bot
```bash
python bot_working.py
```

### Step 5: Test Bot
```
1. Open Telegram
2. Add bot to a group
3. Make bot admin
4. Type: /help
5. Bot should respond
```

---

## 🧪 Testing Commands

### Test 1: Check Bot is Alive
```bash
# In Telegram group, send:
/ping

# Bot should respond:
🏓 Pong!
```

### Test 2: Get IDs
```bash
# In Telegram group, send:
/id

# Bot should show:
User ID: 123456789
Chat ID: -1001234567890
Message ID: 42
```

### Test 3: Ban Command
```bash
1. Reply to a user's message
2. Send: /ban
3. Bot should ban the user (if you're admin)

Note: You must be group admin for this to work!
```

### Test 4: Help Menu
```bash
# In Telegram group, send:
/help

# Bot should show all available commands
```

---

## 🔍 Debugging

### Enable Debug Logging
```bash
# Add to bot_working.py:
import logging
logging.basicConfig(level=logging.DEBUG)

# Then run:
python bot_working.py 2>&1 | tee bot.log

# This will show all messages and errors
```

### Check Bot Status
```bash
# While bot is running, in another terminal:
ps aux | grep python

# Should show bot_working.py process running
```

### Test MongoDB Connection
```bash
# Open Python terminal:
python

# Test:
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
print(client.admin.command('ping'))
# Should print: {'ok': 1.0}
```

---

## ⚠️ Common Mistakes

### ❌ Mistake 1: Wrong Credentials
```
Wrong:
API_ID=my_api_id
API_HASH=my_api_hash
BOT_TOKEN=my_bot_token

Right:
API_ID=123456789
API_HASH=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
BOT_TOKEN=5555555555:AAHxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### ❌ Mistake 2: Using Example Credentials
```
Wrong:
cp .env.example .env
python bot_working.py
# Don't edit .env

Right:
cp .env.example .env
nano .env  # Edit with YOUR credentials
python bot_working.py
```

### ❌ Mistake 3: MongoDB Not Running
```
Wrong:
MONGO_URI=mongodb://localhost:27017
# MongoDB not started
python bot_working.py

Right:
mongod  # Start MongoDB first
# In another terminal:
python bot_working.py
```

### ❌ Mistake 4: Bot Not Admin
```
Wrong:
Add bot to group
Type /ban
Bot doesn't work

Right:
Add bot to group
Make bot admin (click "Administrators" → add bot)
Type /ban
Bot works!
```

---

## 💡 Quick Fixes

### Fix 1: "Token not valid"
```
# Get new token from @BotFather
# /start → /newbot → follow steps
# Copy NEW token
# Update .env
# Restart bot
```

### Fix 2: "Connection refused"
```
# MongoDB not running
# Start: mongod
# Or use MongoDB Atlas (cloud)
# Update MONGO_URI in .env
```

### Fix 3: "Bot stopped working"
```
# Check logs:
tail -f bot.log

# Restart bot:
pkill -f bot_working.py
python bot_working.py
```

### Fix 4: "Commands not working in DM"
```
# Some commands only work in groups
# Add bot to a group
# Make bot admin
# Try commands there
```

---

## 📞 Still Not Working?

### Check These:

1. **API_ID & API_HASH from my.telegram.org**
   ```bash
   echo "API_ID=$API_ID"
   echo "API_HASH=$API_HASH"
   # Should show numbers and hash, not YOUR_API_ID
   ```

2. **BOT_TOKEN from @BotFather**
   ```bash
   echo "BOT_TOKEN=$BOT_TOKEN"
   # Should show: 5555555555:AAHxxxxxxx
   # Not: YOUR_BOT_TOKEN
   ```

3. **MongoDB Running**
   ```bash
   mongosh localhost:27017
   # Should connect without errors
   ```

4. **Dependencies Installed**
   ```bash
   pip list | grep -i pyrogram
   # Should show: pyrogram 2.0.106
   ```

5. **No Spaces in .env**
   ```bash
   # Wrong:
   API_ID = 123456789
   
   # Right:
   API_ID=123456789
   ```

---

## ✅ Success Checklist

- ✅ .env file created with real credentials
- ✅ API_ID & API_HASH from my.telegram.org
- ✅ BOT_TOKEN from @BotFather
- ✅ Dependencies installed (pip install -r requirements.txt)
- ✅ MongoDB running or using Atlas
- ✅ Bot added to group
- ✅ Bot is admin in group
- ✅ python bot_working.py shows ✅ Bot connected
- ✅ /ping returns 🏓 Pong!
- ✅ /help returns command list
- ✅ /id returns user/chat IDs

---

## 🎯 If Everything Works

```
You should see:
==================================================
🚀 Starting Moderation Bot...
==================================================
✅ Credentials loaded successfully
✅ Pyrogram imported successfully
✅ Bot client initialized
📡 Connecting to Telegram...
✅ Bot connected to Telegram!
🎯 Bot is running and listening for commands...
==================================================
Available commands:
/start - Start bot
/help - Show help
/ping - Test bot
/id - Get IDs
/ban - Ban user (admin only)
/mute - Mute user (admin only)
/settings - Group settings
==================================================

Then bot will respond to all commands!
```

---

**If you follow this guide, your bot will work! 100%**
