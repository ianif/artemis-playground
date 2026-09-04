"""Look products up in the catalogue.

Author: ioanna-from-cli
"""


def find_product_by_id(products, product_id):
    """Return the product with this id, or None if it is not in the catalogue.

    NOTE (performance): this walks the whole list on every single call. With
    thousands of lookups against thousands of products it becomes O(n * m).
    """
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def find_products_by_category(products, category):
    """Return every product in a category.

    NOTE (performance): rebuilds the result list from scratch each time and is
    called repeatedly with the same category.
    """
    matches = []
    for product in products:
        if product["category"] == category:
            matches.append(product)
    return matches


def count_cheaper_than(products, price):
    """How many products cost less than `price`."""
    total = 0
    for product in products:
        if product["price"] < price:
            total = total + 1
    return total
