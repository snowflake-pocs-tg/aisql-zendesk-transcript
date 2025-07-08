-- =====================================================================================
-- ZENDESK ANALYTICS POC - AI SQL QUERIES
-- =====================================================================================
-- This file contains Snowflake Cortex AI function queries for analyzing call transcripts
-- and support data to demonstrate AI-powered customer success insights.
-- =====================================================================================

-- =====================================================================================
-- SENTIMENT ANALYSIS ON CALL TRANSCRIPTS
-- =====================================================================================
-- This query uses Snowflake's SENTIMENT() function to analyze call transcript emotions
-- and correlate them with customer satisfaction and resolution outcomes

SELECT 
    ct.transcript_id,
    ct.ticket_id,
    ct.agent_name,
    ct.call_duration,
    ROUND(ct.call_duration / 60.0, 1) as call_duration_minutes,
    ct.customer_satisfaction,
    ct.resolution_provided,
    ct.follow_up_needed,
    
    -- Snowflake Cortex AI Sentiment Analysis
    SNOWFLAKE.CORTEX.SENTIMENT(ct.transcript_text) as sentiment_score,
    
    -- Categorize sentiment into business-friendly labels
    CASE 
        WHEN SNOWFLAKE.CORTEX.SENTIMENT(ct.transcript_text) >= 0.1 THEN 'Positive'
        WHEN SNOWFLAKE.CORTEX.SENTIMENT(ct.transcript_text) <= -0.1 THEN 'Negative'
        ELSE 'Neutral'
    END as sentiment_category,
    
    -- Get ticket context
    t.priority as ticket_priority,
    t.status as ticket_status,
    c.organization_type,
    c.size_category,
    c.subscription_tier,
    
    -- Calculate metrics
    LENGTH(ct.transcript_text) as transcript_length,
    ct.call_date

FROM CALL_TRANSCRIPTS ct
JOIN ZENDESK_TICKETS t ON ct.ticket_id = t.ticket_id
JOIN ZENDESK_CUSTOMERS c ON t.customer_id = c.customer_id
ORDER BY ct.call_date DESC
LIMIT 100;

-- =====================================================================================
-- CONVERSATION CLASSIFICATION ANALYSIS
-- =====================================================================================
-- This query uses Snowflake's AI_CLASSIFY() function to categorize call transcripts
-- into business-relevant categories for better support insights and routing

SELECT 
    ct.transcript_id,
    ct.ticket_id,
    ct.agent_name,
    ct.call_duration,
    ROUND(ct.call_duration / 60.0, 1) as call_duration_minutes,
    ct.customer_satisfaction,
    
    -- Snowflake Cortex AI Classification (raw JSON response)
    SNOWFLAKE.CORTEX.AI_CLASSIFY(
        ct.transcript_text,
        [
            'Payment Processing Issues',
            'Integration and Technical Support', 
            'Training and User Education',
            'Feature Requests and Enhancements',
            'Account Management and Billing'
        ]
    ) as classification_raw,
    
    -- Parse the JSON response to extract the category
    SNOWFLAKE.CORTEX.AI_CLASSIFY(
        ct.transcript_text,
        [
            'Payment Processing Issues',
            'Integration and Technical Support', 
            'Training and User Education',
            'Feature Requests and Enhancements',
            'Account Management and Billing'
        ]
    ):labels[0]::string as conversation_category,
    
    -- Get ticket context for validation
    t.priority as ticket_priority,
    t.status as ticket_status,
    c.organization_type,
    c.size_category,
    
    -- Add sentiment for correlation
    SNOWFLAKE.CORTEX.SENTIMENT(ct.transcript_text) as sentiment_score,
    
    ct.call_date

FROM CALL_TRANSCRIPTS ct
JOIN ZENDESK_TICKETS t ON ct.ticket_id = t.ticket_id
JOIN ZENDESK_CUSTOMERS c ON t.customer_id = c.customer_id
ORDER BY ct.call_date DESC
LIMIT 100;

-- =====================================================================================
-- CONVERSATION SUMMARIZATION ANALYSIS
-- =====================================================================================
-- This query uses Snowflake's SUMMARIZE() function to generate concise summaries
-- of call transcripts for executive reporting and trend analysis

SELECT 
    ct.transcript_id,
    ct.ticket_id,
    ct.agent_name,
    ct.call_duration,
    ROUND(ct.call_duration / 60.0, 1) as call_duration_minutes,
    ct.customer_satisfaction,
    
    -- Snowflake Cortex AI Summarization
    SNOWFLAKE.CORTEX.SUMMARIZE(ct.transcript_text) as conversation_summary,
    
    -- Classification for context
    SNOWFLAKE.CORTEX.AI_CLASSIFY(
        ct.transcript_text,
        [
            'Payment Processing Issues',
            'Integration and Technical Support', 
            'Training and User Education',
            'Feature Requests and Enhancements',
            'Account Management and Billing'
        ]
    ):labels[0]::string as conversation_category,
    
    -- Sentiment for correlation
    SNOWFLAKE.CORTEX.SENTIMENT(ct.transcript_text) as sentiment_score,
    
    -- Get ticket context
    t.priority as ticket_priority,
    t.status as ticket_status,
    c.organization_type,
    c.size_category,
    
    -- Calculate summary length vs original
    LENGTH(ct.transcript_text) as original_length,
    LENGTH(SNOWFLAKE.CORTEX.SUMMARIZE(ct.transcript_text)) as summary_length,
    ROUND(LENGTH(SNOWFLAKE.CORTEX.SUMMARIZE(ct.transcript_text)) * 100.0 / LENGTH(ct.transcript_text), 1) as compression_ratio,
    
    ct.call_date

FROM CALL_TRANSCRIPTS ct
JOIN ZENDESK_TICKETS t ON ct.ticket_id = t.ticket_id
JOIN ZENDESK_CUSTOMERS c ON t.customer_id = c.customer_id
WHERE ct.call_duration > 600  -- Focus on longer calls (>10 minutes) for meaningful summaries
ORDER BY ct.call_duration DESC
LIMIT 50;

-- =====================================================================================
-- ZENDESK CUSTOMER SUCCESS SEMANTIC VIEW
-- =====================================================================================
-- This semantic view combines AI-enriched transcript data with customer, employee, 
-- ticket, and metrics data to provide a comprehensive business intelligence layer
-- for Cortex Analyst and natural language querying

CREATE OR REPLACE SEMANTIC VIEW ZENDESK_CUSTOMER_SUCCESS_ANALYTICS
  TABLES (
    -- Core transcript table with AI enrichment
    transcripts AS ENRICHED_CALL_TRANSCRIPTS
      PRIMARY KEY (ticket_id)
      WITH SYNONYMS ('call transcripts', 'conversations', 'support calls')
      COMMENT = 'Call transcripts enriched with AI sentiment, classification, and summarization',
    
    -- Customer data
    customers AS ZENDESK_CUSTOMERS
      PRIMARY KEY (customer_id)
      WITH SYNONYMS ('clients', 'organizations', 'accounts')
      COMMENT = 'Zendesk customer organizations including enterprises, mid-market, and small businesses',
    
    -- Employee contacts
    employees AS ZENDESK_EMPLOYEES
      PRIMARY KEY (employee_id)
      WITH SYNONYMS ('contacts', 'users', 'staff')
      COMMENT = 'Customer employee contacts who create support tickets',
    
    -- Support tickets
    tickets AS ZENDESK_TICKETS
      PRIMARY KEY (ticket_id)
      WITH SYNONYMS ('support tickets', 'issues', 'requests')
      COMMENT = 'Support tickets with enhanced descriptions and contextual intelligence',
    
    -- Performance metrics
    metrics AS TICKET_METRICS
      PRIMARY KEY (ticket_id)
      WITH SYNONYMS ('performance metrics', 'ticket metrics', 'resolution data')
      COMMENT = 'Ticket resolution metrics with call-duration correlation'
  )
  
  RELATIONSHIPS (
    -- Define relationships between entities
    transcript_to_ticket AS
      transcripts (ticket_id) REFERENCES tickets,
    ticket_to_customer AS
      tickets (customer_id) REFERENCES customers,
    ticket_to_employee AS
      tickets (employee_id) REFERENCES employees,
    metric_to_ticket AS
      metrics (ticket_id) REFERENCES tickets,
    employee_to_customer AS
      employees (customer_id) REFERENCES customers
  )
  
  FACTS (
    transcripts.call_duration AS transcripts.call_duration,
    transcripts.customer_satisfaction AS transcripts.customer_satisfaction,
    transcripts.sentiment_score AS transcripts.sentiment_score,
    metrics.first_resolution_time AS metrics.first_resolution_time,
    customers.employee_count AS customers.employee_count,
    customers.monthly_revenue AS customers.monthly_revenue
  )
  
  DIMENSIONS (
    transcripts.call_date AS transcripts.call_date
      WITH SYNONYMS = ('call date', 'conversation date', 'support date')
      COMMENT = 'Date when the support call occurred',
    transcripts.sentiment_category AS transcripts.sentiment_category
      WITH SYNONYMS = ('sentiment', 'customer mood', 'conversation tone')
      COMMENT = 'AI-determined sentiment category from call transcript',
    transcripts.conversation_category AS transcripts.conversation_category
      WITH SYNONYMS = ('issue category', 'conversation type', 'support category')
      COMMENT = 'AI-classified conversation category based on transcript content',
    customers.organization_type AS customers.organization_type
      WITH SYNONYMS = ('org type', 'customer type', 'industry')
      COMMENT = 'Type of customer organization (faith, school, nonprofit, etc.)',
    customers.size_category AS customers.size_category
      WITH SYNONYMS = ('customer size', 'organization size', 'company size')
      COMMENT = 'Size category of customer organization (small, medium, large)',
    transcripts.agent_name AS transcripts.agent_name
      WITH SYNONYMS = ('agent', 'support agent', 'representative')
      COMMENT = 'Name of support agent who handled the call'
  )
  
  METRICS (
    transcripts.total_calls AS COUNT(ticket_id)
      COMMENT = 'Total number of support calls',
    transcripts.average_call_duration AS AVG(call_duration)
      COMMENT = 'Average call duration in seconds',
    transcripts.average_satisfaction AS AVG(customer_satisfaction)
      COMMENT = 'Average customer satisfaction rating',
    transcripts.average_sentiment_score AS AVG(sentiment_score)
      COMMENT = 'Average AI sentiment score across all calls',
    transcripts.positive_sentiment_rate AS AVG(CASE WHEN sentiment_category = 'Positive' THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of calls with positive sentiment',
    metrics.average_resolution_time AS AVG(first_resolution_time)
      COMMENT = 'Average time to fully resolve tickets in hours'
  )
  
  COMMENT = 'Comprehensive semantic view combining AI-enriched call transcripts with customer success data for natural language business intelligence';