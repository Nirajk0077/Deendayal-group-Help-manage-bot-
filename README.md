# 🤖 Advanced Telegram Moderation Bot

A professional-grade Rose Bot + Support Bot hybrid with advanced moderation, unlimited filters, word filtering, and comprehensive admin controls.

## ✨ Features

### 🔐 Security & Moderation
- **Anti-Link** - Remove messages containing URLs
- **Anti-Forward** - Delete forwarded messages
- **Anti-BadWords** - Word filtering with unlimited bad word list
- **Lock System** - Lock links, forwards, media, stickers, bots
- **Warning System** - Warn users with customizable limits
- **Ban/Mute** - Restrict user access

### 📝 Filters & Notes
- **Unlimited Filters** - Custom keyword responses
- **Hashtag Triggers** - `#repo`, `#rules`, `#help` style
- **Saved Notes** - Quick retrieval with `/get`
- **Button Support** - Add inline buttons to responses
- **Markdown Support** - Full text formatting

### 👋 Welcome & Goodbye
- **Custom Messages** - Personalized join/leave messages
- **Variables** - `{user}`, `{group}`, `{member_count}`, etc
- **Toggle Control** - Enable/disable as needed

### ⚙️ Settings Panel (Rose-Style)
- **Inline Menu** - Beautiful button-based settings
- **Category Groups** - Security, Filters, Admin, Welcome
- **Quick Toggles** - Single-click enable/disable
- **Per-Group Config** - Different settings per group

### 👨‍💼 Admin Tools
- `/ban` - Ban user
- `/unban` - Unban user
- `/mute` - Mute user
- `/unmute` - Unmute user
- `/warn` - Add warning
- `/promote` - Make admin
- `/demote` - Remove admin
- `/purge` - Delete messages
- `/pin` - Pin message
- `/id` - Get IDs
- `/info` - User information

### 📊 Reports
- `/report` - Report messages to admins
- Admin notifications
- Toggle reporting on/off

### 💾 Database
- **MongoDB** - Reliable data storage
- **Per-Group Settings** - Isolated configurations
- **Unlimited Data** - No message limits
- **Fast Queries** - Optimized for speed

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- MongoDB (local or cloud)
- Telegram Bot Token (from @BotFather)
- API_ID & API_HASH (from my.telegram.org)

### Installation

1. **Clone/Download the bot**
```bash
git clone https://github.com/yourusername/moderation-bot.git
cd moderation-bot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Run the bot**
```bash
python -m bot
```

## 📝 Configuration

### .env File
```env
BOT_TOKEN=your_token_here
API_ID=12345678
API_HASH=your_api_hash
MONGO_URI=mongodb://localhost:27017
SUDO_USERS=123456789
LOG_GROUP=-1001234567890
```

### Bot Variables
Edit `config.py` to customize:
- Default settings
- Regex patterns
- Messages
- Collections

## 📚 Command Guide

### Filters & Notes
```
/filter <keyword>     - Add filter (reply with response)
/stop <keyword>       - Remove filter
/filters             - List all filters
/stopall             - Clear all filters
/save <name>         - Save note (reply with content)
/get <name>          - Retrieve note
/notes               - List all notes
```

### Bad Words
```
/addbadword <word>   - Add bad word
/removebadword <word> - Remove bad word
/badwords            - List bad words
/clearbadwords       - Clear all bad words
/antibadwords on/off - Toggle filter
```

### Security
```
/antilink on/off     - Toggle link removal
/antiforward on/off  - Toggle forward removal
/report              - Report message
```

### Welcome/Goodbye
```
/setwelcome          - Set welcome (reply to message)
/welcome on/off      - Toggle welcome
/clearwelcome        - Clear welcome
/setgoodbye          - Set goodbye
/goodbye on/off      - Toggle goodbye
/cleargoodbye        - Clear goodbye
```

### Admin Tools
```
/ban @user           - Ban user
/unban <id>          - Unban user
/mute @user          - Mute user
/unmute @user        - Unmute user
/warn @user [reason] - Warn user
/warns @user         - Check warnings
/resetwarn @user     - Reset warnings
/promote @user       - Make admin
/demote @user        - Remove admin
/purge <count>       - Delete messages
/pin                 - Pin message
/unpin               - Unpin message
/id                  - Get IDs
/info @user          - User info
```

### Settings
```
/settings            - Open settings panel
```

## 🔧 MongoDB Setup

### Local MongoDB
```bash
# Install MongoDB
# Windows: Download from mongodb.com
# Linux: sudo apt-get install mongodb

# Start MongoDB
mongod

# Connection string
MONGO_URI=mongodb://localhost:27017
```

### MongoDB Atlas (Cloud)
1. Create account at mongodb.com/atlas
2. Create cluster
3. Get connection string
4. Update .env:
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

## 🌐 Deployment

### Railway
1. Create account at railway.app
2. Connect GitHub repo
3. Add environment variables
4. Deploy

### Koyeb
1. Create account at koyeb.com
2. Connect GitHub
3. Set environment vars
4. Deploy

### Render
1. Create account at render.com
2. Create web service
3. Connect GitHub repo
4. Add .env variables
5. Deploy

### Heroku (Legacy)
```bash
heroku login
heroku create your-bot-name
heroku config:set BOT_TOKEN=your_token
heroku config:set MONGO_URI=your_mongo_uri
git push heroku main
```

### Docker
```bash
docker build -t moderation-bot .
docker run -d --env-file .env moderation-bot
```

## 📊 Database Structure

### Collections

**group_settings**
```json
{
  "group_id": -1001234567890,
  "anti_link": true,
  "anti_forward": false,
  "anti_badwords": true,
  "welcome_enabled": true,
  "filter_mode": "partial",
  "warn_limit": 3
}
```

**filters**
```json
{
  "group_id": -1001234567890,
  "keyword": "hello",
  "response": "Hello there!",
  "buttons": [],
  "created_at": "2024-01-01T00:00:00Z"
}
```

**badwords**
```json
{
  "group_id": -1001234567890,
  "words": ["badword1", "badword2"]
}
```

**notes**
```json
{
  "group_id": -1001234567890,
  "name": "rules",
  "content": "Group rules here",
  "created_at": "2024-01-01T00:00:00Z"
}
```

## ⚙️ Settings Panel

### Main Settings
- 🔗 Anti-Link (ON/OFF)
- ↩️ Anti-Forward (ON/OFF)
- 🎯 Anti-BadWords (ON/OFF)
- 👋 Welcome (ON/OFF)
- 👋 Goodbye (ON/OFF)
- 🚨 Reports (ON/OFF)

### Locks
- 🔗 Links
- ↩️ Forwards
- 📸 Media
- 🎨 Stickers
- 🤖 Bots

### Advanced
- ⚠️ Warn Limit (1-10)
- 🔎 Filter Mode (exact/partial)
- 📌 Punishment (delete/warn/mute/ban)

## 🛡️ Permission System

### Group Admin Commands
- All settings changes
- Filter management
- Note saving
- Welcome/Goodbye setup
- Admin actions (ban, mute, etc)
- Warning system

### Everyone
- Trigger filters/notes
- Use `/report`
- View help

### Bot Requirements
- Delete messages
- Restrict members
- Pin messages
- Manage video chats

## 🐛 Troubleshooting

### Bot doesn't respond
- Check BOT_TOKEN
- Verify bot is in group
- Check /start in private

### MongoDB connection error
- Verify MONGO_URI
- Check MongoDB running
- Test connection string

### Can't delete messages
- Bot needs admin rights
- Bot needs "Delete Messages" permission
- Check group settings

### Filters not working
- Check filter keyword
- Verify settings enabled
- Check filter case sensitivity

## 📈 Performance Tips

1. **Database Indexing**
```javascript
db.group_settings.createIndex({ "group_id": 1 })
db.filters.createIndex({ "group_id": 1, "keyword": 1 })
db.badwords.createIndex({ "group_id": 1 })
```

2. **Async Optimization**
- All operations are async
- FloodWait handling included
- Batch operations supported

3. **Rate Limiting**
- FLOODWAIT = 0.1 seconds
- MAX_RETRIES = 3
- Auto reconnect enabled

## 🔐 Security

- Permission verification on every command
- Group-only admin controls
- SUDO user override support
- No PII stored unnecessarily
- SQL injection protection (using MongoDB)

## 📄 License

MIT License - See LICENSE file

## 🤝 Contributing

Pull requests welcome! Please ensure:
- Code follows existing style
- All features tested
- No hardcoded values
- Proper error handling

## 📞 Support

- GitHub Issues
- Telegram support group
- Documentation wiki

## 🎯 Roadmap

- [ ] Redis caching layer
- [ ] Custom admin roles
- [ ] Moderation logs
- [ ] Statistics dashboard
- [ ] API integration
- [ ] Multi-language support

## 🙏 Credits

Inspired by:
- Rose Bot (@RoseBot)
- Support Group Bots
- Pyrogram library

---

**Made with ❤️ by DevTeam**

**Version:** 1.0.0  
**Last Updated:** 2024-01-01  
**Python:** 3.9+  
**Pyrogram:** 2.0+
