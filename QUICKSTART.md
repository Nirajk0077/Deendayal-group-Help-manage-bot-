# Quick Start Guide

## ⚡ 5-Minute Setup

### Prerequisites
- Python 3.9+ installed
- MongoDB (local or Atlas)
- Telegram Bot Token (from @BotFather)

### Step 1: Get Credentials

**Bot Token:**
1. Open Telegram and search @BotFather
2. Send `/start`
3. Send `/newbot`
4. Follow instructions
5. Copy the token

**API Credentials:**
1. Go to https://my.telegram.org/
2. Login with your phone
3. Go to API development tools
4. Create new application
5. Copy API_ID and API_HASH

**MongoDB:**
- **Local:** Install MongoDB (see DEPLOYMENT.md)
- **Cloud:** Create free account at mongodb.com/cloud/atlas
- Copy connection string

### Step 2: Clone & Setup

```bash
# Clone repo
git clone https://github.com/yourusername/moderation-bot.git
cd moderation-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy .env template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

### Step 3: Configure .env

```env
BOT_TOKEN=your_bot_token_here
API_ID=12345678
API_HASH=abcdef1234567890
MONGO_URI=mongodb://localhost:27017  # or your Atlas URI
LOG_GROUP=-1001234567890
SUDO_USERS=123456789
```

### Step 4: Run Bot

```bash
python main.py
```

You should see:
```
✅ Database connected
✅ Bot commands setup completed
✅ All handlers registered successfully
🎯 Bot is now running
```

### Step 5: Test

1. Add bot to a group
2. Make bot admin
3. Try commands:
   - `/settings` - Open settings
   - `/help` - View help menu
   - `/filter hello` - Add filter
   - `/warn @user` - Warn user

## 🎯 Common Commands

### Admin Commands
```
/settings       - Configure group
/ban @user      - Ban user
/mute @user     - Mute user
/warn @user     - Warn user
/purge 10       - Delete 10 messages
```

### Filter Commands
```
/filter hello   - Add filter (reply with response)
/filters        - List all filters
/stop hello     - Remove filter
```

### Bad Word Filter
```
/addbadword bad     - Add bad word
/badwords           - List bad words
/antibadwords on    - Enable bad word filter
```

### Welcome/Goodbye
```
/setwelcome     - Set welcome (reply to message)
/setgoodbye     - Set goodbye
/welcome on     - Enable welcome
```

## 🔧 Troubleshooting

### "Database connection failed"
```bash
# Check MongoDB running
# If using local:
mongod

# If using Atlas:
# Verify connection string in .env
# Check whitelist IP in Atlas
```

### "Bot doesn't respond"
```bash
# Check bot token in .env
# Make sure bot is in group
# Make bot admin in group
# Check logs: tail -f bot.log
```

### "Can't delete messages"
```bash
# Make sure bot is admin
# Give bot permission: "Delete Messages"
# Try in a test group
```

## 📚 Documentation

- **README.md** - Full documentation
- **DEPLOYMENT.md** - Deployment guides
- **PROJECT_STRUCTURE.md** - Code structure
- **config.py** - Configuration options

## 🚀 Next Steps

1. **Customize Messages**
   - Edit MESSAGES in config.py
   - Add bot-specific replies

2. **Add Features**
   - Extend handlers for custom commands
   - Add new database collections

3. **Deploy**
   - Choose platform (Railway, Koyeb, VPS)
   - Follow DEPLOYMENT.md guide
   - Set up auto-restart

4. **Monitor**
   - Check logs regularly
   - Monitor database size
   - Track bot performance

## 💡 Tips

1. **Test Locally First**
   - Always test new features in local environment
   - Use test group before production

2. **Backup Database**
   - Regular MongoDB backups
   - Export important data

3. **Update Bot**
   - Keep Pyrogram updated
   - Monitor security patches

4. **Check Logs**
   - Review logs for errors
   - Fix issues immediately

## 🆘 Need Help?

- Check README.md for detailed docs
- Review DEPLOYMENT.md for setup issues
- Check PROJECT_STRUCTURE.md for code overview
- Look at examples in handler files

---

**Now your bot is ready! Start adding it to groups and enjoy advanced moderation! 🎉**
