import uuid
from datetime import datetime
from .database import insert_notification_into_db, get_notifications_from_db, update_notification_status, get_product_stock_from_db, update_stock_in_db, update_notification_status_by_type
from .model import Notification
from .email_service import EmailService, determine_urgency, extract_deadline_type

# Initialize email service
email_service = EmailService()

def process_new_order_and_generate_alerts(order_data):
    """
    Simulates a new order, updates stock, and generates all relevant alerts.
    """
    sku = order_data.get('sku')
    quantity_ordered = order_data.get('quantity')

    if not sku or quantity_ordered is None:
        raise ValueError("SKU and quantity are required.")

    # Get current stock and threshold
    current_stock, threshold = get_product_stock_from_db(sku)
    
    if current_stock is None:
        raise ValueError(f"SKU {sku} not found in stock.")

    # 1. Simulate New Order Alert
    new_order_message = f"New order #{uuid.uuid4().hex[:6]} from Temu for {quantity_ordered} units of {sku}!"
    new_order_alert = Notification(type='new_order', message=new_order_message, source='Temu')
    insert_notification_into_db(new_order_alert.to_dict())

    # 2. Check for low stock alert based on order
    if current_stock < quantity_ordered:
        low_stock_message = f"URGENT: Temu order for {quantity_ordered} of {sku} cannot be fulfilled. Only {current_stock} units left."
        low_stock_alert = Notification(type='low_stock', message=low_stock_message, source='Temu')
        insert_notification_into_db(low_stock_alert.to_dict())
    
    # Update stock
    new_stock, _ = update_stock_in_db(sku, quantity_ordered)

    # 3. Check for low stock alert based on threshold
    if new_stock is not None and new_stock <= threshold:
        low_stock_message = f"SKU: {sku} is low on stock, <{threshold} units left. Remaining stock is below threshold."
        low_stock_alert = Notification(type='low_stock', message=low_stock_message, source='Amazon US')
        insert_notification_into_db(low_stock_alert.to_dict())

    # 4. Simulate Shipment Issue Alert
    shipment_message = f"Shipment SHP-{uuid.uuid4().hex[:6]} has a missing tracking number."
    shipment_alert = Notification(type='delayed_shipment', message=shipment_message, source='Autodoc')
    insert_notification_into_db(shipment_alert.to_dict())

    # 5. Simulate VAT Deadline Alert WITH EMAIL NOTIFICATION
    deadline_message = "VAT filing deadline for Germany in 5 days!"
    deadline_alert = Notification(type='deadline', message=deadline_message, source='Germany')
    insert_notification_into_db(deadline_alert.to_dict())
    
    # Send email notification for deadline
    send_deadline_email_notification(deadline_message)
    
    return {
        "message": "Order processed, alerts generated, and deadline email sent successfully."
    }

def send_deadline_email_notification(deadline_message):
    """
    Send email notification for deadline alerts
    """
    try:
        # Determine urgency and type
        urgency = determine_urgency(deadline_message)
        deadline_type = extract_deadline_type(deadline_message)
        
        # Send email
        email_sent = email_service.send_deadline_alert(
            deadline_message=deadline_message,
            deadline_type=deadline_type,
            urgency=urgency
        )
        
        if email_sent:
            print(f"Deadline email notification sent successfully")
        else:
            print(f"Failed to send deadline email notification")
            
        return email_sent
        
    except Exception as e:
        print(f"Error sending deadline email: {str(e)}")
        return False

def create_deadline_notification_with_email(data):
    """
    Create a deadline notification and send email alert
    """
    # Create the notification
    new_notification = Notification(
        type='deadline',
        message=data['message'],
        source=data['source']
    )
    insert_notification_into_db(new_notification.to_dict())
    
    # Send email notification
    send_deadline_email_notification(data['message'])
    
    return new_notification.to_dict()

def get_all_notifications():
    """
    Fetches all notifications and returns them as a list of Notification objects.
    """
    notifications_data = get_notifications_from_db()
    notifications_list = [Notification(**data) for data in notifications_data]
    return [notification.to_dict() for notification in notifications_list]

def create_notification(data):
    """
    Handles the logic for creating a new notification using the Notification model.
    If it's a deadline notification, also send email.
    """
    new_notification = Notification(
        type=data['type'],
        message=data['message'],
        source=data['source']
    )
    insert_notification_into_db(new_notification.to_dict())
    
    # Send email for deadline notifications
    if data['type'] == 'deadline':
        send_deadline_email_notification(data['message'])
    
    return new_notification.to_dict()

def resolve_notification(notification_id):
    """
    Handles the logic for resolving a single notification.
    """
    return update_notification_status(notification_id, 'resolved')

def resolve_all_notifications_by_type(alert_type):
    """
    Handles the logic for resolving all notifications of a specific type.
    """
    return update_notification_status_by_type(alert_type, 'resolved')

def test_email_configuration():
    """
    Test email configuration by sending a test email
    """
    return email_service.send_test_email()