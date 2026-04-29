"""
Configuration Management for Robinhood Trading Bot
Loads environment variables and provides configuration settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Robinhood Credentials
    ROBINHOOD_USERNAME = os.getenv('ROBINHOOD_USERNAME')
    ROBINHOOD_PASSWORD = os.getenv('ROBINHOOD_PASSWORD')
    ROBINHOOD_MFA_CODE = os.getenv('ROBINHOOD_MFA_CODE', '')
    ROBINHOOD_TOTP_SECRET = os.getenv('ROBINHOOD_TOTP_SECRET', '')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Safety Limits
    MAX_DAILY_TRADES = int(os.getenv('MAX_DAILY_TRADES', 50))
    MAX_POSITION_SIZE_PERCENT = float(os.getenv('MAX_POSITION_SIZE_PERCENT', 15.0))
    MAX_DAILY_LOSS_PERCENT = float(os.getenv('MAX_DAILY_LOSS_PERCENT', 5.0))
    MIN_ACCOUNT_BALANCE = float(os.getenv('MIN_ACCOUNT_BALANCE', 1000.0))
    ENABLE_PAPER_TRADING = os.getenv('ENABLE_PAPER_TRADING', 'True').lower() == 'true'
    
    # Rate Limiting
    API_RATE_LIMIT = int(os.getenv('API_RATE_LIMIT', 60))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'trading_bot.log')
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        errors = []
        
        if not Config.ROBINHOOD_USERNAME:
            errors.append("ROBINHOOD_USERNAME is required")
        if not Config.ROBINHOOD_PASSWORD:
            errors.append("ROBINHOOD_PASSWORD is required")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
    
    @staticmethod
    def get_safety_limits():
        """Return safety limits as dictionary"""
        return {
            'max_daily_trades': Config.MAX_DAILY_TRADES,
            'max_position_size_percent': Config.MAX_POSITION_SIZE_PERCENT,
            'max_daily_loss_percent': Config.MAX_DAILY_LOSS_PERCENT,
            'min_account_balance': Config.MIN_ACCOUNT_BALANCE,
            'paper_trading_enabled': Config.ENABLE_PAPER_TRADING
        }
