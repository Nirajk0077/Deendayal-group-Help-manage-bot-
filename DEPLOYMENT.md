# Advanced Deployment Guide

## 🚀 Deployment Options

### 1. Railway.app (Recommended)

**Pros:** Simple, free tier, MongoDB compatible
**Cons:** Limited resources

**Steps:**
1. Create Railway account
2. Create new project
3. Connect GitHub repo
4. Add environment variables:
   - `BOT_TOKEN` - Your bot token
   - `MONGO_URI` - MongoDB connection string
   - `API_ID`, `API_HASH` - From my.telegram.org
5. Deploy

**Environment Variables:**
```
BOT_TOKEN=your_token
API_ID=your_api_id
API_HASH=your_api_hash
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
LOG_GROUP=-1001234567890
SUDO_USERS=123456789
```

### 2. Koyeb

**Pros:** Good uptime, Docker support
**Cons:** Higher pricing

**Steps:**
1. Sign up at koyeb.com
2. Create new service
3. Choose Docker
4. Add your Dockerfile
5. Set environment variables
6. Deploy

### 3. Render.com

**Pros:** Good documentation
**Cons:** Lower free tier

**Steps:**
1. Create Render account
2. New Web Service
3. Connect GitHub
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
5. Set environment variables
6. Deploy

### 4. VPS (DigitalOcean, Linode, AWS EC2)

**Pros:** Full control, scalable
**Cons:** Requires Linux knowledge

**Setup on Ubuntu 22.04:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install MongoDB
curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Clone bot
git clone https://github.com/yourusername/moderation-bot.git
cd moderation-bot

# Create venv
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup .env
cp .env.example .env
nano .env  # Edit with credentials

# Run bot
python main.py

# Create systemd service (optional)
sudo nano /etc/systemd/system/modbot.service
```

**systemd Service File:**
```ini
[Unit]
Description=Telegram Moderation Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/moderation-bot
ExecStart=/path/to/venv/bin/python main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable modbot
sudo systemctl start modbot
sudo systemctl status modbot
```

### 5. Docker Deployment

**Using Docker Compose (Local):**

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your credentials
nano .env

# Build and run
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop
docker-compose down
```

**Manual Docker Build:**
```bash
# Build image
docker build -t moderation-bot:latest .

# Run container
docker run -d \
  --name modbot \
  -e BOT_TOKEN=your_token \
  -e MONGO_URI=your_mongo_uri \
  -e API_ID=your_api_id \
  -e API_HASH=your_api_hash \
  moderation-bot:latest

# View logs
docker logs -f modbot

# Stop container
docker stop modbot
docker rm modbot
```

### 6. Heroku (Legacy/Paid)

```bash
# Install Heroku CLI
# Windows: Download from heroku.com/downloads
# Linux: curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create your-bot-name

# Add buildpack
heroku buildpacks:add heroku/python

# Set environment variables
heroku config:set BOT_TOKEN=your_token
heroku config:set MONGO_URI=your_mongo_uri
heroku config:set API_ID=your_api_id
heroku config:set API_HASH=your_api_hash

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Scale
heroku ps:scale worker=1
```

## 📊 MongoDB Setup

### Option 1: Local MongoDB

**Installation:**
```bash
# Ubuntu
sudo apt-get install -y mongodb

# macOS
brew tap mongodb/brew
brew install mongodb-community

# Windows
Download from mongodb.com/download/community
```

**Connection String:**
```
mongodb://localhost:27017
```

### Option 2: MongoDB Atlas (Cloud)

**Setup:**
1. Go to mongodb.com/cloud/atlas
2. Create free account
3. Create cluster
4. Get connection string
5. Update .env:
```
MONGO_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

**Security:**
- Create database user
- Whitelist IPs
- Enable automatic backups

## 🔍 Monitoring & Maintenance

### Health Check
```bash
# Check if bot is running
curl -s http://localhost:8080/health

# View logs
tail -f bot.log

# Monitor database
mongo mongodb://localhost:27017/moderationbot
```

### Backup MongoDB

**Local Backup:**
```bash
# Full backup
mongodump --uri="mongodb://localhost:27017" --out backup/

# Restore
mongorestore --uri="mongodb://localhost:27017" backup/
```

**Atlas Backup:**
- Automatic hourly snapshots
- Manual snapshots available
- Export via Atlas UI

### Performance Monitoring

**Memory Usage:**
```bash
ps aux | grep python
```

**Database Queries:**
```bash
mongo
> db.currentOp()
> db.serverStatus()
```

## 🔐 Security Best Practices

1. **Environment Variables**
   - Never commit .env to git
   - Use strong MongoDB passwords
   - Rotate API credentials periodically

2. **Database Security**
   - Enable authentication
   - Whitelist IPs (Atlas)
   - Regular backups
   - Enable audit logging

3. **Bot Security**
   - Rate limiting enabled
   - Permission checking on all commands
   - Log suspicious activity
   - Regular updates

4. **Server Security**
   - Firewall enabled
   - SSH key authentication
   - Fail2ban installed
   - Regular patches

## 🆘 Troubleshooting

### Bot Won't Start
```bash
# Check Python version
python --version  # Should be 3.9+

# Check dependencies
pip list

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### MongoDB Connection Failed
```bash
# Check MongoDB running
sudo systemctl status mongod

# Check connection string
# Verify MONGO_URI in .env

# Test connection
python -c "import pymongo; pymongo.MongoClient('your_mongo_uri').admin.command('ping')"
```

### Bot Permissions Issues
```bash
# Make sure bot is admin in group
# Give bot these permissions:
- Delete messages
- Restrict members
- Pin messages
- Manage video chats
- Manage group settings
```

### High Memory Usage
```bash
# Check running processes
top

# Reduce workers in config.py
workers = 8  # Instead of 24

# Restart bot
systemctl restart modbot
```

## 📈 Scaling

### Single Bot Instance
- Supports unlimited groups
- ~100-200 groups recommended per instance
- ~150MB RAM usage

### Multiple Instances
Use multiple bots with same token (not recommended)
Or use separate tokens with load balancer

### Database Scaling
```javascript
// Create indexes for performance
db.group_settings.createIndex({ "group_id": 1 })
db.filters.createIndex({ "group_id": 1, "keyword": 1 })
db.badwords.createIndex({ "group_id": 1 })

// Add sharding for massive scale
sh.enableSharding("moderationbot")
sh.shardCollection("moderationbot.filters", { "group_id": 1 })
```

## 🔄 Updates & Maintenance

### Updating Code
```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Restart bot
systemctl restart modbot
```

### Database Migration
```bash
# Backup first
mongodump --uri="mongodb://localhost:27017" --out backup/

# Run migration scripts
python migrations/migrate_v1_to_v2.py

# Verify data
mongo localhost:27017/moderationbot
```

## 📞 Support & Debugging

### Enable Debug Logging
```python
# In config.py
logging.basicConfig(level=logging.DEBUG)
```

### Check Logs
```bash
# Last 100 lines
tail -n 100 bot.log

# Real-time
tail -f bot.log

# Search for errors
grep "ERROR" bot.log
```

### Report Issues
- Check GitHub issues
- Create detailed bug report
- Include logs and error messages
- Provide environment details
