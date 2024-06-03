def render_product_list(products):
    return [{
        "id": producto.id,
        "name": producto.name,
        "description": producto.description,
        "price": producto.price,
        "stock": producto.stock
    }
    for producto in products
    ]

def render_product_detail(producto):
    return {
        "id":producto.id,
        "name":producto.name,
        "description":producto.description,
        "price":producto.price,
        "stock":producto.stock
    }