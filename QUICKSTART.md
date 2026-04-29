# 🚀 Quick Start Guide

Get up and running with the AI Trading Bot in 5 minutes!

## ⚡ Fast Setup

### Step 1: Install Dependencies (2 minutes)

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Step 2: Configure Credentials (2 minutes)

1. Open `.env` file in a text editor
2. Add your Robinhood credentials:

```env
ROBINHOOD_USERNAME=your_email@example.com
ROBINHOOD_PASSWORD=your_password
ROBINHOOD_TOTP_SECRET=your_totp_secret  # Optional: for 2FA

# IMPORTANT: Keep paper trading enabled for testing!
ENABLE_PAPER_TRADING=True
```

💡 **Don't have TOTP secret?** See [ROBINHOOD_SETUP.md](ROBINHOOD_SETUP.md) for detailed instructions.

### Step 3: Start Trading (1 minute)

**Linux/macOS:**
```bash
./start_server.sh
```

**Windows:**
```cmd
start_server.bat
```

**Or manually:**
```bash
source venv/bin/activate  # Activate virtual environment
python api_server.py      # Start server
```

### Step 4: Open Web Interface

1. Open `index.html` in your browser
2. Click "Start Simulation"
3. Watch your AI trade! 🤖📈

## 🎯 What You'll See

### Server Console
```
==================================================
🤖 AI Trading Bot API Server Starting
==================================================
Starting API server on port 5000
Paper Trading Mode: True
✅ Successfully authenticated with Robinhood
Account value: $10,000.00
```

### Web Interface
- Real-time portfolio value
- Current holdings
- Trade execution log
- AI decision explanations
- Circuit breaker status

## 🧪 Testing Checklist

- [ ] Server starts without errors
- [ ] Authentication succeeds
- [ ] "Paper Trading Mode" is active
- [ ] Trades show "📝 PAPER TRADE" in logs
- [ ] Circuit breaker is active
- [ ] Emergency stop button works

## ⚠️ Important Notes

### Paper Trading Mode
- **Enabled by default** for safety
- Simulates trades without real money
- Perfect for testing algorithms
- Shows what would happen in real trading

### Safety Features
- **Circuit Breaker**: Stops trading if limits exceeded
- **Daily Trade Limit**: Max 50 trades per day (configurable)
- **Position Size Limit**: Max 15% per position (configurable)
- **Daily Loss Limit**: Stops if loss exceeds 5% (configurable)
- **Emergency Stop**: Manual override button

### Before Real Trading

⚠️ **DO NOT disable paper trading until:**
1. You've tested thoroughly
2. You understand all algorithms
3. You've reviewed all safety limits
4. You're comfortable with potential losses
5. You've read all documentation

## 🐛 Common Issues

### "Backend server not running"
**Fix:** Make sure `api_server.py` is running in a terminal

### "Authentication failed"
**Fix:** Check credentials in `.env` file

### "Module not found"
**Fix:** Activate virtual environment: `source venv/bin/activate`

### "Port 5000 already in use"
**Fix:** Change `FLASK_PORT` in `.env` or stop other services on port 5000

## 📚 Next Steps

1. **Read the full documentation**: [README.md](README.md)
2. **Configure Robinhood properly**: [ROBINHOOD_SETUP.md](ROBINHOOD_SETUP.md)
3. **Understand the algorithms**: See README Algorithm Details section
4. **Customize safety limits**: Edit `.env` file
5. **Monitor performance**: Watch the dashboard metrics

## 🆘 Need Help?

- **Detailed Setup**: See [ROBINHOOD_SETUP.md](ROBINHOOD_SETUP.md)
- **Full Documentation**: See [README.md](README.md)
- **Troubleshooting**: Check server logs and `trading_bot.log`
- **Issues**: Report on GitHub

## ⚖️ Legal Disclaimer

This software is for **educational purposes only**. Trading involves substantial risk of loss. The authors are not responsible for any financial losses. Always consult with qualified financial advisors before making investment decisions.

**USE AT YOUR OWN RISK.**

---

**Happy Trading! 🚀📈**

Remember: Start with paper trading, test thoroughly, and never risk more than you can afford to lose!
