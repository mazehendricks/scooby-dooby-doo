# 🔐 Robinhood API Setup Guide

This guide will help you set up your Robinhood account for API access and configure the trading bot safely.

## 📋 Prerequisites

1. **Active Robinhood Account**
   - Sign up at [robinhood.com](https://robinhood.com)
   - Complete account verification
   - Fund your account (start small for testing!)

2. **Two-Factor Authentication (2FA)**
   - Enable 2FA in Robinhood security settings
   - Choose either:
     - **Authenticator App** (recommended): Google Authenticator, Authy, etc.
     - **SMS**: Text message codes

## 🔑 Getting Your Credentials

### 1. Username and Password

Your Robinhood login credentials:
- **Username**: Your email address
- **Password**: Your account password

⚠️ **Security Best Practices:**
- Use a strong, unique password
- Never share your credentials
- Store them securely (password manager recommended)

### 2. Two-Factor Authentication Setup

#### Option A: TOTP (Authenticator App) - Recommended

1. Go to Robinhood → Settings → Security
2. Enable "Two-Factor Authentication"
3. Choose "Authenticator App"
4. **IMPORTANT**: When shown the QR code, also click "Can't scan?" to reveal the secret key
5. Copy the **TOTP secret key** (long alphanumeric string)
6. Add this to your `.env` file:
   ```env
   ROBINHOOD_TOTP_SECRET=YOUR_SECRET_KEY_HERE
   ```

#### Option B: SMS Codes

1. Enable SMS-based 2FA in Robinhood
2. Leave `ROBINHOOD_TOTP_SECRET` empty in `.env`
3. You'll need to enter the SMS code manually when prompted

## ⚙️ Configuration

### 1. Create `.env` File

Copy the example file:
```bash
cp .env.example .env
```

### 2. Edit `.env` with Your Credentials

```env
# Your Robinhood login
ROBINHOOD_USERNAME=your_email@example.com
ROBINHOOD_PASSWORD=your_secure_password

# TOTP Secret (if using authenticator app)
ROBINHOOD_TOTP_SECRET=ABCD1234EFGH5678IJKL

# Or leave empty for SMS
ROBINHOOD_MFA_CODE=

# Flask Configuration
FLASK_SECRET_KEY=generate_a_random_secret_key_here
FLASK_PORT=5000
FLASK_DEBUG=False

# CRITICAL: Start with paper trading!
ENABLE_PAPER_TRADING=True

# Safety Limits
MAX_DAILY_TRADES=50
MAX_POSITION_SIZE_PERCENT=15.0
MAX_DAILY_LOSS_PERCENT=5.0
MIN_ACCOUNT_BALANCE=1000.0

# Rate Limiting
API_RATE_LIMIT=60

# Logging
LOG_LEVEL=INFO
LOG_FILE=trading_bot.log
```

### 3. Generate a Secure Flask Secret Key

```python
# Run this in Python to generate a secure key
import secrets
print(secrets.token_hex(32))
```

Copy the output to `FLASK_SECRET_KEY` in your `.env` file.

## 🧪 Testing Your Setup

### 1. Test Authentication

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Start the server
python api_server.py
```

Look for:
```
✅ Successfully authenticated with Robinhood
Account value: $X,XXX.XX
```

### 2. Test Paper Trading

1. Open `index.html` in your browser
2. Click "Start Simulation"
3. Watch for "📝 PAPER TRADING MODE" messages in the server console
4. Verify trades are logged but not executed

### 3. Verify Circuit Breaker

1. Check the circuit breaker status in the UI
2. Try triggering the emergency stop button
3. Verify trading stops immediately

## 🛡️ Safety Checklist

Before enabling real trading, ensure:

- [ ] ✅ Paper trading works correctly
- [ ] ✅ All algorithms behave as expected
- [ ] ✅ Circuit breaker triggers properly
- [ ] ✅ Safety limits are appropriate for your risk tolerance
- [ ] ✅ You understand all algorithm behaviors
- [ ] ✅ You've reviewed all code
- [ ] ✅ You're starting with a small amount
- [ ] ✅ You can afford to lose the entire amount
- [ ] ✅ You've read all documentation
- [ ] ✅ You understand the risks

## ⚠️ Important Warnings

### Legal and Financial Risks

1. **Not Financial Advice**: This is educational software only
2. **Regulatory Compliance**: Ensure compliance with SEC, FINRA regulations
3. **Market Risk**: You can lose money, potentially all of it
4. **Algorithm Risk**: AI systems can behave unpredictably
5. **Technical Risk**: Bugs, network issues, API changes can cause losses

### Technical Limitations

1. **Latency**: Retail API access has delays (not suitable for HFT)
2. **Rate Limits**: Robinhood limits API calls (60/minute default)
3. **Market Hours**: Only works during market hours (9:30 AM - 4:00 PM ET)
4. **Pattern Day Trading**: Be aware of PDT rules (4+ day trades in 5 days requires $25k)
5. **Execution**: Market orders may have slippage

### Security Considerations

1. **Credential Storage**: `.env` file contains sensitive data
2. **Network Security**: API calls are over HTTPS but local server is HTTP
3. **Session Management**: Robinhood sessions are stored locally
4. **Access Control**: No authentication on the web interface
5. **Logging**: Credentials may appear in logs if DEBUG=True

## 🔧 Troubleshooting

### "Login Failed" Error

**Possible causes:**
- Incorrect username/password
- 2FA code expired or incorrect
- Robinhood account locked
- Too many login attempts

**Solutions:**
1. Verify credentials in `.env`
2. Check 2FA setup (TOTP secret or SMS)
3. Try logging in manually on robinhood.com
4. Wait 15 minutes if rate limited
5. Check for Robinhood service outages

### "MFA Required" Error

**Solution:**
- If using TOTP: Verify `ROBINHOOD_TOTP_SECRET` is correct
- If using SMS: Enter code when prompted
- Ensure time sync is correct (TOTP is time-based)

### "Session Expired" Error

**Solution:**
- Restart the API server
- Delete cached session files (`.tokens/` directory)
- Re-authenticate

### "Rate Limit Exceeded" Error

**Solution:**
- Reduce `API_RATE_LIMIT` in `.env`
- Increase `tradingSpeed` in the UI
- Wait for rate limit to reset (usually 1 minute)

## 📚 Additional Resources

### Robinhood API Documentation
- [robin-stocks Documentation](https://robin-stocks.readthedocs.io/)
- [Robinhood API Unofficial Docs](https://github.com/sanko/Robinhood)

### Trading Regulations
- [SEC Pattern Day Trading Rules](https://www.sec.gov/fast-answers/answerspatterndaytraderhtm.html)
- [FINRA Day Trading Rules](https://www.finra.org/investors/learn-to-invest/advanced-investing/day-trading-margin-requirements-know-rules)

### Security Best Practices
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

## 🆘 Getting Help

If you encounter issues:

1. **Check Logs**: Review `trading_bot.log` for detailed errors
2. **Console Output**: Check terminal where `api_server.py` is running
3. **GitHub Issues**: Report bugs on the project repository
4. **Robinhood Support**: Contact for account-specific issues

## ⚖️ Legal Disclaimer

This software is provided "as is" without warranty of any kind. The authors and contributors are not responsible for any financial losses, damages, or legal issues arising from the use of this software. Trading stocks involves substantial risk of loss. Past performance does not guarantee future results. Always consult with qualified financial advisors before making investment decisions.

**USE AT YOUR OWN RISK.**
