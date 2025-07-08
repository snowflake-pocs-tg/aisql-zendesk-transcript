import csv
import random
from datetime import datetime, timedelta
import json
import os

def generate_enhanced_call_transcripts():
    """Generate highly variable call transcripts using modular components and contextual intelligence"""
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    
    # Load existing data
    tickets = []
    tickets_file = os.path.join(data_dir, 'zendesk_tickets.csv')
    with open(tickets_file, 'r') as f:
        reader = csv.DictReader(f)
        tickets = list(reader)
    
    customers = {}
    customers_file = os.path.join(data_dir, 'zendesk_customers.csv')
    with open(customers_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            customers[row['customer_id']] = row
    
    employees = {}
    employees_file = os.path.join(data_dir, 'zendesk_employees.csv')
    with open(employees_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            employees[row['employee_id']] = row
    
    print(f"Loaded {len(tickets)} tickets, {len(customers)} customers, {len(employees)} employees")
    
    # =====================================================================================
    # ENHANCED VARIABILITY COMPONENTS
    # =====================================================================================
    
    # 1. DYNAMIC CONVERSATION OPENINGS (50+ variations)
    conversation_openings = {
        'agent_greetings': [
            "Hi, this is {agent_name} with ZENDESK support. How can I help you today?",
            "Thank you for calling ZENDESK, this is {agent_name}. What can I do for you?",
            "Good {time_of_day}, you've reached ZENDESK customer service. This is {agent_name}.",
            "Hello and welcome to ZENDESK support. My name is {agent_name}.",
            "Thanks for contacting ZENDESK. This is {agent_name} speaking.",
            "Hi there! {agent_name} here from ZENDESK support team.",
            "Good {time_of_day}! This is {agent_name} with ZENDESK customer care.",
            "Hello, {agent_name} from ZENDESK support. How may I assist you?",
            "Thanks for calling in today. This is {agent_name}.",
            "Hi, {agent_name} with ZENDESK. What brings you to us today?"
        ],
        'customer_openings': [
            "Hi {agent_name}, I'm calling about {issue_brief}",
            "Hello, I hope you can help me with {issue_brief}",
            "Good {time_of_day}, we're having trouble with {issue_brief}",
            "Hi there, I need assistance with {issue_brief}",
            "Hello {agent_name}, I'm reaching out because {issue_brief}",
            "Hi, I was hoping you could help us resolve {issue_brief}",
            "Good {time_of_day}, we've been experiencing {issue_brief}",
            "Hello, I'm calling to get help with {issue_brief}",
            "Hi {agent_name}, we really need help with {issue_brief}",
            "Good {time_of_day}, I'm calling about {issue_brief}"
        ]
    }
    
    # 2. PROBLEM DESCRIPTION MODULES (100+ variations per category)
    problem_descriptions = {
        'payment_issues': [
            "our payment processing system isn't working correctly",
            "duplicate charges appearing on our account",
            "failed transactions that still show as pending",
            "our card being declined even though it's valid",
            "unexpected fees that weren't disclosed upfront",
            "payment confirmations not being sent to donors",
            "recurring donations stopping without explanation",
            "our payment gateway timing out frequently",
            "charges appearing for services we didn't use",
            "bank deposit amounts not matching our records",
            "payment failures during high-traffic periods",
            "incorrect processing of refund requests",
            "our donor payment methods being marked as invalid",
            "transaction reports showing incomplete data",
            "payment processing delays affecting our cash flow"
        ],
        'integration_issues': [
            "our QuickBooks sync that stopped working last week",
            "data not transferring properly to our CRM system",
            "our website integration showing error messages",
            "API connections timing out repeatedly",
            "our donor management system not receiving updates",
            "accounting software import failing with format errors",
            "webhook notifications not being delivered",
            "our membership database not syncing properly",
            "third-party app connections being dropped",
            "data mapping issues between systems",
            "authentication errors with our integrations",
            "our reporting tools not pulling current data",
            "custom field mappings getting reset",
            "integration performance being extremely slow",
            "our backup systems not receiving data feeds"
        ],
        'training_needs': [
            "learning how to set up recurring donation campaigns",
            "understanding the new reporting dashboard features",
            "training our volunteers on the donation processing system",
            "getting our staff up to speed on the mobile app",
            "learning best practices for donor communication",
            "understanding how to customize our giving forms",
            "training on the event management module",
            "learning to generate custom financial reports",
            "understanding security settings and user permissions",
            "getting familiar with the bulk operations features",
            "learning how to set up automated thank you messages",
            "understanding the peer-to-peer fundraising tools",
            "training on the pledge management system",
            "learning to use the donor analytics features",
            "getting help with campaign performance optimization"
        ],
        'feature_requests': [
            "exploring options for text-to-give functionality",
            "looking into mobile wallet payment options",
            "investigating peer-to-peer fundraising capabilities",
            "learning about advanced reporting features",
            "exploring multi-location management tools",
            "investigating custom branding options for our forms",
            "looking into automated donor segmentation features",
            "exploring integration options for our email platform",
            "investigating compliance and audit trail features",
            "learning about donor portal self-service options",
            "exploring options for handling planned giving",
            "investigating membership management capabilities",
            "looking into volunteer hour tracking integration",
            "exploring options for grant management features",
            "investigating social media integration capabilities"
        ],
        'technical_problems': [
            "our donation forms loading very slowly for users",
            "error messages appearing during the checkout process",
            "our dashboard not displaying current information",
            "mobile app crashes when processing donations",
            "security alerts that we don't understand",
            "our admin panel being inaccessible intermittently",
            "data export functions not working properly",
            "email notifications not being delivered consistently",
            "our custom domain setup having certificate issues",
            "database connection errors affecting operations",
            "our backup and recovery processes failing",
            "performance issues during peak donation periods",
            "our two-factor authentication not working correctly",
            "browser compatibility issues with our donation pages",
            "our scheduled reports not generating automatically"
        ]
    }
    
    # 3. AGENT RESPONSE MODULES (75+ variations per situation)
    agent_responses = {
        'empathy_acknowledgment': [
            "I completely understand how frustrating that must be",
            "I can definitely see why this would be concerning for you",
            "That sounds really challenging, and I want to help resolve this",
            "I appreciate you bringing this to our attention",
            "I can imagine how disruptive this has been to your operations",
            "That's definitely not the experience we want you to have",
            "I understand the urgency of getting this resolved quickly",
            "I can see why this would be impacting your donor relationships",
            "That must be really stressful for your team to deal with",
            "I appreciate your patience while we work through this together"
        ],
        'investigation_starts': [
            "Let me pull up your account details right away",
            "I'm going to investigate this thoroughly for you",
            "Let me check what's happening in your system",
            "I'll review your recent activity to understand the issue",
            "Let me access your account and see what's going on",
            "I'm going to dig into the technical details here",
            "Let me examine your configuration settings",
            "I'll check our system logs to identify the problem",
            "Let me review your account history to find the cause",
            "I'm going to run some diagnostics on your setup"
        ],
        'solution_presentation': [
            "I found the issue and here's what I can do to fix it",
            "I have a solution that should resolve this completely",
            "I can implement a fix right now that will address this",
            "I've identified the problem and have several options for you",
            "I can resolve this immediately and prevent it from happening again",
            "I have both a quick fix and a long-term solution for you",
            "I can correct this issue and set up monitoring to prevent recurrence",
            "I found exactly what's causing this and can fix it today",
            "I have a comprehensive solution that addresses all aspects of this",
            "I can implement changes that will solve this permanently"
        ],
        'process_explanation': [
            "Let me walk you through exactly what I'm doing",
            "I'll explain each step as I make these changes",
            "Here's the process I'm following to resolve this",
            "Let me show you what's happening behind the scenes",
            "I'll break down the technical details for you",
            "Let me explain why this happened and how we're fixing it",
            "I'll walk you through the solution step by step",
            "Here's what I'm implementing and why it will work",
            "Let me explain the technical process for this fix",
            "I'll describe what each change accomplishes"
        ]
    }
    
    # 4. CONTEXTUAL ELEMENTS BY ORGANIZATION TYPE
    org_specific_context = {
        'faith': {
            'seasonal_refs': ['Christmas season', 'Easter giving', 'Thanksgiving appeals', 'year-end stewardship', 'Lenten giving'],
            'terminology': ['congregation', 'stewardship', 'tithe', 'offering', 'ministry', 'fellowship', 'worship', 'pastor', 'deacon'],
            'specific_needs': ['online giving during service', 'text-to-give for events', 'memorial donations', 'building fund campaigns']
        },
        'school': {
            'seasonal_refs': ['back-to-school season', 'graduation time', 'winter break', 'spring fundraisers', 'summer enrollment'],
            'terminology': ['tuition', 'enrollment', 'parent portal', 'student accounts', 'fundraiser', 'PTA', 'athletics', 'principal'],
            'specific_needs': ['payment plans', 'family accounts', 'activity fees', 'lunch money', 'sports team fundraising']
        },
        'nonprofit': {
            'seasonal_refs': ['annual campaign', 'giving season', 'grant deadlines', 'awareness month', 'fundraising gala'],
            'terminology': ['donors', 'supporters', 'mission', 'impact', 'programs', 'volunteers', 'beneficiaries', 'board'],
            'specific_needs': ['peer-to-peer campaigns', 'event ticketing', 'corporate partnerships', 'grant tracking']
        }
    }
    
    # 5. DYNAMIC CONVERSATION BRANCHES
    conversation_branches = {
        'technical_deep_dive': [
            "Can you tell me more about when this first started happening?",
            "Let me check if this is related to any recent system updates",
            "I want to verify your current configuration settings",
            "Let me review the error logs to pinpoint the exact cause"
        ],
        'process_clarification': [
            "Just to make sure I understand correctly, you're seeing {specific_issue}?",
            "Let me confirm the timeline - this started around {timeframe}?",
            "To clarify, this is affecting your system specifically?",
            "I want to verify that this is what you're experiencing"
        ],
        'solution_expansion': [
            "I can also show you some additional features that might help",
            "While we're working on this, let me mention some related improvements",
            "I think you might benefit from some other capabilities we offer",
            "This gives us a good opportunity to optimize your setup further"
        ],
        'follow_up_planning': [
            "I'll monitor this for the next few days to ensure it's working properly",
            "Let me schedule a follow-up to check how everything is performing",
            "I want to make sure you're completely satisfied with this resolution",
            "I'll send you some additional resources that might be helpful"
        ]
    }
    
    # 6. PERSONALITY-DRIVEN LANGUAGE PATTERNS
    personality_traits = {
        'customer_types': {
            'detail_oriented': {
                'speech_patterns': ['specific dates and amounts', 'requests for step-by-step explanations', 'asks for documentation'],
                'language_style': 'precise',
                'question_frequency': 'high',
                'technical_comfort': 'medium'
            },
            'results_focused': {
                'speech_patterns': ['cuts to the point', 'asks about timelines', 'wants bottom-line impact'],
                'language_style': 'direct',
                'question_frequency': 'low',
                'technical_comfort': 'medium'
            },
            'relationship_builder': {
                'speech_patterns': ['personal anecdotes', 'team member references', 'community impact stories'],
                'language_style': 'conversational',
                'question_frequency': 'medium',
                'technical_comfort': 'low'
            },
            'tech_savvy': {
                'speech_patterns': ['technical terminology', 'system specifications', 'integration details'],
                'language_style': 'technical',
                'question_frequency': 'high',
                'technical_comfort': 'high'
            },
            'cautious': {
                'speech_patterns': ['security concerns', 'risk mitigation', 'approval processes'],
                'language_style': 'careful',
                'question_frequency': 'high',
                'technical_comfort': 'low'
            },
            'growth_minded': {
                'speech_patterns': ['scaling concerns', 'future planning', 'expansion possibilities'],
                'language_style': 'forward_thinking',
                'question_frequency': 'medium',
                'technical_comfort': 'medium'
            }
        },
        'agent_styles': {
            'consultative': {
                'approach': 'asks probing questions',
                'language': 'professional and thorough',
                'solution_style': 'comprehensive'
            },
            'efficient': {
                'approach': 'moves quickly to solutions',
                'language': 'clear and direct',
                'solution_style': 'practical'
            },
            'educational': {
                'approach': 'explains underlying concepts',
                'language': 'informative and patient',
                'solution_style': 'teaching-focused'
            },
            'empathetic': {
                'approach': 'acknowledges emotional impact',
                'language': 'warm and understanding',
                'solution_style': 'supportive'
            },
            'technical': {
                'approach': 'dives into system details',
                'language': 'precise and technical',
                'solution_style': 'thorough'
            }
        }
    }
    
    # 7. ENHANCED AGENT PROFILES
    enhanced_agent_profiles = {
        "Sarah Wilson": {"style": "consultative", "experience": "senior", "specialty": "billing_issues", "personality": "detail_oriented"},
        "Mike Johnson": {"style": "efficient", "experience": "mid", "specialty": "technical_support", "personality": "results_focused"},
        "Emily Davis": {"style": "technical", "experience": "senior", "specialty": "integrations", "personality": "tech_savvy"},
        "Chris Brown": {"style": "empathetic", "experience": "junior", "specialty": "customer_onboarding", "personality": "relationship_builder"},
        "Jessica Garcia": {"style": "educational", "experience": "senior", "specialty": "training", "personality": "growth_minded"},
        "David Miller": {"style": "consultative", "experience": "mid", "specialty": "feature_consulting", "personality": "analytical"},
        "Amanda Rodriguez": {"style": "empathetic", "experience": "senior", "specialty": "retention", "personality": "relationship_builder"},
        "Kevin Lee": {"style": "efficient", "experience": "mid", "specialty": "quick_fixes", "personality": "results_focused"},
        "Rachel Thompson": {"style": "educational", "experience": "senior", "specialty": "complex_issues", "personality": "detail_oriented"},
        "James Martinez": {"style": "technical", "experience": "junior", "specialty": "system_troubleshooting", "personality": "tech_savvy"}
    }
    
    # 8. DYNAMIC CONTENT GENERATORS
    def generate_specific_details(issue_type, customer, employee):
        """Generate contextually relevant specific details"""
        details = []
        
        if issue_type == 'payment_issues':
            details = [
                f"${random.randint(50, 2000):.2f} transaction",
                f"happened on {random.choice(['last Tuesday', 'this morning', 'yesterday', 'three days ago'])}",
                f"affecting {random.randint(1, 10)} donors"
            ]
        elif issue_type == 'integration_issues':
            details = [
                f"{random.choice(['QuickBooks', 'Salesforce', 'Mailchimp', 'WordPress', 'donor management system'])}",
                f"error code {random.randint(100, 999)}",
                f"affecting {random.choice(['daily', 'weekly', 'monthly'])} reports"
            ]
        
        return details
    
    def apply_personality_filter(text, personality_type):
        """Modify text based on personality traits"""
        if personality_type == 'detail_oriented':
            if random.random() < 0.3:
                text += f" - this happened at approximately {random.randint(8, 17)}:{random.randint(10, 59):02d}"
        elif personality_type == 'results_focused':
            if random.random() < 0.3:
                text = text.split('.')[0] + ". How quickly can this be resolved?"
        elif personality_type == 'relationship_builder':
            if random.random() < 0.2:
                text += f" Our {random.choice(['team', 'volunteers', 'board'])} is really counting on getting this fixed."
        
        return text
    
    def generate_conversation_components(ticket, customer, employee, agent_profile):
        """Generate conversation components that will be assembled with proper timing"""
        
        # Determine conversation context
        org_type = customer['organization_type']
        org_context = org_specific_context.get(org_type, org_specific_context['nonprofit'])
        
        # Select customer personality
        customer_personality = random.choice(list(personality_traits['customer_types'].keys()))
        customer_traits = personality_traits['customer_types'][customer_personality]
        
        # Determine issue category from ticket description with proper mapping
        description_lower = ticket['description'].lower()
        issue_category = 'technical_problems'  # default
        
        # Map ticket description keywords to conversation categories
        if any(keyword in description_lower for keyword in ['payment', 'charge', 'billing', 'refund', 'transaction', 'ach', 'credit']):
            issue_category = 'payment_issues'
        elif any(keyword in description_lower for keyword in ['quickbooks', 'salesforce', 'integration', 'sync', 'api', 'export', 'webhook']):
            issue_category = 'integration_issues'
        elif any(keyword in description_lower for keyword in ['training', 'help', 'learn', 'workshop', 'tutorial', 'guidance']):
            issue_category = 'training_needs'
        elif any(keyword in description_lower for keyword in ['feature', 'request', 'enhancement', 'suggestion', 'custom']):
            issue_category = 'feature_requests'
        elif any(keyword in description_lower for keyword in ['setup', 'configuration', 'install', 'domain', 'ssl', 'initial']):
            issue_category = 'training_needs'  # Setup often requires training/help
        elif any(keyword in description_lower for keyword in ['error', 'bug', 'crash', 'timeout', 'loading', 'not working', 'failed']):
            issue_category = 'technical_problems'
        
        # Select specific problem description that aligns with ticket description
        # Use ticket description as the primary issue, with fallback to problem descriptions
        if random.random() < 0.7:  # 70% chance to use description-aligned conversation
            # Create aligned description based on ticket description keywords
            if any(keyword in description_lower for keyword in ['webhook', 'notification']):
                problem_desc = "webhook notifications not being delivered properly"
            elif any(keyword in description_lower for keyword in ['quickbooks', 'sync', 'integration']):
                problem_desc = "data synchronization issues affecting our reporting"
            elif any(keyword in description_lower for keyword in ['payment', 'process', 'transaction']):
                problem_desc = "payment processing issues during transactions"
            elif any(keyword in description_lower for keyword in ['card declined', 'declined']):
                problem_desc = "payment cards being declined even though they should be valid"
            elif any(keyword in description_lower for keyword in ['refund', 'refunding']):
                problem_desc = "refund processing taking too long"
            elif any(keyword in description_lower for keyword in ['training', 'help', 'learn']):
                problem_desc = "getting help with system training and usage"
            elif any(keyword in description_lower for keyword in ['setup', 'configuration', 'install']):
                problem_desc = "assistance with system setup and configuration"
            elif any(keyword in description_lower for keyword in ['billing', 'invoice', 'charges']):
                problem_desc = "questions about billing and account charges"
            elif any(keyword in description_lower for keyword in ['feature', 'request', 'enhancement']):
                problem_desc = "exploring options for new features and enhancements"
            elif any(keyword in description_lower for keyword in ['error', 'issue', 'problem']):
                problem_desc = "system issues that are affecting our operations"
            else:
                # Fallback to issue category
                problem_desc = issue_category.replace('_', ' ').lower()
        else:
            # Use original problem descriptions for variety
            problem_desc = random.choice(problem_descriptions[issue_category])
        
        # Generate conversation components
        agent_name = agent_profile['name']
        customer_name = f"{employee['first_name']} {employee['last_name']}"
        issue_brief = problem_desc
        
        return {
            'agent_name': agent_name,
            'customer_name': customer_name,
            'issue_brief': issue_brief,
            'customer_personality': customer_personality,
            'customer_traits': customer_traits,
            'org_context': org_context,
            'agent_profile': agent_profile,
            'ticket': ticket
        }
    
    def build_timed_conversation(components, call_date, target_duration):
        """Build complete conversation with proper time-of-day alignment and duration scaling"""
        
        # Determine accurate time of day based on actual call timestamp
        call_hour = call_date.hour
        if 5 <= call_hour < 12:
            time_of_day = "morning"
        elif 12 <= call_hour < 17:
            time_of_day = "afternoon"
        elif 17 <= call_hour < 21:
            time_of_day = "evening"
        else:
            time_of_day = "evening"  # Late night/early morning still gets "evening" greeting
        
        # Extract components
        agent_name = components['agent_name']
        customer_name = components['customer_name']
        issue_brief = components['issue_brief']
        customer_personality = components['customer_personality']
        customer_traits = components['customer_traits']
        org_context = components['org_context']
        agent_profile = components['agent_profile']
        ticket = components['ticket']
        
        # Generate time-appropriate greetings
        greeting = random.choice(conversation_openings['agent_greetings']).format(
            agent_name=agent_name.split()[0], time_of_day=time_of_day
        )
        
        customer_opening = random.choice(conversation_openings['customer_openings']).format(
            agent_name=agent_name.split()[0], time_of_day=time_of_day, issue_brief=issue_brief
        )
        
        # Build conversation flow
        conversation = []
        conversation.append(f"Agent ({agent_name}): {greeting}")
        conversation.append(f"Customer ({customer_name}): {apply_personality_filter(customer_opening, customer_personality)}")
        
        # Add empathy response
        empathy = random.choice(agent_responses['empathy_acknowledgment'])
        investigation = random.choice(agent_responses['investigation_starts'])
        conversation.append(f"Agent ({agent_name}): {empathy}. {investigation}")
        
        # Add organization-specific context
        if random.random() < 0.4:
            seasonal_ref = random.choice(org_context['seasonal_refs'])
            org_term = random.choice(org_context['terminology'])
            contextual_detail = f"I understand this is particularly challenging during {seasonal_ref}, especially for your {org_term}."
            conversation.append(f"Agent ({agent_name}): {contextual_detail}")
        
        # Add conversation branches based on personality and agent style
        if customer_traits['technical_comfort'] == 'high' and agent_profile['style'] == 'technical':
            tech_branch = random.choice(conversation_branches['technical_deep_dive'])
            conversation.append(f"Agent ({agent_name}): {tech_branch}")
            
            if customer_traits['question_frequency'] == 'high':
                technical_response = f"Yes, specifically we're seeing this in our {random.choice(['admin dashboard', 'reporting module', 'payment gateway', 'integration layer'])}."
                conversation.append(f"Customer ({customer_name}): {technical_response}")
        
        # Add clarification exchange
        if random.random() < 0.6:
            clarification = random.choice(conversation_branches['process_clarification'])
            specific_issue = random.choice(['timeout errors', 'data sync failures', 'payment processing delays', 'report generation issues'])
            timeframe = random.choice(['last week', 'this month', 'after the recent update', 'since Tuesday'])
            
            formatted_clarification = clarification.format(specific_issue=specific_issue, timeframe=timeframe)
            conversation.append(f"Agent ({agent_name}): {formatted_clarification}")
            conversation.append(f"Customer ({customer_name}): That's exactly right.")
        
        # Add solution presentation
        solution = random.choice(agent_responses['solution_presentation'])
        explanation = random.choice(agent_responses['process_explanation'])
        conversation.append(f"Agent ({agent_name}): {solution}. {explanation}")
        
        # Add solution expansion if appropriate
        if random.random() < 0.3 and customer_personality in ['growth_minded', 'tech_savvy']:
            expansion = random.choice(conversation_branches['solution_expansion'])
            conversation.append(f"Agent ({agent_name}): {expansion}")
            
            if customer_traits['question_frequency'] != 'low':
                conversation.append(f"Customer ({customer_name}): I'd be interested to hear about those additional options.")
        
        # Add follow-up planning
        follow_up = random.choice(conversation_branches['follow_up_planning'])
        conversation.append(f"Agent ({agent_name}): {follow_up}")
        
        # Scale conversation content based on target duration
        # Base conversation is ~400-600 characters for 2-5 minutes
        # Scale up content for longer calls
        if target_duration > 600:  # 10+ minutes
            # Generate context-specific troubleshooting based on issue type
            issue_brief = components['issue_brief']
            description_lower = ticket['description'].lower()
            
            # Context-specific troubleshooting steps
            if any(keyword in description_lower for keyword in ['payment', 'charge', 'billing', 'ach', 'refund']):
                troubleshooting_steps = [
                    "Let me check your payment gateway configuration and transaction logs.",
                    "I'm reviewing your merchant account settings and processing rules.",
                    "Let me examine the payment flow and identify where the transaction is failing.",
                    "I'm going to test your payment processing with our sandbox environment.",
                    "Let me verify your bank account details and ACH authorization settings."
                ]
                customer_concerns = [
                    "Will our donors' payment information be secure during this process?",
                    "How will this affect our recurring donations and scheduled payments?",
                    "Should we notify our donors about potential payment delays?",
                    "What's the risk of losing transactions during the fix?",
                    "Can we set up backup payment processing while this is resolved?"
                ]
                detailed_responses = [
                    "I can assure you all donor payment information remains completely secure. The issue is in the processing flow, not data storage. I'm implementing a fix that will restore normal payment processing within 2-4 hours.",
                    "Your recurring donations will be automatically retried once we resolve this. I'm setting up monitoring to ensure all scheduled payments process correctly going forward.",
                    "This appears to be related to recent banking regulations. I'm updating your payment processing rules to ensure full compliance with the new requirements.",
                    "I'm implementing additional validation checks to prevent payment failures and setting up real-time alerts for any processing issues."
                ]
            elif any(keyword in description_lower for keyword in ['integration', 'sync', 'api', 'webhook', 'quickbooks']):
                troubleshooting_steps = [
                    "Let me check your API credentials and authentication tokens.",
                    "I'm reviewing the data sync logs to identify where the connection is breaking.",
                    "Let me test the webhook endpoints and verify the data mapping configuration.",
                    "I'm going to examine your integration settings and permission levels.",
                    "Let me validate the data format and check for any recent schema changes."
                ]
                customer_concerns = [
                    "Will this affect our financial reporting and accounting records?",
                    "How current is our data and what might be missing?",
                    "Should we pause data entry until the sync is working again?",
                    "What's the risk of duplicate records when the sync resumes?",
                    "Can we manually export data as a backup while this is fixed?"
                ]
                detailed_responses = [
                    "Your accounting data integrity is our top priority. I'm implementing a sync validation process that will ensure all transactions are properly matched between systems.",
                    "I can provide you with a data export covering the affected period. Once we restore the sync, I'll run a reconciliation to ensure nothing was missed.",
                    "This appears to be related to API version updates. I'm updating your integration to use the latest version with improved error handling and retry logic.",
                    "I'm setting up duplicate detection rules and will run a cleanup process to ensure your data remains accurate and consolidated."
                ]
            elif any(keyword in description_lower for keyword in ['training', 'help', 'learn', 'workshop']):
                troubleshooting_steps = [
                    "Let me set up a personalized training session tailored to your specific needs.",
                    "I'm going to walk you through each feature step-by-step with your actual data.",
                    "Let me create custom documentation that matches your organization's workflow.",
                    "I'm going to set up practice scenarios using your real use cases.",
                    "Let me schedule follow-up sessions to ensure you're comfortable with all features."
                ]
                customer_concerns = [
                    "How long will it take our team to become proficient with the system?",
                    "What resources are available for ongoing training and support?",
                    "Can you provide training materials specific to our organization type?",
                    "How do we ensure all staff members get proper training?",
                    "What's the best way to train new staff members as we grow?"
                ]
                detailed_responses = [
                    "I'll create a comprehensive training plan that covers both basic functions and advanced features specific to faith-based organizations. Most teams become proficient within 2-3 weeks.",
                    "I'm setting up access to our learning portal with role-based training modules. You'll also have direct access to our support team for any questions.",
                    "I'll provide customized quick-reference guides and video tutorials that show exactly how to handle your most common scenarios.",
                    "I'm scheduling a train-the-trainer session with your key staff so they can help onboard new team members efficiently."
                ]
            else:
                # Generic troubleshooting for other issues
                troubleshooting_steps = [
                    "Let me walk you through the diagnostic steps I'm running on your account.",
                    "I can see several configuration options that might be causing this issue.",
                    "Let me check your historical data to identify any patterns or changes.",
                    "I'm going to run a few tests to isolate the root cause of this problem.",
                    "Let me verify your current settings and compare them to our recommended configuration."
                ]
                customer_concerns = [
                    "How long do you think this will take to resolve completely?",
                    "Will this affect any of our other systems or processes?",
                    "Can you explain what might have caused this issue in the first place?",
                    "Are there any preventive measures we should take to avoid this in the future?",
                    "What should I tell my team about this issue while we're working on it?"
                ]
                detailed_responses = [
                    "That's a great question. Based on what I'm seeing, this typically takes about 24-48 hours to fully resolve. I'll monitor the implementation closely and keep you updated on progress.",
                    "I can assure you this won't impact your other systems. The issue is isolated to this specific module. Let me explain exactly what's happening and why it's contained.",
                    "This appears to be related to a recent platform update. I'm implementing additional safeguards to prevent similar issues in the future.",
                    "I'm setting up proactive monitoring alerts so we can catch any similar issues before they impact your users. This will give us much better visibility going forward."
                ]
            
            conversation.append(f"Agent ({agent_name}): {random.choice(troubleshooting_steps)}")
            conversation.append(f"Customer ({customer_name}): {random.choice(customer_concerns)}")
            conversation.append(f"Agent ({agent_name}): {random.choice(detailed_responses)}")
        
        if target_duration > 1200:  # 20+ minutes
            # Add context-specific complex problem-solving discussion
            if any(keyword in description_lower for keyword in ['payment', 'charge', 'billing', 'ach', 'refund']):
                complex_discussion = [
                    "Let me explain the payment processing architecture and how transactions flow through our system.",
                    "I want to show you different payment methods and redundancy options we can set up for your organization.",
                    "Let me walk you through our enterprise payment security protocols and compliance measures.",
                    "I'm going to coordinate with our payment processing team to implement enhanced fraud protection for your account."
                ]
                clarification_questions = [
                    "How does this payment issue affect your donors' giving experience?",
                    "What's your typical transaction volume and timing patterns?",
                    "Are there any PCI compliance requirements we need to consider?",
                    "How do you handle failed payments and donor communication currently?"
                ]
                detailed_explanations = [
                    "I'll implement a seamless retry system for failed payments and set up automated donor notifications with clear next steps.",
                    "Based on your volume, I'm setting up dedicated processing channels and real-time monitoring to ensure optimal performance.",
                    "I'll coordinate with our compliance team to ensure all PCI requirements are met and provide you with updated security documentation.",
                    "I'm creating an automated donor communication workflow that handles payment issues professionally while maintaining donor relationships."
                ]
            elif any(keyword in description_lower for keyword in ['integration', 'sync', 'api', 'webhook', 'quickbooks']):
                complex_discussion = [
                    "Let me explain the data integration architecture and how information flows between your systems.",
                    "I want to show you different sync strategies and backup options for maintaining data consistency.",
                    "Let me walk you through our enterprise API security and rate limiting protocols.",
                    "I'm going to coordinate with our integration team to implement real-time monitoring and alerting for your data flows."
                ]
                clarification_questions = [
                    "How critical is real-time data sync for your daily operations?",
                    "What's your data volume and how often do you need synchronization?",
                    "Are there any audit trail requirements for financial data transfers?",
                    "How do you currently handle data discrepancies between systems?"
                ]
                detailed_explanations = [
                    "I'll set up near real-time sync with automated conflict resolution and detailed logging for audit purposes.",
                    "Based on your volume, I'm implementing batch processing with incremental updates to optimize performance while maintaining accuracy.",
                    "I'll create comprehensive audit trails that track every data change with timestamps and user attribution for compliance reporting.",
                    "I'm implementing automated data validation rules that will catch and resolve discrepancies before they impact your operations."
                ]
            else:
                # Generic complex discussion for other issues
                complex_discussion = [
                    "Let me explain the technical architecture involved here so you understand why this is happening.",
                    "I want to show you a few different approaches we can take to solve this problem.",
                    "Let me walk you through our enterprise-level troubleshooting protocol for this type of issue.",
                    "I'm going to coordinate with our engineering team to implement a custom solution for your specific use case."
                ]
                clarification_questions = [
                    "Can you help me understand how this fits into your overall workflow?",
                    "What's your timeline for implementing these changes?",
                    "Are there any compliance or security considerations I should be aware of?",
                    "How will this impact your users during the transition period?"
                ]
                detailed_explanations = [
                    "Absolutely. Let me break down the implementation timeline and what you can expect at each stage.",
                    "Good point. I'll coordinate with our compliance team to ensure we meet all your regulatory requirements.",
                    "I'll create a detailed migration plan that minimizes any disruption to your users.",
                    "Let me set up a dedicated support channel for your team during this transition."
                ]
            
            conversation.append(f"Agent ({agent_name}): {random.choice(complex_discussion)}")
            
            # Add multiple rounds of back-and-forth
            for i in range(random.randint(2, 4)):
                conversation.append(f"Customer ({customer_name}): {random.choice(clarification_questions)}")
                conversation.append(f"Agent ({agent_name}): {random.choice(detailed_explanations)}")
        
        if target_duration > 1800:  # 30+ minutes
            # Add context-specific escalation or specialized help
            if any(keyword in description_lower for keyword in ['payment', 'charge', 'billing', 'ach', 'refund']):
                escalation_content = [
                    "I'm bringing in our senior payment processing specialist to provide additional expertise on this complex financial integration.",
                    "Let me connect you with our merchant services team who can provide hands-on assistance with payment gateway optimization.",
                    "I'm scheduling a dedicated follow-up call with our compliance team to address the regulatory aspects of your payment processing.",
                    "Given the complexity of your payment volume, I'm arranging for our enterprise payment team to take over this case."
                ]
                solution_planning = [
                    "I'm creating a comprehensive payment optimization plan with specific SLA targets, fraud prevention measures, and donor experience improvements.",
                    "Let me document all the payment gateway changes we've discussed and create a detailed implementation roadmap with rollback procedures.",
                    "I'll set up daily monitoring calls during the payment system transition to ensure zero transaction downtime.",
                    "I'm preparing a detailed payment processing specification document for your finance team and auditors to review."
                ]
            elif any(keyword in description_lower for keyword in ['integration', 'sync', 'api', 'webhook', 'quickbooks']):
                escalation_content = [
                    "I'm bringing in our senior integration architect to provide additional expertise on this complex data synchronization challenge.",
                    "Let me connect you with our API development team who can provide hands-on assistance with custom integration solutions.",
                    "I'm scheduling a dedicated follow-up call with our data engineering team to address the performance optimization aspects.",
                    "Given the complexity of your data environment, I'm arranging for our enterprise integration team to take over this case."
                ]
                solution_planning = [
                    "I'm creating a comprehensive data integration plan with specific sync schedules, error handling protocols, and data validation checkpoints.",
                    "Let me document all the API changes we've discussed and create a detailed implementation roadmap with testing phases.",
                    "I'll set up automated monitoring and alert systems to track data flow health and catch any integration issues immediately.",
                    "I'm preparing a detailed technical integration specification document for your IT team and data administrators to review."
                ]
            else:
                # Generic escalation for other issues
                escalation_content = [
                    "I'm bringing in our senior technical specialist to provide additional expertise on this complex issue.",
                    "Let me connect you with our implementation team who can provide hands-on assistance with the setup.",
                    "I'm scheduling a dedicated follow-up call with our product team to address the feature enhancement aspects.",
                    "Given the complexity of your environment, I'm arranging for our enterprise support team to take over this case."
                ]
                solution_planning = [
                    "I'm creating a comprehensive action plan with specific timelines, milestones, and success criteria.",
                    "Let me document all the configuration changes we've discussed and create a detailed implementation roadmap.",
                    "I'll set up regular check-in calls to monitor progress and address any questions that come up.",
                    "I'm preparing a detailed technical specification document for your IT team to review."
                ]
            
            conversation.append(f"Agent ({agent_name}): {random.choice(escalation_content)}")
            conversation.append(f"Agent ({agent_name}): {random.choice(solution_planning)}")
        
        # Add closing based on customer satisfaction pattern
        if ticket['satisfaction_rating'] == 'good':
            conversation.append(f"Customer ({customer_name}): This has been really helpful. Thank you for taking the time to explain everything.")
        elif ticket['satisfaction_rating'] == 'bad':
            conversation.append(f"Customer ({customer_name}): I appreciate the effort, but this has been an ongoing issue and we need it fully resolved.")
        else:
            conversation.append(f"Customer ({customer_name}): Okay, that sounds like it should work. I'll keep an eye on it.")
        
        return "\\n\\n".join(conversation)
    
    # =====================================================================================
    # TRANSCRIPT GENERATION WITH ENHANCED VARIABILITY
    # =====================================================================================
    
    # Select eligible tickets (same logic as original)
    eligible_tickets = []
    for ticket in tickets:
        customer = customers[ticket['customer_id']]
        
        call_probability = 0.5
        
        if ticket['priority'] == 'urgent':
            call_probability += 0.3
        elif ticket['priority'] == 'high':
            call_probability += 0.2
        elif ticket['priority'] == 'low':
            call_probability -= 0.15
        
        if ticket['via_channel'] == 'phone':
            call_probability = 0.95
        elif ticket['via_channel'] == 'chat':
            call_probability += 0.1
        
        if customer['size_category'] == 'large':
            call_probability += 0.15
        elif customer['size_category'] == 'small':
            call_probability -= 0.1
        
        if customer['subscription_tier'] == 'premium':
            call_probability += 0.1
        elif customer['subscription_tier'] == 'basic':
            call_probability -= 0.05
        
        if ticket['satisfaction_rating'] == 'bad':
            call_probability += 0.2
        
        description_keywords = ['payment', 'billing', 'charge', 'refund']
        if any(keyword in ticket['description'].lower() for keyword in description_keywords):
            call_probability += 0.15
        
        call_probability = max(0.1, min(0.95, call_probability))
        
        if random.random() < call_probability:
            eligible_tickets.append(ticket)
    
    print(f"Selected {len(eligible_tickets)} tickets for enhanced call transcripts")
    
    # Generate enhanced transcripts
    transcripts = []
    transcript_counter = 1
    
    for ticket in eligible_tickets:
        customer = customers[ticket['customer_id']]
        employee = employees[ticket['employee_id']]
        
        # Calculate call timing
        ticket_created = datetime.strptime(ticket['created_at'], '%Y-%m-%d %H:%M:%S')
        ticket_updated = datetime.strptime(ticket['updated_at'], '%Y-%m-%d %H:%M:%S')
        
        ticket_solved = None
        if ticket['solved_at']:
            ticket_solved = datetime.strptime(ticket['solved_at'], '%Y-%m-%d %H:%M:%S')
        
        if ticket_solved:
            call_date = ticket_created + timedelta(
                seconds=random.uniform(0, (ticket_solved - ticket_created).total_seconds() * 0.8)
            )
        else:
            call_date = ticket_created + timedelta(
                seconds=random.uniform(0, (ticket_updated - ticket_created).total_seconds())
            )
        
        # Select agent with enhanced profile
        agent_name = random.choice(list(enhanced_agent_profiles.keys()))
        agent_profile = enhanced_agent_profiles[agent_name]
        agent_profile['name'] = agent_name
        
        # Generate conversation components first
        conversation_components = generate_conversation_components(ticket, customer, employee, agent_profile)
        
        # Calculate realistic call duration based on multiple factors (before building conversation)
        
        # Base duration by priority and complexity
        if ticket['priority'] == 'urgent':
            base_duration = random.randint(900, 2400)  # 15-40 minutes (complex urgent issues)
        elif ticket['priority'] == 'high':
            base_duration = random.randint(480, 1500)  # 8-25 minutes (significant issues)
        elif ticket['priority'] == 'normal':
            base_duration = random.randint(240, 900)   # 4-15 minutes (standard issues)
        else:  # low priority
            base_duration = random.randint(180, 600)   # 3-10 minutes (simple issues)
        
        # Adjust based on ticket category
        description_lower = ticket['description'].lower()
        if any(keyword in description_lower for keyword in ['training', 'help', 'learn', 'workshop']):
            base_duration = int(base_duration * random.uniform(1.3, 1.8))  # Training takes longer
        elif any(keyword in description_lower for keyword in ['integration', 'sync', 'api', 'technical']):
            base_duration = int(base_duration * random.uniform(1.2, 1.6))  # Technical issues longer
        elif any(keyword in description_lower for keyword in ['billing', 'invoice', 'payment']):
            base_duration = int(base_duration * random.uniform(0.8, 1.2))  # Billing can be quick or complex
        elif any(keyword in description_lower for keyword in ['feature', 'request', 'enhancement']):
            base_duration = int(base_duration * random.uniform(1.1, 1.4))  # Feature discussions longer
        
        # Organization size impact (larger orgs have more complex setups)
        org_size = customer['size_category']
        if org_size == 'large':
            base_duration = int(base_duration * random.uniform(1.1, 1.3))
        elif org_size == 'small':
            base_duration = int(base_duration * random.uniform(0.8, 1.0))
        
        # Subscription tier impact (premium gets more detailed support)
        if customer['subscription_tier'] == 'premium':
            base_duration = int(base_duration * random.uniform(1.0, 1.2))
        elif customer['subscription_tier'] == 'basic':
            base_duration = int(base_duration * random.uniform(0.9, 1.0))
        
        # Agent experience impact
        if agent_profile['experience'] == 'junior':
            base_duration = int(base_duration * random.uniform(1.1, 1.4))  # Junior agents take longer
        elif agent_profile['experience'] == 'senior':
            base_duration = int(base_duration * random.uniform(0.8, 1.0))  # Senior agents more efficient
        
        # Customer satisfaction correlation (bad satisfaction = longer, more difficult calls)
        if ticket['satisfaction_rating'] == 'bad':
            base_duration = int(base_duration * random.uniform(1.3, 1.8))  # Difficult calls
        elif ticket['satisfaction_rating'] == 'good':
            base_duration = int(base_duration * random.uniform(0.9, 1.1))  # Efficient resolution
        
        # Final variance for realism
        duration_variance = random.uniform(0.7, 1.4)  # ±40% final variance
        call_duration = int(base_duration * duration_variance)
        
        # Reasonable bounds: 2 minutes to 1 hour
        call_duration = max(120, min(3600, call_duration))
        
        # Build conversation with proper timing alignment and duration scaling
        transcript_text = build_timed_conversation(conversation_components, call_date, call_duration)
        
        # Determine satisfaction based on conversation tone and ticket data
        satisfaction_base = 3
        if ticket['satisfaction_rating'] == 'good':
            satisfaction_base = random.choice([4, 5, 5])
        elif ticket['satisfaction_rating'] == 'bad':
            satisfaction_base = random.choice([1, 2, 2])
        else:
            satisfaction_base = random.choice([3, 4])
        
        # Adjust satisfaction based on agent experience and customer personality
        if agent_profile['experience'] == 'senior':
            satisfaction_base = min(5, satisfaction_base + random.choice([0, 1]))
        elif agent_profile['experience'] == 'junior':
            satisfaction_base = max(1, satisfaction_base - random.choice([0, 1]))
        
        customer_satisfaction = satisfaction_base
        
        # Determine resolution and follow-up flags
        resolution_provided = customer_satisfaction >= 3 and random.random() < 0.8
        follow_up_needed = customer_satisfaction <= 3 or random.random() < 0.25
        
        transcript = {
            'transcript_id': transcript_counter,
            'ticket_id': int(ticket['ticket_id']),
            'call_duration': call_duration,
            'transcript_text': transcript_text,
            'call_date': call_date.strftime('%Y-%m-%d %H:%M:%S'),
            'agent_name': agent_name,
            'customer_satisfaction': customer_satisfaction,
            'resolution_provided': resolution_provided,
            'follow_up_needed': follow_up_needed
        }
        
        transcripts.append(transcript)
        transcript_counter += 1
    
    print(f"Generated {len(transcripts)} enhanced call transcript records")
    
    # Write to CSV
    output_file = os.path.join(data_dir, 'call_transcripts.csv')
    with open(output_file, 'w', newline='') as f:
        if transcripts:
            fieldnames = transcripts[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transcripts)
    
    # Enhanced statistics
    satisfaction_dist = {}
    for i in range(1, 6):
        satisfaction_dist[i] = sum(1 for t in transcripts if t['customer_satisfaction'] == i)
    
    agent_dist = {}
    for t in transcripts:
        agent = t['agent_name']
        if agent not in agent_dist:
            agent_dist[agent] = 0
        agent_dist[agent] += 1
    
    avg_duration = sum(t['call_duration'] for t in transcripts) / len(transcripts)
    avg_length = sum(len(t['transcript_text']) for t in transcripts) / len(transcripts)
    
    print(f"\n📊 Enhanced Transcript Statistics:")
    print(f"  Satisfaction distribution: {satisfaction_dist}")
    print(f"  Agent distribution: {agent_dist}")
    print(f"  Average call duration: {avg_duration:.0f} seconds")
    print(f"  Average transcript length: {avg_length:.0f} characters")
    print(f"  Resolution rate: {sum(1 for t in transcripts if t['resolution_provided'])/len(transcripts)*100:.1f}%")
    print(f"  Follow-up rate: {sum(1 for t in transcripts if t['follow_up_needed'])/len(transcripts)*100:.1f}%")
    
    return transcripts

if __name__ == "__main__":
    generate_enhanced_call_transcripts()