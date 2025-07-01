"""
Configure Neon PostgreSQL Database Connection for PharmQAgentAI
Sets up environment variables and tests connection
"""

import os
import streamlit as st
from auth.external_db_connector import ExternalDBUserManager

def main():
    st.title("🔗 Neon PostgreSQL Database Configuration")
    st.markdown("Connecting PharmQAgentAI to your Neon database")
    
    # Database configuration from the provided details
    db_config = {
        'EMEDCHAIN_DATABASE_URL': 'postgresql://neondb_owner:npg_3euGUH6ElYfr@ep-spring-frog-ady3sn8s.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require',
        'PGHOST': 'ep-spring-frog-ady3sn8s.c-2.us-east-1.aws.neon.tech',
        'PGPORT': '5432',
        'PGUSER': 'neondb_owner',
        'PGPASSWORD': 'npg_3euGUH6ElYfr',
        'PGDATABASE': 'neondb'
    }
    
    st.subheader("📋 Database Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Database Type", "PostgreSQL (Neon)")
        st.metric("Host", "ep-spring-frog-ady3sn8s.c-2.us-east-1.aws.neon.tech")
        st.metric("Port", "5432")
    
    with col2:
        st.metric("Database", "neondb")
        st.metric("User", "neondb_owner")
        st.metric("SSL Mode", "require")
    
    # Test connection
    st.subheader("🧪 Testing Database Connection")
    
    database_url = db_config['EMEDCHAIN_DATABASE_URL']
    
    if st.button("Test Connection", type="primary"):
        try:
            with st.spinner("Testing connection to Neon database..."):
                db_manager = ExternalDBUserManager(database_url)
                
                if db_manager.test_connection():
                    st.success("✅ Successfully connected to Neon PostgreSQL database!")
                    
                    # Show database info
                    db_info = db_manager.get_database_info()
                    st.json(db_info)
                    
                    # Test table creation
                    st.info("📋 PharmQAgentAI tables will be created automatically")
                    
                else:
                    st.error("❌ Connection test failed")
                    
        except Exception as e:
            st.error(f"❌ Connection error: {e}")
    
    # Environment setup instructions
    st.subheader("⚙️ Environment Setup")
    
    st.markdown("""
    **To complete the setup, add this to your Replit Secrets:**
    
    Key: `DATABASE_URL`
    Value: `postgresql://neondb_owner:npg_3euGUH6ElYfr@ep-spring-frog-ady3sn8s.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require`
    """)
    
    # Check if DATABASE_URL is already set
    current_db_url = os.getenv('DATABASE_URL')
    
    if current_db_url:
        if current_db_url == database_url:
            st.success("✅ DATABASE_URL is correctly configured!")
        else:
            st.warning("⚠️ DATABASE_URL is set but doesn't match the provided credentials")
    else:
        st.info("📝 DATABASE_URL not yet configured. Add it to Replit Secrets.")
    
    # Manual test if DATABASE_URL is set
    if current_db_url == database_url:
        st.subheader("🔧 Database Operations Test")
        
        if st.button("Initialize PharmQAgentAI Tables"):
            try:
                db_manager = ExternalDBUserManager()
                st.success("✅ PharmQAgentAI tables initialized successfully")
                st.info("Tables created: pharmq_users, pharmq_subscriptions, pharmq_usage_tracking")
            except Exception as e:
                st.error(f"❌ Table initialization failed: {e}")
        
        if st.button("Test User Registration"):
            try:
                db_manager = ExternalDBUserManager()
                success = db_manager.register_user(
                    email="test@pharmqagent.ai",
                    password="test123",
                    full_name="Test User",
                    organization="PharmQAgentAI Testing"
                )
                if success:
                    st.success("✅ Test user registered successfully")
                else:
                    st.warning("⚠️ Test user already exists or registration failed")
            except Exception as e:
                st.error(f"❌ Registration test failed: {e}")
    
    st.markdown("---")
    st.markdown("**Next Steps:**")
    st.markdown("1. Add DATABASE_URL to Replit Secrets")
    st.markdown("2. Restart the PharmQAgentAI Server workflow")
    st.markdown("3. The app will automatically connect to your Neon database")

if __name__ == "__main__":
    main()