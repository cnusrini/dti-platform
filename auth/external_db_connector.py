"""
External Database Connector for PharmQAgentAI
Simple PostgreSQL connector to connect to emdcian_website database
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional, List

class ExternalDBUserManager:
    """Simple PostgreSQL user manager for external database connection"""
    
    def __init__(self, database_url: str = None):
        """Initialize with database URL"""
        self.database_url = database_url or os.getenv('DATABASE_URL')
        
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable must be set")
        
        # Test connection on initialization
        self.test_connection()
        
        # Initialize tables if they don't exist
        self.init_tables()
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.database_url)
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            print("✅ Successfully connected to external PostgreSQL database")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def init_tables(self):
        """Initialize required tables if they don't exist"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create users table for PharmQAgentAI
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pharmq_users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255) NOT NULL,
                    organization VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
            
            # Create subscriptions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pharmq_subscriptions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES pharmq_users(id),
                    plan_type VARCHAR(50) NOT NULL,
                    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_date TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
            
            # Create usage tracking table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pharmq_usage_tracking (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES pharmq_users(id),
                    feature VARCHAR(100) NOT NULL,
                    usage_count INTEGER DEFAULT 1,
                    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Database tables initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing tables: {e}")
            raise e
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, email: str, password: str, full_name: str, organization: str = None) -> bool:
        """Register a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT id FROM pharmq_users WHERE email = %s", (email,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return False
            
            # Create new user
            password_hash = self.hash_password(password)
            cursor.execute("""
                INSERT INTO pharmq_users (email, password_hash, full_name, organization)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (email, password_hash, full_name, organization))
            
            user_id = cursor.fetchone()[0]
            
            # Create default starter subscription
            end_date = datetime.now() + timedelta(days=30)
            cursor.execute("""
                INSERT INTO pharmq_subscriptions (user_id, plan_type, end_date)
                VALUES (%s, %s, %s)
            """, (user_id, "Starter", end_date))
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error registering user: {e}")
            return False
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            password_hash = self.hash_password(password)
            cursor.execute("""
                SELECT id, email, full_name, organization, created_at, last_login
                FROM pharmq_users 
                WHERE email = %s AND password_hash = %s AND is_active = TRUE
            """, (email, password_hash))
            
            user = cursor.fetchone()
            
            if user:
                # Update last login
                cursor.execute("""
                    UPDATE pharmq_users SET last_login = CURRENT_TIMESTAMP WHERE id = %s
                """, (user['id'],))
                conn.commit()
                
                cursor.close()
                conn.close()
                return dict(user)
            
            cursor.close()
            conn.close()
            return None
            
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
    
    def get_user_subscription(self, user_id: int) -> Optional[Dict]:
        """Get active subscription for user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT id, plan_type, start_date, end_date, is_active
                FROM pharmq_subscriptions 
                WHERE user_id = %s AND is_active = TRUE
                ORDER BY start_date DESC LIMIT 1
            """, (user_id,))
            
            subscription = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return dict(subscription) if subscription else None
            
        except Exception as e:
            print(f"Error getting user subscription: {e}")
            return None
    
    def create_subscription(self, user_id: int, plan_type: str, duration_days: int = 30) -> bool:
        """Create new subscription for user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Deactivate existing subscriptions
            cursor.execute("""
                UPDATE pharmq_subscriptions SET is_active = FALSE 
                WHERE user_id = %s AND is_active = TRUE
            """, (user_id,))
            
            # Create new subscription
            end_date = datetime.now() + timedelta(days=duration_days)
            cursor.execute("""
                INSERT INTO pharmq_subscriptions (user_id, plan_type, end_date)
                VALUES (%s, %s, %s)
            """, (user_id, plan_type, end_date))
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error creating subscription: {e}")
            return False
    
    def track_usage(self, user_id: int, feature: str):
        """Track feature usage for analytics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if usage record exists
            cursor.execute("""
                SELECT id, usage_count FROM pharmq_usage_tracking 
                WHERE user_id = %s AND feature = %s
            """, (user_id, feature))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                cursor.execute("""
                    UPDATE pharmq_usage_tracking 
                    SET usage_count = usage_count + 1, last_used = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (existing[0],))
            else:
                # Create new record
                cursor.execute("""
                    INSERT INTO pharmq_usage_tracking (user_id, feature, usage_count)
                    VALUES (%s, %s, 1)
                """, (user_id, feature))
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error tracking usage: {e}")
    
    def get_usage_stats(self, user_id: int) -> Dict:
        """Get usage statistics for user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT feature, usage_count, last_used
                FROM pharmq_usage_tracking 
                WHERE user_id = %s
            """, (user_id,))
            
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            
            stats = {
                'total_predictions': 0,
                'features_used': {},
                'last_activity': None
            }
            
            for record in records:
                stats['features_used'][record['feature']] = record['usage_count']
                stats['total_predictions'] += record['usage_count']
                
                if stats['last_activity'] is None or record['last_used'] > stats['last_activity']:
                    stats['last_activity'] = record['last_used']
            
            return stats
            
        except Exception as e:
            print(f"Error getting usage stats: {e}")
            return {'total_predictions': 0, 'features_used': {}, 'last_activity': None}
    
    def get_database_info(self) -> Dict:
        """Get database connection information"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(self.database_url)
            host_info = f"{parsed.hostname}:{parsed.port}" if parsed.port else parsed.hostname
            return {
                'type': 'PostgreSQL',
                'host': host_info,
                'database': parsed.path.lstrip('/'),
                'status': 'connected',
                'tables': ['pharmq_users', 'pharmq_subscriptions', 'pharmq_usage_tracking']
            }
        except:
            return {
                'type': 'PostgreSQL',
                'host': 'external',
                'database': 'emdcian_website',
                'status': 'connected',
                'tables': ['pharmq_users', 'pharmq_subscriptions', 'pharmq_usage_tracking']
            }