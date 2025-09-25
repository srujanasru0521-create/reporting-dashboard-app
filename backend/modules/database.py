import csv
import os
import time
import json
import uuid

NOTIFICATIONS_FILE = 'notifications.csv'
PRODUCTS_FILE = 'products.csv'
STOCK_FILE = 'stock.csv'

def create_tables():
    """Initializes CSV files with headers if they don't exist."""
    files_to_check = {
        NOTIFICATIONS_FILE: ['id', 'type', 'message', 'source', 'timestamp', 'status'],
        PRODUCTS_FILE: ['sku', 'name', 'category', 'price', 'description'],
        STOCK_FILE: ['sku', 'quantity', 'threshold', 'last_updated']
    }
    for file, headers in files_to_check.items():
        if not os.path.exists(file):
            with open(file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
    print("CSV files initialized successfully.")

def get_notifications_from_db():
    """Fetches all active notifications from the CSV file."""
    if not os.path.exists(NOTIFICATIONS_FILE):
        return []
    notifications = []
    with open(NOTIFICATIONS_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['status'] == 'active':
                notifications.append(row)
    return sorted(notifications, key=lambda x: x['timestamp'], reverse=True)

def insert_notification_into_db(notification_data):
    """Inserts a new notification record into the CSV file."""
    mode = 'a' if os.path.exists(NOTIFICATIONS_FILE) else 'w'
    with open(NOTIFICATIONS_FILE, mode, newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=notification_data.keys())
        if f.tell() == 0 or not os.path.exists(NOTIFICATIONS_FILE):
            writer.writeheader()
        writer.writerow(notification_data)

def update_notification_status(notification_id, new_status):
    """Updates the status of a specific notification in the CSV file."""
    rows = []
    with open(NOTIFICATIONS_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    rows_affected = 0
    with open(NOTIFICATIONS_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = rows[0].keys() if rows else ['id', 'type', 'message', 'source', 'timestamp', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if row['id'] == notification_id:
                row['status'] = new_status
                rows_affected += 1
            writer.writerow(row)
    return rows_affected

def update_notification_status_by_type(alert_type, new_status):
    """Updates the status of all notifications of a specific type."""
    rows = []
    with open(NOTIFICATIONS_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    rows_affected = 0
    with open(NOTIFICATIONS_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = rows[0].keys() if rows else ['id', 'type', 'message', 'source', 'timestamp', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if row['type'] == alert_type and row['status'] == 'active':
                row['status'] = new_status
                rows_affected += 1
            writer.writerow(row)
    return rows_affected

def get_products_from_db():
    """Fetches all products from the CSV file."""
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def insert_product_into_db(product_data):
    """Inserts a new product record into the CSV file."""
    mode = 'a' if os.path.exists(PRODUCTS_FILE) else 'w'
    with open(PRODUCTS_FILE, mode, newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=product_data.keys())
        if f.tell() == 0 or not os.path.exists(PRODUCTS_FILE):
            writer.writeheader()
        writer.writerow(product_data)
    
    # Also initialize stock for the new product
    stock_data = {'sku': product_data['sku'], 'quantity': '100', 'threshold': '50', 'last_updated': str(int(time.time()))}
    mode = 'a' if os.path.exists(STOCK_FILE) else 'w'
    with open(STOCK_FILE, mode, newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=stock_data.keys())
        if f.tell() == 0 or not os.path.exists(STOCK_FILE):
            writer.writeheader()
        writer.writerow(stock_data)

def update_stock_in_db(sku, quantity_change):
    """Updates the stock quantity for a given SKU in the CSV file."""
    rows = []
    with open(STOCK_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    new_quantity, threshold = None, None
    with open(STOCK_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = rows[0].keys() if rows else ['sku', 'quantity', 'threshold', 'last_updated']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if row['sku'] == sku:
                new_quantity = int(row['quantity']) - int(quantity_change)
                row['quantity'] = str(new_quantity)
                row['last_updated'] = str(int(time.time()))
                threshold = int(row['threshold'])
            writer.writerow(row)
    return new_quantity, threshold

def get_product_stock_from_db(sku):
    """Fetches the current stock quantity and threshold for a given SKU."""
    if not os.path.exists(STOCK_FILE):
        return None, None
    with open(STOCK_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['sku'] == sku:
                return int(row['quantity']), int(row['threshold'])
    return None, None