import uuid
from datetime import datetime

class Notification:
    """
    Represents a notification object.
    """
    def __init__(self, type, message, source, timestamp=None, status='active', id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.type = type
        self.message = message
        self.source = source
        self.timestamp = timestamp if timestamp is not None else datetime.now().isoformat()
        self.status = status

    def to_dict(self):
        """
        Converts the Notification object to a dictionary for JSON serialization.
        """
        return {
            'id': self.id,
            'type': self.type,
            'message': self.message,
            'source': self.source,
            'timestamp': self.timestamp,
            'status': self.status
        }
        
class Product:
    """
    Represents a product object for the e-commerce store.
    """
    def __init__(self, sku, name, category, price, description):
        self.sku = sku
        self.name = name
        self.category = category
        self.price = price
        self.description = description

    def to_dict(self):
        """
        Converts the Product object to a dictionary for JSON serialization.
        """
        return {
            'sku': self.sku,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'description': self.description
        }
