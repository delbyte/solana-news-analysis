# Configuration file for the Solana News Analysis application

# API Keys and Endpoints
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
NEWS_API_URL = "https://gnews.io/api/v4"
NEWS_API_KEY = "NEWS_API_KEY"  # Replace with your actual API key

# LLM Configuration
LLM_PROVIDER = "ollama"  # Options: "ollama", "deepseek", "huggingface"
OLLAMA_URL = "http://localhost:11434/api/generate"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = "DEEPSEEK_API_KEY"  # Replace if using DeepSeek
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HUGGINGFACE_API_KEY = "HUGGINGFACE_API_KEY"  # Replace if using Hugging Face

# Database Configuration
DATABASE_URL = "sqlite:///./data/solana_news.db"

# Solana Configuration
SOLANA_SYMBOL = "solana"
SOLANA_ID = "solana"

# Time Configurations
DEFAULT_LOOKBACK_DAYS = 30
TIMEZONE = "UTC"

# Granularity settings
GRANULARITY_MAPPINGS = {
    "1d": "30min",    # For 1 day, use 30-minute intervals
    "7d": "2h",       # For 1 week, use 2-hour intervals
    "30d": "8h",      # For 1 month, use 8-hour intervals
    "90d": "1d",      # For 3 months, use 1-day intervals
    "180d": "2d",     # For 6 months, use 2-day intervals
    "365d": "1w",     # For 1 year, use 1-week intervals
    "max": "2w"       # For all-time, use 2-week intervals
}

# Sentiment Analysis Configuration
SENTIMENT_THRESHOLD_POSITIVE = 0.6
SENTIMENT_THRESHOLD_NEGATIVE = 0.4

# Server Configuration
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True