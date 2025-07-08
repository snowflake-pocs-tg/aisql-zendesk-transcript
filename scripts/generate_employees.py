import csv
import random
import json
import os
from datetime import datetime, timedelta

def generate_employees():
    """Generate employee records for all Zendesk customers"""
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    
    # Read customer data to get organization info
    customers = []
    customer_file = os.path.join(data_dir, 'zendesk_customers.csv')
    with open(customer_file, 'r') as f:
        reader = csv.DictReader(f)
        customers = list(reader)
    
    print(f"Loaded {len(customers)} customers")
    
    # Employee data by organization type
    roles_by_org_type = {
        'faith': {
            'church': ['Pastor', 'Associate Pastor', 'Finance Director', 'Administrative Assistant', 'Music Director', 'Youth Pastor', 'Office Manager'],
            'synagogue': ['Rabbi', 'Cantor', 'Executive Director', 'Administrative Assistant', 'Education Director', 'Office Manager'],
            'mosque': ['Imam', 'Administrative Director', 'Education Coordinator', 'Office Assistant', 'Community Outreach Coordinator']
        },
        'school': {
            'elementary': ['Principal', 'Assistant Principal', 'Secretary', 'Registrar', 'Finance Manager', 'IT Coordinator'],
            'middle': ['Principal', 'Assistant Principal', 'Dean of Students', 'Secretary', 'Finance Manager', 'IT Coordinator'],
            'high': ['Principal', 'Assistant Principal', 'Dean of Students', 'Athletic Director', 'Finance Manager', 'IT Coordinator', 'Registrar']
        },
        'nonprofit': {
            'charity': ['Executive Director', 'Program Director', 'Development Coordinator', 'Administrative Assistant', 'Finance Manager'],
            'foundation': ['President', 'Program Officer', 'Grant Coordinator', 'Administrative Assistant', 'Finance Director'],
            'community': ['Director', 'Program Coordinator', 'Administrative Assistant', 'Volunteer Coordinator', 'Finance Manager']
        },
        'childcare': {
            'daycare': ['Director', 'Assistant Director', 'Lead Teacher', 'Administrative Assistant', 'Finance Coordinator'],
            'preschool': ['Director', 'Educational Director', 'Lead Teacher', 'Administrative Assistant', 'Parent Coordinator']
        },
        'community_ed': {
            'arts': ['Executive Director', 'Program Director', 'Instructor Coordinator', 'Administrative Assistant', 'Marketing Coordinator'],
            'adult_education': ['Director', 'Academic Coordinator', 'Student Services', 'Administrative Assistant', 'Finance Manager'],
            'sports': ['Athletic Director', 'Program Coordinator', 'Facilities Manager', 'Administrative Assistant', 'Registration Coordinator']
        }
    }
    
    # Names for variety
    first_names = [
        'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
        'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
        'Thomas', 'Sarah', 'Christopher', 'Karen', 'Charles', 'Nancy', 'Daniel', 'Lisa',
        'Matthew', 'Betty', 'Anthony', 'Helen', 'Mark', 'Sandra', 'Donald', 'Donna',
        'Steven', 'Carol', 'Paul', 'Ruth', 'Andrew', 'Sharon', 'Joshua', 'Michelle',
        'Kenneth', 'Laura', 'Kevin', 'Sarah', 'Brian', 'Kimberly', 'George', 'Deborah',
        'Timothy', 'Dorothy', 'Ronald', 'Lisa', 'Jason', 'Nancy', 'Edward', 'Karen',
        'Jeffrey', 'Betty', 'Ryan', 'Helen', 'Jacob', 'Sandra', 'Gary', 'Donna'
    ]
    
    last_names = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
        'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas',
        'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White',
        'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young',
        'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
        'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell'
    ]
    
    employees = []
    employee_counter = 1
    used_emails = set()
    
    for customer in customers:
        customer_id = customer['customer_id']
        org_name = customer['organization_name']
        org_type = customer['organization_type']
        org_subtype = customer['organization_subtype']
        size_category = customer['size_category']
        setup_date = customer['setup_date']
        
        # Determine number of employees based on size
        if size_category == 'small':
            num_employees = random.choice([3, 4])
        elif size_category == 'medium':
            num_employees = random.choice([4, 5])
        else:  # large
            num_employees = 5
        
        # Get appropriate roles for this organization type
        available_roles = roles_by_org_type.get(org_type, {}).get(org_subtype, ['Director', 'Manager', 'Assistant', 'Coordinator', 'Specialist'])
        
        # Ensure we have enough roles
        if len(available_roles) < num_employees:
            available_roles.extend(['Staff Member', 'Assistant', 'Coordinator', 'Specialist'])
        
        # Select roles for this organization
        selected_roles = random.sample(available_roles, min(num_employees, len(available_roles)))
        
        # Make first employee the primary contact (matches customer data)
        primary_contact_assigned = False
        
        for i in range(num_employees):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            # Assign role
            if i < len(selected_roles):
                title = selected_roles[i]
            else:
                title = random.choice(['Assistant', 'Coordinator', 'Staff Member'])
            
            # Determine if this is primary contact
            is_primary = not primary_contact_assigned and (i == 0 or random.random() < 0.3)
            if is_primary:
                primary_contact_assigned = True
            
            # Generate email
            domain_base = org_name.lower().replace(' ', '').replace("'", '').replace('#', '').replace('.', '')
            email = f'{first_name.lower()}.{last_name.lower()}@{domain_base}.org'
            
            # Ensure email uniqueness
            counter = 1
            original_email = email
            while email in used_emails:
                email = f'{first_name.lower()}.{last_name.lower()}{counter}@{domain_base}.org'
                counter += 1
            used_emails.add(email)
            
            # Generate hire date (after organization setup)
            setup_dt = datetime.strptime(setup_date, '%Y-%m-%d')
            
            # Hire date between setup date and now
            days_since_setup = (datetime.now() - setup_dt).days
            if days_since_setup > 0:
                hire_offset = random.randint(0, min(days_since_setup, 2000))  # Max 5.5 years
                hire_date = setup_dt + timedelta(days=hire_offset)
            else:
                hire_date = setup_dt
            
            # Department based on role
            if any(keyword in title.lower() for keyword in ['pastor', 'rabbi', 'imam', 'principal']):
                department = 'Leadership'
            elif any(keyword in title.lower() for keyword in ['finance', 'accounting']):
                department = 'Finance'
            elif any(keyword in title.lower() for keyword in ['admin', 'secretary', 'office']):
                department = 'Administration'
            elif any(keyword in title.lower() for keyword in ['program', 'education', 'academic']):
                department = 'Programs'
            else:
                department = 'Operations'
            
            # Role categorization
            if any(keyword in title.lower() for keyword in ['director', 'principal', 'pastor', 'rabbi', 'imam', 'president']):
                role = 'admin'
            elif any(keyword in title.lower() for keyword in ['finance', 'accounting']):
                role = 'finance'
            else:
                role = random.choice(['volunteer', 'director', 'teacher'])
            
            # Permissions based on role
            if is_primary or role == 'admin':
                permissions = ['billing', 'reports', 'settings', 'users']
            elif role == 'finance':
                permissions = ['billing', 'reports']
            else:
                permissions = ['basic_access']
            
            # Training completion (higher for newer employees)
            days_employed = (datetime.now() - hire_date).days
            if days_employed < 90:
                training_completed = random.choice([True, False])
            else:
                training_completed = random.choice([True, True, True, False])  # 75% trained
            
            # Recent login dates (within last 30 days)
            last_login = datetime(2024, 11, 20) - timedelta(days=random.randint(1, 30))
            
            employee = {
                'employee_id': f'EMP{employee_counter:04d}',
                'customer_id': customer_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': f'555-{random.randint(100,999)}-{random.randint(1000,9999)}',
                'title': title,
                'role': role,
                'department': department,
                'hire_date': hire_date.strftime('%Y-%m-%d'),
                'is_primary_contact': is_primary,
                'is_active': random.choice([True] * 19 + [False]),  # 95% active
                'last_login_date': last_login.strftime('%Y-%m-%d'),
                'training_completed': training_completed,
                'permissions': json.dumps(permissions),
                'created_at': hire_date.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': datetime(2024, 11, 20, 14, 30).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            employees.append(employee)
            employee_counter += 1
    
    print(f"Generated {len(employees)} employee records")
    
    # Write to CSV
    output_file = os.path.join(data_dir, 'zendesk_employees.csv')
    with open(output_file, 'w', newline='') as f:
        if employees:
            fieldnames = employees[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(employees)
    
    # Statistics
    org_type_counts = {}
    primary_contacts = 0
    
    for emp in employees:
        # Find customer for this employee
        customer = next(c for c in customers if c['customer_id'] == emp['customer_id'])
        org_type = customer['organization_type']
        org_type_counts[org_type] = org_type_counts.get(org_type, 0) + 1
        
        if emp['is_primary_contact']:
            primary_contacts += 1
    
    print(f"Employee distribution by org type: {org_type_counts}")
    print(f"Primary contacts: {primary_contacts}")
    print(f"Average employees per customer: {len(employees) / len(customers):.1f}")
    
    return employees

if __name__ == "__main__":
    generate_employees()