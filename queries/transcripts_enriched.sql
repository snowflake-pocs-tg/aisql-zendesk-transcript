-- =====================================================================================
-- ENRICHED TRANSCRIPT BASE TABLE - ALL AI FUNCTIONS
-- =====================================================================================
-- This table creates a comprehensive view of call transcripts enriched with all three
-- core Snowflake Cortex AI functions: SENTIMENT, AI_CLASSIFY, and SUMMARIZE

CREATE OR REPLACE TABLE ENRICHED_CALL_TRANSCRIPTS AS
SELECT 
    -- Core transcript fields
    ct.transcript_id,
    ct.ticket_id,
    ct.call_duration,
    ROUND(ct.call_duration / 60.0, 1) as call_duration_minutes,
    ct.transcript_text,
    ct.call_date,
    ct.agent_name,
    ct.customer_satisfaction,
    ct.resolution_provided,
    ct.follow_up_needed,
    
    -- AI Function 1: SENTIMENT Analysis
    SNOWFLAKE.CORTEX.SENTIMENT(ct.transcript_text) as sentiment_score,
    CASE 
        WHEN SNOWFLAKE.CORTEX.SENTIMENT(ct.transcript_text) >= 0.1 THEN 'Positive'
        WHEN SNOWFLAKE.CORTEX.SENTIMENT(ct.transcript_text) <= -0.1 THEN 'Negative'
        ELSE 'Neutral'
    END as sentiment_category,
    
    -- AI Function 2: AI_CLASSIFY for Conversation Categories
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
    
    -- AI Function 3: SUMMARIZE for Key Insights
    SNOWFLAKE.CORTEX.SUMMARIZE(ct.transcript_text) as conversation_summary,
    
    -- Metadata for analysis
    LENGTH(ct.transcript_text) as original_text_length,
    LENGTH(SNOWFLAKE.CORTEX.SUMMARIZE(ct.transcript_text)) as summary_length,
    ROUND(LENGTH(SNOWFLAKE.CORTEX.SUMMARIZE(ct.transcript_text)) * 100.0 / LENGTH(ct.transcript_text), 1) as compression_ratio

FROM CALL_TRANSCRIPTS ct
ORDER BY ct.call_date DESC;