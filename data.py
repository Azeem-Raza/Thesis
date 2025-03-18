# Product inventory
products = [
    {
        "id": "P001",
        "name": "iPhone 15 Pro",
        "brand": "Apple",
        "price": 999.99,
        "stock": 15,
        "description": "Latest iPhone with A17 Pro chip, 48MP camera, and titanium design",
        "specs": {
            "screen_size": "6.1 inches",
            "storage": "256GB",
            "colors": ["Black", "White", "Blue", "Natural"]
        }
    },
    {
        "id": "P002",
        "name": "Samsung Galaxy S24 Ultra",
        "brand": "Samsung",
        "price": 1199.99,
        "stock": 10,
        "description": "Samsung's flagship with Snapdragon 8 Gen 3, 200MP camera, and S Pen",
        "specs": {
            "screen_size": "6.8 inches",
            "storage": "512GB",
            "colors": ["Titanium Black", "Titanium Gray", "Titanium Violet"]
        }
    },
    {
        "id": "P003",
        "name": "Google Pixel 8 Pro",
        "brand": "Google",
        "price": 899.99,
        "stock": 8,
        "description": "Google's premium phone with Tensor G3 chip and advanced AI features",
        "specs": {
            "screen_size": "6.7 inches",
            "storage": "128GB",
            "colors": ["Obsidian", "Porcelain", "Bay"]
        }
    },
    {
        "id": "P004",
        "name": "Xiaomi 14 Ultra",
        "brand": "Xiaomi",
        "price": 1099.99,
        "stock": 0,
        "description": "Photography-focused flagship with Leica optics and Snapdragon 8 Gen 3",
        "specs": {
            "screen_size": "6.73 inches",
            "storage": "256GB",
            "colors": ["Black", "White"]
        }
    },
    {
        "id": "P005",
        "name": "OnePlus 12",
        "brand": "OnePlus",
        "price": 799.99,
        "stock": 20,
        "description": "Fast-charging flagship with Snapdragon 8 Gen 3 and Hasselblad cameras",
        "specs": {
            "screen_size": "6.82 inches",
            "storage": "256GB",
            "colors": ["Flowy Emerald", "Silky Black"]
        }
    }
]

# Order data
orders = [
    {
        "order_id": "ORD10001",
        "customer_name": "John Smith",
        "product_id": "P001",
        "quantity": 1,
        "status": "Shipped",
        "shipping_address": "123 Main St, New York, NY",
        "tracking_number": "TRK78945612",
        "order_date": "2023-04-15"
    },
    {
        "order_id": "ORD10002",
        "customer_name": "Emma Johnson",
        "product_id": "P002",
        "quantity": 1,
        "status": "Processing",
        "shipping_address": "456 Oak Ave, Los Angeles, CA",
        "tracking_number": None,
        "order_date": "2023-04-18"
    },
    {
        "order_id": "ORD10003",
        "customer_name": "Michael Brown",
        "product_id": "P003",
        "quantity": 2,
        "status": "Delivered",
        "shipping_address": "789 Pine Rd, Chicago, IL",
        "tracking_number": "TRK36547891",
        "order_date": "2023-04-10"
    },
    {
        "order_id": "ORD10004",
        "customer_name": "Sophia Williams",
        "product_id": "P005",
        "quantity": 1,
        "status": "Cancelled",
        "shipping_address": "101 Cedar Ln, Houston, TX",
        "tracking_number": None,
        "order_date": "2023-04-12"
    },
    {
        "order_id": "ORD10005",
        "customer_name": "James Davis",
        "product_id": "P001",
        "quantity": 1,
        "status": "Pending",
        "shipping_address": "202 Maple Dr, Phoenix, AZ",
        "tracking_number": None,
        "order_date": "2023-04-20"
    }
] 