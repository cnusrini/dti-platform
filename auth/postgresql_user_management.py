"""
PostgreSQL User Management System for PharmQAgentAI
Connects to external PostgreSQL database (emdcian_website project)
Handles authentication, subscription plans, and user access control
"""

import streamlit as st
import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    """User model for PostgreSQL"""
    __tablename__ = 'pharmq_users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    organization = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationship to subscriptions
    subscriptions = relationship("Subscription", back_populates="user")

class Subscription(Base):
    """Subscription model for PostgreSQL"""
    __tablename__ = 'pharmq_subscriptions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('pharmq_users.id'), nullable=False)
    plan_type = Column(String(50), nullable=False)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationship to user
    user = relationship("User", back_populates="subscriptions")

class UsageTracking(Base):
    """Usage tracking model for PostgreSQL"""
    __tablename__ = 'pharmq_usage_tracking'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('pharmq_users.id'), nullable=False)
    feature = Column(String(100), nullable=False)
    usage_count = Column(Integer, default=1)
    last_used = Column(DateTime, default=func.now())

class PostgreSQLUserManager:
    """Manages user authentication and subscriptions using PostgreSQL"""
    
    def __init__(self, database_url: str = None):
        """Initialize with database URL from environment or parameter"""
        self.database_url = database_url or os.getenv('DATABASE_URL')
        
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable must be set")
        
        # Create SQLAlchemy engine
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables if they don't exist
        self.init_database()
    
    def init_database(self):
        """Initialize PostgreSQL database tables"""
        try:
            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            print("✅ PostgreSQL tables created/verified successfully")
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")
            raise e
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, email: str, password: str, full_name: str, organization: str = None) -> bool:
        """Register a new user"""
        session = self.get_session()
        try:
            # Check if user already exists
            existing_user = session.query(User).filter(User.email == email).first()
            if existing_user:
                return False
            
            # Create new user
            password_hash = self.hash_password(password)
            new_user = User(
                email=email,
                password_hash=password_hash,
                full_name=full_name,
                organization=organization or ""
            )
            
            session.add(new_user)
            session.flush()  # Get the ID without committing
            
            # Create default starter subscription
            self.create_subscription(new_user.id, "Starter", 30)
            session.commit()
            
            return True
            
        except Exception as e:
            session.rollback()
            print(f"Error registering user: {e}")
            return False
        finally:
            session.close()
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data"""
        session = self.get_session()
        try:
            password_hash = self.hash_password(password)
            user = session.query(User).filter(
                User.email == email,
                User.password_hash == password_hash,
                User.is_active == True
            ).first()
            
            if user:
                # Update last login
                user.last_login = datetime.now()
                session.commit()
                
                return {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'organization': user.organization,
                    'created_at': user.created_at,
                    'last_login': user.last_login
                }
            
            return None
            
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
        finally:
            session.close()
    
    def get_user_subscription(self, user_id: int) -> Optional[Dict]:
        """Get active subscription for user"""
        session = self.get_session()
        try:
            subscription = session.query(Subscription).filter(
                Subscription.user_id == user_id,
                Subscription.is_active == True
            ).order_by(Subscription.start_date.desc()).first()
            
            if subscription:
                return {
                    'id': subscription.id,
                    'plan_type': subscription.plan_type,
                    'start_date': subscription.start_date,
                    'end_date': subscription.end_date,
                    'is_active': subscription.is_active
                }
            
            return None
            
        except Exception as e:
            print(f"Error getting user subscription: {e}")
            return None
        finally:
            session.close()
    
    def create_subscription(self, user_id: int, plan_type: str, duration_days: int = 30) -> bool:
        """Create new subscription for user"""
        session = self.get_session()
        try:
            # Deactivate existing subscriptions
            session.query(Subscription).filter(
                Subscription.user_id == user_id,
                Subscription.is_active == True
            ).update({'is_active': False})
            
            # Create new subscription
            end_date = datetime.now() + timedelta(days=duration_days)
            new_subscription = Subscription(
                user_id=user_id,
                plan_type=plan_type,
                end_date=end_date
            )
            
            session.add(new_subscription)
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            print(f"Error creating subscription: {e}")
            return False
        finally:
            session.close()
    
    def track_usage(self, user_id: int, feature: str):
        """Track feature usage for analytics"""
        session = self.get_session()
        try:
            # Check if usage record exists
            usage = session.query(UsageTracking).filter(
                UsageTracking.user_id == user_id,
                UsageTracking.feature == feature
            ).first()
            
            if usage:
                usage.usage_count += 1
                usage.last_used = datetime.now()
            else:
                usage = UsageTracking(
                    user_id=user_id,
                    feature=feature,
                    usage_count=1
                )
                session.add(usage)
            
            session.commit()
            
        except Exception as e:
            session.rollback()
            print(f"Error tracking usage: {e}")
        finally:
            session.close()
    
    def get_usage_stats(self, user_id: int) -> Dict:
        """Get usage statistics for user"""
        session = self.get_session()
        try:
            usage_records = session.query(UsageTracking).filter(
                UsageTracking.user_id == user_id
            ).all()
            
            stats = {
                'total_predictions': 0,
                'features_used': {},
                'last_activity': None
            }
            
            for record in usage_records:
                stats['features_used'][record.feature] = record.usage_count
                stats['total_predictions'] += record.usage_count
                
                if stats['last_activity'] is None or record.last_used > stats['last_activity']:
                    stats['last_activity'] = record.last_used
            
            return stats
            
        except Exception as e:
            print(f"Error getting usage stats: {e}")
            return {'total_predictions': 0, 'features_used': {}, 'last_activity': None}
        finally:
            session.close()
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            session = self.get_session()
            # Simple query to test connection
            from sqlalchemy import text
            session.execute(text("SELECT 1"))
            session.close()
            return True
        except Exception as e:
            print(f"Database connection test failed: {e}")
            return False

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
        return cls.PLANS.get(plan_type, cls.PLANS["Starter"])
    
    @classmethod
    def check_feature_access(cls, user_plan: str, feature: str) -> bool:
        """Check if user's plan allows access to specific feature"""
        plan = cls.PLANS.get(user_plan, cls.PLANS["Starter"])
        
        # Define feature access mapping
        feature_access = {
            "advanced_agents": user_plan in ["Professional", "Enterprise"],
            "api_access": user_plan in ["Professional", "Enterprise"],
            "unlimited_predictions": user_plan == "Enterprise",
            "custom_reporting": user_plan in ["Professional", "Enterprise"],
            "multi_user": user_plan == "Enterprise"
        }
        
        return feature_access.get(feature, True)  # Default to True for basic features