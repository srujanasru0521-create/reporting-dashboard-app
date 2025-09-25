import uuid
from .database import get_products_from_db, insert_product_into_db
from .model import Product

def create_product(data):
    """
    Handles the logic for creating a new product.
    """
    new_product = Product(
        sku=data['sku'],
        name=data['name'],
        category=data['category'],
        price=data['price'],
        description=data.get('description')
    )

    insert_product_into_db(new_product.to_dict())

    return new_product.to_dict()

def get_all_products():
    """
    Fetches all products and returns them as a list of dictionaries.
    """
    products_data = get_products_from_db()
    products_list = [Product(**data).to_dict() for data in products_data]
    return products_list

def initialize_products():
    """
    Initializes a set of default products in the database.
    """
    products_to_add = [
        {"sku": "SHIRT-001", "name": "Classic T-Shirt", "category": "Apparel", "price": 19.99, "description": "A comfortable cotton t-shirt."},
        {"sku": "SHOES-002", "name": "Running Shoes", "category": "Footwear", "price": 75.50, "description": "Lightweight running shoes with good support."},
        {"sku": "HAT-003", "name": "Baseball Cap", "category": "Apparel", "price": 12.00, "description": "Adjustable baseball cap with a logo."}
    ]

    for product_data in products_to_add:
        try:
            create_product(product_data)
        except Exception as e:
            # Ignore if product already exists (due to primary key constraint)
            print(f"Product {product_data['sku']} already exists.")
