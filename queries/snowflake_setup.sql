-- =====================================================================================
-- ZENDESK Zendesk Analytics POC - Snowflake Setup Script
-- =====================================================================================
-- This script creates the Bronze layer tables and sets up data loading infrastructure
-- for the ZENDESK Analytics POC demonstrating Snowflake AI functions with support data.
--
-- Execute sections in order:
-- 1. Database and Schema Creation
-- 2. Bronze Layer Table Creation  
-- 3. File Format and Stage Setup
-- 4. Data Loading Commands
-- 5. Validation Queries
-- =====================================================================================

-- =====================================================================================
-- 1. CREATE DATABASE AND SCHEMA
-- =====================================================================================

-- Create database and schema for the POC
CREATE DATABASE IF NOT EXISTS ZENDESK_ANALYTICS_POC;
USE DATABASE ZENDESK_ANALYTICS_POC;

CREATE SCHEMA IF NOT EXISTS BRONZE;
USE SCHEMA BRONZE;

-- =====================================================================================
-- 2. CREATE BRONZE LAYER TABLES
-- =====================================================================================

-- ZENDESK_CUSTOMERS table (1,000 records)
-- Core customer data representing ZENDESK's market distribution
CREATE OR REPLACE TABLE ZENDESK_CUSTOMERS (
    customer_id VARCHAR(20) PRIMARY KEY,
    organization_name VARCHAR(255) NOT NULL,
    organization_type VARCHAR(50) NOT NULL,
    organization_subtype VARCHAR(50),
    size_category VARCHAR(20) NOT NULL,
    employee_count INTEGER NOT NULL,
    subscription_tier VARCHAR(20) NOT NULL,
    monthly_revenue DECIMAL(10,2),
    setup_date DATE NOT NULL,
    primary_contact_name VARCHAR(255),
    primary_contact_email VARCHAR(255),
    primary_contact_phone VARCHAR(20),
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(2),
    zip_code VARCHAR(10),
    time_zone VARCHAR(50),
    payment_methods VARCHAR(500),
    integration_count INTEGER,
    last_login_date DATE,
    support_tier VARCHAR(20),
    created_at TIMESTAMP_NTZ NOT NULL,
    updated_at TIMESTAMP_NTZ NOT NULL
);

-- ZENDESK_EMPLOYEES table (3,954 records)  
-- Employee contacts with role-based distribution
CREATE OR REPLACE TABLE ZENDESK_EMPLOYEES (
    employee_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    title VARCHAR(100),
    role VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    hire_date DATE NOT NULL,
    is_primary_contact BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    last_login_date DATE,
    training_completed BOOLEAN,
    permissions VARCHAR(500),
    created_at TIMESTAMP_NTZ NOT NULL,
    updated_at TIMESTAMP_NTZ NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES ZENDESK_CUSTOMERS(customer_id)
);

-- ZENDESK_TICKETS table (19,824 records)
-- Support tickets with enhanced descriptions, seasonal patterns, and contextual intelligence
CREATE OR REPLACE TABLE ZENDESK_TICKETS (
    ticket_id INTEGER PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    employee_id VARCHAR(20) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    type VARCHAR(50) NOT NULL,
    via_channel VARCHAR(20) NOT NULL,
    satisfaction_rating VARCHAR(10),
    satisfaction_comment TEXT,
    tags VARCHAR(500),
    due_at TIMESTAMP_NTZ,
    created_at TIMESTAMP_NTZ NOT NULL,
    updated_at TIMESTAMP_NTZ NOT NULL,
    solved_at TIMESTAMP_NTZ,
    FOREIGN KEY (customer_id) REFERENCES ZENDESK_CUSTOMERS(customer_id),
    FOREIGN KEY (employee_id) REFERENCES ZENDESK_EMPLOYEES(employee_id)
);

-- CALL_TRANSCRIPTS table (13,550 records) - KEY AI INPUT
-- Rich conversation transcripts with enhanced variability and duration-aligned content
-- Context-intelligent conversations with realistic escalation patterns and specialized content
CREATE OR REPLACE TABLE CALL_TRANSCRIPTS (
    ticket_id INTEGER PRIMARY KEY,
    transcript_id INTEGER NOT NULL,
    call_duration INTEGER NOT NULL,
    transcript_text TEXT NOT NULL,
    call_date TIMESTAMP_NTZ NOT NULL,
    agent_name VARCHAR(100) NOT NULL,
    customer_satisfaction INTEGER NOT NULL,
    resolution_provided BOOLEAN NOT NULL,
    follow_up_needed BOOLEAN NOT NULL,
    FOREIGN KEY (ticket_id) REFERENCES ZENDESK_TICKETS(ticket_id)
);

-- TICKET_METRICS table (19,824 records)
-- Performance metrics with call-duration correlation and enhanced intelligence
CREATE OR REPLACE TABLE TICKET_METRICS (
    ticket_id INTEGER PRIMARY KEY,
    metric_id INTEGER,
    first_resolution_time INTEGER,
    full_resolution_time INTEGER,
    agent_work_time INTEGER,
    requester_wait_time INTEGER,
    reply_time INTEGER,
    group_stations INTEGER,
    assignee_stations INTEGER,
    reopens INTEGER,
    replies INTEGER,
    assignee_updated_at TIMESTAMP_NTZ,
    requester_updated_at TIMESTAMP_NTZ,
    status_updated_at TIMESTAMP_NTZ,
    initially_assigned_at TIMESTAMP_NTZ,
    assigned_at TIMESTAMP_NTZ,
    solved_at TIMESTAMP_NTZ,
    FOREIGN KEY (ticket_id) REFERENCES ZENDESK_TICKETS(ticket_id)
);

-- =====================================================================================
-- 3. CREATE FILE FORMAT AND STAGE
-- =====================================================================================

-- Create file format for CSV files with proper handling of quotes and nulls
CREATE OR REPLACE FILE FORMAT CSV_FORMAT 
TYPE = 'CSV' 
COMPRESSION = 'AUTO' 
FIELD_DELIMITER = ',' 
RECORD_DELIMITER = '\n' 
SKIP_HEADER = 1 
FIELD_OPTIONALLY_ENCLOSED_BY = '"' 
TRIM_SPACE = FALSE 
ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE 
ESCAPE = 'NONE' 
ESCAPE_UNENCLOSED_FIELD = '\134'
NULL_IF = ('\\N', 'NULL', 'null', '', 'nil');

-- Create internal stage for data loading
CREATE OR REPLACE STAGE ZENDESK_DATA_STAGE;

-- =====================================================================================
-- 4. DATA LOADING COMMANDS
-- =====================================================================================
-- Execute these commands after uploading CSV files to your local system
-- Replace /path/to/your/ with actual file paths from your zendesk_demo/data/ directory

-- Load ZENDESK_CUSTOMERS (load first due to foreign key dependencies)
PUT file:///Users/tgordonjr/Desktop/zendesk_demo/data/zendesk_customers.csv @ZENDESK_DATA_STAGE;

COPY INTO ZENDESK_CUSTOMERS
FROM @ZENDESK_DATA_STAGE/zendesk_customers.csv
FILE_FORMAT = (FORMAT_NAME = CSV_FORMAT)
ON_ERROR = 'ABORT_STATEMENT';

-- Load ZENDESK_EMPLOYEES (depends on customers)
PUT file:///Users/tgordonjr/Desktop/zendesk_demo/data/zendesk_employees.csv @ZENDESK_DATA_STAGE;

COPY INTO ZENDESK_EMPLOYEES  
FROM @ZENDESK_DATA_STAGE/zendesk_employees.csv
FILE_FORMAT = (FORMAT_NAME = CSV_FORMAT)
ON_ERROR = 'ABORT_STATEMENT';

-- Load ZENDESK_TICKETS (depends on customers and employees)
PUT file:///Users/tgordonjr/Desktop/zendesk_demo/data/zendesk_tickets.csv @ZENDESK_DATA_STAGE OVERWRITE=TRUE;

COPY INTO ZENDESK_TICKETS
FROM @ZENDESK_DATA_STAGE/zendesk_tickets.csv
FILE_FORMAT = (FORMAT_NAME = CSV_FORMAT)
ON_ERROR = 'ABORT_STATEMENT';

-- Load CALL_TRANSCRIPTS (depends on tickets) - KEY AI INPUT
PUT file:///Users/tgordonjr/Desktop/zendesk_demo/data/call_transcripts.csv @ZENDESK_DATA_STAGE OVERWRITE=TRUE;

COPY INTO CALL_TRANSCRIPTS
FROM @ZENDESK_DATA_STAGE/call_transcripts.csv
FILE_FORMAT = (FORMAT_NAME = CSV_FORMAT)  
ON_ERROR = 'ABORT_STATEMENT';

-- Load TICKET_METRICS (depends on tickets)
PUT file:///Users/tgordonjr/Desktop/zendesk_demo/data/ticket_metrics.csv @ZENDESK_DATA_STAGE OVERWRITE=TRUE;

COPY INTO TICKET_METRICS
FROM @ZENDESK_DATA_STAGE/ticket_metrics.csv
FILE_FORMAT = (FORMAT_NAME = CSV_FORMAT)
ON_ERROR = 'ABORT_STATEMENT';

-- =====================================================================================
-- NEXT STEPS AFTER DATA LOADING
-- =====================================================================================
/*
After successful data loading, you can proceed with:

1. Create Silver Layer Views with AI Functions:
   - SENTIMENT() analysis on enhanced call transcripts (context-aware conversations)
   - AI_CLASSIFY() for conversation categorization (payment, integration, training, etc.)
   - SUMMARIZE() for key insights extraction from varied transcript content
   - AI_SUMMARIZE_AGG() for trend analysis across customer segments

2. Create Gold Layer Business Views:
   - Customer health dashboards with call-resolution correlation
   - Churn risk scoring using satisfaction patterns and resolution times
   - Upselling opportunity identification from training/feature requests
   - Proactive outreach recommendations based on conversation analysis

3. Build Streamlit Application:
   - Interactive dashboards showing duration-transcript correlations
   - Cortex Analyst integration with enhanced contextual data
   - Real-time AI insights from sophisticated conversation patterns

Enhanced Features Now Available:
- Call transcripts with duration-aligned content (2-60 minutes with realistic scaling)
- Context-intelligent conversations (payment issues contain payment terminology)
- Enhanced ticket descriptions with thousands of variations
- Resolution time correlation with call complexity
- Realistic escalation patterns in long calls
- Organization-specific terminology and seasonal context

This Bronze layer provides a sophisticated foundation for demonstrating Snowflake's AI 
capabilities with realistic, varied conversation data that scales intelligently across
the complete customer lifecycle and support complexity spectrum.
*/

-- =====================================================================================
-- END OF SCRIPT
-- =====================================================================================