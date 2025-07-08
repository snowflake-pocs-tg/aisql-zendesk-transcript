import csv
import random
import os
from datetime import datetime, timedelta

def generate_ticket_metrics():
    """Generate ticket metrics with proper temporal sequencing and enhanced alignment"""
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    
    # Read ticket data
    tickets = []
    tickets_file = os.path.join(data_dir, 'zendesk_tickets.csv')
    with open(tickets_file, 'r') as f:
        reader = csv.DictReader(f)
        tickets = list(reader)
    
    # Read customer data for context
    customers = {}
    customers_file = os.path.join(data_dir, 'zendesk_customers.csv')
    with open(customers_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            customers[row['customer_id']] = row
    
    # Read call transcripts to identify tickets with calls and their durations
    call_tickets = set()
    call_durations = {}
    try:
        transcripts_file = os.path.join(data_dir, 'call_transcripts.csv')
        with open(transcripts_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ticket_id = int(row['ticket_id'])
                call_tickets.add(ticket_id)
                call_durations[ticket_id] = int(row['call_duration']) // 60  # duration in minutes
    except FileNotFoundError:
        print("No call transcripts found - proceeding without call correlation")
    
    print(f"Loaded {len(tickets)} tickets, {len(customers)} customers, {len(call_tickets)} tickets with calls")
    
    metrics = []
    
    for ticket in tickets:
        ticket_id = int(ticket['ticket_id'])
        status = ticket['status']
        priority = ticket['priority']
        customer_id = ticket['customer_id']
        
        # Get customer context for enhanced metrics
        customer = customers.get(customer_id, {})
        org_type = customer.get('organization_type', 'unknown')
        org_size = customer.get('size_category', 'medium')
        subscription_tier = customer.get('subscription_tier', 'standard')
        
        # Check if this ticket has a call transcript
        has_call_transcript = ticket_id in call_tickets
        
        # Get satisfaction rating
        satisfaction = ticket.get('satisfaction_rating', '')
        
        # Parse ticket timestamps
        created_at = datetime.strptime(ticket['created_at'], '%Y-%m-%d %H:%M:%S')
        updated_at = datetime.strptime(ticket['updated_at'], '%Y-%m-%d %H:%M:%S')
        
        solved_at = None
        if ticket['solved_at']:
            solved_at = datetime.strptime(ticket['solved_at'], '%Y-%m-%d %H:%M:%S')
        
        # Calculate ticket lifecycle duration
        if solved_at:
            total_duration = (solved_at - created_at).total_seconds() / 3600  # hours
        else:
            total_duration = (updated_at - created_at).total_seconds() / 3600  # hours
        
        # Generate assignment timing (tickets get assigned quickly)
        # Initially assigned within first few hours
        initial_assign_delay = random.uniform(0.1, min(4, total_duration * 0.1))
        initially_assigned_at = created_at + timedelta(hours=initial_assign_delay)
        
        # Final assignment (sometimes tickets get reassigned)
        if random.random() < 0.15:  # 15% get reassigned
            assign_delay = random.uniform(initial_assign_delay, min(total_duration * 0.3, initial_assign_delay + 24))
            assigned_at = created_at + timedelta(hours=assign_delay)
            assignee_stations = 2
        else:
            assigned_at = initially_assigned_at
            assignee_stations = 1
        
        # Group stations (most tickets stay in one group)
        group_stations = random.choices([1, 2, 3], weights=[80, 15, 5])[0]
        
        # Enhanced agent work time based on priority, org context, and call presence
        if priority == 'urgent':
            base_work_time = random.randint(30, 120)  # 30-120 minutes
        elif priority == 'high':
            base_work_time = random.randint(20, 90)   # 20-90 minutes
        elif priority == 'normal':
            base_work_time = random.randint(15, 60)   # 15-60 minutes
        else:  # low
            base_work_time = random.randint(10, 45)   # 10-45 minutes
        
        # Organization size impact (larger orgs require more work)
        org_size_multiplier = {
            'small': 0.9,
            'medium': 1.0,
            'large': 1.2
        }.get(org_size, 1.0)
        
        # Subscription tier impact (premium gets more attention)
        tier_multiplier = {
            'basic': 0.85,
            'standard': 1.0,
            'premium': 1.15
        }.get(subscription_tier, 1.0)
        
        # Call transcript impact (calls mean more complex issues)
        call_multiplier = 1.3 if has_call_transcript else 1.0
        
        # Satisfaction impact (bad satisfaction might mean more work was needed)
        satisfaction_multiplier = 1.0
        if satisfaction == 'bad':
            satisfaction_multiplier = 1.4  # More work on unsatisfied tickets
        elif satisfaction == 'good':
            satisfaction_multiplier = 1.1  # Slightly more work for good resolution
        
        # Status-based multiplier
        if status in ['solved', 'closed']:
            work_time_multiplier = random.uniform(1.0, 1.5)  # Solved tickets took more work
        else:
            work_time_multiplier = random.uniform(0.5, 1.0)  # Open tickets haven't had full work yet
        
        # Apply all multipliers
        agent_work_time = int(base_work_time * org_size_multiplier * tier_multiplier * 
                            call_multiplier * satisfaction_multiplier * work_time_multiplier)
        
        # Calculate resolution times with call transcript intelligence
        if status in ['solved', 'closed'] and solved_at:
            # First resolution time (initial response)
            first_resolution_hours = max(1, (assigned_at - created_at).total_seconds() / 3600 + random.uniform(1, 8))
            first_resolution_time = int(first_resolution_hours)
            
            # Full resolution time with call duration correlation
            base_resolution_hours = (solved_at - created_at).total_seconds() / 3600
            
            # Adjust resolution time based on call presence and characteristics
            if has_call_transcript:
                # Get call duration from pre-loaded data
                call_duration_minutes = call_durations.get(ticket_id, 0)
                
                # Intelligent resolution time based on call duration
                if call_duration_minutes > 0:
                    if call_duration_minutes <= 5:
                        # Very short calls - likely quick fixes or escalated later
                        if random.random() < 0.3:  # 30% quick resolution
                            base_resolution_hours = random.uniform(1, 8)  # 1-8 hours
                        else:  # 70% needed follow-up work
                            base_resolution_hours = random.uniform(24, 120)  # 1-5 days
                    
                    elif call_duration_minutes <= 15:
                        # Medium calls - standard resolution patterns
                        if random.random() < 0.4:  # 40% resolved quickly
                            base_resolution_hours = random.uniform(2, 24)  # 2-24 hours
                        else:  # 60% needed additional work
                            base_resolution_hours = random.uniform(12, 96)  # 12 hours to 4 days
                    
                    elif call_duration_minutes <= 30:
                        # Long calls - either resolved on call or very complex
                        if random.random() < 0.5:  # 50% resolved quickly after thorough call
                            base_resolution_hours = random.uniform(1, 12)  # 1-12 hours
                        else:  # 50% very complex, needed extensive work
                            base_resolution_hours = random.uniform(48, 168)  # 2-7 days
                    
                    else:  # 30+ minute calls
                        # Very long calls - usually complex issues
                        if random.random() < 0.6:  # 60% resolved same day after detailed work
                            base_resolution_hours = random.uniform(2, 24)  # 2-24 hours
                        else:  # 40% extremely complex
                            base_resolution_hours = random.uniform(72, 240)  # 3-10 days
                
                # Satisfaction impact on resolution time
                if satisfaction == 'bad':
                    base_resolution_hours *= random.uniform(1.5, 2.5)  # Bad satisfaction = longer resolution
                elif satisfaction == 'good':
                    base_resolution_hours *= random.uniform(0.7, 1.0)  # Good satisfaction = efficient resolution
            
            full_resolution_time = max(1, int(base_resolution_hours))
        else:
            # Open tickets - no resolution yet, but may have first response
            if status in ['open', 'pending', 'hold']:
                first_resolution_hours = max(1, (assigned_at - created_at).total_seconds() / 3600 + random.uniform(1, 4))
                first_resolution_time = int(first_resolution_hours)
            else:  # new tickets
                first_resolution_time = 0
            
            full_resolution_time = 0
        
        # Reply time (time to first agent response)
        reply_hours = (assigned_at - created_at).total_seconds() / 3600 + random.uniform(0.5, 3)
        reply_time = max(1, int(reply_hours))
        
        # Requester wait time (how long customer waited)
        if status in ['solved', 'closed']:
            # For solved tickets, customer waited until resolution
            requester_wait_hours = (solved_at - created_at).total_seconds() / 3600
        else:
            # For open tickets, customer is still waiting
            requester_wait_hours = (updated_at - created_at).total_seconds() / 3600
        
        requester_wait_time = max(1, int(requester_wait_hours))
        
        # Reopens (some tickets get reopened)
        if status in ['solved', 'closed']:
            reopens = random.choices([0, 1, 2], weights=[85, 12, 3])[0]
        else:
            reopens = 0
        
        # Enhanced replies calculation (back and forth conversation)
        if priority == 'urgent':
            base_replies = random.randint(3, 8)
        elif priority == 'high':
            base_replies = random.randint(2, 6)
        else:
            base_replies = random.randint(1, 4)
        
        # Organization type impact (faith orgs tend to be more communicative)
        org_type_multiplier = {
            'faith': 1.2,
            'school': 1.1,
            'nonprofit': 1.0,
            'childcare': 1.0,
            'community_ed': 0.9
        }.get(org_type, 1.0)
        
        # Call transcript impact (calls usually mean more back-and-forth)
        if has_call_transcript:
            call_reply_boost = random.randint(1, 3)  # 1-3 additional replies
        else:
            call_reply_boost = 0
        
        # Satisfaction impact (bad satisfaction means more replies)
        satisfaction_reply_boost = 0
        if satisfaction == 'bad':
            satisfaction_reply_boost = random.randint(1, 4)  # More back-and-forth
        elif satisfaction == 'good':
            satisfaction_reply_boost = random.randint(0, 1)  # Efficient resolution
        
        # Calculate total replies
        replies = int(base_replies * org_type_multiplier) + call_reply_boost + satisfaction_reply_boost
        
        # Adjust replies based on reopens
        replies += reopens * random.randint(1, 3)
        
        # Generate update timestamps
        # Assignee updated (when agent last worked on it)
        if status in ['solved', 'closed']:
            assignee_updated_at = solved_at - timedelta(hours=random.uniform(0.1, 2))
        else:
            assignee_updated_at = updated_at - timedelta(hours=random.uniform(0.1, 6))
        
        # Requester updated (when customer last interacted)
        if random.random() < 0.7:  # 70% have customer interactions
            if status in ['solved', 'closed']:
                # Customer might have responded before resolution
                requester_updated_at = solved_at - timedelta(hours=random.uniform(1, 12))
            else:
                # Customer interaction during open period
                requester_updated_at = created_at + timedelta(
                    hours=random.uniform(0, (updated_at - created_at).total_seconds() / 3600)
                )
        else:
            # No customer response after initial ticket
            requester_updated_at = created_at + timedelta(hours=random.uniform(0.1, 1))
        
        # Status updated (when status last changed)
        if status in ['solved', 'closed']:
            status_updated_at = solved_at
        else:
            # Status changed sometime during ticket lifecycle
            status_updated_at = created_at + timedelta(
                hours=random.uniform(1, (updated_at - created_at).total_seconds() / 3600)
            )
        
        # Ensure temporal consistency
        assignee_updated_at = max(assignee_updated_at, assigned_at)
        requester_updated_at = max(requester_updated_at, created_at)
        status_updated_at = max(status_updated_at, created_at)
        
        metric = {
            'metric_id': ticket_id,
            'ticket_id': ticket_id,
            'first_resolution_time': first_resolution_time,
            'full_resolution_time': full_resolution_time,
            'agent_work_time': agent_work_time,
            'requester_wait_time': requester_wait_time,
            'reply_time': reply_time,
            'group_stations': group_stations,
            'assignee_stations': assignee_stations,
            'reopens': reopens,
            'replies': replies,
            'assignee_updated_at': assignee_updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'requester_updated_at': requester_updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'status_updated_at': status_updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'initially_assigned_at': initially_assigned_at.strftime('%Y-%m-%d %H:%M:%S'),
            'assigned_at': assigned_at.strftime('%Y-%m-%d %H:%M:%S'),
            'solved_at': solved_at.strftime('%Y-%m-%d %H:%M:%S') if solved_at else ''
        }
        
        metrics.append(metric)
    
    print(f"Generated {len(metrics)} ticket metric records")
    
    # Write to CSV
    output_file = os.path.join(data_dir, 'ticket_metrics.csv')
    with open(output_file, 'w', newline='') as f:
        if metrics:
            fieldnames = metrics[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(metrics)
    
    # Statistics
    solved_metrics = [m for m in metrics if m['full_resolution_time'] > 0]
    open_metrics = [m for m in metrics if m['full_resolution_time'] == 0]
    
    if solved_metrics:
        avg_resolution = sum(m['full_resolution_time'] for m in solved_metrics) / len(solved_metrics)
        avg_first_response = sum(m['first_resolution_time'] for m in solved_metrics) / len(solved_metrics)
        avg_work_time = sum(m['agent_work_time'] for m in metrics) / len(metrics)
        
        reassigned_count = sum(1 for m in metrics if m['assignee_stations'] > 1)
        reopened_count = sum(1 for m in metrics if m['reopens'] > 0)
        
        call_metrics = [m for m in metrics if m['ticket_id'] in call_tickets]
        
        print(f"Enhanced Statistics:")
        print(f"  Solved tickets: {len(solved_metrics)} ({len(solved_metrics)/len(metrics)*100:.1f}%)")
        print(f"  Open tickets: {len(open_metrics)} ({len(open_metrics)/len(metrics)*100:.1f}%)")
        print(f"  Tickets with calls: {len(call_metrics)} ({len(call_metrics)/len(metrics)*100:.1f}%)")
        print(f"  Average resolution time: {avg_resolution:.1f} hours")
        print(f"  Average first response: {avg_first_response:.1f} hours")
        print(f"  Average agent work time: {avg_work_time:.1f} minutes")
        print(f"  Reassigned tickets: {reassigned_count} ({reassigned_count/len(metrics)*100:.1f}%)")
        print(f"  Reopened tickets: {reopened_count} ({reopened_count/len(metrics)*100:.1f}%)")
        
        # Enhanced correlations
        if call_metrics:
            avg_call_work_time = sum(m['agent_work_time'] for m in call_metrics) / len(call_metrics)
            avg_no_call_work_time = sum(m['agent_work_time'] for m in metrics if m['ticket_id'] not in call_tickets) / (len(metrics) - len(call_metrics))
            print(f"  Call tickets work time: {avg_call_work_time:.1f} min vs No-call: {avg_no_call_work_time:.1f} min")
        
        # Organization type analysis
        org_stats = {}
        for m in metrics:
            customer_id = next(t['customer_id'] for t in tickets if int(t['ticket_id']) == m['ticket_id'])
            org_type = customers.get(customer_id, {}).get('organization_type', 'unknown')
            if org_type not in org_stats:
                org_stats[org_type] = {'count': 0, 'total_work': 0}
            org_stats[org_type]['count'] += 1
            org_stats[org_type]['total_work'] += m['agent_work_time']
        
        print(f"  Organization type work time averages:")
        for org_type, stats in org_stats.items():
            avg_work = stats['total_work'] / stats['count']
            print(f"    {org_type}: {avg_work:.1f} minutes ({stats['count']} tickets)")
    
    return metrics

if __name__ == "__main__":
    generate_ticket_metrics()