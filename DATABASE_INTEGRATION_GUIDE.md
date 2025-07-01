# PostgreSQL Database Integration Guide

## Overview

PharmQAgentAI can now connect to your external PostgreSQL database from the emdcian_website project for shared user authentication and subscription management.

## Setup Steps

### 1. Get DATABASE_URL from emdcian_website project

1. Go to your emdcian_website project in Replit
2. Open the Secrets tab (🔒 icon in left sidebar)
3. Copy the `DATABASE_URL` value

### 2. Configure PharmQAgentAI

1. In this PharmQAgentAI project, go to Secrets tab
2. Add a new secret:
   - **Key**: `DATABASE_URL`
   - **Value**: The PostgreSQL connection string from emdcian_website

### 3. Restart the Application

1. Stop the current workflow (if running)
2. Restart the PharmQAgentAI Server workflow
3. The app will automatically detect and connect to PostgreSQL

## Database Tables Created

The system will automatically create these tables in your PostgreSQL database:

- **pharmq_users** - User accounts for PharmQAgentAI
- **pharmq_subscriptions** - Subscription plans and billing
- **pharmq_usage_tracking** - Feature usage analytics

## Features

### Automatic Fallback
- If PostgreSQL connection fails, automatically uses local SQLite
- No data loss or application downtime

### Shared Authentication
- Users can sign up/login with same credentials across projects
- Subscription management is centralized

### Data Isolation
- PharmQAgentAI tables are prefixed with `pharmq_` to avoid conflicts
- emdcian_website tables remain untouched

## Testing the Connection

Run the database setup utility:
```bash
streamlit run setup_external_db.py
```

This will:
- Test the database connection
- Show database information
- Allow testing user registration/authentication
- Verify table creation

## Connection Status

The application will show connection status in the sidebar:
- ✅ PostgreSQL (External) - Connected to emdcian_website database
- 📝 SQLite (Local) - Using fallback local database

## Troubleshooting

### Connection Issues
1. Verify DATABASE_URL is correctly set in Secrets
2. Check if emdcian_website database is accessible
3. Restart the PharmQAgentAI application

### Table Creation Issues
- The app automatically creates required tables
- If creation fails, check database permissions
- Tables use standard PostgreSQL syntax

### Authentication Issues
1. Users from emdcian_website won't automatically have PharmQAgentAI accounts
2. New registrations will be stored in the shared database
3. Password hashing is compatible between projects

## Security Notes

- Database connection uses SSL by default
- Passwords are hashed using SHA-256
- No sensitive data is stored in plain text
- Environment variables protect connection credentials

## Benefits

1. **Unified User Management** - Single user database across projects
2. **Centralized Billing** - One subscription system for multiple services
3. **Enhanced Analytics** - Cross-project usage insights
4. **Simplified Administration** - Manage users from one location
5. **Scalability** - PostgreSQL handles concurrent users better than SQLite

## Next Steps

After successful connection:
1. Test user registration and login
2. Verify subscription management works
3. Monitor usage tracking
4. Consider implementing cross-project features