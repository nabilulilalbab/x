"""
Database module for metrics tracking
SQLite database for storing all metrics
"""

import sqlite3
import os
from datetime import datetime, date
from typing import Optional, Dict, List, Tuple
import json


class Database:
    """SQLite database handler for metrics"""
    
    def __init__(self, db_path: str = "data/metrics.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Daily activity tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE UNIQUE NOT NULL,
                tweets_posted INTEGER DEFAULT 0,
                likes_given INTEGER DEFAULT 0,
                replies_made INTEGER DEFAULT 0,
                follows_made INTEGER DEFAULT 0,
                retweets_made INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tweet performance tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tweet_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id TEXT UNIQUE NOT NULL,
                tweet_text TEXT,
                tweet_type TEXT,
                posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                retweets INTEGER DEFAULT 0,
                replies INTEGER DEFAULT 0,
                engagement_rate FLOAT DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Follower growth tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS follower_growth (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE UNIQUE NOT NULL,
                followers_count INTEGER NOT NULL,
                following_count INTEGER NOT NULL,
                ratio FLOAT,
                new_followers INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Business conversions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                wa_messages INTEGER DEFAULT 0,
                orders INTEGER DEFAULT 0,
                revenue FLOAT DEFAULT 0,
                source TEXT DEFAULT 'twitter',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Keyword performance
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keyword_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                date DATE NOT NULL,
                tweets_found INTEGER DEFAULT 0,
                engaged INTEGER DEFAULT 0,
                conversions INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(keyword, date)
            )
        """)
        
        # Bot activity log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                activity_type TEXT NOT NULL,
                details TEXT,
                success BOOLEAN DEFAULT 1,
                error_message TEXT
            )
        """)
        
        # Configuration history (for tracking changes)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                config_type TEXT NOT NULL,
                changes TEXT,
                user TEXT DEFAULT 'system'
            )
        """)
        
        # Twitter accounts management
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                display_name TEXT,
                wa_number TEXT,
                wa_link TEXT,
                is_active BOOLEAN DEFAULT 1,
                cookies_file TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tracking for replied tweets (prevent duplicate comments)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS commented_tweets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id TEXT NOT NULL,
                tweet_author TEXT NOT NULL,
                tweet_text TEXT,
                our_reply_id TEXT,
                our_reply_text TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(tweet_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    # ============= DAILY ACTIVITY =============
    
    def get_or_create_daily_activity(self, target_date: Optional[date] = None) -> int:
        """Get or create daily activity record, return ID"""
        if target_date is None:
            target_date = date.today()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT OR IGNORE INTO daily_activity (date) VALUES (?)",
            (target_date,)
        )
        
        cursor.execute(
            "SELECT id FROM daily_activity WHERE date = ?",
            (target_date,)
        )
        
        row = cursor.fetchone()
        conn.commit()
        conn.close()
        
        return row['id'] if row else None
    
    def increment_activity(self, activity_type: str, count: int = 1):
        """Increment activity counter for today"""
        self.get_or_create_daily_activity()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        column_map = {
            'tweet': 'tweets_posted',
            'like': 'likes_given',
            'reply': 'replies_made',
            'follow': 'follows_made',
            'retweet': 'retweets_made'
        }
        
        column = column_map.get(activity_type)
        if not column:
            conn.close()
            return
        
        cursor.execute(f"""
            UPDATE daily_activity 
            SET {column} = {column} + ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE date = ?
        """, (count, date.today()))
        
        conn.commit()
        conn.close()
    
    def get_daily_activity(self, target_date: Optional[date] = None) -> Dict:
        """Get daily activity stats"""
        if target_date is None:
            target_date = date.today()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM daily_activity WHERE date = ?",
            (target_date,)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return {
            'date': target_date,
            'tweets_posted': 0,
            'likes_given': 0,
            'replies_made': 0,
            'follows_made': 0,
            'retweets_made': 0
        }
    
    # ============= TWEET PERFORMANCE =============
    
    def add_tweet(self, tweet_id: str, tweet_text: str, tweet_type: str = 'promo'):
        """Add new tweet to tracking"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR IGNORE INTO tweet_performance 
            (tweet_id, tweet_text, tweet_type)
            VALUES (?, ?, ?)
        """, (tweet_id, tweet_text, tweet_type))
        
        conn.commit()
        conn.close()
    
    def update_tweet_stats(self, tweet_id: str, views: int, likes: int, 
                          retweets: int, replies: int):
        """Update tweet performance stats"""
        engagement_rate = (likes + retweets + replies) / views if views > 0 else 0
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE tweet_performance
            SET views = ?, likes = ?, retweets = ?, replies = ?,
                engagement_rate = ?, last_updated = CURRENT_TIMESTAMP
            WHERE tweet_id = ?
        """, (views, likes, retweets, replies, engagement_rate, tweet_id))
        
        conn.commit()
        conn.close()
    
    def get_tweet_stats(self, tweet_id: str) -> Optional[Dict]:
        """Get stats for specific tweet"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM tweet_performance WHERE tweet_id = ?",
            (tweet_id,)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_recent_tweets(self, limit: int = 10) -> List[Dict]:
        """Get recent tweets with stats"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM tweet_performance 
            ORDER BY posted_at DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_best_tweet(self, days: int = 7) -> Optional[Dict]:
        """Get best performing tweet in last N days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM tweet_performance 
            WHERE posted_at >= datetime('now', '-' || ? || ' days')
            ORDER BY engagement_rate DESC
            LIMIT 1
        """, (days,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    # ============= FOLLOWER GROWTH =============
    
    def record_follower_count(self, followers: int, following: int):
        """Record daily follower count"""
        ratio = followers / following if following > 0 else 0
        today = date.today()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get yesterday's count
        cursor.execute("""
            SELECT followers_count FROM follower_growth 
            WHERE date < ? 
            ORDER BY date DESC 
            LIMIT 1
        """, (today,))
        
        row = cursor.fetchone()
        yesterday_followers = row['followers_count'] if row else 0
        new_followers = followers - yesterday_followers
        
        cursor.execute("""
            INSERT OR REPLACE INTO follower_growth 
            (date, followers_count, following_count, ratio, new_followers)
            VALUES (?, ?, ?, ?, ?)
        """, (today, followers, following, ratio, new_followers))
        
        conn.commit()
        conn.close()
    
    def get_follower_growth(self, days: int = 30) -> List[Dict]:
        """Get follower growth for last N days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM follower_growth 
            WHERE date >= date('now', '-' || ? || ' days')
            ORDER BY date ASC
        """, (days,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_current_follower_count(self) -> Tuple[int, int]:
        """Get latest follower/following count"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT followers_count, following_count 
            FROM follower_growth 
            ORDER BY date DESC 
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return row['followers_count'], row['following_count']
        return 0, 0
    
    # ============= CONVERSIONS =============
    
    def add_conversion(self, wa_messages: int = 0, orders: int = 0, 
                      revenue: float = 0, notes: str = None):
        """Add conversion data"""
        today = date.today()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversions 
            (date, wa_messages, orders, revenue, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (today, wa_messages, orders, revenue, notes))
        
        conn.commit()
        conn.close()
    
    def get_conversions(self, days: int = 7) -> List[Dict]:
        """Get conversions for last N days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM conversions 
            WHERE date >= date('now', '-' || ? || ' days')
            ORDER BY date DESC
        """, (days,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_conversion_summary(self, days: int = 7) -> Dict:
        """Get conversion summary"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                SUM(wa_messages) as total_messages,
                SUM(orders) as total_orders,
                SUM(revenue) as total_revenue
            FROM conversions 
            WHERE date >= date('now', '-' || ? || ' days')
        """, (days,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'total_messages': row['total_messages'] or 0,
                'total_orders': row['total_orders'] or 0,
                'total_revenue': row['total_revenue'] or 0
            }
        return {'total_messages': 0, 'total_orders': 0, 'total_revenue': 0}
    
    # ============= KEYWORD PERFORMANCE =============
    
    def record_keyword_activity(self, keyword: str, tweets_found: int, engaged: int):
        """Record keyword search activity"""
        today = date.today()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO keyword_performance 
            (keyword, date, tweets_found, engaged)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(keyword, date) DO UPDATE SET
                tweets_found = tweets_found + ?,
                engaged = engaged + ?
        """, (keyword, today, tweets_found, engaged, tweets_found, engaged))
        
        conn.commit()
        conn.close()
    
    def get_keyword_performance(self, days: int = 7) -> List[Dict]:
        """Get keyword performance summary"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                keyword,
                SUM(tweets_found) as total_found,
                SUM(engaged) as total_engaged,
                ROUND(CAST(SUM(engaged) AS FLOAT) / SUM(tweets_found) * 100, 2) as engagement_rate
            FROM keyword_performance 
            WHERE date >= date('now', '-' || ? || ' days')
            GROUP BY keyword
            ORDER BY total_engaged DESC
        """, (days,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    # ============= ACTIVITY LOG =============
    
    def log_activity(self, activity_type: str, details: str = None, 
                    success: bool = True, error_message: str = None):
        """Log bot activity"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO activity_log 
            (activity_type, details, success, error_message)
            VALUES (?, ?, ?, ?)
        """, (activity_type, details, success, error_message))
        
        conn.commit()
        conn.close()
    
    def get_recent_logs(self, limit: int = 50) -> List[Dict]:
        """Get recent activity logs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM activity_log 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    # ============= ACCOUNTS MANAGEMENT =============
    
    def add_account(self, username: str, display_name: str = None, 
                    wa_number: str = None, wa_link: str = None,
                    cookies_file: str = None, notes: str = None) -> bool:
        """Add a new Twitter account"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO accounts (username, display_name, wa_number, wa_link, cookies_file, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, display_name, wa_number, wa_link, cookies_file, notes))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False  # Account already exists
    
    def get_accounts(self, active_only: bool = False) -> List[Dict]:
        """Get all accounts"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if active_only:
            cursor.execute("SELECT * FROM accounts WHERE is_active = 1 ORDER BY username")
        else:
            cursor.execute("SELECT * FROM accounts ORDER BY username")
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_account_by_id(self, account_id: int) -> Optional[Dict]:
        """Get account by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_account_by_username(self, username: str) -> Optional[Dict]:
        """Get account by username"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def update_account(self, account_id: int, **kwargs) -> bool:
        """Update account information"""
        allowed_fields = ['display_name', 'wa_number', 'wa_link', 'is_active', 
                          'cookies_file', 'notes']
        
        updates = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                values.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.append(account_id)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = f"UPDATE accounts SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, values)
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete_account(self, account_id: int) -> bool:
        """Delete an account"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def toggle_account_status(self, account_id: int) -> bool:
        """Toggle account active status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE accounts 
            SET is_active = NOT is_active, 
                updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (account_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    # ============= REPLIED TWEETS TRACKING =============
    
    def has_replied_to_tweet(self, tweet_id: str) -> bool:
        """Check if we already replied to this tweet"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM commented_tweets WHERE tweet_id = ?", (tweet_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    
    def has_replied_to_author_today(self, author: str) -> bool:
        """Check if we already replied to this author today"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 1 FROM commented_tweets 
            WHERE tweet_author = ? 
            AND date(timestamp) = date('now')
        """, (author,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    
    def add_replied_tweet(self, tweet_id: str, tweet_author: str, tweet_text: str, 
                          our_reply_id: str, our_reply_text: str) -> bool:
        """Track a tweet we replied to"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO commented_tweets (tweet_id, tweet_author, tweet_text, our_reply_id, our_reply_text)
                VALUES (?, ?, ?, ?, ?)
            """, (tweet_id, tweet_author, tweet_text, our_reply_id, our_reply_text))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False  # Already exists
    
    def get_reply_count_today(self) -> int:
        """Get number of replies posted today"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM commented_tweets 
            WHERE date(timestamp) = date('now')
        """)
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def get_recent_replies(self, limit: int = 10) -> List[Dict]:
        """Get recent replies"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM commented_tweets 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    # ============= DASHBOARD STATS =============
    
    def get_dashboard_stats(self) -> Dict:
        """Get comprehensive stats for dashboard"""
        today_activity = self.get_daily_activity()
        followers, following = self.get_current_follower_count()
        conversions_7d = self.get_conversion_summary(7)
        conversions_30d = self.get_conversion_summary(30)
        
        # Get growth stats
        growth_data = self.get_follower_growth(30)
        
        # Calculate average metrics
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                AVG(views) as avg_views,
                AVG(likes) as avg_likes,
                AVG(engagement_rate) as avg_engagement
            FROM tweet_performance
            WHERE posted_at >= datetime('now', '-7 days')
        """)
        
        avg_stats = cursor.fetchone()
        conn.close()
        
        return {
            'today': today_activity,
            'followers': {
                'current': followers,
                'following': following,
                'ratio': followers / following if following > 0 else 0,
                'growth_30d': len(growth_data)
            },
            'tweets': {
                'avg_views': avg_stats['avg_views'] or 0 if avg_stats else 0,
                'avg_likes': avg_stats['avg_likes'] or 0 if avg_stats else 0,
                'avg_engagement': avg_stats['avg_engagement'] or 0 if avg_stats else 0
            },
            'conversions': {
                'week': conversions_7d,
                'month': conversions_30d
            }
        }
