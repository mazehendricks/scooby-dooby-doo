# 🤖 AI Trading Monitor - Deep Reinforcement Learning Portfolio Simulator

A comprehensive web-based trading simulation system that demonstrates deep reinforcement learning (DRL) algorithms for portfolio optimization. This educational tool simulates AI-driven trading decisions while highlighting both the potential and risks of automated financial systems.

![AI Trading Monitor](https://img.shields.io/badge/AI-Trading%20Monitor-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Educational-yellow)

## 🎯 Overview

This AI Trading Monitor implements three state-of-the-art deep reinforcement learning algorithms to simulate autonomous portfolio management:

- **PPO (Proximal Policy Optimization)** - Superior risk-adjusted performance with stable policy updates
- **A2C (Advantage Actor-Critic)** - Balances value estimation with policy optimization
- **SAC (Soft Actor-Critic)** - Maximizes entropy for enhanced exploration

## ✨ Features

### Core Functionality
- **Real-time Trading Simulation** - Simulates live market conditions with realistic price movements
- **Multiple DRL Algorithms** - Switch between PPO, A2C, and SAC strategies
- **Technical Indicators** - Comprehensive state representation including:
  - Trend: SMA (50), EMA (20)
  - Momentum: RSI, MACD
  - Volatility: Bollinger Bands, ATR
  - Volume: OBV, VWAP
- **Market Sentiment Analysis** - News sentiment, VIX (fear index), and AI confidence metrics
- **Portfolio Management** - Automated position sizing with risk-adjusted allocation
- **Transaction Costs** - Realistic 0.2% transaction fees for accurate simulation

### Performance Metrics
- **Current Portfolio Value** - Real-time tracking
- **Total Return** - Absolute and percentage gains/losses
- **Sharpe Ratio** - Risk-adjusted return measurement
- **Maximum Drawdown** - Largest peak-to-trough decline
- **Win Rate** - Percentage of profitable trades
- **Trade History** - Complete audit trail of all transactions

### Safety & Ethics Features

#### 🚨 Circuit Breaker
Human-in-the-loop override to prevent "too fast to stop" scenarios during volatile conditions.

#### 🔍 Explainable AI (XAI)
Real-time explanations of AI decision-making process, addressing the "too opaque to understand" problem.

#### 🛡️ Misinformation Resilience
News sentiment filtering to guard against financial deepfakes and AI-driven misinformation.

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No server or installation required - runs entirely in the browser

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-trading-monitor.git
cd ai-trading-monitor
```

2. Open [`index.html`](index.html) in your web browser:
```bash
# On Windows
start index.html

# On macOS
open index.html

# On Linux
xdg-open index.html
```

That's it! The application runs entirely client-side.

## 📖 Usage Guide

### Starting a Simulation

1. **Configure Parameters**:
   - **Initial Capital**: Set starting portfolio value ($1,000 - $1,000,000)
   - **DRL Algorithm**: Choose PPO, A2C, or SAC
   - **Risk Tolerance (λ)**: Adjust from 0 (conservative) to 1 (aggressive)
   - **Trading Speed**: Control simulation speed (0.5s - 2s per step)

2. **Start Trading**: Click the "Start Simulation" button

3. **Monitor Performance**: Watch real-time updates of:
   - Portfolio value and returns
   - Holdings and positions
   - Trade execution log
   - Technical indicators
   - AI decision explanations

4. **Control Simulation**:
   - **Pause/Resume**: Temporarily halt trading
   - **Reset**: Clear all data and start fresh
   - **Circuit Breaker**: Emergency stop with human override

### Understanding the Dashboard

#### Portfolio Performance
Displays key metrics including current value, total return, Sharpe ratio, maximum drawdown, win rate, and total trades executed.

#### Market Intelligence
Shows news sentiment (Bullish/Neutral/Bearish), VIX volatility index, and AI confidence level.

#### Current Holdings
Table view of all positions with:
- Symbol and share count
- Average purchase price vs. current price
- Unrealized P&L (profit/loss)
- Portfolio weight percentage

#### Recent Trades
Chronological log of executed trades with timestamps, type (BUY/SELL), symbol, quantity, price, and algorithm used.

#### Technical Indicators
Real-time state representation showing trend, momentum, volatility, and volume indicators used by the AI agent.

#### AI Decision Explanation (XAI)
Transparent breakdown of why the AI made specific trading decisions, including:
- Algorithm reasoning
- Technical indicator analysis
- Confidence levels
- Risk management considerations

## 🧠 Algorithm Details

### PPO (Proximal Policy Optimization)
**Best for**: Risk-adjusted returns and drawdown control

**Strategy**:
- Uses clipped objective function for stable policy updates
- Buys on oversold conditions (RSI < 30) with positive momentum (MACD > 0)
- Sells on overbought conditions (RSI > 70) with negative momentum
- Conservative position sizing (15% of portfolio)

**Reward Function**:
```
R_t = r_t - λ₁ · TC_t + λ₂ · SR_t
```
Where:
- `r_t` = return at time t
- `TC_t` = transaction costs
- `SR_t` = Sharpe ratio component

### A2C (Advantage Actor-Critic)
**Best for**: Balancing exploration and exploitation

**Strategy**:
- Calculates advantage function to determine expected value
- Actor network proposes actions, critic evaluates them
- Buys when advantage > 0.3 and RSI < 50
- Sells when advantage < -0.3
- Moderate position sizing (12% of portfolio)

**Advantage Calculation**:
```
A(s,a) = Q(s,a) - V(s)
```

### SAC (Soft Actor-Critic)
**Best for**: Maximum exploration and entropy

**Strategy**:
- Maximizes entropy to encourage diverse trading strategies
- Stochastic policy with exploration bonus
- More aggressive position sizing (18% of portfolio)
- Balances immediate rewards with long-term exploration

**Entropy-Regularized Objective**:
```
J(π) = E[Σ(r_t + α·H(π(·|s_t)))]
```

## 📊 Technical Architecture

### Data Flow
```
Market Data → Technical Indicators → State Representation → DRL Agent → Action → Execution → Portfolio Update
```

### State Representation
The AI agent observes:
- Current stock prices and price history (20 periods)
- Technical indicators (RSI, MACD, SMA, EMA, ATR)
- Market sentiment (news, VIX)
- Portfolio state (cash ratio, holdings)

### Action Space
- **BUY**: Purchase shares with risk-adjusted position sizing
- **SELL**: Liquidate partial or full positions
- **HOLD**: Maintain current portfolio allocation

### Reward Function Components
1. **Return Maximization**: Portfolio value increase
2. **Transaction Cost Penalty**: 0.2% fee per trade
3. **Risk Adjustment**: Sharpe ratio bonus for consistent returns

## ⚠️ Risk Warnings & Limitations

### Systemic Risks Addressed

#### 1. "Too Fast to Stop"
**Problem**: AI systems can execute trades faster than humans can intervene during flash crashes.

**Mitigation**: Circuit breaker button provides immediate human override capability.

#### 2. "Too Opaque to Understand"
**Problem**: Black-box AI models make decisions without transparency.

**Mitigation**: Explainable AI (XAI) provides real-time reasoning for every trade decision.

#### 3. "Financial Deepfakes"
**Problem**: AI-generated misinformation can manipulate sentiment-based trading systems.

**Mitigation**: News sentiment filtering and validation mechanisms.

### Educational Disclaimer

⚠️ **IMPORTANT**: This is a **simulation for educational purposes only**. It is **NOT**:
- Financial advice or investment recommendation
- A real trading system connected to actual markets
- Guaranteed to reflect real-world performance
- Suitable for making actual investment decisions

**Real-world AI trading involves**:
- Regulatory compliance (SEC, FINRA, MiFID II)
- Market impact and liquidity constraints
- Execution slippage and latency
- Model overfitting and regime changes
- Systemic risk and correlation breakdowns

## 🔧 Customization

### Adding New Stocks
Edit [`script.js`](script.js:29) to modify the available stocks:
```javascript
this.availableStocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'JPM'];
```

### Adjusting Transaction Costs
Modify the transaction cost rate in [`script.js`](script.js:267):
```javascript
const transactionCost = 0.002; // 0.2% default
```

### Customizing Algorithms
Each algorithm's decision logic can be modified in:
- [`ppoDecision()`](script.js:189) - PPO strategy
- [`a2cDecision()`](script.js:226) - A2C strategy
- [`sacDecision()`](script.js:256) - SAC strategy

## 📚 Academic Context

This project is based on research exploring:

### Benefits of AI in Finance
- **Automated Portfolio Optimization**: Deep RL can process vast amounts of historical data and technical indicators
- **Adaptive Algorithms**: Continuous learning from market conditions
- **Retail Investor Access**: Democratization of sophisticated trading strategies
- **Enhanced Efficiency**: Faster execution and reduced emotional bias

### Risks of AI in Finance
- **Market Manipulation**: AI can facilitate rapid spread of misinformation
- **Flash Crashes**: Algorithmic trading can amplify volatility
- **Opacity**: Black-box models lack interpretability
- **Systemic Risk**: Correlated AI strategies can destabilize markets

### Recommended Reading
1. "Deep Reinforcement Learning for Automated Stock Trading" - FinRL Library
2. "The Dangers of AI in Financial Markets" - Legal Analysis
3. "Explainable AI for Financial Services" - DARPA XAI Program
4. "Market Manipulation in the Age of AI" - SEC Research

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Algorithms**: Custom DRL implementations (PPO, A2C, SAC)
- **Architecture**: Client-side MVC pattern
- **Data**: Simulated market data with realistic volatility

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

1. **Additional Algorithms**: Implement DQN, DDPG, or TD3
2. **Real Data Integration**: Connect to Yahoo Finance or Alpha Vantage APIs
3. **Advanced Indicators**: Add Ichimoku Cloud, Fibonacci retracements
4. **Backtesting**: Historical performance analysis
5. **Multi-Asset**: Expand beyond stocks (crypto, forex, commodities)
6. **Risk Models**: VaR, CVaR, stress testing

### Development Setup
```bash
# Clone repository
git clone https://github.com/yourusername/ai-trading-monitor.git

# No build process required - edit files directly
# Open index.html in browser to test changes
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FinRL Library**: Inspiration for DRL trading algorithms
- **Stable-Baselines3**: Reference implementations of PPO, A2C, SAC
- **OpenAI Gym**: Environment design patterns
- **Academic Research**: Papers on AI in finance and risk management

## 📞 Contact & Support

- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Join GitHub Discussions for questions
- **Email**: support@example.com

## 🔮 Future Roadmap

- [ ] Real-time data integration (yfinance, Polygon.io)
- [ ] Advanced charting with TradingView integration
- [ ] Multi-agent portfolio management
- [ ] Sentiment analysis using LLMs (Llama 3, GPT-4)
- [ ] Backtesting framework with historical data
- [ ] Export reports (PDF, CSV)
- [ ] Mobile-responsive design improvements
- [ ] WebSocket support for live data streaming

---

**Built with ❤️ for education and research in AI-driven finance**

⚠️ **Remember**: Past performance does not guarantee future results. AI trading carries significant risks. Always consult with qualified financial advisors before making investment decisions.
