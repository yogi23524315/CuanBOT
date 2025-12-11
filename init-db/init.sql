-- CuanBot Database Initialization Script
-- This script is run automatically when PostgreSQL container starts

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE cuanbot_db TO cuanbot;

-- Additional setup can be added here
