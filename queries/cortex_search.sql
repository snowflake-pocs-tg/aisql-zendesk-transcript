-- =====================================================================================
-- ZENDESK CORTEX SEARCH SERVICE SETUP
-- =====================================================================================
-- This script creates a comprehensive Cortex Search service for the Zendesk Analytics POC
-- leveraging AI-enriched call transcripts with dynamic filtering capabilities.
--
-- Features:
-- - Hybrid vector and keyword search on conversation summaries
-- - Rich metadata for filtering (customer tiers, sentiment, agent performance)
-- - Cross-table joins for comprehensive business context
-- - Support for natural language queries with business intelligence
-- - BOOLEAN columns converted to VARCHAR ('Yes'/'No') for Cortex Search compatibility
-- =====================================================================================

-- =====================================================================================
-- 1. PREREQUISITES AND SETUP
-- =====================================================================================

-- Use the existing database and schema
USE DATABASE ZENDESK_ANALYTICS_POC;
USE SCHEMA BRONZE;

-- Create dedicated warehouse for Cortex Search (recommended best practice)
CREATE OR REPLACE WAREHOUSE CORTEX_SEARCH_WH 
WITH 
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    COMMENT = 'Dedicated warehouse for Zendesk Cortex Search operations';

-- Enable change tracking on source tables (required for Cortex Search)
ALTER TABLE ENRICHED_CALL_TRANSCRIPTS SET CHANGE_TRACKING = TRUE;
ALTER TABLE ZENDESK_CUSTOMERS SET CHANGE_TRACKING = TRUE;
ALTER TABLE ZENDESK_EMPLOYEES SET CHANGE_TRACKING = TRUE;
ALTER TABLE ZENDESK_TICKETS SET CHANGE_TRACKING = TRUE;
ALTER TABLE TICKET_METRICS SET CHANGE_TRACKING = TRUE;

-- =====================================================================================
-- 2. CREATE SEARCH-OPTIMIZED VIEW WITH RICH METADATA
-- =====================================================================================

-- Create a comprehensive view that joins all relevant tables for search and filtering
CREATE OR REPLACE VIEW CORTEX_SEARCH_ENRICHED_VIEW AS
SELECT 
    -- Primary search content (conversation summaries)
    ect.conversation_summary,
    ect.transcript_text,
    
    -- Core identifiers
    ect.transcript_id,
    ect.ticket_id,
    ect.call_date,
    
    -- Call and sentiment metrics  
    ect.call_duration,
    ect.call_duration_minutes,
    ect.sentiment_score,
    ect.sentiment_category,
    ect.conversation_category,
    ect.customer_satisfaction,
    CASE WHEN ect.resolution_provided = TRUE THEN 'Yes' ELSE 'No' END as resolution_provided,
    CASE WHEN ect.follow_up_needed = TRUE THEN 'Yes' ELSE 'No' END as follow_up_needed,
    ect.agent_name,
    
    -- Customer context for filtering
    c.customer_id,
    c.organization_name,
    c.organization_type,
    c.organization_subtype,
    c.size_category,
    c.subscription_tier,
    c.support_tier,
    c.monthly_revenue,
    c.employee_count,
    c.integration_count,
    
    -- Ticket context for filtering
    t.priority,
    t.status,
    t.type as ticket_type,
    t.via_channel,
    t.created_at as ticket_created_at,
    t.updated_at as ticket_updated_at,
    
    -- Employee context
    e.first_name as employee_first_name,
    e.last_name as employee_last_name,
    e.email as employee_email,
    e.title as employee_title,
    e.role as employee_role,
    e.department as employee_department,
    CASE WHEN e.is_primary_contact = TRUE THEN 'Yes' ELSE 'No' END as is_primary_contact,
    CASE WHEN e.is_active = TRUE THEN 'Yes' ELSE 'No' END as is_active,
    
    -- Performance metrics for filtering
    tm.first_resolution_time,
    tm.full_resolution_time,
    tm.agent_work_time,
    tm.requester_wait_time,
    tm.reply_time,
    tm.reopens,
    tm.replies,
    
    -- Derived business metrics for advanced filtering
    CASE 
        WHEN tm.first_resolution_time <= 24 THEN 'SLA_Met'
        ELSE 'SLA_Missed'
    END as sla_status,
    
    CASE 
        WHEN ect.customer_satisfaction >= 4 THEN 'High_Satisfaction'
        WHEN ect.customer_satisfaction >= 3 THEN 'Medium_Satisfaction'
        ELSE 'Low_Satisfaction'
    END as satisfaction_level,
    
    CASE 
        WHEN c.monthly_revenue >= 1000 THEN 'High_Value'
        WHEN c.monthly_revenue >= 500 THEN 'Medium_Value'
        ELSE 'Low_Value'
    END as customer_value_tier,
    
    CASE 
        WHEN ect.call_duration_minutes <= 5 THEN 'Quick_Call'
        WHEN ect.call_duration_minutes <= 20 THEN 'Standard_Call'
        ELSE 'Extended_Call'
    END as call_duration_category,
    
    -- Search-friendly concatenated fields
    CONCAT(c.organization_name, ' - ', c.organization_type, ' - ', c.size_category) as customer_profile,
    CONCAT(ect.agent_name, ' - ', e.department, ' - ', e.role) as agent_profile,
    CONCAT(t.type, ' - ', t.priority, ' - ', t.via_channel) as ticket_profile

FROM ENRICHED_CALL_TRANSCRIPTS ect
    INNER JOIN ZENDESK_TICKETS t ON ect.ticket_id = t.ticket_id
    INNER JOIN ZENDESK_CUSTOMERS c ON t.customer_id = c.customer_id
    INNER JOIN ZENDESK_EMPLOYEES e ON t.employee_id = e.employee_id
    LEFT JOIN TICKET_METRICS tm ON ect.ticket_id = tm.ticket_id
ORDER BY ect.call_date DESC;

-- =====================================================================================
-- 3. CREATE CORTEX SEARCH SERVICE
-- =====================================================================================

-- Create the main Cortex Search service on conversation summaries with rich attributes
CREATE OR REPLACE CORTEX SEARCH SERVICE ZENDESK_CONVERSATION_SEARCH
    ON conversation_summary
    ATTRIBUTES 
        transcript_id,
        ticket_id,
        call_date,
        sentiment_category,
        conversation_category,
        customer_satisfaction,
        resolution_provided,
        follow_up_needed,
        agent_name,
        organization_name,
        organization_type,
        size_category,
        subscription_tier,
        support_tier,
        monthly_revenue,
        priority,
        status,
        ticket_type,
        via_channel,
        employee_role,
        employee_department,
        is_primary_contact,
        is_active,
        first_resolution_time,
        sla_status,
        satisfaction_level,
        customer_value_tier,
        call_duration_category,
        customer_profile,
        agent_profile,
        ticket_profile
    WAREHOUSE = CORTEX_SEARCH_WH
    TARGET_LAG = '1 hour'
    EMBEDDING_MODEL = 'snowflake-arctic-embed-l-v2.0'
    COMMENT = 'Zendesk customer success conversation search with AI-enriched summaries and business context'
AS (
    SELECT * FROM CORTEX_SEARCH_ENRICHED_VIEW
);

-- =====================================================================================
-- 4. ADDITIONAL SEARCH SERVICES FOR SPECIFIC USE CASES
-- =====================================================================================

-- Create a secondary search service on full transcript text for detailed analysis
CREATE OR REPLACE CORTEX SEARCH SERVICE ZENDESK_TRANSCRIPT_SEARCH
    ON transcript_text
    ATTRIBUTES 
        transcript_id,
        ticket_id,
        conversation_summary,
        sentiment_category,
        conversation_category,
        agent_name,
        organization_name,
        customer_satisfaction
    WAREHOUSE = CORTEX_SEARCH_WH
    TARGET_LAG = '2 hours'
    EMBEDDING_MODEL = 'snowflake-arctic-embed-l-v2.0'
    COMMENT = 'Full transcript text search for detailed conversation analysis'
AS (
    SELECT 
        transcript_text,
        transcript_id,
        ticket_id,
        conversation_summary,
        sentiment_category,
        conversation_category,
        agent_name,
        organization_name,
        customer_satisfaction
    FROM CORTEX_SEARCH_ENRICHED_VIEW
);

-- =====================================================================================
-- 5. SEARCH QUERY EXAMPLES AND TESTING
-- =====================================================================================

-- Example 1: Basic conversation search
-- SELECT * FROM TABLE(SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
--     'ZENDESK_CONVERSATION_SEARCH',
--     'payment processing issues'
-- ));

-- Example 2: Search with filtering
-- SELECT * FROM TABLE(SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
--     'ZENDESK_CONVERSATION_SEARCH',
--     'integration problems',
--     '{
--         "filter": {
--             "AND": [
--                 {"@eq": {"subscription_tier": "Enterprise"}},
--                 {"@eq": {"sentiment_category": "Negative"}}
--             ]
--         }
--     }'
-- ));

-- Example 3: Search with multiple filters and ranking
-- SELECT * FROM TABLE(SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
--     'ZENDESK_CONVERSATION_SEARCH',
--     'training and education requests',
--     '{
--         "filter": {
--             "AND": [
--                 {"@eq": {"organization_type": "school"}},
--                 {"@eq": {"sla_status": "SLA_Met"}},
--                 {"@gte": {"customer_satisfaction": 4}}
--             ]
--         },
--         "limit": 10
--     }'
-- ));

-- =====================================================================================
-- 6. UTILITY QUERIES FOR SEARCH SERVICE MANAGEMENT
-- =====================================================================================

-- Show all Cortex Search services
-- SHOW CORTEX SEARCH SERVICES;

-- Describe the search service structure
-- DESCRIBE CORTEX SEARCH SERVICE ZENDESK_CONVERSATION_SEARCH;

-- Check search service status and refresh information
-- SELECT 
--     service_name,
--     service_url,
--     definition,
--     enabled,
--     search_column,
--     attribute_columns,
--     created_on,
--     refreshed_on
-- FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));

-- =====================================================================================
-- 7. ADVANCED SEARCH PATTERNS AND USE CASES
-- =====================================================================================

-- Common search patterns for business users:

-- 1. Customer Success Analysis
/*
SELECT 
    transcript_id,
    organization_name,
    conversation_summary,
    sentiment_category,
    customer_satisfaction,
    monthly_revenue
FROM TABLE(SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'ZENDESK_CONVERSATION_SEARCH',
    'customer concerns dissatisfaction',
    '{"filter": {"@eq": {"customer_value_tier": "High_Value"}}, "limit": 20}'
));
*/

-- 2. Agent Performance Analysis
/*
SELECT 
    agent_name,
    conversation_summary,
    resolution_provided,
    customer_satisfaction,
    call_duration_category
FROM TABLE(SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'ZENDESK_CONVERSATION_SEARCH',
    'quick resolution excellent service',
    '{"filter": {"AND": [{"@eq": {"call_duration_category": "Quick_Call"}}, {"@eq": {"resolution_provided": "Yes"}}]}, "limit": 15}'
));
*/

-- 3. Product Issue Analysis
/*
SELECT 
    conversation_category,
    conversation_summary,
    organization_type,
    ticket_type,
    priority
FROM TABLE(SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'ZENDESK_CONVERSATION_SEARCH',
    'feature request enhancement improvement',
    '{"filter": {"@eq": {"conversation_category": "Feature Requests and Enhancements"}}, "limit": 25}'
));
*/

-- 4. SLA and Performance Monitoring
/*
SELECT 
    organization_name,
    conversation_summary,
    sla_status,
    first_resolution_time,
    agent_name
FROM TABLE(SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'ZENDESK_CONVERSATION_SEARCH',
    'urgent critical immediate',
    '{"filter": {"@eq": {"sla_status": "SLA_Missed"}}, "limit": 30}'
));
*/

-- =====================================================================================
-- 8. MAINTENANCE AND MONITORING
-- =====================================================================================

-- Monitor search service performance
-- CREATE OR REPLACE VIEW CORTEX_SEARCH_PERFORMANCE AS
-- SELECT 
--     COUNT(*) as total_searchable_records,
--     COUNT(DISTINCT organization_type) as unique_org_types,
--     COUNT(DISTINCT conversation_category) as unique_categories,
--     COUNT(DISTINCT agent_name) as unique_agents,
--     AVG(customer_satisfaction) as avg_satisfaction,
--     COUNT(CASE WHEN sentiment_category = 'Positive' THEN 1 END) as positive_conversations,
--     COUNT(CASE WHEN sla_status = 'SLA_Met' THEN 1 END) as sla_compliant_calls
-- FROM CORTEX_SEARCH_ENRICHED_VIEW;

-- =====================================================================================
-- END OF SCRIPT
-- =====================================================================================

-- Next Steps:
-- 1. Execute this script to create the Cortex Search services
-- 2. Test search functionality with the provided examples
-- 3. Integrate with Cortex Analyst for natural language business intelligence
-- 4. Build applications using the search services for customer success insights
-- 5. Monitor and optimize search performance based on usage patterns