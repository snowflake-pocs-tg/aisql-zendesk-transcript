import csv
import random
from datetime import datetime, timedelta
import json
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')

# Read existing records
existing = []
existing_file = os.path.join(data_dir, 'zendesk_customers.csv')
try:
    with open(existing_file, 'r') as f:
        reader = csv.DictReader(f)
        existing = list(reader)
except FileNotFoundError:
    print("No existing customer records found - starting fresh")

print(f'Starting with {len(existing)} existing records')

# Data for generation
faith_types = ['church', 'synagogue', 'mosque']
school_types = ['elementary', 'middle', 'high']
nonprofit_types = ['charity', 'foundation', 'community']
childcare_types = ['daycare', 'preschool']
community_ed_types = ['arts', 'adult_education', 'sports']

# Church names
church_names = ['St. Mary', 'First Baptist', 'Grace Community', 'Hope Methodist', 'Trinity Lutheran', 'Calvary Baptist', 'New Life', 'Faith Community', 'Emmanuel Baptist', 'Christ the King', 'St. Paul', 'Cornerstone', 'Living Water', 'Mount Olive', 'Riverside', 'Crossroads', 'Harvest', 'Victory', 'Blessed Sacrament', 'Good Shepherd']
church_suffixes = ['Church', 'Community Church', 'Baptist Church', 'Methodist Church', 'Lutheran Church', 'Presbyterian Church', 'Catholic Church', 'Episcopal Church']

# School names  
school_names = ['Lincoln', 'Washington', 'Roosevelt', 'Jefferson', 'Madison', 'Jackson', 'Adams', 'Wilson', 'Kennedy', 'Franklin', 'Oakwood', 'Riverside', 'Hillcrest', 'Sunset', 'Valley View', 'Pine Ridge', 'Cedar Creek', 'Maple Grove', 'Spring Valley', 'North Star']
school_suffixes = ['Elementary School', 'Middle School', 'High School', 'Elementary', 'Academy']

# Cities and states
us_locations = [
    ('New York', 'NY', 10001, 'America/New_York'),
    ('Los Angeles', 'CA', 90001, 'America/Los_Angeles'),
    ('Chicago', 'IL', 60601, 'America/Chicago'),
    ('Houston', 'TX', 77001, 'America/Chicago'),
    ('Phoenix', 'AZ', 85001, 'America/Phoenix'),
    ('Philadelphia', 'PA', 19101, 'America/New_York'),
    ('San Antonio', 'TX', 78201, 'America/Chicago'),
    ('San Diego', 'CA', 92101, 'America/Los_Angeles'),
    ('Dallas', 'TX', 75201, 'America/Chicago'),
    ('San Jose', 'CA', 95101, 'America/Los_Angeles'),
    ('Austin', 'TX', 73301, 'America/Chicago'),
    ('Jacksonville', 'FL', 32201, 'America/New_York'),
    ('Fort Worth', 'TX', 76101, 'America/Chicago'),
    ('Columbus', 'OH', 43201, 'America/New_York'),
    ('Charlotte', 'NC', 28201, 'America/New_York'),
    ('San Francisco', 'CA', 94101, 'America/Los_Angeles'),
    ('Indianapolis', 'IN', 46201, 'America/New_York'),
    ('Seattle', 'WA', 98101, 'America/Los_Angeles'),
    ('Denver', 'CO', 80201, 'America/Denver'),
    ('Boston', 'MA', 2101, 'America/New_York')
] * 50  # Repeat to have enough options

# Generate 980 more records
new_records = []
used_names = set(r['organization_name'] for r in existing)
used_emails = set(r['primary_contact_email'] for r in existing)

# Distribution targets
faith_count = 640 - sum(1 for r in existing if r['organization_type'] == 'faith')
school_count = 200 - sum(1 for r in existing if r['organization_type'] == 'school')
nonprofit_count = 100 - sum(1 for r in existing if r['organization_type'] == 'nonprofit')
childcare_count = 40 - sum(1 for r in existing if r['organization_type'] == 'childcare')
community_ed_count = 20 - sum(1 for r in existing if r['organization_type'] == 'community_ed')

record_id = len(existing) + 1

for org_type, target_count, subtypes in [
    ('faith', faith_count, faith_types),
    ('school', school_count, school_types),
    ('nonprofit', nonprofit_count, nonprofit_types),
    ('childcare', childcare_count, childcare_types),
    ('community_ed', community_ed_count, community_ed_types)
]:
    
    for i in range(target_count):
        if record_id > 1000:
            break
            
        # Generate unique organization name
        if org_type == 'faith':
            base_name = random.choice(church_names)
            suffix = random.choice(church_suffixes)
            org_name = f'{base_name} {suffix}'
        elif org_type == 'school':
            base_name = random.choice(school_names)
            suffix = random.choice(school_suffixes)
            org_name = f'{base_name} {suffix}'
        else:
            org_name = f'{random.choice(["Community", "City", "Metro", "Valley", "County"])} {org_type.title()} Center'
            
        # Ensure uniqueness
        counter = 1
        original_name = org_name
        while org_name in used_names:
            org_name = f'{original_name} #{counter}'
            counter += 1
        used_names.add(org_name)
        
        # Generate other fields
        subtype = random.choice(subtypes)
        size_cat = random.choices(['small', 'medium', 'large'], weights=[60, 30, 10])[0]
        
        if size_cat == 'small':
            emp_count = random.randint(5, 50)
            revenue = random.randint(400, 2000)
        elif size_cat == 'medium':
            emp_count = random.randint(51, 150)
            revenue = random.randint(2000, 8000)
        else:
            emp_count = random.randint(151, 500)
            revenue = random.randint(8000, 25000)
            
        tier = random.choices(['basic', 'standard', 'premium'], weights=[40, 40, 20])[0]
        
        # Location
        city, state, base_zip, timezone = random.choice(us_locations)
        zip_code = base_zip + random.randint(0, 99)
        
        # Contact info
        first_names = ['John', 'Sarah', 'Michael', 'Jennifer', 'David', 'Lisa', 'Robert', 'Mary', 'William', 'Patricia']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        if org_type == 'faith' and subtype == 'church':
            contact_name = f'Rev. {first_name} {last_name}'
        elif org_type == 'faith' and subtype == 'synagogue':
            contact_name = f'Rabbi {first_name} {last_name}'
        elif org_type == 'faith' and subtype == 'mosque':
            contact_name = f'Imam {first_name} {last_name}'
        elif org_type == 'school':
            contact_name = f'Principal {first_name} {last_name}'
        else:
            contact_name = f'{first_name} {last_name}'
            
        # Email
        domain = org_name.lower().replace(' ', '').replace('#', '').replace("'", '') + '.org'
        email = f'{first_name.lower()}.{last_name.lower()}@{domain}'
        
        counter = 1
        original_email = email
        while email in used_emails:
            email = f'{first_name.lower()}.{last_name.lower()}{counter}@{domain}'
            counter += 1
        used_emails.add(email)
        
        # Dates
        setup_year = random.randint(2015, 2024)
        setup_month = random.randint(1, 12)
        setup_day = random.randint(1, 28)
        setup_date = f'{setup_year}-{setup_month:02d}-{setup_day:02d}'
        
        # Payment methods
        methods = ['online']
        if random.random() < 0.6:
            methods.append('mobile')
        if random.random() < 0.4:
            methods.append('text')
        if size_cat == 'large' and random.random() < 0.3:
            methods.append('pos')
            
        record = {
            'customer_id': f'ZENDESK{record_id:04d}',
            'organization_name': org_name,
            'organization_type': org_type,
            'organization_subtype': subtype,
            'size_category': size_cat,
            'employee_count': emp_count,
            'subscription_tier': tier,
            'monthly_revenue': f'{revenue:.2f}',
            'setup_date': setup_date,
            'primary_contact_name': contact_name,
            'primary_contact_email': email,
            'primary_contact_phone': f'555-{random.randint(100,999)}-{random.randint(1000,9999)}',
            'street_address': f'{random.randint(100, 9999)} {random.choice(["Main", "Oak", "Park", "Church", "School"])} {random.choice(["St", "Ave", "Blvd", "Dr"])}',
            'city': city,
            'state': state,
            'zip_code': str(zip_code),
            'time_zone': timezone,
            'payment_methods': json.dumps(methods),
            'integration_count': random.randint(1, 15),
            'last_login_date': f'2024-{random.randint(10,11)}-{random.randint(1,20):02d}',
            'support_tier': 'premium' if tier == 'premium' else 'basic',
            'created_at': f'{setup_date} {random.randint(8,17):02d}:{random.randint(0,59):02d}:00',
            'updated_at': f'2024-11-{random.randint(15,20):02d} {random.randint(8,17):02d}:{random.randint(0,59):02d}:00'
        }
        
        new_records.append(record)
        record_id += 1
        
        if record_id > 1000:
            break

print(f'Generated {len(new_records)} new records')

# Combine and write
all_records = existing + new_records
output_file = os.path.join(data_dir, 'zendesk_customers.csv')
with open(output_file, 'w', newline='') as f:
    if all_records:
        fieldnames = all_records[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_records)

print(f'Wrote {len(all_records)} total records to zendesk_customers.csv')