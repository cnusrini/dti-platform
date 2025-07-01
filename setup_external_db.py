"""
Setup Script for External PostgreSQL Database Connection
Run this script to configure PharmQAgentAI to use your emdcian_website database
"""

import os
import streamlit as st
from auth.external_db_connector import ExternalDBUserManager

def main():
    st.title("🔗 PharmQAgentAI Database Setup")
    st.markdown("Connect to your emdcian_website PostgreSQL database")
    
    # Check current database configuration
    current_db_url = os.getenv('DATABASE_URL')
    
    if current_db_url:
        st.success("✅ DATABASE_URL is configured")
        
        # Test connection
        try:
            db_manager = ExternalDBUserManager(current_db_url)
            db_info = db_manager.get_database_info()
            
            st.subheader("📊 Database Information")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Database Type", db_info['type'])
                st.metric("Status", db_info['status'])
            
            with col2:
                st.metric("Host", db_info['host'])
                st.metric("Database", db_info['database'])
            
            st.subheader("📋 Tables Created")
            for table in db_info['tables']:
                st.write(f"• {table}")
            
            # Test operations
            st.subheader("🧪 Test Database Operations")
            
            if st.button("Test User Registration"):
                test_email = "test@pharmqagent.ai"
                success = db_manager.register_user(
                    email=test_email,
                    password="test123",
                    full_name="Test User",
                    organization="PharmQAgentAI"
                )
                if success:
                    st.success(f"✅ Test user {test_email} registered successfully")
                else:
                    st.warning("⚠️ Test user already exists or registration failed")
            
            if st.button("Test User Authentication"):
                user = db_manager.authenticate_user("test@pharmqagent.ai", "test123")
                if user:
                    st.success("✅ Authentication test successful")
                    st.json(user)
                else:
                    st.error("❌ Authentication test failed")
        
        except Exception as e:
            st.error(f"❌ Database connection failed: {e}")
            st.info("Please check your DATABASE_URL configuration")
    
    else:
        st.warning("⚠️ DATABASE_URL not configured")
        st.markdown("""
        ### Setup Instructions:
        
        1. **Get your emdcian_website DATABASE_URL:**
           - Go to your emdcian_website project
           - Copy the DATABASE_URL from your environment variables
           
        2. **Set the DATABASE_URL in this project:**
           - Go to Secrets tab in Replit
           - Add key: `DATABASE_URL`
           - Add value: Your PostgreSQL connection string
           
        3. **Format should be:**
           ```
           postgresql://username:password@host:port/database
           ```
        
        4. **Restart the application** after setting the DATABASE_URL
        """)
    
    st.markdown("---")
    st.subheader("🔄 Switch Database Backend")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Current Backend:**")
        if current_db_url:
            st.success("PostgreSQL (External)")
        else:
            st.info("SQLite (Local)")
    
    with col2:
        st.markdown("**Available Options:**")
        st.write("• PostgreSQL - Connect to emdcian_website database")
        st.write("• SQLite - Use local database (fallback)")

if __name__ == "__main__":
    main()