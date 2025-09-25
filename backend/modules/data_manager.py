import json
import os
from datetime import datetime

REPORTS_FILE = 'reports.json'
DATA_FILE = 'sample_data.json'

def load_reports():
    """Loads all report requests from the reports.json file."""
    if not os.path.exists(REPORTS_FILE):
        return []
    try:
        with open(REPORTS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_reports(reports):
    """Saves the list of reports to the reports.json file."""
    with open(REPORTS_FILE, 'w') as f:
        json.dump(reports, f, indent=4)

def load_data():
    """Loads the sample financial data from the sample_data.json file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def filter_data(report_details):
    """
    Filters and prepares data based on the frontend selections, including the date range.
    """
    all_data = load_data()
    
    print(f"Total data records: {len(all_data)}")
    print(f"Report details: {report_details}")

    # Map frontend report types to data types
    report_type_mapping = {
        'VAT Report': 'VAT Report',
        'Payments Report': 'Payments Report',
        'P&L Report': 'P&L Report'
    }
    
    # Extract report type from the name (before " for ")
    report_type_from_name = report_details['name'].split(' for ')[0]
    expected_report_type = report_type_mapping.get(report_type_from_name)
    
    print(f"Looking for report type: {expected_report_type}")
    print(f"Looking for country: {report_details['accountant']}")
    print(f"Looking for currency: {report_details['currency']}")
    
    # Convert date strings to datetime objects for comparison
    start_date_str = report_details.get('startDate')
    end_date_str = report_details.get('endDate')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
    
    print(f"Date range: {start_date} to {end_date}")
    
    # Filter by accountant location, currency, and report type
    filtered_data = []
    for item in all_data:
        # Check basic criteria
        country_match = item.get('country') == report_details['accountant']
        currency_match = item.get('currency') == report_details['currency']
        report_type_match = item.get('reportType') == expected_report_type
        
        print(f"Item {item.get('id')}: country={country_match}, currency={currency_match}, type={report_type_match}")
        
        if country_match and currency_match and report_type_match:
            # Check date range
            if start_date and end_date and 'date' in item:
                try:
                    item_date = datetime.strptime(item['date'], '%Y-%m-%d').date()
                    if start_date <= item_date <= end_date:
                        filtered_data.append(item)
                        print(f"Item {item.get('id')} included (date match)")
                    else:
                        print(f"Item {item.get('id')} excluded (date mismatch: {item_date})")
                except ValueError:
                    print(f"Item {item.get('id')} has invalid date format: {item.get('date')}")
            else:
                filtered_data.append(item)
                print(f"Item {item.get('id')} included (no date filtering)")

    print(f"Filtered data count: {len(filtered_data)}")
    return filtered_data





















