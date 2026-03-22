from fastapi import FastAPI, Query

app = FastAPI()

products = [
    {"product_id": 123, "name": "Smartphone", "category": "Electronics", "price": 599.99},
    {"product_id": 456, "name": "Phone Case", "category": "Accessories", "price": 19.99},
    {"product_id": 789, "name": "iPhone", "category": "Electronics", "price": 1299.99},
    {"product_id": 101, "name": "Headphones", "category": "Accessories", "price": 99.99},
    {"product_id": 202, "name": "Smartwatch", "category": "Electronics", "price": 299.99}
]

def get_product(id: int):
    for product in products:
        if product.get('product_id') == id:
            return product
    return None

@app.get('/products/search')
def products_search(
        keyword: str,
        category: str | None = None,
        limit: int = Query(10, ge=1, le=100)):
        result = []
        for product in products:
            if category == None or product.get('category') == category:
                if keyword.lower() in product.get('name').lower():
                    result.append(product)
        return result[:limit]

@app.get('/product/{product_id}')
def get_product_by_id (product_id: int):
    product = get_product(product_id)
    if product:
        return product
    return {'error': 'Product not found'}
