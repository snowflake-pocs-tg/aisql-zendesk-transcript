import csv
import random
import json
import os
from datetime import datetime, timedelta

def generate_enhanced_description(category, category_type, org_type, org_subtype, size_category, priority, requester):
    """Generate highly variable ticket descriptions with contextual intelligence"""
    
    # Description templates by category with multiple variations
    description_patterns = {
        'payment_processing': {
            'urgent_patterns': [
                "URGENT: {issue} - This is severely impacting our {org_activity} and we need immediate assistance.",
                "Critical issue with {issue}. We have {impact_scale} affected and need emergency support.",
                "Emergency: {issue} is preventing all donation processing. Please prioritize this ticket.",
                "PRIORITY: {issue} - Our {seasonal_context} is at risk. Immediate help needed."
            ],
            'normal_patterns': [
                "We're experiencing {issue} which started {timeframe}. This is affecting our {workflow_area}.",
                "Hello Support, {issue} and we need guidance on resolution. {additional_context}",
                "Support needed for {issue}. We've attempted {troubleshooting_attempted} but need expert help.",
                "Hi team, {issue} is causing delays in our {business_process}. Can you assist?",
                "Good {time_greeting}, we have {issue} that needs attention. {impact_description}"
            ],
            'detailed_patterns': [
                "We are encountering {issue} in our system. Background: {background_context}. The issue manifests as {specific_symptoms}. We have tried {troubleshooting_attempted} without success. Please advise on next steps.",
                "Reporting {issue} that began {timeframe}. Environment details: {environment_details}. Impact assessment: {impact_description}. Looking for both immediate resolution and preventive measures.",
                "Technical issue report: {issue}. This affects {affected_users} users across our {org_structure}. Error patterns: {error_details}. Please provide detailed troubleshooting steps."
            ]
        },
        'setup': {
            'getting_started': [
                "New to your platform and need help with {issue}. We're a {org_description} looking to {goal_description}.",
                "Just signed up and working on {issue}. Our team includes {team_description} and we want to ensure proper setup.",
                "Beginning our implementation and need guidance on {issue}. Timeline: {timeline_context}."
            ],
            'configuration': [
                "Configuration assistance needed for {issue}. Our specific requirements: {requirements_context}.",
                "Setup help required: {issue}. We have {technical_context} and need customization guidance.",
                "Implementation support for {issue}. Organization specifics: {org_specifics}."
            ]
        },
        'training': {
            'team_training': [
                "Training request for {issue}. We have {team_size} {team_type} who need to learn the system.",
                "Educational support needed: {issue}. Our staff includes {staff_description} with varying technical comfort levels.",
                "Workshop request for {issue}. We'd like to schedule training for our {department} team."
            ],
            'individual_help': [
                "Personal assistance with {issue}. I'm {requester_role} and need to understand {learning_goal}.",
                "One-on-one help needed for {issue}. My background: {background} and I'm trying to {objective}.",
                "Individual training on {issue}. I handle {responsibilities} and need to get up to speed quickly."
            ]
        },
        'integration': {
            'technical': [
                "Integration issue: {issue}. Technical details: {tech_specs}. Error logs: {error_context}.",
                "API/sync problem with {issue}. Our setup: {integration_setup}. Need technical assistance.",
                "Connection failure: {issue}. System details: {system_details}. Requires engineering support."
            ],
            'business': [
                "Data sync issue with {issue} affecting our {business_workflow}. Need business continuity solution.",
                "Integration problem: {issue} is disrupting our {operational_process}. Please prioritize.",
                "Workflow interruption due to {issue}. This impacts {business_impact}. Need rapid resolution."
            ]
        },
        'billing': {
            'inquiry': [
                "Billing inquiry about {issue}. Our account details: {account_context}. Need clarification.",
                "Question regarding {issue}. We're reviewing our {billing_context} and need information.",
                "Account question: {issue}. Looking for details about {billing_aspect}."
            ],
            'dispute': [
                "Billing concern: {issue}. This appears incorrect based on our {expectation_context}.",
                "Invoice discrepancy: {issue}. Need review of charges for {billing_period}.",
                "Billing issue requiring attention: {issue}. Please investigate and advise."
            ]
        },
        'feature_request': {
            'enhancement': [
                "Feature enhancement idea: {issue}. This would help us {benefit_description}.",
                "Product suggestion: {issue}. Our use case: {use_case_description}.",
                "Feature request for {issue}. This would improve our {improvement_area}."
            ],
            'new_functionality': [
                "New feature request: {issue}. We need this capability to {capability_need}.",
                "Product enhancement: {issue} would enable us to {enablement_goal}.",
                "Functionality request: {issue} to support our {support_need}."
            ]
        },
        'bug_report': {
            'technical': [
                "Bug report: {issue}. Steps to reproduce: {reproduction_steps}. Expected vs actual behavior: {behavior_description}.",
                "System error: {issue}. Error details: {error_details}. Environment: {environment_info}.",
                "Technical malfunction: {issue}. This occurs when {trigger_condition}. Screenshots attached."
            ],
            'user_impact': [
                "User-facing issue: {issue} is preventing {user_goal}. Multiple users affected.",
                "Workflow disruption: {issue} blocks normal operations. Urgent user experience fix needed.",
                "Customer impact: {issue} affects {customer_interaction}. Please prioritize resolution."
            ]
        }
    }
    
    # Context generators for variable replacement
    def get_org_activity():
        org_activities = {
            'faith': ['worship services', 'tithing campaign', 'building fund drive', 'holiday giving', 'stewardship program'],
            'school': ['tuition collection', 'fundraising event', 'enrollment period', 'payment processing', 'family billing'],
            'nonprofit': ['fundraising campaign', 'donor outreach', 'grant application', 'donation drive', 'annual campaign'],
            'childcare': ['tuition payments', 'family billing', 'enrollment process', 'payment collection', 'fee processing'],
            'community_ed': ['course enrollment', 'program registration', 'membership billing', 'class payments', 'workshop fees']
        }
        return random.choice(org_activities.get(org_type, org_activities['nonprofit']))
    
    def get_seasonal_context():
        seasonal_contexts = {
            'faith': ['Christmas giving season', 'Easter campaign', 'year-end stewardship', 'Thanksgiving appeal', 'Lenten giving'],
            'school': ['back-to-school enrollment', 'spring fundraiser', 'graduation season', 'winter break processing', 'summer camp registration'],
            'nonprofit': ['annual gala', 'giving season', 'grant deadline period', 'awareness month campaign', 'year-end drive'],
            'childcare': ['enrollment period', 'summer program', 'holiday break billing', 'new year registration', 'spring enrollment'],
            'community_ed': ['course registration', 'workshop season', 'membership renewal', 'program launch', 'community outreach']
        }
        return random.choice(seasonal_contexts.get(org_type, seasonal_contexts['nonprofit']))
    
    def get_impact_scale():
        scales = {
            'small': ['several families', '10-15 users', 'multiple members', 'our core team'],
            'medium': ['dozens of families', '50+ users', 'significant portion of members', 'multiple departments'],
            'large': ['hundreds of families', '200+ users', 'majority of our community', 'entire organization']
        }
        return random.choice(scales.get(size_category, scales['medium']))
    
    def get_troubleshooting_attempted():
        return random.choice([
            'basic troubleshooting steps', 'restarting our browser', 'clearing cache and cookies',
            'checking with our IT person', 'reviewing documentation', 'testing different browsers',
            'verifying our internet connection', 'checking account permissions', 'consulting with team members'
        ])
    
    def get_timeframe():
        return random.choice([
            'yesterday morning', 'two days ago', 'earlier this week', 'last Friday',
            'over the weekend', 'this morning', 'after our last update', 'since Tuesday',
            'beginning of this week', 'late last week'
        ])
    
    def get_business_process():
        processes = {
            'faith': ['Sunday giving collection', 'online tithing', 'building fund donations', 'memorial gifts', 'pledge payments'],
            'school': ['tuition processing', 'lunch payments', 'activity fees', 'fundraiser collections', 'parent payments'],
            'nonprofit': ['donor management', 'fundraising operations', 'grant tracking', 'volunteer coordination', 'membership billing'],
            'childcare': ['parent billing', 'enrollment payments', 'program fees', 'extended care charges', 'supply fees'],
            'community_ed': ['class registrations', 'workshop payments', 'membership processing', 'program enrollments', 'facility rentals']
        }
        return random.choice(processes.get(org_type, processes['nonprofit']))
    
    def get_org_description():
        descriptions = {
            'faith': {
                'church': f'{size_category.title()} congregation with active {get_seasonal_context().lower()}',
                'synagogue': f'{size_category.title()} Jewish community focused on {get_org_activity()}',
                'mosque': f'{size_category.title()} Islamic center managing {get_org_activity()}'
            },
            'school': {
                'elementary': f'{size_category.title()} elementary school handling {get_business_process()}',
                'middle': f'{size_category.title()} middle school with {get_impact_scale()}',
                'high': f'{size_category.title()} high school managing {get_business_process()}'
            },
            'nonprofit': f'{size_category.title()} nonprofit organization focused on {get_org_activity()}',
            'childcare': f'{size_category.title()} childcare center with {get_impact_scale()}',
            'community_ed': f'{size_category.title()} community education program offering {get_business_process()}'
        }
        
        if org_type == 'faith' and org_subtype in descriptions[org_type]:
            return descriptions[org_type][org_subtype]
        elif org_type == 'school' and org_subtype in descriptions[org_type]:
            return descriptions[org_type][org_subtype]
        else:
            return descriptions.get(org_type, f'{size_category.title()} organization')
    
    def get_requester_context():
        role_contexts = {
            'admin': 'system administrator',
            'finance': 'finance team member', 
            'volunteer': 'volunteer coordinator',
            'pastor': 'pastoral staff',
            'principal': 'school administrator',
            'teacher': 'faculty member',
            'director': 'program director'
        }
        role = requester.get('role', 'staff')
        return role_contexts.get(role, 'team member')
    
    # Select appropriate pattern based on priority and category
    if category not in description_patterns:
        # Fallback for any missing categories
        return f"We need assistance with {category.replace('_', ' ').lower()}. This is affecting our {get_org_activity()} and we'd appreciate your help resolving it."
    
    patterns = description_patterns[category]
    
    # Choose pattern type based on priority and requester role
    if priority == 'urgent':
        pattern_type = 'urgent_patterns'
    elif requester.get('role') in ['admin', 'principal', 'director'] or size_category == 'large':
        pattern_type = 'detailed_patterns' if 'detailed_patterns' in patterns else 'normal_patterns'
    else:
        pattern_type = 'normal_patterns' if 'normal_patterns' in patterns else list(patterns.keys())[0]
    
    # Get available patterns for this type
    available_patterns = patterns.get(pattern_type, patterns[list(patterns.keys())[0]])
    selected_pattern = random.choice(available_patterns)
    
    # Create context replacements
    context_replacements = {
        'issue': category.replace('_', ' ').lower(),
        'org_activity': get_org_activity(),
        'seasonal_context': get_seasonal_context(),
        'impact_scale': get_impact_scale(),
        'troubleshooting_attempted': get_troubleshooting_attempted(),
        'timeframe': get_timeframe(),
        'workflow_area': get_business_process(),
        'business_process': get_business_process(),
        'org_description': get_org_description(),
        'requester_role': get_requester_context(),
        'time_greeting': random.choice(['morning', 'afternoon', 'day']),
        'impact_description': f"This affects {get_impact_scale()} in our {get_org_activity()}",
        'additional_context': f"We noticed this during our {get_business_process()}",
        'background_context': f"We're a {get_org_description()} that relies heavily on this functionality",
        'specific_symptoms': f"Users report issues when trying to {get_business_process().rstrip('s')}",
        'environment_details': f"Our {size_category} {org_type} organization using {random.choice(['Windows', 'Mac', 'mixed platform'])} systems",
        'affected_users': get_impact_scale(),
        'org_structure': f"{org_type} with {random.choice(['centralized', 'distributed', 'hybrid'])} operations",
        'error_details': f"Occurs primarily during {get_business_process()}",
        'goal_description': f"streamline our {get_org_activity()}",
        'team_description': f"{get_impact_scale()} including {get_requester_context()}s",
        'timeline_context': f"Planning to launch during {get_seasonal_context().lower()}",
        'requirements_context': f"Support for {get_business_process()} with {get_impact_scale()}",
        'technical_context': f"{random.choice(['basic', 'intermediate', 'advanced'])} technical capabilities",
        'org_specifics': f"We're a {get_org_description()}",
        'team_size': random.choice(['5-8', '10-12', '15-20', '20+']),
        'team_type': random.choice(['staff members', 'volunteers', 'administrators', 'coordinators']),
        'staff_description': f"{get_impact_scale()} across {random.choice(['multiple departments', 'different locations', 'various roles'])}",
        'department': random.choice(['finance', 'administration', 'operations', 'outreach']),
        'learning_goal': f"effectively manage {get_business_process()}",
        'background': f"I'm responsible for {get_org_activity()}",
        'objective': f"optimize our {get_business_process()}",
        'responsibilities': f"{get_org_activity()} and related {random.choice(['reporting', 'coordination', 'management'])}",
        'tech_specs': f"Using {random.choice(['REST API', 'webhook integration', 'batch sync', 'real-time connection'])}",
        'error_context': f"Error occurs during {get_business_process()}",
        'integration_setup': f"{random.choice(['QuickBooks Online', 'Salesforce', 'custom CRM', 'accounting software'])} integration",
        'system_details': f"{size_category.title()} organization with {random.choice(['cloud-based', 'on-premise', 'hybrid'])} infrastructure",
        'business_workflow': get_business_process(),
        'operational_process': get_org_activity(),
        'business_impact': f"our ability to {get_business_process()}",
        'account_context': f"We're a {size_category} {org_type} organization",
        'billing_context': f"{random.choice(['monthly charges', 'annual subscription', 'usage fees', 'service costs'])}",
        'billing_aspect': f"{random.choice(['subscription tier', 'usage calculations', 'discount application', 'payment timing'])}",
        'expectation_context': f"our {random.choice(['contract terms', 'initial agreement', 'previous billing', 'quoted pricing'])}",
        'billing_period': f"{random.choice(['this month', 'last quarter', 'annual billing', 'recent charges'])}",
        'benefit_description': f"better serve our {get_impact_scale()}",
        'use_case_description': f"We need to {get_business_process()} more efficiently",
        'improvement_area': f"{get_org_activity()} management",
        'capability_need': f"support our {get_seasonal_context().lower()}",
        'enablement_goal': f"expand our {get_org_activity()}",
        'support_need': f"growing {get_business_process()} demands",
        'reproduction_steps': f"Occurs when accessing {get_business_process()} during {get_seasonal_context().lower()}",
        'behavior_description': f"Expected normal {get_business_process()}, but system {random.choice(['freezes', 'errors', 'crashes', 'times out'])}",
        'error_details': f"Error appears during {get_business_process()}",
        'environment_info': f"{size_category.title()} {org_type} environment with {get_impact_scale()}",
        'trigger_condition': f"users attempt {get_business_process()}",
        'user_goal': f"completing {get_business_process()}",
        'customer_interaction': f"our {get_impact_scale()}"
    }
    
    # Replace placeholders in the selected pattern
    try:
        formatted_description = selected_pattern.format(**context_replacements)
        return formatted_description
    except KeyError as e:
        # Fallback if any replacement fails
        return f"We need assistance with {category.replace('_', ' ').lower()}. This is impacting our {get_org_activity()} and we'd appreciate your help."

def generate_tickets():
    """Generate ticket records for all Zendesk customers"""
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    
    # Read customer and employee data
    customers = []
    customer_file = os.path.join(data_dir, 'zendesk_customers.csv')
    with open(customer_file, 'r') as f:
        reader = csv.DictReader(f)
        customers = list(reader)
    
    employees = []
    employee_file = os.path.join(data_dir, 'zendesk_employees.csv')
    with open(employee_file, 'r') as f:
        reader = csv.DictReader(f)
        employees = list(reader)
    
    print(f"Loaded {len(customers)} customers and {len(employees)} employees")
    
    # Create customer to employees mapping
    customer_employees = {}
    for emp in employees:
        customer_id = emp['customer_id']
        if customer_id not in customer_employees:
            customer_employees[customer_id] = []
        customer_employees[customer_id].append(emp)
    
    # Category mapping for ticket types (subject removed - AI_CLASSIFY will handle categorization)
    category_mapping = {
        'payment_processing': 'Payment Processing Issues',
        'setup': 'Account Management and Billing',
        'training': 'Training and User Education', 
        'integration': 'Integration and Technical Support',
        'billing': 'Account Management and Billing',
        'feature_request': 'Feature Requests and Enhancements',
        'bug_report': 'Integration and Technical Support'
    }
    
    # Seasonal patterns for different org types
    def get_ticket_months_weights(org_type):
        if org_type == 'faith':
            # Higher activity in Nov-Dec (holidays), Mar-Apr (Easter), Sep (fall programs)
            return [6, 6, 8, 8, 7, 7, 6, 6, 9, 7, 12, 12]
        elif org_type == 'school':
            # Higher in Aug-Sep (start of year), Jan (after break), May (end of year)
            return [10, 8, 9, 8, 11, 7, 4, 12, 10, 8, 7, 6]
        elif org_type == 'childcare':
            # More consistent, slight increases in Sep, Jan
            return [9, 8, 8, 8, 8, 7, 6, 8, 10, 8, 8, 9]
        else:  # nonprofit, community_ed
            # More consistent throughout year
            return [8, 8, 8, 8, 8, 8, 7, 7, 9, 9, 8, 8]
    
    tickets = []
    ticket_counter = 1
    
    for customer in customers:
        customer_id = customer['customer_id']
        org_type = customer['organization_type']
        org_subtype = customer['organization_subtype']
        size_category = customer['size_category']
        setup_date = datetime.strptime(customer['setup_date'], '%Y-%m-%d')
        customer_created = datetime.strptime(customer['created_at'], '%Y-%m-%d %H:%M:%S')
        
        # Determine number of tickets based on size and subscription tier
        base_tickets = {
            'small': 15,
            'medium': 25,
            'large': 35
        }
        
        tier_multiplier = {
            'basic': 0.8,
            'standard': 1.0,
            'premium': 1.3
        }
        
        num_tickets = int(base_tickets[size_category] * tier_multiplier[customer['subscription_tier']])
        num_tickets += random.randint(-5, 5)  # Add some randomness
        num_tickets = max(10, num_tickets)  # Minimum 10 tickets
        
        # Get employees for this customer
        customer_emps = customer_employees.get(customer_id, [])
        if not customer_emps:
            print(f"Warning: No employees found for {customer_id}")
            continue
        
        # Get seasonal weights
        month_weights = get_ticket_months_weights(org_type)
        
        for i in range(num_tickets):
            # Select random employee as requester
            requester = random.choice(customer_emps)
            employee_hire_date = datetime.strptime(requester['hire_date'], '%Y-%m-%d')
            
            # Ticket can only be created after BOTH customer setup AND employee hire date
            earliest_ticket_date = max(customer_created, employee_hire_date)
            
            # Generate ticket date (between earliest valid date and now)
            days_since_earliest = (datetime(2024, 11, 20) - earliest_ticket_date).days
            if days_since_earliest <= 0:
                ticket_date = earliest_ticket_date
            else:
                # Use seasonal weights to pick month
                ticket_month = random.choices(range(1, 13), weights=month_weights)[0]
                
                # Pick a year between earliest valid date and current
                possible_years = []
                for year in range(earliest_ticket_date.year, 2025):
                    if year == earliest_ticket_date.year and ticket_month < earliest_ticket_date.month:
                        continue
                    if year == 2024 and ticket_month > 11:
                        continue
                    possible_years.append(year)
                
                if possible_years:
                    ticket_year = random.choice(possible_years)
                    ticket_day = random.randint(1, 28)  # Safe day for any month
                    proposed_date = datetime(ticket_year, ticket_month, ticket_day)
                    
                    # Ensure ticket date is not before earliest valid date
                    if proposed_date < earliest_ticket_date:
                        ticket_date = earliest_ticket_date + timedelta(days=random.randint(1, 30))
                    else:
                        ticket_date = proposed_date
                else:
                    ticket_date = earliest_ticket_date + timedelta(days=random.randint(0, min(days_since_earliest, 730)))
            
            # Determine ticket category based on org type and timing
            if org_type == 'faith':
                category_weights = {
                    'payment_processing': 30,
                    'setup': 15,
                    'training': 20,
                    'integration': 10,
                    'billing': 10,
                    'feature_request': 10,
                    'bug_report': 5
                }
            elif org_type == 'school':
                category_weights = {
                    'payment_processing': 25,
                    'setup': 20,
                    'training': 25,
                    'integration': 15,
                    'billing': 5,
                    'feature_request': 7,
                    'bug_report': 3
                }
            else:
                category_weights = {
                    'payment_processing': 35,
                    'setup': 15,
                    'training': 15,
                    'integration': 12,
                    'billing': 8,
                    'feature_request': 10,
                    'bug_report': 5
                }
            
            category = random.choices(
                list(category_weights.keys()),
                weights=list(category_weights.values())
            )[0]
            
            # Priority based on category (moved up before description generation)
            priority_weights = {
                'payment_processing': {'low': 10, 'normal': 30, 'high': 40, 'urgent': 20},
                'bug_report': {'low': 5, 'normal': 25, 'high': 50, 'urgent': 20},
                'setup': {'low': 20, 'normal': 50, 'high': 25, 'urgent': 5},
                'training': {'low': 40, 'normal': 45, 'high': 10, 'urgent': 5},
                'integration': {'low': 15, 'normal': 40, 'high': 35, 'urgent': 10},
                'billing': {'low': 25, 'normal': 45, 'high': 25, 'urgent': 5},
                'feature_request': {'low': 50, 'normal': 40, 'high': 8, 'urgent': 2}
            }
            
            priority = random.choices(
                list(priority_weights[category].keys()),
                weights=list(priority_weights[category].values())
            )[0]
            
            # Generate enhanced description with variability (no subject needed - AI will classify)
            description = generate_enhanced_description(category, category, org_type, org_subtype, size_category, priority, requester)
            
            # Status distribution (more solved/closed for older tickets)
            days_old = (datetime(2024, 11, 20) - ticket_date).days
            if days_old > 30:
                status_weights = {'new': 2, 'open': 8, 'pending': 5, 'hold': 2, 'solved': 45, 'closed': 38}
            elif days_old > 7:
                status_weights = {'new': 5, 'open': 20, 'pending': 15, 'hold': 5, 'solved': 35, 'closed': 20}
            else:
                status_weights = {'new': 15, 'open': 40, 'pending': 20, 'hold': 10, 'solved': 10, 'closed': 5}
            
            status = random.choices(
                list(status_weights.keys()),
                weights=list(status_weights.values())
            )[0]
            
            # Type based on category
            if category in ['bug_report']:
                ticket_type = random.choice(['problem', 'incident'])
            elif category in ['feature_request']:
                ticket_type = 'task'
            else:
                ticket_type = random.choice(['question', 'task', 'problem'])
            
            # Channel distribution
            via_channel = random.choices(
                ['web', 'email', 'phone', 'chat'],
                weights=[40, 35, 20, 5]
            )[0]
            
            # Satisfaction rating (only for solved/closed tickets)
            satisfaction_rating = None
            satisfaction_comment = None
            if status in ['solved', 'closed'] and random.random() < 0.7:  # 70% provide satisfaction
                satisfaction_rating = random.choices(
                    ['good', 'bad'],
                    weights=[85, 15]  # 85% positive
                )[0]
                
                if satisfaction_rating == 'good':
                    satisfaction_comment = random.choice([
                        'Great support, very helpful!',
                        'Quick resolution, thank you!',
                        'Excellent service as always.',
                        'Problem solved efficiently.',
                        'Very satisfied with the help.'
                    ])
                else:
                    satisfaction_comment = random.choice([
                        'Took too long to resolve.',
                        'Could have been faster.',
                        'Had to follow up multiple times.',
                        'Solution was unclear.',
                        'Expected better response time.'
                    ])
            
            # Tags based on category and org type
            tags = [category.replace('_', '')]
            if org_type == 'faith':
                tags.append('church')
            elif org_type == 'school':
                tags.append('education')
            
            if priority in ['high', 'urgent']:
                tags.append('urgent')
            
            if size_category == 'large':
                tags.append('enterprise')
            
            # Due date (20% of tickets have due dates, mainly high/urgent priority)
            due_at = None
            if priority in ['high', 'urgent'] and random.random() < 0.4:
                due_days = {'high': 5, 'urgent': 2}[priority]
                due_at = (ticket_date + timedelta(days=due_days)).strftime('%Y-%m-%d %H:%M:%S')
            
            # Solved date for solved/closed tickets
            solved_at = None
            if status in ['solved', 'closed']:
                resolution_days = random.randint(1, 14)  # 1-14 days to resolve
                solved_at = (ticket_date + timedelta(days=resolution_days)).strftime('%Y-%m-%d %H:%M:%S')
            
            # Updated date (recent for open tickets, solved date for closed)
            if status in ['solved', 'closed'] and solved_at:
                updated_at = solved_at
            else:
                # Recent update for open tickets
                max_days_since_update = max(0, min(7, days_old))
                if max_days_since_update > 0:
                    days_since_update = random.randint(0, max_days_since_update)
                    update_date = datetime(2024, 11, 20) - timedelta(days=days_since_update)
                else:
                    update_date = ticket_date + timedelta(hours=random.randint(1, 24))
                updated_at = update_date.strftime('%Y-%m-%d %H:%M:%S')
            
            ticket = {
                'ticket_id': ticket_counter,
                'customer_id': customer_id,
                'employee_id': requester['employee_id'],
                'description': description,
                'status': status,
                'priority': priority,
                'type': ticket_type,
                'via_channel': via_channel,
                'satisfaction_rating': satisfaction_rating if satisfaction_rating else '',
                'satisfaction_comment': satisfaction_comment if satisfaction_comment else '',
                'tags': json.dumps(tags),
                'due_at': due_at if due_at else '',
                'created_at': ticket_date.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': updated_at,
                'solved_at': solved_at if solved_at else ''
            }
            
            tickets.append(ticket)
            ticket_counter += 1
    
    print(f"Generated {len(tickets)} ticket records")
    
    # Write to CSV
    output_file = os.path.join(data_dir, 'zendesk_tickets.csv')
    with open(output_file, 'w', newline='') as f:
        if tickets:
            fieldnames = tickets[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(tickets)
    
    # Statistics
    status_counts = {}
    priority_counts = {}
    org_type_counts = {}
    
    for ticket in tickets:
        status_counts[ticket['status']] = status_counts.get(ticket['status'], 0) + 1
        priority_counts[ticket['priority']] = priority_counts.get(ticket['priority'], 0) + 1
        
        # Find customer for this ticket
        customer = next(c for c in customers if c['customer_id'] == ticket['customer_id'])
        org_type = customer['organization_type']
        org_type_counts[org_type] = org_type_counts.get(org_type, 0) + 1
    
    print(f"Status distribution: {status_counts}")
    print(f"Priority distribution: {priority_counts}")
    print(f"Org type distribution: {org_type_counts}")
    print(f"Average tickets per customer: {len(tickets) / len(customers):.1f}")
    
    return tickets

if __name__ == "__main__":
    generate_tickets()