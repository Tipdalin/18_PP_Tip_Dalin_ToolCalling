phones = [
    {
        "id": 1,
        "name": "iPhone 18 Pro Max",
        "brand": "Apple",
        "price": 2000,
        "stock": 10,
    },
    {
        "id": 2,
        "name": "Galaxy S25 Ultra",
        "brand": "Samsung",
        "price": 1299,
        "stock": 7,
    },
    {
        "id": 3,
        "name": "Pixel 9 Pro",
        "brand": "Google",
        "price": 999,
        "stock": 5,
    },
    {
        "id": 4,
        "name": "Xiaomi 15 Ultra",
        "brand": "Xiaomi",
        "price": 899,
        "stock": 8,
    },
    {
        "id": 5,
        "name": "OnePlus 13",
        "brand": "OnePlus",
        "price": 799,
        "stock": 6,
    },
    {
        "id": 6,
        "name": "Huawei Pura 70 Pro",
        "brand": "Huawei",
        "price": 899,
        "stock": 4,
    },
    {
        "id": 7,
        "name": "Sony Xperia 1 VI",
        "brand": "Sony",
        "price": 1099,
        "stock": 3,
    },
    {
        "id": 8,
        "name": "Oppo Find X8 Pro",
        "brand": "Oppo",
        "price": 849,
        "stock": 9,
    },
    {
        "id": 9,
        "name": "Vivo X200 Pro",
        "brand": "Vivo",
        "price": 899,
        "stock": 0,
    },
    {
        "id": 10,
        "name": "Nothing Phone 3",
        "brand": "Nothing",
        "price": 699,
        "stock": 12,
    },
]

def search_phone(query: str):
    """
    Search phones by name or brand.
    """
    
    if not isinstance(query, str):
        return {
            "success": False,
            "error": "INVALID_QUERY",
            "message": "Query must be a string.",
        }

    query = query.strip().lower()

    if not query:
        return {
            "success": False,
            "error": "EMPTY_QUERY",
            "message": "Search query cannot be empty.",
        }

    results = [
        phone
        for phone in phones
        if query in phone["name"].lower()
        or query in phone["brand"].lower()
    ]

    return {
        "success": True,
        "results": results,
    }


def check_stock(phone_id: int):
    """
    Check the stock quantity of a phone.
    """

    if not isinstance(phone_id, int) or isinstance(phone_id, bool):
        return {
            "success": False,
            "error": "INVALID_PHONE_ID",
            "message": "Phone ID must be an integer.",
        }

    if phone_id <= 0:
        return {
            "success": False,
            "error": "INVALID_PHONE_ID",
            "message": "Phone ID must be greater than 0.",
        }

    for phone in phones:
        if phone["id"] == phone_id:
            return {
                "success": True,
                "phone_id": phone["id"],
                "phone_name": phone["name"],
                "stock": phone["stock"],
            }

    return {
        "success": False,
        "error": "PHONE_NOT_FOUND",
        "message": f"Phone with ID {phone_id} was not found.",
    }


def delete_phone(phone_id: int):
    """
    Delete a phone from the system.

    Permission checking is handled by harness.py.
    """

    if not isinstance(phone_id, int) or isinstance(phone_id, bool):
        return {
            "success": False,
            "error": "INVALID_PHONE_ID",
            "message": "Phone ID must be an integer.",
        }

    if phone_id <= 0:
        return {
            "success": False,
            "error": "INVALID_PHONE_ID",
            "message": "Phone ID must be greater than 0.",
        }

    for phone in phones:
        if phone["id"] == phone_id:
            phones.remove(phone)

            return {
                "success": True,
                "message": f"Phone '{phone['name']}' was deleted.",
                "phone_id": phone_id,
            }

    return {
        "success": False,
        "error": "PHONE_NOT_FOUND",
        "message": f"Phone with ID {phone_id} was not found.",
    }

