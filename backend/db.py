import sqlite3
from datetime import datetime
import json
from typing import Dict, List, Any, Optional, Tuple
import os
from pathlib import Path

class Database:
    def __init__(self, db_path: str = "data/solana_news.db"):
        """Initialize the database connection."""
        # Ensure data directory exists
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create the necessary tables if they don't exist."""
        # Solana price data table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS solana_price (
            timestamp INTEGER PRIMARY KEY,
            price REAL,
            volume REAL,
            market_cap REAL
        )
        ''')
        
        # News table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            title TEXT,
            url TEXT,
            published_at INTEGER,
            content TEXT,
            sentiment_score REAL,
            created_at INTEGER
        )
        ''')
        
        # Analysis results table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_date INTEGER,
            end_date INTEGER,
            granularity TEXT,
            price_data TEXT,
            volume_data TEXT,
            volatility_data TEXT,
            news_data TEXT,
            analysis_result TEXT,
            created_at INTEGER
        )
        ''')
        
        self.conn.commit()
    
    def save_price_data(self, timestamp: int, price: float, volume: float, market_cap: float) -> None:
        """
        Save Solana price data to the database.
        
        Args:
            timestamp: Unix timestamp
            price: Solana price in USD
            volume: Trading volume in USD
            market_cap: Market capitalization in USD
        """
        self.cursor.execute(
            "INSERT OR REPLACE INTO solana_price (timestamp, price, volume, market_cap) VALUES (?, ?, ?, ?)",
            (timestamp, price, volume, market_cap)
        )
        self.conn.commit()
    
    def save_news(self, source: str, title: str, url: str, published_at: int, 
                 content: str, sentiment_score: float) -> int:
        """
        Save news article to the database.
        
        Args:
            source: News source
            title: Article title
            url: Article URL
            published_at: Publication timestamp
            content: Article content
            sentiment_score: Calculated sentiment score
            
        Returns:
            Inserted row ID
        """
        current_time = int(datetime.now().timestamp())
        self.cursor.execute(
            "INSERT INTO news (source, title, url, published_at, content, sentiment_score, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (source, title, url, published_at, content, sentiment_score, current_time)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def save_analysis(self, start_date: int, end_date: int, granularity: str,
                     price_data: List[Dict], volume_data: List[Dict], 
                     volatility_data: List[Dict], news_data: List[Dict],
                     analysis_result: str) -> int:
        """
        Save analysis results to the database.
        
        Args:
            start_date: Start timestamp
            end_date: End timestamp
            granularity: Time granularity used
            price_data: List of price data points
            volume_data: List of volume data points
            volatility_data: List of volatility data points
            news_data: List of news data points
            analysis_result: LLM analysis result
            
        Returns:
            Inserted row ID
        """
        current_time = int(datetime.now().timestamp())
        self.cursor.execute(
            "INSERT INTO analysis (start_date, end_date, granularity, price_data, volume_data, volatility_data, news_data, analysis_result, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                start_date, 
                end_date, 
                granularity, 
                json.dumps(price_data),
                json.dumps(volume_data),
                json.dumps(volatility_data),
                json.dumps(news_data),
                analysis_result,
                current_time
            )
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_price_data(self, start_timestamp: int, end_timestamp: int) -> List[Dict]:
        """
        Get Solana price data for a specific time range.
        
        Args:
            start_timestamp: Start timestamp
            end_timestamp: End timestamp
            
        Returns:
            List of price data dictionaries
        """
        self.cursor.execute(
            "SELECT * FROM solana_price WHERE timestamp >= ? AND timestamp <= ? ORDER BY timestamp",
            (start_timestamp, end_timestamp)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_news_in_range(self, start_timestamp: int, end_timestamp: int) -> List[Dict]:
        """
        Get news articles for a specific time range.
        
        Args:
            start_timestamp: Start timestamp
            end_timestamp: End timestamp
            
        Returns:
            List of news data dictionaries
        """
        self.cursor.execute(
            "SELECT * FROM news WHERE published_at >= ? AND published_at <= ? ORDER BY published_at",
            (start_timestamp, end_timestamp)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_cached_analysis(self, start_date: int, end_date: int) -> Optional[Dict]:
        """
        Get cached analysis results if available.
        
        Args:
            start_date: Start timestamp
            end_date: End timestamp
            
        Returns:
            Analysis data dictionary or None if not cached
        """
        self.cursor.execute(
            "SELECT * FROM analysis WHERE start_date = ? AND end_date = ? ORDER BY created_at DESC LIMIT 1",
            (start_date, end_date)
        )
        result = self.cursor.fetchone()
        if result:
            return dict(result)
        return None
    
    def close(self):
        """Close the database connection."""
        self.conn.close()