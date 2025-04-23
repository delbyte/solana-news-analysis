# 🧠 Solana News Analysis

A lightweight, full-stack analytics tool that correlates Solana blockchain activity with macro financial news to uncover patterns in price volatility and market behavior.

## 🚀 Overview

Solana News Analysis helps traders, researchers, and crypto enthusiasts make sense of market shifts by analyzing:
- 📈 Solana price and volume trends
- ⚡ Volatility spikes and dips
- 📰 Top global news events from finance, politics, and DeFi

The tool uses an LLM to correlate headlines with price action and may eventually generate predictions based on user-inputted news.

## 🧱 Stack

**Frontend**
- HTML + Tailwind CSS
- Lightweight and responsive interface

**Backend**
- Python + FastAPI
- SQLite for time-series storage
- LLM for event correlation
- Dynamic time granularity for graphs

## 📊 Features

- Custom date range selection
- Automatically adjusts time resolution (hourly, daily, weekly)
- Displays:
  - Solana price chart
  - Trading volume chart
  - Volatility chart (highlighting sudden changes)
- Top 30 financial/news events for selected period
- Optional prediction of future price volatility from input headlines

## 🗂 Directory Structure

```
solana-news-analysis/
├── backend/        # FastAPI backend with LLM and database logic
├── frontend/       # Simple HTML + Tailwind dashboard UI
├── utils/          # News scraping, cleaning, and correlation logic
├── requirements.txt
└── README.md
```

## ⚙️ Getting Started

### Prerequisites
- Python 3.10+
- Node.js (if frontend becomes dynamic)
- [Poetry](https://python-poetry.org/) or `pip`

### Installation

```bash
git clone https://github.com/delbyte/solana-news-analysis.git
cd solana-news-analysis
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Navigate to `frontend/` and open `index.html` in your browser.

## 📌 Roadmap

- [x] Basic plotting with Solana price/volume data
- [x] Volatility detection logic
- [x] LLM correlation with top 30 headlines
- [ ] User-inputted headline prediction
- [ ] Multi-chain support
- [ ] Deployment (Render, Vercel, etc.)

## 🧠 LLM Usage

Uses a local or API-based LLM (configurable) to:
- Extract entities and themes from headlines
- Correlate them with observed market anomalies
- Explain correlations in natural language

## 🤝 Contributing

Pull requests welcome! Please follow the style guide and comment your logic. Open an issue to discuss major changes first.

## 📜 License

[MIT](LICENSE)

---

Built with 🧠 + ❤️ by [@delbyte](https://github.com/delbyte)
```
