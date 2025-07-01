"""
Database Configuration for PharmQAgentAI
Handles switching between SQLite and PostgreSQL authentication backends
"""

import os
import streamlit as st
from typing import Union

# Import both user management systems
from auth.user_management import UserManager as SQLiteUserManager
from auth.external_db_connector import ExternalDBUserManager

class DatabaseConfig:
    """Handles database configuration and user manager selection"""
    
    @staticmethod
    def get_user_manager() -> Union[SQLiteUserManager, ExternalDBUserManager]:
        """
        Get the appropriate user manager based on configuration
        
        Priority:
        1. If DATABASE_URL is set, use External PostgreSQL
        2. Otherwise, use SQLite
        """
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            try:
                # Test PostgreSQL connection
                pg_manager = ExternalDBUserManager(database_url)
                st.success("✅ Connected to PostgreSQL database (emdcian_website)")
                return pg_manager
            except Exception as e:
                st.error(f"❌ PostgreSQL setup failed: {e}")
                st.info("📝 Falling back to SQLite")
        
        # Fallback to SQLite
        return SQLiteUserManager()
    
    @staticmethod
    def is_postgresql_configured() -> bool:
        """Check if PostgreSQL is configured and available"""
        return bool(os.getenv('DATABASE_URL'))
    
    @staticmethod
    def get_database_info() -> dict:
        """Get information about the current database configuration"""
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            # Parse PostgreSQL URL for display (without password)
            if database_url.startswith('postgresql://'):
                # Extract host info for display
                try:
                    from urllib.parse import urlparse
                    parsed = urlparse(database_url)
                    host_info = f"{parsed.hostname}:{parsed.port}" if parsed.port else parsed.hostname
                    return {
                        'type': 'PostgreSQL',
                        'host': host_info,
                        'database': parsed.path.lstrip('/'),
                        'status': 'configured'
                    }
                except:
                    return {
                        'type': 'PostgreSQL',
                        'host': 'configured',
                        'database': 'external',
                        'status': 'configured'
                    }
        
        return {
            'type': 'SQLite',
            'host': 'local',
            'database': 'auth/users.db',
            'status': 'default'
        }