"""
Robinhood API Client
Handles authentication and trading operations with Robinhood
"""

import logging
import robin_stocks.robinhood as rh
import pyotp
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from config import Config
from circuit_breaker import circuit_breaker

logger = logging.getLogger(__name__)


class RobinhoodClient:
    """
    Robinhood API Client with safety features
    
    Provides secure authentication and trade execution with
    circuit breaker integration
    """
    
    def __init__(self):
        self.authenticated = False
        self.account_info = None
        self.positions = {}
        logger.info("Robinhood Client initialized")
    
    def login(self) -> Tuple[bool, str]:
        """
        Authenticate with Robinhood
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Validate configuration
            Config.validate()
            
            # Handle MFA/2FA
            mfa_code = None
            if Config.ROBINHOOD_TOTP_SECRET:
                # Use TOTP (authenticator app)
                totp = pyotp.TOTP(Config.ROBINHOOD_TOTP_SECRET)
                mfa_code = totp.now()
                logger.info("Generated TOTP code for authentication")
            elif Config.ROBINHOOD_MFA_CODE:
                # Use provided SMS code
                mfa_code = Config.ROBINHOOD_MFA_CODE
                logger.info("Using provided MFA code")
            
            # Attempt login
            logger.info(f"Attempting login for user: {Config.ROBINHOOD_USERNAME}")
            
            login_result = rh.login(
                username=Config.ROBINHOOD_USERNAME,
                password=Config.ROBINHOOD_PASSWORD,
                mfa_code=mfa_code,
                store_session=True  # Store session to avoid repeated logins
            )
            
            if login_result:
                self.authenticated = True
                self.account_info = self._fetch_account_info()
                
                # Activate circuit breaker with current balance
                portfolio_value = self.get_portfolio_value()
                circuit_breaker.activate(portfolio_value)
                
                logger.info("✅ Successfully authenticated with Robinhood")
                logger.info(f"Account value: ${portfolio_value:,.2f}")
                
                return True, "Successfully authenticated"
            else:
                logger.error("❌ Authentication failed")
                return False, "Authentication failed - check credentials"
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False, f"Login error: {str(e)}"
    
    def logout(self):
        """Logout from Robinhood"""
        try:
            rh.logout()
            self.authenticated = False
            circuit_breaker.deactivate()
            logger.info("Logged out from Robinhood")
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
    
    def get_portfolio_value(self) -> float:
        """Get total portfolio value"""
        try:
            profile = rh.load_portfolio_profile()
            if profile and 'equity' in profile:
                return float(profile['equity'])
            return 0.0
        except Exception as e:
            logger.error(f"Error fetching portfolio value: {str(e)}")
            return 0.0
    
    def get_buying_power(self) -> float:
        """Get available buying power"""
        try:
            profile = rh.load_account_profile()
            if profile and 'buying_power' in profile:
                return float(profile['buying_power'])
            return 0.0
        except Exception as e:
            logger.error(f"Error fetching buying power: {str(e)}")
            return 0.0
    
    def get_positions(self) -> List[Dict]:
        """Get current stock positions"""
        try:
            positions = rh.get_open_stock_positions()
            result = []
            
            for position in positions:
                symbol = rh.get_symbol_by_url(position['instrument'])
                quantity = float(position['quantity'])
                avg_price = float(position['average_buy_price'])
                
                # Get current price
                current_price = self.get_stock_price(symbol)
                current_value = quantity * current_price
                pnl = current_value - (quantity * avg_price)
                pnl_percent = (pnl / (quantity * avg_price)) * 100 if avg_price > 0 else 0
                
                result.append({
                    'symbol': symbol,
                    'quantity': quantity,
                    'average_price': avg_price,
                    'current_price': current_price,
                    'current_value': current_value,
                    'pnl': pnl,
                    'pnl_percent': pnl_percent
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Error fetching positions: {str(e)}")
            return []
    
    def get_stock_price(self, symbol: str) -> float:
        """Get current stock price"""
        try:
            quote = rh.get_latest_price(symbol)
            if quote and len(quote) > 0:
                return float(quote[0])
            return 0.0
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {str(e)}")
            return 0.0
    
    def get_stock_quote(self, symbol: str) -> Dict:
        """Get detailed stock quote"""
        try:
            quote = rh.get_quote(symbol)
            if quote:
                return {
                    'symbol': symbol,
                    'price': float(quote['last_trade_price']),
                    'ask_price': float(quote['ask_price']) if quote['ask_price'] else 0.0,
                    'bid_price': float(quote['bid_price']) if quote['bid_price'] else 0.0,
                    'volume': int(quote['volume']) if quote['volume'] else 0,
                    'previous_close': float(quote['previous_close']) if quote['previous_close'] else 0.0
                }
            return {}
        except Exception as e:
            logger.error(f"Error fetching quote for {symbol}: {str(e)}")
            return {}
    
    def execute_buy(self, symbol: str, quantity: float, order_type: str = 'market') -> Tuple[bool, str, Optional[Dict]]:
        """
        Execute a BUY order with circuit breaker protection
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares
            order_type: 'market' or 'limit'
        
        Returns:
            (success: bool, message: str, order_details: Dict)
        """
        if not self.authenticated:
            return False, "Not authenticated", None
        
        try:
            # Get current price
            price = self.get_stock_price(symbol)
            if price == 0:
                return False, f"Could not fetch price for {symbol}", None
            
            # Check with circuit breaker
            portfolio_value = self.get_portfolio_value()
            allowed, reason = circuit_breaker.check_trade_allowed(
                symbol, 'BUY', quantity, price, portfolio_value
            )
            
            if not allowed:
                logger.warning(f"Trade blocked by circuit breaker: {reason}")
                return False, f"Trade blocked: {reason}", None
            
            # Paper trading mode
            if Config.ENABLE_PAPER_TRADING:
                logger.info(f"📝 PAPER TRADE: BUY {quantity} {symbol} @ ${price:.2f}")
                order_details = {
                    'symbol': symbol,
                    'quantity': quantity,
                    'price': price,
                    'total_value': quantity * price,
                    'type': 'BUY',
                    'status': 'PAPER_TRADE',
                    'timestamp': datetime.now().isoformat()
                }
                circuit_breaker.record_trade(symbol, 'BUY', quantity, price)
                return True, "Paper trade executed", order_details
            
            # Execute real order
            logger.info(f"Executing BUY order: {quantity} {symbol}")
            order = rh.order_buy_market(symbol, quantity)
            
            if order and order.get('state') != 'failed':
                circuit_breaker.record_trade(symbol, 'BUY', quantity, price)
                circuit_breaker.update_balance(self.get_portfolio_value())
                
                order_details = {
                    'symbol': symbol,
                    'quantity': quantity,
                    'price': price,
                    'order_id': order.get('id'),
                    'status': order.get('state'),
                    'timestamp': datetime.now().isoformat()
                }
                
                logger.info(f"✅ BUY order executed: {quantity} {symbol} @ ${price:.2f}")
                return True, "Order executed successfully", order_details
            else:
                error_msg = order.get('detail', 'Order failed') if order else 'Order failed'
                logger.error(f"❌ BUY order failed: {error_msg}")
                return False, error_msg, None
                
        except Exception as e:
            logger.error(f"Error executing BUY order: {str(e)}")
            return False, f"Error: {str(e)}", None
    
    def execute_sell(self, symbol: str, quantity: float, order_type: str = 'market') -> Tuple[bool, str, Optional[Dict]]:
        """
        Execute a SELL order with circuit breaker protection
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares
            order_type: 'market' or 'limit'
        
        Returns:
            (success: bool, message: str, order_details: Dict)
        """
        if not self.authenticated:
            return False, "Not authenticated", None
        
        try:
            # Get current price
            price = self.get_stock_price(symbol)
            if price == 0:
                return False, f"Could not fetch price for {symbol}", None
            
            # Check with circuit breaker
            portfolio_value = self.get_portfolio_value()
            allowed, reason = circuit_breaker.check_trade_allowed(
                symbol, 'SELL', quantity, price, portfolio_value
            )
            
            if not allowed:
                logger.warning(f"Trade blocked by circuit breaker: {reason}")
                return False, f"Trade blocked: {reason}", None
            
            # Paper trading mode
            if Config.ENABLE_PAPER_TRADING:
                logger.info(f"📝 PAPER TRADE: SELL {quantity} {symbol} @ ${price:.2f}")
                order_details = {
                    'symbol': symbol,
                    'quantity': quantity,
                    'price': price,
                    'total_value': quantity * price,
                    'type': 'SELL',
                    'status': 'PAPER_TRADE',
                    'timestamp': datetime.now().isoformat()
                }
                circuit_breaker.record_trade(symbol, 'SELL', quantity, price)
                return True, "Paper trade executed", order_details
            
            # Execute real order
            logger.info(f"Executing SELL order: {quantity} {symbol}")
            order = rh.order_sell_market(symbol, quantity)
            
            if order and order.get('state') != 'failed':
                # Calculate P&L (simplified - would need position tracking for accuracy)
                circuit_breaker.record_trade(symbol, 'SELL', quantity, price)
                circuit_breaker.update_balance(self.get_portfolio_value())
                
                order_details = {
                    'symbol': symbol,
                    'quantity': quantity,
                    'price': price,
                    'order_id': order.get('id'),
                    'status': order.get('state'),
                    'timestamp': datetime.now().isoformat()
                }
                
                logger.info(f"✅ SELL order executed: {quantity} {symbol} @ ${price:.2f}")
                return True, "Order executed successfully", order_details
            else:
                error_msg = order.get('detail', 'Order failed') if order else 'Order failed'
                logger.error(f"❌ SELL order failed: {error_msg}")
                return False, error_msg, None
                
        except Exception as e:
            logger.error(f"Error executing SELL order: {str(e)}")
            return False, f"Error: {str(e)}", None
    
    def _fetch_account_info(self) -> Dict:
        """Fetch account information"""
        try:
            profile = rh.load_account_profile()
            return profile if profile else {}
        except Exception as e:
            logger.error(f"Error fetching account info: {str(e)}")
            return {}
    
    def get_account_summary(self) -> Dict:
        """Get comprehensive account summary"""
        try:
            portfolio_value = self.get_portfolio_value()
            buying_power = self.get_buying_power()
            positions = self.get_positions()
            
            total_pnl = sum(pos['pnl'] for pos in positions)
            
            return {
                'authenticated': self.authenticated,
                'portfolio_value': portfolio_value,
                'buying_power': buying_power,
                'positions_count': len(positions),
                'positions': positions,
                'total_pnl': total_pnl,
                'circuit_breaker': circuit_breaker.get_status()
            }
        except Exception as e:
            logger.error(f"Error getting account summary: {str(e)}")
            return {'error': str(e)}


# Global client instance
robinhood_client = RobinhoodClient()
