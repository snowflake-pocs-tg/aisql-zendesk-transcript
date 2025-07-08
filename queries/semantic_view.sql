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
    metrics.full_resolution_time AS metrics.full_resolution_time,
    metrics.agent_work_time AS metrics.agent_work_time,
    metrics.requester_wait_time AS metrics.requester_wait_time,
    metrics.reply_time AS metrics.reply_time,
    metrics.reopens AS metrics.reopens,
    metrics.replies AS metrics.replies,
    customers.employee_count AS customers.employee_count,
    customers.monthly_revenue AS customers.monthly_revenue,
    customers.integration_count AS customers.integration_count
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
      COMMENT = 'Name of support agent who handled the call',
    customers.subscription_tier AS customers.subscription_tier
      WITH SYNONYMS = ('plan', 'subscription', 'tier')
      COMMENT = 'Customer subscription tier (Basic, Professional, Enterprise)',
    customers.support_tier AS customers.support_tier
      WITH SYNONYMS = ('support level', 'support plan', 'support tier')
      COMMENT = 'Customer support tier level',
    tickets.priority AS tickets.priority
      WITH SYNONYMS = ('ticket priority', 'urgency', 'importance')
      COMMENT = 'Priority level of support ticket',
    tickets.status AS tickets.status
      WITH SYNONYMS = ('ticket status', 'current status', 'state')
      COMMENT = 'Current status of support ticket',
    tickets.type AS tickets.type
      WITH SYNONYMS = ('ticket type', 'issue type', 'request type')
      COMMENT = 'Type of support ticket or request',
    tickets.via_channel AS tickets.via_channel
      WITH SYNONYMS = ('channel', 'contact method', 'submission method')
      COMMENT = 'Channel through which ticket was submitted',
    transcripts.resolution_provided AS transcripts.resolution_provided
      WITH SYNONYMS = ('resolved', 'solution provided', 'issue resolved')
      COMMENT = 'Whether a resolution was provided during the call',
    transcripts.follow_up_needed AS transcripts.follow_up_needed
      WITH SYNONYMS = ('follow up', 'needs follow up', 'requires follow up')
      COMMENT = 'Whether follow-up action is needed after the call'
  )
  
  METRICS (
    -- Call Volume and Duration Metrics
    transcripts.total_calls AS COUNT(ticket_id)
      COMMENT = 'Total number of support calls',
    transcripts.average_call_duration AS AVG(call_duration)
      COMMENT = 'Average call duration in seconds',
    transcripts.median_call_duration AS MEDIAN(call_duration)
      COMMENT = 'Median call duration in seconds',
    transcripts.total_call_minutes AS SUM(call_duration) / 60
      COMMENT = 'Total call time in minutes across all calls',
    transcripts.short_calls_rate AS AVG(CASE WHEN call_duration < 300 THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of calls under 5 minutes',
    transcripts.long_calls_rate AS AVG(CASE WHEN call_duration > 1800 THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of calls over 30 minutes',
    
    -- Customer Satisfaction Metrics
    transcripts.average_satisfaction AS AVG(customer_satisfaction)
      COMMENT = 'Average customer satisfaction rating',
    transcripts.high_satisfaction_rate AS AVG(CASE WHEN customer_satisfaction >= 4 THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of calls with high satisfaction (4-5 rating)',
    transcripts.low_satisfaction_rate AS AVG(CASE WHEN customer_satisfaction <= 2 THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of calls with low satisfaction (1-2 rating)',
    transcripts.satisfaction_distribution AS COUNT(ticket_id)
      COMMENT = 'Distribution of satisfaction ratings',
    
    -- AI Sentiment Analysis Metrics
    transcripts.average_sentiment_score AS AVG(sentiment_score)
      COMMENT = 'Average AI sentiment score across all calls',
    transcripts.positive_sentiment_rate AS AVG(CASE WHEN sentiment_category = 'Positive' THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of calls with positive sentiment',
    transcripts.negative_sentiment_rate AS AVG(CASE WHEN sentiment_category = 'Negative' THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of calls with negative sentiment',
    transcripts.neutral_sentiment_rate AS AVG(CASE WHEN sentiment_category = 'Neutral' THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of calls with neutral sentiment',
    
    -- Resolution and Performance Metrics
    metrics.average_first_resolution_time AS AVG(first_resolution_time)
      COMMENT = 'Average time to first resolution in hours',
    metrics.average_full_resolution_time AS AVG(full_resolution_time)
      COMMENT = 'Average time to full resolution in hours',
    metrics.average_agent_work_time AS AVG(agent_work_time)
      COMMENT = 'Average agent work time in hours',
    metrics.average_requester_wait_time AS AVG(requester_wait_time)
      COMMENT = 'Average requester wait time in hours',
    metrics.average_reply_time AS AVG(reply_time)
      COMMENT = 'Average reply time in hours',
    metrics.sla_compliance_rate AS AVG(CASE WHEN first_resolution_time <= 24 THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of tickets resolved within 24 hours',
    
    -- Ticket Reopen and Reply Metrics
    metrics.average_reopens AS AVG(reopens)
      COMMENT = 'Average number of times tickets are reopened',
    metrics.reopen_rate AS AVG(CASE WHEN reopens > 0 THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of tickets that were reopened',
    metrics.average_replies AS AVG(replies)
      COMMENT = 'Average number of replies per ticket',
    metrics.high_touch_tickets_rate AS AVG(CASE WHEN replies > 5 THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of tickets with more than 5 replies',
    
    -- Resolution Quality Metrics
    transcripts.resolution_rate AS AVG(CASE WHEN resolution_provided = TRUE THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of calls where resolution was provided',
    transcripts.follow_up_rate AS AVG(CASE WHEN follow_up_needed = TRUE THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of calls requiring follow-up',
    transcripts.one_call_resolution_rate AS AVG(CASE WHEN resolution_provided = TRUE AND follow_up_needed = FALSE THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of issues resolved in one call without follow-up',
    
    -- Customer Success Metrics
    customers.total_revenue AS SUM(monthly_revenue)
      COMMENT = 'Total monthly revenue across all customers',
    customers.average_revenue_per_customer AS AVG(monthly_revenue)
      COMMENT = 'Average monthly revenue per customer',
    customers.enterprise_customer_rate AS AVG(CASE WHEN subscription_tier = 'Enterprise' THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of enterprise customers',
    customers.large_organization_rate AS AVG(CASE WHEN size_category = 'large' THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of large organizations',
    customers.average_employee_count AS AVG(employee_count)
      COMMENT = 'Average number of employees per customer organization',
    customers.average_integration_count AS AVG(integration_count)
      COMMENT = 'Average number of integrations per customer',
    
    -- Ticket Volume and Distribution Metrics
    tickets.total_tickets AS COUNT(tickets.ticket_id)
      COMMENT = 'Total number of support tickets',
    tickets.urgent_ticket_rate AS AVG(CASE WHEN priority = 'urgent' THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of urgent priority tickets',
    tickets.high_priority_rate AS AVG(CASE WHEN priority IN ('urgent', 'high') THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of high priority tickets',
    tickets.open_ticket_rate AS AVG(CASE WHEN status = 'open' THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of tickets that are currently open',
    tickets.solved_ticket_rate AS AVG(CASE WHEN status = 'solved' THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of tickets that are solved',
    
    -- Channel Performance Metrics
    tickets.web_channel_rate AS AVG(CASE WHEN via_channel = 'web' THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of tickets submitted via web',
    tickets.email_channel_rate AS AVG(CASE WHEN via_channel = 'email' THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of tickets submitted via email',
    tickets.phone_channel_rate AS AVG(CASE WHEN via_channel = 'phone' THEN 1 ELSE 0 END)
      COMMENT = 'Percentage of tickets submitted via phone',
    
    -- Agent Performance Metrics
    transcripts.unique_agents AS COUNT(DISTINCT agent_name)
      COMMENT = 'Number of unique support agents',
    transcripts.calls_per_agent AS COUNT(ticket_id) / COUNT(DISTINCT agent_name)
      COMMENT = 'Average number of calls per agent',
    transcripts.agent_satisfaction_score AS AVG(customer_satisfaction)
      COMMENT = 'Average satisfaction score by agent'
  )
  
  COMMENT = 'Comprehensive semantic view combining AI-enriched call transcripts with customer success data for natural language business intelligence';