import csv
import json
import sys
from pathlib import Path

def csv_to_json(csv_file_path, json_file_path=None, pretty=True, sample_size=None):
    """
    Convert CSV file to JSON format
    
    Args:
        csv_file_path (str): Path to the CSV file
        json_file_path (str, optional): Path for output JSON file. If None, replaces .csv with .json
        pretty (bool): Whether to format JSON with indentation
        sample_size (int, optional): Number of records to include (for large files)
    
    Returns:
        dict: JSON data with metadata
    """
    
    csv_path = Path(csv_file_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
    
    # Determine output path
    if json_file_path is None:
        json_path = csv_path.with_suffix('.json')
    else:
        json_path = Path(json_file_path)
    
    # Read CSV data
    records = []
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        
        for i, row in enumerate(reader):
            # Convert numeric fields
            for key, value in row.items():
                if value.isdigit():
                    row[key] = int(value)
                elif key == 'monthly_revenue' and value.replace('.', '').isdigit():
                    row[key] = float(value)
                elif key == 'payment_methods' and value.startswith('['):
                    try:
                        row[key] = json.loads(value)
                    except:
                        pass  # Keep as string if parsing fails
            
            records.append(row)
            
            # Limit records if sample_size specified
            if sample_size and i + 1 >= sample_size:
                break
    
    # Create JSON structure with metadata
    json_data = {
        "metadata": {
            "source_file": str(csv_path),
            "total_records": len(records),
            "fields": fieldnames,
            "sample_size": sample_size if sample_size else len(records),
            "organization_types": {}
        },
        "records": records
    }
    
    # Add organization type distribution
    if 'organization_type' in fieldnames:
        org_types = {}
        for record in records:
            org_type = record.get('organization_type', 'unknown')
            org_types[org_type] = org_types.get(org_type, 0) + 1
        json_data["metadata"]["organization_types"] = org_types
    
    # Write JSON file
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        if pretty:
            json.dump(json_data, jsonfile, indent=2, ensure_ascii=False)
        else:
            json.dump(json_data, jsonfile, ensure_ascii=False)
    
    print(f"✅ Converted {len(records)} records from CSV to JSON")
    print(f"📁 Input:  {csv_path}")
    print(f"📁 Output: {json_path}")
    print(f"📊 Organization distribution: {json_data['metadata']['organization_types']}")
    
    return json_data

def main():
    """Command line interface"""
    if len(sys.argv) < 2:
        print("Usage: python csv_to_json.py <csv_file> [json_file] [--sample=N]")
        print("Example: python csv_to_json.py ZENDESK_customers.csv --sample=10")
        return
    
    csv_file = sys.argv[1]
    json_file = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
    
    # Parse sample size
    sample_size = None
    for arg in sys.argv:
        if arg.startswith('--sample='):
            sample_size = int(arg.split('=')[1])
    
    try:
        csv_to_json(csv_file, json_file, sample_size=sample_size)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()