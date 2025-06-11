"""
User Management System for PharmQAgentAI
Handles authentication, subscription plans, and user access control
"""

import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import sqlite3

class UserManager:
    """Manages user authentication and subscriptions"""
    
    def __init__(self):
        self.db_path = "auth/users.db"
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for user management"""
        os.makedirs("auth", exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                organization TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Subscriptions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                plan_type TEXT NOT NULL,
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                payment_status TEXT DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Usage tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                feature_used TEXT,
                usage_count INTEGER DEFAULT 1,
                usage_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, email: str, password: str, full_name: str, organization: str = None) -> bool:
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (email, password_hash, full_name, organization)
                VALUES (?, ?, ?, ?)
            ''', (email, password_hash, full_name, organization))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False  # Email already exists
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        cursor.execute('''
            SELECT id, email, full_name, organization, created_at
            FROM users 
            WHERE email = ? AND password_hash = ? AND is_active = TRUE
        ''', (email, password_hash))
        
        user = cursor.fetchone()
        
        if user:
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (user[0],))
            conn.commit()
            
            user_data = {
                'id': user[0],
                'email': user[1],
                'full_name': user[2],
                'organization': user[3],
                'created_at': user[4]
            }
            
            conn.close()
            return user_data
        
        conn.close()
        return None
    
    def get_user_subscription(self, user_id: int) -> Optional[Dict]:
        """Get active subscription for user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT plan_type, start_date, end_date, payment_status
            FROM subscriptions 
            WHERE user_id = ? AND is_active = TRUE
            ORDER BY start_date DESC
            LIMIT 1
        ''', (user_id,))
        
        subscription = cursor.fetchone()
        conn.close()
        
        if subscription:
            return {
                'plan_type': subscription[0],
                'start_date': subscription[1],
                'end_date': subscription[2],
                'payment_status': subscription[3]
            }
        return None
    
    def create_subscription(self, user_id: int, plan_type: str, duration_days: int = 30) -> bool:
        """Create new subscription for user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            end_date = datetime.now() + timedelta(days=duration_days)
            
            cursor.execute('''
                INSERT INTO subscriptions (user_id, plan_type, end_date, payment_status)
                VALUES (?, ?, ?, 'active')
            ''', (user_id, plan_type, end_date))
            
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def track_usage(self, user_id: int, feature: str):
        """Track feature usage for analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO usage_tracking (user_id, feature_used)
            VALUES (?, ?)
        ''', (user_id, feature))
        
        conn.commit()
        conn.close()
    
    def get_usage_stats(self, user_id: int) -> Dict:
        """Get usage statistics for user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT feature_used, COUNT(*) as count
            FROM usage_tracking 
            WHERE user_id = ? 
            GROUP BY feature_used
        ''', (user_id,))
        
        stats = dict(cursor.fetchall())
        conn.close()
        return stats

class SubscriptionPlans:
    """Defines subscription plans and their features"""
    
    PLANS = {
        "Starter": {
            "price": "$49/month",
            "description": "Perfect for academic researchers and small biotech teams",
            "features": [
                "100 predictions per month",
                "Basic DTI and DTA analysis",
                "Standard ADMET predictions",
                "Email support",
                "Basic reporting"
            ],
            "limits": {
                "predictions_per_month": 100,
                "concurrent_analyses": 1,
                "data_storage_gb": 1
            }
        },
        "Professional": {
            "price": "$149/month",
            "description": "Ideal for pharmaceutical companies and advanced research",
            "features": [
                "1,000 predictions per month",
                "Full AI agent access (24 agents)",
                "Advanced analytics and insights",
                "Molecular optimization tools",
                "Priority support",
                "Custom reporting",
                "API access"
            ],
            "limits": {
                "predictions_per_month": 1000,
                "concurrent_analyses": 5,
                "data_storage_gb": 10
            }
        },
        "Enterprise": {
            "price": "$499/month",
            "description": "Complete solution for large pharmaceutical enterprises",
            "features": [
                "Unlimited predictions",
                "All AI agents and features",
                "Multi-user collaboration",
                "White-label deployment",
                "24/7 dedicated support",
                "Custom integrations",
                "Advanced security",
                "Training and consultation"
            ],
            "limits": {
                "predictions_per_month": -1,  # Unlimited
                "concurrent_analyses": -1,    # Unlimited
                "data_storage_gb": 100
            }
        }
    }
    
    @classmethod
    def get_plan_features(cls, plan_type: str) -> Dict:
        """Get features for a specific plan"""
        return cls.PLANS.get(plan_type, {})
    
    @classmethod
    def check_feature_access(cls, user_plan: str, feature: str) -> bool:
        """Check if user's plan allows access to specific feature"""
        if not user_plan or user_plan not in cls.PLANS:
            return False
        
        plan_limits = cls.PLANS[user_plan].get("limits", {})
        
        # Define feature requirements
        feature_requirements = {
            "ai_agents": ["Professional", "Enterprise"],
            "advanced_analytics": ["Professional", "Enterprise"],
            "molecular_optimization": ["Professional", "Enterprise"],
            "collaboration": ["Enterprise"],
            "api_access": ["Professional", "Enterprise"]
        }
        
        required_plans = feature_requirements.get(feature, ["Starter", "Professional", "Enterprise"])
        return user_plan in required_plans