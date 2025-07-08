# Cortex Analyst Test Queries for Zendesk Customer Success Analytics

This document contains natural language queries organized by business use cases to test the `ZENDESK_CUSTOMER_SUCCESS_ANALYTICS` semantic view with Snowflake Cortex Analyst.

## Use Case 1: AI-Powered Customer Sentiment Analysis

#### Cortex Analyst Questions:
1. **Overall sentiment health**: "What's the average sentiment score across all customer calls?"
2. **Sentiment distribution**: "What percentage of calls are classified as positive, negative, or neutral sentiment?"
3. **Sentiment by organization**: "Which organization types have the highest sentiment scores?"
4. **Sentiment trends**: "Show me the trend in positive sentiment calls over the last 6 months"
5. **Negative sentiment analysis**: "What are the most common conversation categories for calls with negative sentiment?"
6. **Duration correlation**: "Do longer calls tend to have more negative sentiment scores?"
7. **Subscription tier sentiment**: "Compare sentiment scores between Basic, Professional, and Enterprise customers"
8. **Resolution impact**: "What percentage of negative sentiment calls result in resolution provided?"
9. **Channel sentiment**: "Which support channels have the highest positive sentiment rates?"
10. **Sentiment recovery**: "What's the sentiment score for calls that were reopened versus one-time resolutions?"

### Cortex Search

#### Using ZENDESK_CONVERSATION_SEARCH:
1. **Search for sentiment patterns**: "Find conversations with customers expressing frustration about our service"
2. **Customer tier insights**: "Show me conversations from Enterprise customers with negative sentiment"
3. **Agent performance examples**: "Find conversations where agents provided excellent customer service"
4. **Topic-specific search**: "Search for conversations about pricing concerns or billing issues"
5. **Resolution success stories**: "Find conversations where customers were highly satisfied with quick resolutions"

#### Using ZENDESK_TRANSCRIPT_SEARCH:
1. **Exact phrase analysis**: "Find transcripts containing 'refund policy' or 'cancellation request'"
2. **Training examples**: "Search for transcripts with excellent agent responses to technical questions"
3. **Compliance review**: "Find transcripts mentioning 'data privacy' or 'security concerns'"
4. **Product feedback**: "Search for detailed customer feedback about specific features"
5. **Escalation analysis**: "Find transcripts with customers asking to speak to a manager"

## Use Case 2: AI-Classified Conversation Analysis

#### Cortex Analyst Questions:
1. **Category distribution**: "What are the most common conversation categories in our support calls?"
2. **Payment issues analysis**: "How many calls are classified as 'Payment Processing Issues' and what's their sentiment?"
3. **Integration vs training**: "Compare sentiment scores between 'Integration and Technical Support' and 'Training and User Education' calls"
4. **Feature request sentiment**: "What's the average sentiment score for calls classified as 'Feature Requests and Enhancements'?"
5. **Billing trends**: "Show me the trend in 'Account Management and Billing' conversations over time"
6. **Priority by category**: "Which conversation categories have the highest percentage of urgent priority tickets?"
7. **First-call resolution**: "What percentage of calls are resolved on the first try for each conversation category?"
8. **Duration patterns**: "Which conversation categories have the longest average call duration?"
9. **Follow-up requirements**: "Which conversation categories most frequently require follow-up actions?"
10. **Size correlation**: "How do conversation categories differ between small, medium, and large customer organizations?"

### Cortex Search

#### Using ZENDESK_CONVERSATION_SEARCH:
1. **Issue categorization**: "Find conversations about integration problems with CRM systems"
2. **Category performance**: "Search for payment processing conversations with positive outcomes"
3. **Feature request analysis**: "Find conversations where customers requested new features"
4. **Training vs support**: "Show me conversations categorized as training requests from school customers"
5. **Category-specific sentiment**: "Find billing-related conversations with negative sentiment"

#### Using ZENDESK_TRANSCRIPT_SEARCH:
1. **Detailed issue analysis**: "Search transcripts for specific error messages or technical problems"
2. **Solution identification**: "Find transcripts with successful troubleshooting steps for integration issues"
3. **Category validation**: "Search for transcripts to validate conversation categorization accuracy"
4. **Customer language patterns**: "Find how customers actually describe payment processing problems"
5. **Agent response quality**: "Search for transcripts showing excellent handling of feature requests"

## Use Case 3: Support Performance & Resolution Metrics

#### Cortex Analyst Questions:
1. **Resolution time overview**: "What's the average first resolution time across all tickets?"
2. **SLA compliance**: "What percentage of tickets are resolved within 24 hours?"
3. **Agent efficiency**: "Which agents have the lowest average agent work time while maintaining high satisfaction?"
4. **Wait time analysis**: "What's the average requester wait time by ticket priority level?"
5. **Reopen patterns**: "Which customer organization types have the highest ticket reopen rates?"
6. **High-touch tickets**: "What percentage of tickets require more than 5 replies?"
7. **Channel performance**: "Compare average resolution times between web, email, and phone support channels"
8. **Resolution gap**: "What's the difference between first resolution time and full resolution time by ticket type?"
9. **Tier performance**: "Do Enterprise customers get faster resolution times than Basic customers?"
10. **Escalation analysis**: "Which ticket types have the highest number of average replies before resolution?"

### Cortex Search

#### Using ZENDESK_CONVERSATION_SEARCH:
1. **Performance optimization**: "Find conversations from tickets that met SLA targets with high satisfaction"
2. **Resolution examples**: "Search for conversations with quick first-time resolution success"
3. **Wait time analysis**: "Find conversations mentioning long wait times or delays"
4. **Channel effectiveness**: "Search for conversations from phone support with excellent outcomes"
5. **Escalation patterns**: "Find conversations that required multiple interactions to resolve"

#### Using ZENDESK_TRANSCRIPT_SEARCH:
1. **Efficiency examples**: "Search for transcripts showing rapid problem identification and resolution"
2. **SLA compliance**: "Find transcripts from tickets that barely met or missed SLA targets"
3. **Performance bottlenecks**: "Search for transcripts revealing common delays in resolution process"
4. **Best practices**: "Find transcripts demonstrating efficient troubleshooting techniques"
5. **Channel comparison**: "Search for differences in conversation quality between web and phone support"

## Use Case 4: Support Agent AI Performance Analysis

#### Cortex Analyst Questions:
1. **Agent sentiment impact**: "Which support agents generate the highest average sentiment scores?"
2. **Issue-specific performance**: "Which agents handle 'Payment Processing Issues' with the best sentiment outcomes?"
3. **Resolution effectiveness**: "What percentage of calls by each agent result in resolution provided?"
4. **Follow-up efficiency**: "Which agents have the lowest follow-up needed rates?"
5. **Efficiency balance**: "Which agents have the best balance of call duration and positive sentiment?"
6. **Workload analysis**: "How many calls does each agent handle on average and what's their satisfaction score?"
7. **One-call resolution**: "Which agents have the highest one-call resolution rate without follow-up needed?"
8. **Tier performance**: "Which agents perform best when handling Enterprise versus Basic tier customers?"
9. **Escalation management**: "Which agents have the lowest average number of ticket reopens?"
10. **Duration optimization**: "Which agents maintain high satisfaction while keeping call duration under 15 minutes?"

### Cortex Search

#### Using ZENDESK_CONVERSATION_SEARCH:
1. **Agent excellence**: "Find conversations handled by top-performing agents with high satisfaction"
2. **Training opportunities**: "Search for conversations showing areas where agents need improvement"
3. **Agent specialization**: "Find conversations where specific agents excel at certain issue types"
4. **Performance consistency**: "Search for conversations from agents with variable performance"
5. **Customer feedback on agents**: "Find conversations with specific customer praise or concerns about agent performance"

#### Using ZENDESK_TRANSCRIPT_SEARCH:
1. **Agent communication**: "Search for transcripts showing excellent agent communication skills"
2. **Training examples**: "Find transcripts perfect for agent training on difficult situations"
3. **Performance analysis**: "Search for transcripts showing different agent approaches to same problem type"
4. **Customer rapport**: "Find transcripts where agents built strong customer relationships"
5. **Agent efficiency**: "Search for transcripts showing how top agents handle complex issues quickly"

## Use Case 5: Customer Success & Revenue Impact Analysis

#### Cortex Analyst Questions:
1. **Revenue satisfaction correlation**: "What's the total monthly revenue from customers with high satisfaction scores versus low satisfaction?"
2. **Enterprise vs Basic analysis**: "How do Enterprise customers compare to Basic customers in terms of call volume and satisfaction?"
3. **Organization size impact**: "Do large organizations require more support calls than small organizations?"
4. **Integration complexity**: "Do customers with more integrations have higher support call volumes?"
5. **Tier performance**: "Which subscription tier has the highest average satisfaction scores?"
6. **Revenue per customer**: "What's the average revenue per customer for each organization type?"
7. **Support tier effectiveness**: "Do customers with higher support tiers get better resolution times?"
8. **High-value risk analysis**: "Which high-revenue customers (>$1000/month) have the lowest satisfaction scores?"
9. **Growth indicators**: "Which customer segments show the best balance of low support needs and high satisfaction?"
10. **Churn risk correlation**: "What percentage of customers with negative sentiment also have low satisfaction ratings?"

### Cortex Search

#### Using ZENDESK_CONVERSATION_SEARCH:
1. **Revenue-risk analysis**: "Find conversations from high-value customers with low satisfaction"
2. **Success patterns**: "Search for conversations from profitable customers with excellent experiences"
3. **Churn indicators**: "Find conversations from customers expressing cancellation concerns"
4. **Upsell opportunities**: "Search for conversations where customers requested advanced features"
5. **Customer value insights**: "Find conversations from different subscription tiers to understand value perception"

#### Using ZENDESK_TRANSCRIPT_SEARCH:
1. **Revenue impact**: "Search for transcripts where customers discuss budget or ROI concerns"
2. **Customer success**: "Find transcripts with customers praising value received from service"
3. **Retention insights**: "Search for transcripts revealing why customers stay or consider leaving"
4. **Expansion opportunities**: "Find transcripts where customers discuss growing needs or additional requirements"
5. **Value messaging**: "Search for transcripts showing how agents communicate value propositions"

## Use Case 6: Call Volume & Duration Analytics

#### Cortex Analyst Questions:
1. **Peak volume analysis**: "What are the busiest days and times for support calls?"
2. **Duration distribution**: "What percentage of calls are under 5 minutes versus over 30 minutes?"
3. **Short call effectiveness**: "Do short calls (under 5 minutes) have higher or lower satisfaction than average?"
4. **Long call analysis**: "What conversation categories dominate calls longer than 30 minutes?"
5. **Duration comparison**: "Compare median call duration to average call duration by ticket priority"
6. **Total call time**: "What's the total call time in hours for each organization type?"
7. **Channel duration**: "Which support channel has the longest average call duration?"
8. **Duration vs resolution**: "Do longer calls have higher resolution rates?"
9. **Efficiency trends**: "Is average call duration increasing or decreasing over time?"
10. **Follow-up correlation**: "Are longer calls less likely to require follow-up?"

### Cortex Search

#### Using ZENDESK_CONVERSATION_SEARCH:
1. **Duration patterns**: "Find conversations that took longer than 30 minutes to understand complexity"
2. **Quick resolution**: "Search for conversations resolved in under 5 minutes to identify efficiency patterns"
3. **Extended call analysis**: "Find conversations with long duration but high satisfaction"
4. **Volume spike investigation**: "Search for conversations during peak periods to understand demand drivers"
5. **Duration vs satisfaction**: "Find conversations showing correlation between call length and customer satisfaction"

#### Using ZENDESK_TRANSCRIPT_SEARCH:
1. **Efficiency analysis**: "Search for transcripts of quick calls to identify successful resolution patterns"
2. **Complex issue deep dive**: "Find transcripts of extended calls to understand what makes issues complex"
3. **Volume pattern insights**: "Search for transcripts during busy periods to understand common issues"
4. **Duration optimization**: "Find transcripts showing how agents efficiently handle time-sensitive issues"
5. **Peak period analysis**: "Search for transcripts during high-volume times to identify resource needs"

## Use Case 7: Ticket Priority & Status Analytics

#### Cortex Analyst Questions:
1. **Priority distribution**: "What percentage of tickets are urgent versus normal priority?"
2. **Priority vs resolution**: "How much faster are urgent tickets resolved compared to normal priority?"
3. **Priority satisfaction**: "Do urgent tickets have higher or lower satisfaction scores?"
4. **Status distribution**: "What percentage of tickets are currently open versus solved?"
5. **Escalation patterns**: "Which ticket types are most likely to be marked as urgent?"
6. **Status transitions**: "What's the average time between ticket statuses?"
7. **Channel priority**: "Which support channels generate the most urgent tickets?"
8. **Agent priority performance**: "Which agents handle urgent tickets most effectively?"
9. **Customer tier status**: "Do Enterprise customers have more open tickets than Basic customers?"
10. **Priority resolution success**: "What's the one-call resolution rate for urgent versus normal priority tickets?"

### Cortex Search

#### Using ZENDESK_CONVERSATION_SEARCH:
1. **Priority escalation**: "Find conversations that started normal priority but escalated to urgent"
2. **Urgent resolution**: "Search for conversations from urgent tickets with successful quick resolution"
3. **Status progression**: "Find conversations showing ticket status changes from open to solved"
4. **Priority patterns**: "Search for conversations to understand what makes tickets urgent vs normal"
5. **Status correlation**: "Find conversations from tickets with specific status and priority combinations"

#### Using ZENDESK_TRANSCRIPT_SEARCH:
1. **Urgency indicators**: "Search for transcripts containing language that indicates urgent situations"
2. **Priority justification**: "Find transcripts showing why tickets were marked as high priority"
3. **Status updates**: "Search for transcripts with agent communications about ticket status changes"
4. **Escalation triggers**: "Find transcripts showing what causes tickets to escalate in priority"
5. **Resolution confirmation**: "Search for transcripts with customers confirming issues are resolved"

## Use Case 8: Multi-Channel Support Analysis

#### Cortex Analyst Questions:
1. **Channel preferences**: "Which support channels do customers prefer by organization type?"
2. **Channel performance**: "Compare resolution times across web, email, and phone channels"
3. **Channel satisfaction**: "Which support channel has the highest customer satisfaction?"
4. **Channel volume**: "What percentage of tickets come through each support channel?"
5. **Channel issue types**: "Which conversation categories are most common for each channel?"
6. **Channel efficiency**: "Which channel has the highest one-call resolution rate?"
7. **Channel escalation**: "Which support channels have the highest ticket reopen rates?"
8. **Channel customer tiers**: "Do Enterprise customers use different channels than Basic customers?"
9. **Channel follow-up**: "Which channels most frequently require follow-up actions?"
10. **Channel optimization**: "Which support channel combination provides the best satisfaction per interaction?"

### Cortex Search

#### Using ZENDESK_CONVERSATION_SEARCH:
1. **Channel effectiveness**: "Find conversations from phone support with excellent customer satisfaction"
2. **Channel preferences**: "Search for conversations where customers mention preferred contact methods"
3. **Cross-channel analysis**: "Find conversations from web support vs email support quality differences"
4. **Channel-specific issues**: "Search for conversations showing issues unique to specific channels"
5. **Channel optimization**: "Find conversations highlighting strengths and weaknesses of each channel"

#### Using ZENDESK_TRANSCRIPT_SEARCH:
1. **Channel quality**: "Search for transcripts showing communication quality differences between channels"
2. **Channel limitations**: "Find transcripts where channel limitations affected customer experience"
3. **Channel switching**: "Search for transcripts where customers switched between channels"
4. **Channel satisfaction**: "Find transcripts with customer feedback about their preferred support channels"
5. **Channel efficiency**: "Search for transcripts comparing resolution speed across different channels"

## Usage Instructions

1. Open Snowflake Cortex Analyst in your Snowflake interface
2. Select the `ZENDESK_CUSTOMER_SUCCESS_ANALYTICS` semantic view
3. Copy and paste each query into the natural language input field
4. Observe how Cortex Analyst interprets and executes the queries

## Expected Capabilities

These queries test the semantic view's ability to:
- ✅ **AI-Powered Insights**: Leverage sentiment analysis and conversation categorization
- ✅ **Business Intelligence**: Provide executive-level metrics and trends
- ✅ **Natural Language Processing**: Understand business terminology and synonyms
- ✅ **Cross-Table Analysis**: Join customer, agent, and performance data
- ✅ **Aggregation Functions**: Calculate averages, percentages, and distributions
- ✅ **Revenue Analytics**: Connect support metrics to business outcomes
- ✅ **Multi-Channel Analysis**: Compare performance across support channels
- ✅ **Agent Performance**: Detailed agent efficiency and effectiveness metrics
- ✅ **Customer Success**: Revenue impact and customer tier analysis
- ✅ **Operational Excellence**: SLA compliance and resolution metrics

## Key Semantic View Features Being Tested

### **AI-Enhanced Dimensions**
- `sentiment_category`, `conversation_category`, `agent_name`
- `resolution_provided`, `follow_up_needed`

### **Business Dimensions**
- `organization_type`, `size_category`, `subscription_tier`, `support_tier`
- `priority`, `status`, `type`, `via_channel`

### **AI-Powered Metrics (46 total)**
- **Call Analytics**: `average_call_duration`, `median_call_duration`, `short_calls_rate`, `long_calls_rate`
- **Sentiment Analysis**: `average_sentiment_score`, `positive_sentiment_rate`, `negative_sentiment_rate`
- **Customer Satisfaction**: `average_satisfaction`, `high_satisfaction_rate`, `low_satisfaction_rate`
- **Resolution Performance**: `average_first_resolution_time`, `sla_compliance_rate`, `one_call_resolution_rate`
- **Agent Performance**: `calls_per_agent`, `unique_agents`, `agent_satisfaction_score`
- **Revenue Impact**: `total_revenue`, `average_revenue_per_customer`, `enterprise_customer_rate`
- **Channel Analytics**: `web_channel_rate`, `email_channel_rate`, `phone_channel_rate`
- **Ticket Distribution**: `urgent_ticket_rate`, `high_priority_rate`, `solved_ticket_rate`

### **Natural Language Synonyms**
- Business terms: 'plan' → 'subscription_tier', 'urgency' → 'priority'
- Technical terms: 'resolution' → 'resolution_provided', 'follow up' → 'follow_up_needed'
- Channel terms: 'contact method' → 'via_channel', 'submission method' → 'via_channel'

## Query Categories Summary

1. **AI-Powered Customer Sentiment Analysis** (10 queries) - Sentiment trends, impact analysis
2. **AI-Classified Conversation Analysis** (10 queries) - Issue categorization, type analysis
3. **Support Performance & Resolution Metrics** (10 queries) - SLA, resolution times, efficiency
4. **Support Agent AI Performance Analysis** (10 queries) - Agent effectiveness, workload
5. **Customer Success & Revenue Impact Analysis** (10 queries) - Revenue correlation, customer tiers
6. **Call Volume & Duration Analytics** (10 queries) - Call patterns, duration analysis
7. **Ticket Priority & Status Analytics** (10 queries) - Priority distribution, status tracking
8. **Multi-Channel Support Analysis** (10 queries) - Channel performance, preferences

**Total: 80 comprehensive natural language queries** leveraging 46 metrics across 16 dimensions.