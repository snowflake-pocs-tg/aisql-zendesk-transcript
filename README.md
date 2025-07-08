# Zendesk Customer Success Analytics - Setup Guide

AI-powered customer success analytics platform using Snowflake Cortex for sentiment analysis, conversation classification, search services, and natural language business intelligence.

## Prerequisites

- Snowflake account with Cortex AI functions enabled
- ACCOUNTADMIN or equivalent privileges

## Setup Steps

### Step 1: Snowflake Setup

1. Update file paths in `queries/snowflake_setup.sql`:
   - Replace `<YOUR_REPO_PATH>` with your actual repository path

2. Execute the setup script to create database, tables, and load data

### Step 2: Create AI-Enriched Transcripts

Execute `queries/transcripts_enriched.sql` to apply Cortex AI functions

### Step 3: Set Up Search Services

Execute `queries/cortex_search.sql` to create search services

### Step 4: Create Semantic View

Execute `queries/semantic_view.sql` to create the analytics interface

### Step 5: Set Up AI Agent (Optional)

1. Navigate to Snowflake AI & ML Studio
2. Create new agent named "Zendy"
3. Connect to `ZENDESK_CUSTOMER_SUCCESS_ANALYTICS` semantic view
4. Connect both search services

## Testing

Use the questions in `SI.md` to test:
- 80 Cortex Analyst queries
- 80 Cortex Search queries

## Project Structure

```
zendesk_demo/
├── README.md                    # This setup guide
├── SI.md                        # Test queries
├── data/                        # Generated datasets
├── scripts/                     # Data generation
├── queries/                     # SQL setup files
└── validation/                  # Data validation
```

## Troubleshooting

**Snowflake errors**: Verify Cortex AI functions are enabled
**Boolean errors**: Use the provided `cortex_search.sql` file
**Search service errors**: Check change tracking is enabled on tables

---

Complete setup creates 50,000+ records with AI-powered analytics across customer conversations, sentiment analysis, and business intelligence.